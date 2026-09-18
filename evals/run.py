"""Foundry eval runner.

Stages:
  match   run foundry.py match on every golden brief; compare to expected_pack / min_confidence.
  grill   match -> apply-prefilled -> grill-plan round 1 in a temp dir; check budget and confirms.
  prd     gate prd against the fixture under evals/fixtures/restaurant-pos.

Usage: python evals/run.py [--stage match|grill|prd]
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import foundry as F  # noqa: E402

BRIEFS = ROOT / "evals" / "briefs"
EXPECTED = ROOT / "evals" / "expected"
FIXTURES = ROOT / "evals" / "fixtures"
STAGES = ("match", "grill", "prd")


def load_cases() -> list[dict]:
    cases = []
    for brief in sorted(BRIEFS.glob("*.md")):
        exp_path = EXPECTED / f"{brief.stem}.yaml"
        text = brief.read_text(encoding="utf-8")
        body = "\n".join(l for l in text.splitlines() if not l.startswith("#")).strip()
        exp = F.parse_yaml(exp_path.read_text(encoding="utf-8")) if exp_path.exists() else {}
        cases.append({"name": brief.stem, "brief": body, "expected": exp})
    return cases


def stage_match(cases: list[dict]) -> int:
    print(f"{'brief':<22} {'expected':<15} {'chosen':<15} {'conf':>5} {'min':>4} {'flags':<40} result")
    print("-" * 112)
    passed = 0
    for c in cases:
        exp = c["expected"]
        res = F.match_brief(c["brief"], ROOT)
        conf = res["confidence"]
        ok = res["chosen"] == exp.get("expected_pack") and conf >= float(exp.get("min_confidence", 0))
        for flag in exp.get("expected_flags", []) or []:
            ok = ok and flag in res["flags"]
        passed += ok
        print(f"{c['name']:<22} {exp.get('expected_pack', '?'):<15} {res['chosen']:<15} {conf:>5.2f} "
              f"{float(exp.get('min_confidence', 0)):>4.1f} {','.join(res['flags']) or '-':<40} {'pass' if ok else 'FAIL'}")
    print(f"\nmatch: {passed}/{len(cases)} pass")
    return 0 if passed == len(cases) else 1


def stage_grill(cases: list[dict]) -> int:
    print(f"{'brief':<22} {'pack':<15} {'r1':>3} {'maxQ':>4} {'confirms':>8} {'mode':<11} result")
    print("-" * 80)
    passed = 0
    for c in cases:
        exp = c["expected"]
        tmp = Path(tempfile.mkdtemp(prefix="foundry-eval-"))
        try:
            (tmp / ".foundry").mkdir()
            (tmp / ".foundry" / "brief.md").write_text("# Brief\n\n" + c["brief"] + "\n", encoding="utf-8")
            res = F.match_brief(c["brief"], ROOT)
            sel = F.selection_from_match(res)
            (tmp / ".foundry" / "pack.yaml").write_text(F.dump_yaml(sel), encoding="utf-8")
            pack = F.load_pack(ROOT, sel["chosen"])
            ledger = F.load_ledger(tmp, sel["chosen"])
            unattended = "no-questions-requested" in sel["flags"] or os.environ.get("FOUNDRY_UNATTENDED") == "1"
            if unattended:
                ledger["mode"] = "unattended"
            for pf in sel["prefilled"]:
                F.decide(ledger, pack, pf["question_id"], pf["value"], "brief", None, 0)
            plan = F.grill_plan(pack, ledger, sel["prefilled"], 1)
            asked = 0 if unattended else len(plan)
            confirms = [q["id"] for q in plan if q["why"] == "confirm-prefill"]
            irreversible_prefills = [p["question_id"] for p in sel["prefilled"]
                                     if any(q["id"] == p["question_id"] and not q.get("reversible", True) for q in pack["questions"])]
            ok = (len(plan) <= 7 and asked <= int(exp.get("max_questions", 7))
                  and set(confirms) == set(irreversible_prefills)
                  and (not unattended or asked == 0))
            passed += ok
            print(f"{c['name']:<22} {sel['chosen']:<15} {asked:>3} {int(exp.get('max_questions', 7)):>4} {len(confirms):>8} "
                  f"{ledger['mode']:<11} {'pass' if ok else 'FAIL'}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    print(f"\ngrill: {passed}/{len(cases)} pass")
    return 0 if passed == len(cases) else 1


def stage_prd(cases: list[dict]) -> int:
    fixtures = sorted(p for p in FIXTURES.iterdir() if (p / ".foundry" / "prd.md").exists()) if FIXTURES.exists() else []
    passed = 0
    for fx in fixtures:
        errs = F.gate_prd(fx, ROOT)
        ok = not errs
        passed += ok
        print(f"prd fixture {fx.name:<20} {'pass' if ok else 'FAIL'}")
        for e in errs:
            print(f"    {e}")
    print(f"\nprd: {passed}/{len(fixtures)} pass")
    return 0 if fixtures and passed == len(fixtures) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stage", choices=STAGES, help="run one stage (default: all implemented)")
    a = ap.parse_args(argv)
    cases = load_cases()
    if not cases:
        print("no briefs found")
        return 1
    rc = 0
    for st in ([a.stage] if a.stage else list(STAGES)):
        rc |= {"match": stage_match, "grill": stage_grill, "prd": stage_prd}[st](cases)
        print()
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
