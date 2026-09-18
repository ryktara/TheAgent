# Changelog

One entry per build step. Newest first.

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
