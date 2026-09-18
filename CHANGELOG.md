# Changelog

One entry per build step. Newest first.

## P9 — Isolation, routing, evals, dogfood (2026-09-18)

- Context isolation: /foundry-build is a thin parent (card → one implementer subagent → ≤300-token return →
  complete → handoff); implement-ticket writes `T-xxx.progress.md` after RED, GREEN and each DoD run and returns
  a JSON contract; reviewers are dispatched by the implementer with their frontmatter models.
- Model routing enforced (docs/models.md): ui-review, compliance, to-tickets on haiku; architecture and threat-model
  on opus; escalation to opus once after three failed DoD loops (`metrics --escalated true`).
- Metrics: ingest records per-model tokens/cost, context peak and subagent turns; `metrics report --by-model`;
  status shows blended cost per ticket and escalations; `data/model-prices.csv` rows for sonnet/haiku/opus.
- Screens: `routes: [{path, query?, state?}]` in screen frontmatter (skeleton + gate); the DoD screenshot pass
  iterates the variants.
- security-review cites SYNC-RULES.md ids for offline/REST parity.
- Evals: `evals/thresholds.yaml` with regression ceilings; stages `golden` (artefact diffs against
  evals/expected/restaurant-pos with an allowlist), `triggers` (40 prompts → skill via `claude -p`), `e2e`
  (unattended phases 0–10 + `/foundry-build --n 2` + release smoke via `claude -p`); `--update-thresholds`,
  `--update-golden`.

## P8 — Efficiency, metrics, wizard, release, handoff (2026-09-18)

- fix: release smoke tears the prod servers down with a synchronous kill and sets exitCode (reason: an async
  taskkill during exit tripped a libuv assertion on Windows and failed `gate release` after 5/5 checks passed).
- Loop efficiency: `dod --tier fast|full` (fast = typecheck+lint+unit in parallel; stop hook uses it); one Playwright
  run (`tests/e2e/dod.spec.ts`) serves axe + screenshots for declared routes, `fullPage` off for list routes, dev
  servers reused between runs (`FOUNDRY_DOD` instead of `CI`); `build activate` prints the ticket card (the spec,
  ≤80 lines) and stamps the window; `review-pack --ticket` builds the only reviewer input (≤1.5k-token header +
  diff); implement-ticket applies blocking items at file+line and reruns only the fast tier + the blocking family;
  toast stacks at top-end (max 3, safe area, RTL aware) with `ToastViewport` + `toast()`.
- Real metrics: `metrics ingest` reads Claude Code transcripts (`~/.claude/projects/<cwd-encoded>/…`) and sums
  input/output/cache tokens per assistant turn into ticket windows from `build.yaml` stamps (back-filled from
  ticket-end rows for older tickets), priced by `data/model-prices.csv`; `metrics report` shows self-reported and
  transcript columns, `--compare a b`, `--phases`.
- Wizard skill + `wizard scaffold|status`: md with exact steps, ps1/sh that prompt, validate by regex, write
  `.env.local`, run the validation command; ticket continues behind `FEATURE_<SLUG>`.
- Release skill + `release-skeleton` + `gate release`: CHANGELOG from ticket commits, Dockerfiles, compose.prod.yml +
  Caddyfile (VPS) or fly.toml per ADR 0007, runbook, smoke.mjs, user docs (cashier en/ar, manager en) from screens
  and copy.csv; the gate builds and smokes a local production start.
- Handoff/resume: `handoff write|show` with a frontmatter schema; SessionStart injects frontmatter + next_command
  only; /foundry-resume continues at the exact ticket; `status` dashboard.
- Pack schema 1.8: `jobs[].extra_readers` (api-skeleton authz) and `jobs[].merge_into` (tickets-skeleton).
- doctor reports the codebase-memory watcher flag; eslint template adds the `fetch` global.

## P7b — Build loop on real tickets (2026-09-18)

- fix: `metrics report` sums the agent-reported `grep_read_calls` on ticket-end records (reason: the P7b
  report showed 0 for every ticket although the values were recorded).
- fix: scaffold `globals.css` adds `@source "../../../packages/ui/src"` (reason: Tailwind v4 never scanned the
  shared UI package, so `grid-cols-3` on Numpad was missing and the T-004 RTL numpad test failed once `.next` was
  rebuilt in T-008).
- fix: screenshot spec waits for network idle and for `[aria-busy="true"]` to detach before capturing (reason:
  T-008 shots captured the loading skeleton while PGlite initialised).
- fix: `schema-skeleton` no longer appends `created_at`/`updated_at`/`deleted_at` when the pack entity already
  lists them (reason: `prisma validate` failed on SyncEvent with a duplicate created_at in T-003).
- fix: ESLint template declares `console`, `process`, `URL`, `Buffer` globals for `.mjs` scripts (reason:
  build-tokens.mjs and pg-local.mjs failed `no-undef` in T-003).
- fix: `tickets-skeleton` purges stale `T-*.md` before writing (reason: a re-run after re-ranking left two
  ticket series with duplicate ids in proj7, and `build activate T-008` picked the stale one).
- fix: DoD `e2e-smoke` runs every Playwright spec except axe and screenshot suites, so per-ticket
  screen state tests are part of the gate (reason: pin.spec.ts never ran under DoD).
- fix: ESLint unused-vars ignores `_`-prefixed destructured names (reason: `{ pin_hash: _p, ...rest }`
  failed lint in T-001).
- fix: Playwright screenshot cookie URL uses WEB_PORT (reason: P7a answer 4).
- `foundry.py metrics report` and `metrics --ticket … --tokens-in …` ticket-end records with
  graph_calls, grep_read_calls, dod_loops, review_blocking_count.
- doctor warns about semgrep (CI-only on Windows).

## P7a — Build loop machinery and T-000 (2026-09-18)

- schema 1.7 `jobs[].priority`; tickets ordered by priority, entity graph, pack job order.
- Unreviewed copy rows render with `<!-- unreviewed -->` in screen specs.
- `doctor --build` requires codebase-memory-mcp on PATH and registered as an MCP server.
- scripts/foundry_build.py: `build activate|complete|index|status` (.foundry/build.yaml),
  `dod --ticket` (10 steps, status.yaml, metrics), `scaffold --stack nextjs-pwa` (T-000: pnpm
  monorepo with Next 15 + Tailwind 4 + next-intl, Hono api, Prisma db, ui components, vitest,
  Playwright + axe, docker compose, CI).
- hooks/: bash_guard, edit_guard, metrics, session_start, stop_check; hooks.json registered in
  the plugin manifest; hooks/test_hooks.py.
- Skills: implement-ticket, code-review, ui-review, security-review; /foundry-build real.

## P6 — Security, compliance, tickets (2026-09-18)

- fix: palettes.csv carries a full dark role set and design-check validates dark pairs;
  tokens.json dark theme complete; MASTER.md palette table has a Use column; gate design
  rejects non-text-only roles used as text.
- schema 1.6: `ui_profile.palette / typography / style / themes`; restaurant-pos pinned to
  ember-kitchen (cashier) and kds-dark (kitchen).
- data: security-controls.csv (ASVS 5.0, OWASP API Top 10, PCI-DSS 4.0, OWASP Agentic Top 10 on
  the build process), threat-patterns.csv (STRIDE per boundary type), copy.csv (en/ar/ur, all
  rows reviewed=false); screens-skeleton fills Arabic and Urdu from copy.csv.
- scripts/foundry_security.py: `threat-skeleton`, `tickets-skeleton`, `tickets next`; gates
  security and tickets.
- Skills: threat-model, compliance, to-tickets; /foundry and /foundry-resume cover 0–10 and end
  with "Run /foundry-build to implement".
- Evals: stages security and tickets; fixture through phase 10.

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
