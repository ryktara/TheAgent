"""Unit tests for scripts/foundry.py. Run: python -m unittest discover -s scripts -p "test_*.py" """
from __future__ import annotations

import io
import json
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

PACK_EXAMPLE = """version: "1.5"
threshold: 0.7
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

    def test_index_drift_fails(self):
        run(foundry.run_scaffold_pack, "x-pos", self.root)
        (self.root / "packs" / "index.csv").write_text(foundry.build_index_text(self.root / "packs").replace("X POS", "X Pos"), encoding="utf-8")
        code, out = run(foundry.run_validate, self.root)
        self.assertEqual(code, 1)
        self.assertIn("sync-index", out)
        run(foundry.run_sync_index, self.root)
        self.assertEqual(run(foundry.run_validate, self.root)[0], 0)

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
        run(foundry.run_sync_index, self.root)
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
        run(foundry.run_sync_index, self.root)
        code, out = run(foundry.run_validate, self.root)
        self.assertEqual(code, 0, out)

    def test_scaffold_refuses_overwrite_and_bad_slug(self):
        self.assertEqual(run(foundry.run_scaffold_pack, "x-pos", self.root)[0], 0)
        self.assertEqual(run(foundry.run_scaffold_pack, "x-pos", self.root)[0], 1)
        self.assertEqual(run(foundry.run_scaffold_pack, "Bad Slug", self.root)[0], 1)

    def test_unimplemented_commands_exit_2(self):
        code, out = run(foundry.main, ["gate", "9"])
        self.assertEqual(code, 2)
        self.assertIn("not implemented", out)


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


class GrillTests(unittest.TestCase):
    """grill-plan is pure: exercised on every golden brief plus the gate brief."""

    def _setup(self, brief: str):
        res = foundry.match_brief(brief, REPO)
        sel = foundry.selection_from_match(res)
        pack = foundry.load_pack(REPO, sel["chosen"])
        ledger = foundry.empty_ledger(sel["chosen"])
        for pf in sel["prefilled"]:
            foundry.decide(ledger, pack, pf["question_id"], pf["value"], "brief", None, 0)
        return sel, pack, ledger

    def test_every_golden_brief_round1_within_budget(self):
        for exp_path in sorted((REPO / "evals" / "expected").glob("*.yaml")):
            exp = foundry.parse_yaml(exp_path.read_text(encoding="utf-8"))
            sel, pack, ledger = self._setup(load_brief(exp_path.stem))
            plan = foundry.grill_plan(pack, ledger, sel["prefilled"], 1)
            self.assertLessEqual(len(plan), 7, exp_path.stem)
            self.assertLessEqual(len(plan), int(exp["max_questions"]), exp_path.stem)
            ids = [q["id"] for q in plan]
            self.assertEqual(len(ids), len(set(ids)), "duplicate question in plan")
            confirms = [q for q in plan if q["why"] == "confirm-prefill"]
            self.assertEqual(ids[:len(confirms)], [q["id"] for q in confirms], "confirms come first")

    def test_gate_brief_confirm_and_followups(self):
        sel, pack, ledger = self._setup("restaurant in Sharjah, dine-in only, we use Network International for cards")
        plan = foundry.grill_plan(pack, ledger, sel["prefilled"], 1)
        self.assertEqual(plan[0]["id"], "service-model")
        self.assertEqual(plan[0]["why"], "confirm-prefill")
        self.assertEqual(plan[0]["default"], "dine-in")
        self.assertNotIn("region", [q["id"] for q in plan], "reversible prefill is not re-asked")
        self.assertNotIn("central-menu-sync", [q["id"] for q in plan], "followup-only question stays out of round 1")
        self.assertEqual([q["id"] for q in foundry.grill_plan(pack, ledger, sel["prefilled"], 2)], ["reservations"], "prefilled dine-in unlocks only reservations before round 1")
        for q in plan:
            foundry.decide(ledger, pack, q["id"], "multi" if q["id"] == "branches" else (True if q["id"] == "delivery" else q["default"]), "human", None, 1)
        r2 = foundry.grill_plan(pack, ledger, sel["prefilled"], 2)
        self.assertEqual({q["id"] for q in r2}, {"reservations", "central-menu-sync", "delivery-platforms"})
        self.assertTrue(all(q["why"] == "followup" for q in r2))
        self.assertEqual(foundry.grill_plan(pack, ledger, sel["prefilled"], 1), [])

    def test_decide_rejects_bad_choice_and_coerces(self):
        sel, pack, ledger = self._setup("restaurant with kitchen display and tables in Dubai")
        with self.assertRaises(ValueError):
            foundry.decide(ledger, pack, "kds", "hologram", "human")
        e = foundry.decide(ledger, pack, "offline", "yes", "human")
        self.assertIs(e["value"], True)
        e2 = foundry.decide(ledger, pack, "offline", "false", "human")
        self.assertIs(e2["value"], False)
        self.assertEqual(sum(1 for d in ledger["decisions"] if d["id"] == "offline"), 1, "update, not append")

    def test_ledger_roundtrip_and_schema(self):
        sel, pack, ledger = self._setup("restaurant in Sharjah, dine-in only")
        tmp = Path(tempfile.mkdtemp())
        try:
            foundry.save_ledger(tmp, ledger)
            back = foundry.load_ledger(tmp)
            self.assertEqual(back["decisions"], ledger["decisions"])
            self.assertEqual(foundry.validate_schema(back, foundry.load_schema("decisions.schema.json")), [])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class P3Tests(unittest.TestCase):
    def test_sharjah_confidence_and_derived_provider(self):
        res = foundry.match_brief("restaurant in Sharjah, dine-in only, we use Network International for cards", REPO)
        self.assertEqual(res["chosen"], "restaurant-pos")
        self.assertGreaterEqual(res["confidence"], 0.85, res)
        sel = foundry.selection_from_match(res)
        pack = foundry.load_pack(REPO, "restaurant-pos")
        ledger = foundry.empty_ledger("restaurant-pos")
        for pf in sel["prefilled"]:
            foundry.decide(ledger, pack, pf["question_id"], pf["value"], "brief", None, 0)
        foundry.apply_defaults(ledger, pack, sel["prefilled"])
        e = next(d for d in ledger["decisions"] if d["id"] == "payment-provider-name")
        self.assertEqual(e["value"], "Network International")
        self.assertEqual(e["source"], "agent-fact")
        self.assertIn("derived from payments=network-intl", e["rationale"])

    def test_derive_null_falls_to_default(self):
        pack = foundry.load_pack(REPO, "restaurant-pos")
        ledger = foundry.empty_ledger("restaurant-pos")
        foundry.decide(ledger, pack, "payments", "other", "human", None, 1)
        plan = foundry.grill_plan(pack, ledger, [], 2)
        self.assertIn("payment-provider-name", [q["id"] for q in plan], "null map unlocks the follow-up")
        foundry.apply_defaults(ledger, pack, [])
        e = next(d for d in ledger["decisions"] if d["id"] == "payment-provider-name")
        self.assertEqual((e["value"], e["source"]), ("unknown", "pack-default"))

    def test_when_list(self):
        pack = foundry.load_pack(REPO, "restaurant-pos")
        ledger = foundry.empty_ledger("restaurant-pos")
        foundry.decide(ledger, pack, "service-model", "both", "human", None, 1)
        self.assertIn("reservations", [q["id"] for q in foundry.grill_plan(pack, ledger, [], 2)])

    def test_rematch_shop_groceries(self):
        first = foundry.match_brief("I want an app for my shop", REPO)
        self.assertEqual(first["chosen"], "generic")
        ledger = foundry.empty_ledger("generic")
        gen = foundry.load_pack(REPO, "generic")
        foundry.decide(ledger, gen, "product-summary", "we sell groceries and mobile top-ups", "human", None, 1)
        second = foundry.match_brief(foundry.rematch_text("I want an app for my shop", ledger), REPO)
        self.assertEqual(second["chosen"], "retail-pos")
        self.assertGreaterEqual(second["confidence"], 0.7)

    def test_rematch_cli_switches_pack_and_ledger(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / ".foundry").mkdir()
            (tmp / ".foundry" / "brief.md").write_text("# Brief\n\nI want an app for my shop\n", encoding="utf-8")
            b = str(tmp / ".foundry" / "brief.md")
            run(foundry.main, ["match", "--brief", b, "--write", "--dir", str(tmp)])
            run(foundry.main, ["decide", "--id", "product-summary", "--value", "we sell groceries and mobile top-ups", "--source", "human", "--round", "1", "--dir", str(tmp)])
            code, out = run(foundry.main, ["match", "--brief", b, "--rematch", "--write", "--dir", str(tmp), "--json"])
            self.assertEqual(code, 0)
            self.assertIn('"rematched"', out)
            ledger = foundry.load_ledger(tmp)
            self.assertEqual(ledger["pack"], "retail-pos")
            self.assertIn("rematched", ledger["flags"])
            self.assertEqual(ledger["decisions"], [])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_variant_briefs(self):
        for exp_path in sorted((REPO / "evals" / "expected" / "restaurant-variants").glob("*.yaml")):
            exp = foundry.parse_yaml(exp_path.read_text(encoding="utf-8"))
            text = (REPO / "evals" / "briefs" / "restaurant-variants" / f"{exp_path.stem}.md").read_text(encoding="utf-8")
            body = "\n".join(l for l in text.splitlines() if not l.startswith("#"))
            res = foundry.match_brief(body, REPO)
            self.assertEqual(res["chosen"], "restaurant-pos", exp_path.stem)
            self.assertGreaterEqual(res["confidence"], float(exp["min_confidence"]), exp_path.stem)

    def test_prd_skeleton_then_gate(self):
        fx = REPO / "evals" / "fixtures" / "restaurant-pos"
        pack = foundry.load_pack(REPO, "restaurant-pos")
        ledger = foundry.load_ledger(fx)
        text = foundry.prd_skeleton(pack, ledger, "restaurant in Sharjah")
        self.assertEqual(text.count(foundry.MODEL_BLOCK), 2)
        for fid in pack["must_have"]:
            self.assertIn(f"`{fid}`", text)
        for d in ledger["decisions"]:
            self.assertIn(f"[D:{d['id']}]", text)
        tmp = Path(tempfile.mkdtemp())
        try:
            shutil.copytree(fx / ".foundry", tmp / ".foundry")
            (tmp / ".foundry" / "prd.md").write_text(text, encoding="utf-8")
            errs = foundry.gate_prd(tmp, REPO)
            self.assertTrue(any("model: write" in e for e in errs), "unfilled model blocks must fail the gate")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_complete_pack_lint_catches_missing_screen(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            root = make_repo(tmp)
            shutil.copytree(REPO / "packs" / "restaurant-pos", root / "packs" / "restaurant-pos")
            sc = root / "packs" / "restaurant-pos" / "reference" / "screens.md"
            sc.write_text(sc.read_text(encoding="utf-8").replace("## kds\n", "## kitchen-screen\n"), encoding="utf-8")
            run(foundry.run_sync_index, root)
            code, out = run(foundry.run_validate, root)
            self.assertEqual(code, 1)
            self.assertIn("screen 'kds' has no", out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class P4Tests(unittest.TestCase):
    """Phases 4-6 on the restaurant fixture."""

    def setUp(self):
        import foundry_phases as P
        self.P = P
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(REPO / "evals" / "fixtures" / "restaurant-pos" / ".foundry", self.tmp / ".foundry")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_yaml_block_map_in_list(self):
        d = foundry.parse_yaml("items:\n  - name: a\n    n: 1\n  - name: b\n    n: 2\nx: 3\n")
        self.assertEqual(d, {"items": [{"name": "a", "n": 1}, {"name": "b", "n": 2}], "x": 3})

    def test_enables_replaces_heuristic(self):
        pack = foundry.load_pack(REPO, "restaurant-pos")
        self.assertIsNotNone(foundry.should_have_enabled("multi-branch", [{"id": "branches", "value": "multi", "source": "human"}], pack))
        self.assertIsNone(foundry.should_have_enabled("multi-branch", [{"id": "branches", "value": "single", "source": "human"}], pack))
        self.assertIsNotNone(foundry.should_have_enabled("delivery-integration", [{"id": "delivery", "value": True, "source": "pack-default"}], pack))
        self.assertIsNone(foundry.should_have_enabled("accounting-sync", [{"id": "central-menu-sync", "value": "central", "source": "human"}], pack))

    def test_prd_region_scoping_and_tax_table(self):
        pack = foundry.load_pack(REPO, "restaurant-pos")
        ledger = foundry.load_ledger(self.tmp)
        text = foundry.prd_skeleton(pack, ledger, "x")
        sec8 = text.split("## 8.")[1].split("## 9.")[0]
        self.assertIn("`C-AE-01`", sec8)
        self.assertNotIn("C-SA-", sec8)
        self.assertNotIn("C-PK-", sec8)
        foundry.decide(ledger, pack, "region", "PK", "human", None, 1)
        text = foundry.prd_skeleton(pack, ledger, "x")
        sec8 = text.split("## 8.")[1].split("## 9.")[0]
        self.assertIn("| Punjab | 16% | 5% | PRA |", sec8)
        self.assertIn("`C-PK-02`", sec8)
        self.assertNotIn("C-AE-", sec8)

    def test_gate_prd_rejects_foreign_region_control(self):
        prd = self.tmp / ".foundry" / "prd.md"
        prd.write_text(prd.read_text(encoding="utf-8").replace("`C-AE-01`", "`C-AE-01`, `C-SA-01`"), encoding="utf-8")
        errs = foundry.gate_prd(self.tmp, REPO)
        self.assertTrue(any("C-SA-01" in e for e in errs), errs)

    def test_domain_skeleton_passes_gate(self):
        self.P.run_domain_skeleton(self.tmp, REPO)
        self.assertEqual(self.P.gate_domain(self.tmp, REPO), [])
        d = foundry.parse_yaml((self.tmp / ".foundry" / "domain.yaml").read_text(encoding="utf-8"))
        self.assertEqual(len(d["entities"]), 25)
        order = next(e for e in d["entities"] if e["name"] == "Order")
        self.assertIn({"from": "draft", "to": "sent", "by": "waiter", "guard": ""}, order["transitions"])
        self.assertTrue(any(ev["name"] == "OrderSent" and "kitchen" in ev["consumers"] for ev in d["events"]))
        ctx = (self.tmp / "CONTEXT.md").read_text(encoding="utf-8")
        self.assertIn("| KOT |", ctx)
        self.assertIn("kitchen output", ctx)

    def test_domain_gate_catches_missing_actor(self):
        self.P.run_domain_skeleton(self.tmp, REPO)
        p = self.tmp / ".foundry" / "domain.yaml"
        p.write_text(p.read_text(encoding="utf-8").replace('by: "waiter"', 'by: "nobody"', 1), encoding="utf-8")
        self.assertTrue(any("not a persona" in e for e in self.P.gate_domain(self.tmp, REPO)))

    def test_arch_skeleton_passes_gate(self):
        self.P.run_domain_skeleton(self.tmp, REPO)
        self.P.run_arch_skeleton(self.tmp, REPO)
        self.assertEqual(self.P.gate_architecture(self.tmp, REPO), [])
        adrs = sorted((self.tmp / ".foundry" / "adr").glob("*.md"))
        self.assertEqual([p.name[:4] for p in adrs], self.P.ADR_IDS)
        for p in adrs:
            self.assertLessEqual(len(p.read_text(encoding="utf-8").splitlines()), 60, p.name)

    def test_schema_and_api_pass_gates(self):
        self.P.run_domain_skeleton(self.tmp, REPO)
        self.P.run_arch_skeleton(self.tmp, REPO)
        self.P.run_schema_skeleton(self.tmp, REPO, "prisma")
        self.assertEqual(self.P.gate_data(self.tmp, REPO), [])
        schema = (self.tmp / "prisma" / "schema.prisma").read_text(encoding="utf-8")
        self.assertIn("model Order {", schema)
        self.assertIn("enum OrderState {", schema)
        self.assertIn("@db.Decimal(12, 2)", schema)
        self.P.run_api_skeleton(self.tmp, REPO)
        self.assertEqual(self.P.gate_api(self.tmp, REPO), [])
        spec = foundry.parse_yaml((self.tmp / "openapi.yaml").read_text(encoding="utf-8"))
        self.assertIn("/orders/{id}/send-to-kitchen", spec["paths"])
        self.assertIn("/sync/push", spec["paths"])
        self.assertIn("/webhooks/payments/{provider}", spec["paths"])
        self.P.run_schema_skeleton(self.tmp, REPO, "drizzle")
        self.assertIn("pgTable", (self.tmp / "db" / "schema.ts").read_text(encoding="utf-8"))

    def test_api_gate_catches_duplicate_operation_id(self):
        self.P.run_domain_skeleton(self.tmp, REPO)
        self.P.run_arch_skeleton(self.tmp, REPO)
        self.P.run_schema_skeleton(self.tmp, REPO, "prisma")
        self.P.run_api_skeleton(self.tmp, REPO)
        p = self.tmp / "openapi.yaml"
        p.write_text(p.read_text(encoding="utf-8").replace('operationId: "order_get"', 'operationId: "order_list"'), encoding="utf-8")
        self.assertTrue(any("used 2 times" in e for e in self.P.gate_api(self.tmp, REPO)))

    def test_query_and_doctor(self):
        code, out = run(foundry.main, ["query", "stacks", "--layer", "api"])
        self.assertEqual(code, 0)
        self.assertIn("hono-node", out)
        self.assertIn("nestjs", out)
        code, out = run(foundry.main, ["query", "stacks", "--layer", "api", "--json"])
        self.assertEqual(code, 0)
        self.assertIn('"total": 3', out)
        code, out = run(foundry.main, ["doctor"])
        self.assertIn("python", out)
        self.assertIn("codebase-memory-mcp", out)


class P5Tests(unittest.TestCase):
    def setUp(self):
        import foundry_design as D
        import foundry_phases as P
        self.D, self.P = D, P
        self.tmp = Path(tempfile.mkdtemp())
        fx = REPO / "evals" / "fixtures" / "restaurant-pos"
        shutil.copytree(fx / ".foundry", self.tmp / ".foundry")
        for name in ("CONTEXT.md", "openapi.yaml"):
            shutil.copy(fx / name, self.tmp / name)
        for d in ("prisma", "migrations"):
            shutil.copytree(fx / d, self.tmp / d)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_contrast_formula(self):
        self.assertAlmostEqual(self.D.contrast_ratio("#000000", "#ffffff"), 21.0, places=2)
        self.assertAlmostEqual(self.D.contrast_ratio("#767676", "#ffffff"), 4.54, places=2)
        self.assertAlmostEqual(self.D.contrast_ratio("#fff", "#000"), 21.0, places=2)

    def test_palettes_pass_and_row_counts(self):
        n, errs = self.D.check_palettes(REPO / "data" / "palettes.csv")
        self.assertGreaterEqual(n, 60)
        self.assertEqual(errs, [])
        import csv
        for name, minimum in (("ux-rules", 220), ("typography", 30), ("styles", 25), ("product-types", 60), ("charts", 25), ("components", 45)):
            with (REPO / "data" / f"{name}.csv").open(encoding="utf-8", newline="") as fh:
                rows = list(csv.DictReader(fh))
            self.assertGreaterEqual(len(rows), minimum, name)
        self.assertTrue(any("2.5.8" in r for r in (REPO / "data" / "ux-rules.csv").read_text(encoding="utf-8").splitlines()))

    def test_token_checks(self):
        tokens = {"font": {"size": {"base": {"$value": "16px"}, "md": {"$value": "20px"}, "lg": {"$value": "24px"}}}, "space": {"0": {"$value": "0px"}, "1": {"$value": "4px"}},
                  "radius": {"r0": {"$value": "0px"}}, "z": {"base": {"$value": 0}}, "motion": {"duration": {"fast": {"$value": "100ms"}}, "reduced": {"$value": "none"}},
                  "touch": {"min": {"$value": "48px"}}, "foundry": {"tabular_numerals": True}}
        self.assertEqual(self.D.check_tokens(tokens, 48, True), [])
        bad = json.loads(json.dumps(tokens)); bad["font"]["size"]["base"]["$value"] = "14px"; bad["space"]["1"]["$value"] = "5px"; bad["motion"]["duration"]["fast"]["$value"] = "900ms"
        errs = self.D.check_tokens(bad, 48, True)
        self.assertTrue(any("base" in e for e in errs) and any("space" in e for e in errs) and any("motion" in e for e in errs), errs)

    def test_design_and_screens_skeletons_pass_gates(self):
        self.D.run_design_skeleton(self.tmp, REPO)
        self.assertEqual(self.D.gate_design(self.tmp, REPO), [])
        master = (self.tmp / "design-system" / "MASTER.md").read_text(encoding="utf-8")
        for sec in self.D.REQUIRED_MASTER_SECTIONS:
            self.assertIn(f"## {sec}", master)
        tokens = json.loads((self.tmp / "design-system" / "tokens.json").read_text(encoding="utf-8"))
        self.assertEqual(tokens["touch"]["min"]["$value"], "48px")
        self.assertTrue(tokens["foundry"]["tabular_numerals"])
        self.D.run_screens_skeleton(self.tmp, REPO)
        self.assertEqual(self.D.gate_screens(self.tmp, REPO), [])
        oe = (self.tmp / ".foundry" / "screens" / "order-entry.md").read_text(encoding="utf-8")
        self.assertIn("order_send_to_kitchen", oe)
        self.assertIn('"numpad"', oe)
        self.assertIn("| offline |", oe)

    def test_screens_gate_catches_bad_binding_and_missing_state(self):
        self.D.run_design_skeleton(self.tmp, REPO); self.D.run_screens_skeleton(self.tmp, REPO)
        p = self.tmp / ".foundry" / "screens" / "tender.md"
        p.write_text(p.read_text(encoding="utf-8").replace('"payment_create"', '"payment_nope"').replace("| locked |", "| lockedx |"), encoding="utf-8")
        errs = self.D.gate_screens(self.tmp, REPO)
        self.assertTrue(any("payment_nope" in e for e in errs), errs)
        self.assertTrue(any("locked" in e for e in errs), errs)

    def test_api_pruned_by_exposure(self):
        spec = foundry.parse_yaml((self.tmp / "openapi.yaml").read_text(encoding="utf-8"))
        ops = sum(1 for m in spec["paths"].values() for k in m if k in ("get", "post", "patch", "delete"))
        self.assertLessEqual(ops, 90)
        self.assertNotIn("/kitchen-tickets", spec["paths"])
        self.assertIn("/admin/receipts", spec["paths"])
        self.assertIn("/order-lines/{id}/modify-order", spec["paths"])


class GateTests(unittest.TestCase):
    def test_fixture_passes_all_gates(self):
        fx = REPO / "evals" / "fixtures" / "restaurant-pos"
        for name in ("intake", "pack-match", "grill", "prd"):
            self.assertEqual(foundry.GATES[name](fx, REPO), [], name)

    def test_prd_gate_reports_missing_must_have_and_stale_hash(self):
        fx = REPO / "evals" / "fixtures" / "restaurant-pos"
        tmp = Path(tempfile.mkdtemp())
        try:
            shutil.copytree(fx / ".foundry", tmp / ".foundry")
            prd = tmp / ".foundry" / "prd.md"
            prd.write_text(prd.read_text(encoding="utf-8").replace("- `kds` —", "- kds —").replace("decisions_hash: ", "decisions_hash: x"), encoding="utf-8")
            errs = foundry.gate_prd(tmp, REPO)
            self.assertTrue(any("`kds`" in e for e in errs), errs)
            self.assertTrue(any("stale" in e for e in errs), errs)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_unattended_flow_end_to_end(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / ".foundry").mkdir()
            (tmp / ".foundry" / "brief.md").write_text("# Brief\n\nBuild me everything. Don't ask me any questions.\n", encoding="utf-8")
            self.assertEqual(run(foundry.main, ["match", "--brief", str(tmp / ".foundry" / "brief.md"), "--write", "--dir", str(tmp)])[0], 0)
            self.assertEqual(run(foundry.main, ["decide", "--apply-prefilled", "--dir", str(tmp)])[0], 0)
            self.assertEqual(run(foundry.main, ["decide", "--auto-unattended", "--dir", str(tmp)])[0], 0)
            self.assertEqual(run(foundry.main, ["decide", "--apply-defaults", "--dir", str(tmp)])[0], 0)
            self.assertEqual(run(foundry.main, ["gate", "2", "--dir", str(tmp)])[0], 0)
            ledger = foundry.load_ledger(tmp)
            self.assertEqual(ledger["mode"], "unattended")
            self.assertIn("no-questions-requested", ledger["flags"])
            self.assertEqual({d["source"] for d in ledger["decisions"]} - {"timeout-default", "pack-default", "brief"}, set())
            self.assertEqual(run(foundry.main, ["metrics", "--phase", "2", "--start", "--dir", str(tmp)])[0], 0)
            self.assertEqual(run(foundry.main, ["metrics", "--phase", "2", "--note", "x", "--dir", str(tmp)])[0], 0)
            lines = (tmp / ".foundry" / "metrics.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
