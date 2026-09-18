"""Unit tests for scripts/foundry.py. Run: python -m unittest scripts/test_foundry.py"""
from __future__ import annotations

import io
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import foundry  # noqa: E402

REPO = Path(__file__).resolve().parents[1]

GOOD_SKILL = """---
name: sample
description: Build a sample thing when the user asks for one.
invocation: model
model: haiku
reads: [.foundry/brief.md]
writes: []
gate: python scripts/foundry.py validate
---

# Sample
"""

PACK_EXAMPLE = """slug: restaurant-pos
name: Restaurant POS
aliases: [restaurant point of sale, cafe pos, qsr pos]
confidence_keywords: [restaurant, cafe, kitchen, table, menu, order, kds, bill]
personas: [cashier, waiter, kitchen, manager, owner]
jobs: [{id: take-order, must: true, screens: [order-entry, table-map]}]
must_have: [order-entry, modifiers, split-bill, kds, payments, shift-close]
should_have: [reservations, loyalty, multi-branch]
entities: {Order: {states: [draft, sent, ready, served, paid, void]}}
invariants: ["Order total == sum(lines) - discounts + tax"]
integrations: {payments: [stripe, tap], delivery: [talabat]}
regional: {AE: {tax: "VAT 5%", receipt_lang: [en, ar]}}
compliance_must: [PCI-DSS SAQ-A via hosted fields]
nfr_defaults: {offline: required, p95_order_entry_ms: 200}
stack_default: {web: nextjs, api: hono, db: postgres, mobile: expo}
ui_profile: {style: high-contrast-operational, density: high, touch: 48dp}
questions: [{id: service-model, ask: "Dine-in, quick-service, or both?", default: both, reversible: false}]
reference: {screens: reference/screens.md, workflows: reference/workflows.md, glossary: reference/glossary.csv, compliance: reference/compliance.md, ux_patterns: reference/ux-patterns.md}
"""


def make_repo(tmp: Path) -> Path:
    """Minimal repo: real schemas, one good skill, empty index."""
    (tmp / "schemas").mkdir()
    for s in (REPO / "schemas").glob("*.json"):
        shutil.copy(s, tmp / "schemas" / s.name)
    (tmp / "skills" / "sample").mkdir(parents=True)
    (tmp / "skills" / "sample" / "SKILL.md").write_text(GOOD_SKILL, encoding="utf-8")
    (tmp / "packs").mkdir()
    (tmp / "packs" / "index.csv").write_text(",".join(foundry.INDEX_HEADER) + "\n", encoding="utf-8")
    return tmp


def run(fn, *a, **kw):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = fn(*a, **kw)
    return code, buf.getvalue()


class YamlSubsetTests(unittest.TestCase):
    def test_pack_example_parses(self):
        d = foundry.parse_yaml(PACK_EXAMPLE)
        self.assertEqual(d["slug"], "restaurant-pos")
        self.assertEqual(d["jobs"][0]["screens"], ["order-entry", "table-map"])
        self.assertEqual(d["entities"]["Order"]["states"][-1], "void")
        self.assertEqual(d["regional"]["AE"]["tax"], "VAT 5%")
        self.assertIs(d["questions"][0]["reversible"], False)
        self.assertEqual(d["nfr_defaults"]["p95_order_entry_ms"], 200)

    def test_block_lists_and_comments(self):
        d = foundry.parse_yaml("a:\n  - x  # c\n  - \"y: z\"\nb: 1.5\n# full comment\nc: 'it''s'\n")
        self.assertEqual(d, {"a": ["x", "y: z"], "b": 1.5, "c": "it's"})

    def test_errors_carry_line(self):
        with self.assertRaises(foundry.YamlError) as cm:
            foundry.parse_yaml("a: 1\nb: [1, 2\n")
        self.assertEqual(cm.exception.line, 2)


class SchemaTests(unittest.TestCase):
    def test_pack_example_matches_schema(self):
        errs = foundry.validate_schema(foundry.parse_yaml(PACK_EXAMPLE), foundry.load_schema("pack.schema.json"))
        self.assertEqual(errs, [])

    def test_additional_property_rejected(self):
        errs = foundry.validate_schema({"name": "x", "bogus": 1}, {"type": "object", "additionalProperties": False, "properties": {"name": {"type": "string"}}})
        self.assertTrue(any("bogus" in e for e in errs))


class ValidateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = make_repo(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_happy_path(self):
        code, out = run(foundry.run_validate, self.root)
        self.assertEqual(code, 0, out)

    def test_real_repo_validates(self):
        code, out = run(foundry.run_validate, REPO)
        self.assertEqual(code, 0, out)

    def test_over_150_lines_fails(self):
        p = self.root / "skills" / "sample" / "SKILL.md"
        p.write_text(GOOD_SKILL + "\n" * 150, encoding="utf-8")
        code, out = run(foundry.run_validate, self.root)
        self.assertEqual(code, 1)
        self.assertIn("SKILL.md:151:", out)
        self.assertIn("max 150", out)

    def test_bad_frontmatter_fails(self):
        p = self.root / "skills" / "sample" / "SKILL.md"
        p.write_text(GOOD_SKILL.replace("invocation: model", "invocation: sometimes").replace("model: haiku\n", ""), encoding="utf-8")
        code, out = run(foundry.run_validate, self.root)
        self.assertEqual(code, 1)
        self.assertIn("missing required 'model'", out)
        self.assertIn("'sometimes' not in", out)

    def test_description_trigger_word(self):
        p = self.root / "skills" / "sample" / "SKILL.md"
        p.write_text(GOOD_SKILL.replace("description: Build a", "description: This skill builds a"), encoding="utf-8")
        code, out = run(foundry.run_validate, self.root)
        self.assertEqual(code, 1)
        self.assertIn("verb or trigger noun", out)

    def test_missing_frontmatter_fails(self):
        p = self.root / "skills" / "sample" / "SKILL.md"
        p.write_text("# no frontmatter\n", encoding="utf-8")
        code, out = run(foundry.run_validate, self.root)
        self.assertEqual(code, 1)
        self.assertIn("missing frontmatter opener", out)

    def test_bad_index_header_fails(self):
        (self.root / "packs" / "index.csv").write_text("slug,name\n", encoding="utf-8")
        code, out = run(foundry.run_validate, self.root)
        self.assertEqual(code, 1)
        self.assertIn("index.csv:1:", out)


class ScaffoldPackTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = make_repo(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_scaffold_output_validates(self):
        code, out = run(foundry.run_scaffold_pack, "retail-pos", self.root)
        self.assertEqual(code, 0, out)
        pack = self.root / "packs" / "retail-pos"
        self.assertTrue((pack / "pack.yaml").exists())
        for name in foundry.REFERENCE_FILES:
            self.assertTrue((pack / "reference" / name).exists(), name)
        (self.root / "packs" / "index.csv").write_text(
            ",".join(foundry.INDEX_HEADER) + "\nretail-pos,Retail POS,retail point of sale,retail;shop,0.7\n", encoding="utf-8")
        code, out = run(foundry.run_validate, self.root)
        self.assertEqual(code, 0, out)

    def test_scaffold_refuses_overwrite_and_bad_slug(self):
        self.assertEqual(run(foundry.run_scaffold_pack, "x-pos", self.root)[0], 0)
        self.assertEqual(run(foundry.run_scaffold_pack, "x-pos", self.root)[0], 1)
        self.assertEqual(run(foundry.run_scaffold_pack, "Bad Slug", self.root)[0], 1)

    def test_unimplemented_commands_exit_2(self):
        for cmd in ("query", "metrics", "gate"):
            code, out = run(foundry.main, [cmd])
            self.assertEqual(code, 2)
            self.assertIn("not implemented in P0", out)


if __name__ == "__main__":
    unittest.main()
