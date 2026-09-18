# Changelog

One entry per build step. Newest first.

## P2 — Bounded grilling, decision ledger, PRD, /foundry 0–3 (2026-09-18)

- pack.schema.json 1.2: `threshold` in pack.yaml, `followups` on questions (round-2 unlocks).
  All four packs bumped; each gains 2–3 followups and their target questions.
- `foundry.py sync-index` regenerates packs/index.csv; `validate` fails on drift.
- `foundry.py match`: tie resolution by must_have overlap moved in (`chosen_by`); `--write`
  emits .foundry/pack.yaml; matcher 1.1.
- `foundry.py grill-plan`, `decide` (incl. `--apply-prefilled`, `--apply-defaults`,
  `--auto-unattended`), `gate` (intake, pack-match, grill, prd), `metrics` (phase start/end).
- decisions.schema.json: `mode`, `budget.round*_used`, `value`, `maps_to`.
- Skills: bounded-grilling, prd (+ PRD-TEMPLATE.md), pack-match (deterministic, no pack reads),
  /foundry real for phases 0–3, /foundry-resume real for 0–3, /foundry-continue stub.
- Evals: stages `grill` (5/5) and `prd` (fixture under evals/fixtures/restaurant-pos).

## P1 — Pack schema 1.1, generic pack, pack-match (2026-09-18)

- pack.schema.json 1.1: `version`, ranked question bank (≤12) with `rank`, `answer_type`,
  `choices`, `skip_if_brief_mentions`, `brief_hints`, `maps_to`. Round budget moves to grill time.
- packs/generic: full fallback pack with 12 ranked questions and five reference files.
- packs/restaurant-pos, retail-pos, trading-app: scaffolded with real aliases and keywords so
  matching works today; reference content arrives in P3 and P10.
- `foundry.py match --brief <path|-> [--json]`: deterministic scorer with prefill and flags.
- skills/pack-match: phase 1 skill (haiku).
- schemas/pack-selection.schema.json; validate checks `.foundry/pack.yaml` in cwd when present.
- evals/run.py stage `match`: 5/5 golden briefs.

## P0 — Scaffold (2026-09-18)

- Plugin manifest, house style, orchestrator stubs, schemas, validate, scaffold-pack, tests,
  CI, golden briefs.
