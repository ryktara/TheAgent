# Changelog

One entry per build step. Newest first.

## P5 — Design layer and screens (2026-09-18)

- fix: schema 1.5 `entities[].exposure` (public|internal|derived) prunes the API to 87 operations
  on the Sharjah run; `jobs[].entity` required for complete packs replaces the job hint table.
- data/: ux-rules (243), palettes (60, all pairs pass), typography (32), styles (26),
  product-types (64), charts (27), components (50); data/SOURCES.md.
- `foundry.py design-check` (WCAG contrast + token scale checks), `design-skeleton`,
  `screens-skeleton`; gates design and screens; scripts/foundry_design.py.
- Skills: design-system, screen-spec; /foundry and /foundry-resume cover phases 0–8.
- Evals: stages design and screens; CI runs design-check on palettes.

## P4 — Domain, architecture, data, API (2026-09-18)

- fix: schema 1.4 `questions[].enables` replaces the should-have token heuristic; region-scoped
  `regional[R].compliance_must/should` and gate prd rejects controls of a non-decided region;
  `regional.PK.tax_by_province` table rendered in PRD §8; sources.md statuses updated.
- `foundry.py doctor`, `query <csv> --col value`, data/stacks.csv (14 rows).
- scripts/foundry_phases.py: `domain-skeleton` (domain.yaml + CONTEXT.md), `arch-skeleton`
  (9 ADRs + architecture.md), `schema-skeleton --orm prisma|drizzle`, `api-skeleton`
  (openapi.yaml 3.1 + events.yaml); gates domain, architecture, data, api.
- YAML subset parser reads block mappings inside lists (nested OpenAPI output).
- Schemas: domain, adr, events, architecture-frontmatter.
- Skills: domain-model, architecture (+ ADR-TEMPLATE), data-model, api-contract; /foundry and
  /foundry-resume cover phases 0–6.
- Evals: stages domain, architecture, data, api on the restaurant fixture; fixture extended.

## P3 — restaurant-pos pack, prd-skeleton, fixes (2026-09-18)

- fix: `followups[].when` accepts a list (schema 1.3); `derive_from` resolves a question from its
  parent answer with `source: agent-fact`; payment vocabulary removed from keyword lists so a
  provider name no longer ties two packs; saturation at 2 distinct hits.
- packs/restaurant-pos: complete pack (27 jobs, 25 entities, 24 invariants, 8 regions, 12 ranked
  questions) with reference/ screens, workflows, glossary (104 terms), compliance (control ids),
  ux-patterns, sources (verified vs UNVERIFIED).
- `foundry.py prd-skeleton` writes sections 2–8 and 10; prd skill fills 1 and 9; gate prd rejects
  unfilled model blocks.
- `foundry.py match --rematch --answers` re-scores with round-1 free-text answers.
- Pack lint for `complete: true`: screens headings, entity references, compliance ids, glossary
  size, sources.md, unique maps_to. generic marked complete and brought up to the lint.
- Evals: 6 restaurant variant briefs (match 11/11).

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
