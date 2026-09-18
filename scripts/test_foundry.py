"""Unit tests for scripts/foundry.py. Run: python -m unittest discover -s scripts -p "test_*.py" """
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

PACK_EXAMPLE = """version: "1.1"
slug: restaurant-pos
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
questions: [{id: service-model, rank: 1, ask: "Dine-in, quick-service, or both?", answer_type: choice, choices: [dine-in, quick-service, both], default: both, reversible: false, skip_if_brief_mentions: [dine-in, quick-service, qsr], maps_to: service.model}]
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


def load_expected(name: str) -> dict:
    return foundry.parse_yaml((REPO / "evals" / "expected" / f"{name}.yaml").read_text(encoding="utf-8"))


def load_brief(name: str) -> str:
    text = (REPO / "evals" / "briefs" / f"{name}.md").read_text(encoding="utf-8")
    return "\n".join(l for l in text.splitlines() if not l.startswith("#")).strip()


class YamlSubsetTests(unittest.TestCase):
    def test_pack_example_parses(self):
        d = foundry.parse_yaml(PACK_EXAMPLE)
        self.assertEqual(d["slug"], "restaurant-pos")
        self.assertEqual(d["jobs"][0]["screens"], ["order-entry", "table-map"])
        self.assertEqual(d["entities"]["Order"]["states"][-1], "void")
        self.assertEqual(d["regional"]["AE"]["tax"], "VAT 5%")
        self.assertIs(d["questions"][0]["reversible"], False)
        self.assertEqual(d["questions"][0]["rank"], 1)
        self.assertEqual(d["nfr_defaults"]["p95_order_entry_ms"], 200)

    def test_block_lists_and_comments(self):
        d = foundry.parse_yaml("a:\n  - x  # c\n  - \"y: z\"\nb: 1.5\n# full comment\nc: 'it''s'\n")
        self.assertEqual(d, {"a": ["x", "y: z"], "b": 1.5, "c": "it's"})

    def test_nested_flow_mapping_in_block_list(self):
        d = foundry.parse_yaml("q:\n  - {id: r, brief_hints: {AE: [dubai, uae], SA: [riyadh]}, choices: [AE, SA]}\n")
        self.assertEqual(d["q"][0]["brief_hints"]["AE"], ["dubai", "uae"])

    def test_errors_carry_line(self):
        with self.assertRaises(foundry.YamlError) as cm:
            foundry.parse_yaml("a: 1\nb: [1, 2\n")
        self.assertEqual(cm.exception.line, 2)


class SchemaTests(unittest.TestCase):
    def test_pack_example_matches_schema(self):
        errs = foundry.validate_schema(foundry.parse_yaml(PACK_EXAMPLE), foundry.load_schema("pack.schema.json"))
        self.assertEqual(errs, [])

    def test_pack_schema_requires_v11_fields(self):
        d = foundry.parse_yaml(PACK_EXAMPLE)
        del d["questions"][0]["rank"]
        del d["version"]
        errs = foundry.validate_schema(d, foundry.load_schema("pack.schema.json"))
        self.assertTrue(any("rank" in e for e in errs))
        self.assertTrue(any("version" in e for e in errs))

    def test_additional_property_rejected(self):
        errs = foundry.validate_schema({"name": "x", "bogus": 1}, {"type": "object", "additionalProperties": False, "properties": {"name": {"type": "string"}}})
        self.assertTrue(any("bogus" in e for e in errs))

    def test_all_shipped_packs_validate(self):
        schema = foundry.load_schema("pack.schema.json")
        for p in (REPO / "packs").glob("*/pack.yaml"):
            self.assertEqual(foundry.validate_pack(p, schema), [], p)


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

    def test_duplicate_rank_fails(self):
        run(foundry.run_scaffold_pack, "x-pos", self.root)
        p = self.root / "packs" / "x-pos" / "pack.yaml"
        p.write_text(p.read_text(encoding="utf-8").replace("rank: 2", "rank: 1"), encoding="utf-8")
        (self.root / "packs" / "index.csv").write_text(",".join(foundry.INDEX_HEADER) + "\nx-pos,X,x,x,0.7\n", encoding="utf-8")
        code, out = run(foundry.run_validate, self.root)
        self.assertEqual(code, 1)
        self.assertIn("duplicate rank", out)

    def test_selection_file_validated(self):
        sel = {"chosen": "generic", "confidence": 0.2, "alternates": [], "unmatched_aspects": [], "prefilled": [], "flags": ["bogus"], "matcher_version": "1.0"}
        errs = foundry.validate_schema(sel, foundry.load_schema("pack-selection.schema.json"))
        self.assertTrue(any("bogus" in e for e in errs))
        sel["flags"] = ["below-threshold"]
        self.assertEqual(foundry.validate_schema(sel, foundry.load_schema("pack-selection.schema.json")), [])


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


class MatchTests(unittest.TestCase):
    def _check(self, name: str):
        exp = load_expected(name)
        res = foundry.match_brief(load_brief(name), REPO)
        self.assertEqual(res["chosen"], exp["expected_pack"], res)
        if res["chosen"] != "generic":
            self.assertGreaterEqual(res["candidates"][0]["confidence"], float(exp["min_confidence"]), res)
        return res

    def test_restaurant_brief(self):
        res = self._check("restaurant-pos")
        ids = {p["question_id"]: p["value"] for p in res["prefilled"]}
        self.assertEqual(ids.get("region"), "AE")
        self.assertEqual(ids.get("branches"), "multi")
        self.assertIs(ids.get("offline"), True)

    def test_retail_brief(self):
        res = self._check("retail-pos")
        ids = {p["question_id"]: p["value"] for p in res["prefilled"]}
        self.assertEqual(ids.get("region"), "SA")
        self.assertIs(ids.get("einvoice"), True)

    def test_trading_brief(self):
        res = self._check("trading-app")
        ids = {p["question_id"]: p["value"] for p in res["prefilled"]}
        self.assertEqual(ids.get("market"), "PSX")

    def test_ambiguous_brief_is_generic(self):
        res = self._check("ambiguous-shop")
        self.assertEqual(res["chosen"], "generic")

    def test_hostile_brief_flags(self):
        res = self._check("hostile-no-questions")
        self.assertEqual(res["chosen"], "generic")
        self.assertIn("no-questions-requested", res["flags"])

    def test_gate_brief_prefill(self):
        res = foundry.match_brief("restaurant in Sharjah, dine-in only, we use Network International for cards", REPO)
        self.assertEqual(res["chosen"], "restaurant-pos")
        self.assertGreaterEqual(res["candidates"][0]["confidence"], 0.7)
        ids = {p["question_id"]: p["value"] for p in res["prefilled"]}
        self.assertEqual(ids, {**ids, "region": "AE", "service-model": "dine-in", "payments": "network-intl"})

    def test_match_cli_stdin_json(self):
        import json
        real_stdin = sys.stdin
        sys.stdin = io.StringIO("forex trading app for DFM investors, don't ask me questions")
        try:
            code, out = run(foundry.main, ["match", "--brief", "-", "--json"])
        finally:
            sys.stdin = real_stdin
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["chosen"], "trading-app")
        self.assertIn("no-questions-requested", data["flags"])

    def test_deterministic(self):
        b = load_brief("restaurant-pos")
        self.assertEqual(foundry.match_brief(b, REPO), foundry.match_brief(b, REPO))


if __name__ == "__main__":
    unittest.main()
