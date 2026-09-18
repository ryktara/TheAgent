"""Foundry eval runner.

Stages implemented:
  match   run foundry.py match on every golden brief; compare to expected_pack / min_confidence.

Later stages (grill, prd, ...) arrive with their pipeline phases. Usage:
  python evals/run.py [--stage match]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from foundry import match_brief, parse_yaml  # noqa: E402

BRIEFS = ROOT / "evals" / "briefs"
EXPECTED = ROOT / "evals" / "expected"
STAGES = ("match",)


def load_cases() -> list[dict]:
    cases = []
    for brief in sorted(BRIEFS.glob("*.md")):
        exp_path = EXPECTED / f"{brief.stem}.yaml"
        text = brief.read_text(encoding="utf-8")
        body = "\n".join(l for l in text.splitlines() if not l.startswith("#")).strip()
        exp = parse_yaml(exp_path.read_text(encoding="utf-8")) if exp_path.exists() else {}
        cases.append({"name": brief.stem, "brief": body, "expected": exp})
    return cases


def stage_match(cases: list[dict]) -> int:
    print(f"{'brief':<22} {'expected':<15} {'chosen':<15} {'conf':>5} {'min':>4} {'flags':<32} result")
    print("-" * 104)
    passed = 0
    for c in cases:
        exp = c["expected"]
        res = match_brief(c["brief"], ROOT)
        top = res["candidates"][0]
        conf = top["confidence"] if res["chosen"] == top["slug"] else 0.0
        ok = res["chosen"] == exp.get("expected_pack") and conf >= float(exp.get("min_confidence", 0))
        for flag in exp.get("expected_flags", []) or []:
            ok = ok and flag in res["flags"]
        passed += ok
        print(f"{c['name']:<22} {exp.get('expected_pack', '?'):<15} {res['chosen']:<15} {conf:>5.2f} "
              f"{float(exp.get('min_confidence', 0)):>4.1f} {','.join(res['flags']) or '-':<32} {'pass' if ok else 'FAIL'}")
    print(f"\nmatch: {passed}/{len(cases)} pass")
    return 0 if passed == len(cases) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stage", choices=STAGES, help="run one stage (default: all implemented)")
    a = ap.parse_args(argv)
    cases = load_cases()
    if not cases:
        print("no briefs found")
        return 1
    stages = [a.stage] if a.stage else list(STAGES)
    rc = 0
    for st in stages:
        rc |= {"match": stage_match}[st](cases)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
