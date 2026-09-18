"""Foundry eval runner (P0 stub).

Loads every brief under evals/briefs and its matching expected/*.yaml, then prints a table.
Pipeline execution, scoring and token accounting arrive in P9.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from foundry import parse_yaml  # noqa: E402

BRIEFS = ROOT / "evals" / "briefs"
EXPECTED = ROOT / "evals" / "expected"


def load() -> list[dict]:
    rows = []
    for brief in sorted(BRIEFS.glob("*.md")):
        exp_path = EXPECTED / f"{brief.stem}.yaml"
        text = brief.read_text(encoding="utf-8")
        body = "\n".join(l for l in text.splitlines() if not l.startswith("#")).strip()
        exp = parse_yaml(exp_path.read_text(encoding="utf-8")) if exp_path.exists() else {}
        rows.append({
            "brief": brief.stem,
            "words": len(body.split()),
            "expected_pack": exp.get("expected_pack", "?"),
            "max_questions": exp.get("max_questions", "?"),
            "artifacts": len(exp.get("required_artifacts", [])),
            "has_expected": exp_path.exists(),
        })
    return rows


def main() -> int:
    rows = load()
    header = f"{'brief':<24} {'words':>5} {'pack':<16} {'maxQ':>4} {'artifacts':>9} {'expected':>8}"
    print(header)
    print("-" * len(header))
    for r in rows:
        print(f"{r['brief']:<24} {r['words']:>5} {r['expected_pack']:<16} {r['max_questions']!s:>4} "
              f"{r['artifacts']:>9} {'yes' if r['has_expected'] else 'MISSING':>8}")
    missing = [r["brief"] for r in rows if not r["has_expected"]]
    print()
    print(f"{len(rows)} briefs loaded. Pipeline execution: not implemented in P0.")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
