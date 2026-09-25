# Changelog

One entry per build step. Newest first.

## 1.0.0 (2026-09-24) — summary of P0–P11

Foundry 1.0 is a Claude Code plugin that takes a one-line brief to a designed, architected, implemented,
reviewed and released web app while asking at most 7 questions (plus 3 follow-ups). Subscription-only: it runs
inside a logged-in Claude Code session, reads no API key and has no headless mode.

- Pipeline (P0–P6): pack match with a deterministic confidence formula, bounded grilling with a decision ledger,
  PRD, domain model with invariants and state machines, architecture with nine ADRs, Prisma schema, OpenAPI 3.1
  with authz per operation, design system from CSV data (palettes with WCAG contrast, typography, components,
  UX rules), screen specs with six states and bilingual copy, STRIDE threat model, compliance map, ticket DAG.
  Every phase has a skeleton generator and a machine-checked gate.
- Build loop (P7–P10): codebase-memory graph first, red/green per ticket, definition of done in two tiers (fast:
  typecheck/lint/unit; full: integration, one Playwright run for smoke + axe + light/dark × ltr/rtl screenshots),
  thin parent → ticket-builder → ticket-finisher → three reviewers on a ≤600-token pack with hunk-only re-review,
  a 120-tool-call builder budget, wizards for human-only steps, release artefacts (Dockerfiles, compose + Caddy or
  fly.toml, runbook, smoke, user docs), handoff and resume, real per-ticket cost from transcripts by model.
- Packs (P3, P10, P11): restaurant-pos, retail-pos and trading-app complete (schema 2.0 with `vocabulary`,
  `contexts`, `regulated`), generic fallback, pack-level CSV overrides; the core carries no restaurant wording.
- Evals (P9–P11): deterministic stages for every pack (match, grill, skeleton gates, golden artefact diffs) in CI;
  `/foundry-eval` for the trigger test and the unattended end-to-end run, scored into `evals/results/`.
- Reference app: restaurant-pos for a Sharjah café, 49 tickets built through the loop, release gate passing;
  cost and medians in docs/examples/restaurant-pos/COST.md.
- Install: `claude plugin marketplace add` + `claude plugin install foundry@foundry-local` + `/foundry-setup`;
  docs/INSTALL-WINDOWS.md, docs/INSTALL-MAC-LINUX.md, docs/QUICKSTART.md (en, ar), docs/PACK-AUTHORING.md,
  docs/ORCHESTRATOR.md.

## P11 — v1.0

- fix: CI installs pnpm and the DoD runner unit test skips without pnpm/node (reason: ubuntu runner had no pnpm, so the stub scripts all failed).
- fix: tickets-skeleton sorts the screens folder (reason: CI on ubuntu produced different ticket slugs and screen order because ext4 returns glob results unordered; golden 0/3 there).
- fix: Python 3.11 compatibility (reason: CI on 3.11 rejected a nested same-quote f-string in foundry_design.py; the DoD unit test also ran a real semgrep when one was installed, now mocked out).
- GitHub release: marketplace renamed `theagent` (install `foundry@theagent` from `ryktara/TheAgent`),
  CONTRIBUTING.md, SECURITY.md, CI runs the hook tests, tracked eval results carry no machine paths.
- fix: smoke template regex escape (reason: the Python source emitted a SyntaxWarning on import).
- fix: the smoke template's `--start` now boots an embedded loopback Postgres (`.pg/smoke`, FOUNDRY_PG_PORT+1),
  migrates, seeds and supplies the production-required env before starting the api (reason: `gate release`
  timed out on /health because the fail-fast production config loader had no database and no env).
- Reference app finished 49/49: T-900 release gate passes; COST.md regenerated from all 49 tickets
  ($1,059.64 total, feature median $21.20); README cost table filled; evals/thresholds.yaml refreshed.

- Pack schema 2.0: `vocabulary:` block (scaffold ticket titles, ADR hints/refs, design defaults, glossary hint terms,
  copy overrides, money tokens, terms, operator role, smoke route, containers, event consumers); required on complete packs.
- Core is pack-agnostic: restaurant prose, MONEY_TOKENS/MONEY_JOBS, KDS/table-map component and screen rules, smoke route,
  user-doc names and seed roles now come from the pack; restaurant-only data rows moved to `packs/restaurant-pos/reference/*.csv`
  and merge over `data/*.csv` in place (`foundry.data_rows`, `query --pack`).
- restaurant-pos vocabulary reproduces its golden artefacts byte for byte; retail-pos and trading-app got real vocabularies and
  regenerated goldens; generic got a minimal vocabulary.
- Tests read domain strings from `evals/fixtures/reference-pack.yaml`; new VocabularyTests cover merge, money tokens and fallbacks.
- Builder turn budget (120 tool calls, `status: budget` → fresh builder from the progress file); the finisher skips
  review families that passed and whose files did not change.
- `/foundry-setup` + `foundry.py setup [--apply]`: doctor, pnpm, Playwright browsers, codebase-memory MCP registration,
  validate, 30-second self-test; fresh-clone install tested with a minimal PATH.
- fix: the plugin manifest listed hooks/hooks.json, which Claude Code 2.1 loads automatically and rejected as a
  duplicate; the installed plugin had failed to load (reason: found by the fresh-install test).
- fix: eval fixture and golden `.foundry` folders were gitignored (never reached CI); now tracked.
- fix: ticket globs ignore progress and status files (status counted a progress file as a ticket).
- fix: `gate release` sets `FOUNDRY_SMOKE=1` for the local production smoke so apps can relax host-only checks
  such as TLS to a localhost Postgres (reason: T-041's DB-TLS-in-production control stopped the api from starting
  under the local smoke; the control stays enforced for real deployments).
- fix: the embedded Postgres helper walks up to 30 ports when Windows reserves the requested one and prints the
  port it bound (reason: a dynamic excluded port range swallowed 54329 mid-build and the integration tier could not
  start; `netsh int ipv4 show excludedportrange` shows such ranges).
- Founder docs (QUICKSTART en/ar, INSTALL-WINDOWS, INSTALL-MAC-LINUX, PACK-AUTHORING, ORCHESTRATOR), README for 1.0,
  LICENSE (Al Sadq IT Solutions LLC), plugin 1.0.0.

## P10 — Subscription-only, context split, retail/trading packs (2026-09-23)

- Subscription-only hard rule (CLAUDE.md, README): no API key anywhere, no non-interactive CLI, no headless mode.
  `evals/run.py` keeps deterministic stages only and prints "model stages: run /foundry-eval in Claude Code";
  new `/foundry-eval` skill runs `--stage triggers` (session answers 40 prompts, `--score-triggers` records
  `evals/results/triggers-<date>.json`) and `--stage e2e` (unattended run in a temp dir, `--assert-e2e` records
  `evals/results/e2e-<date>.json`); `--stage results` reads the newest pair in CI.
- Context split: implement-ticket is now ticket-builder (card → RED → GREEN → fast tier → progress file, ≤150-token
  contract) then ticket-finisher (full tier → review pack → three parallel reviewers → fixes → hunk-only re-review →
  commit, ≤300-token contract); the parent dispatches them in sequence, a second builder is the escalation slot and
  opus only after it. `foundry.py run --tail 30 -- <cmd>` caps runner output; `review-pack --hunks-since <sha>|last`
  with a ≤600-token header and each family's previous blocking list; reviewer prompts are JSON-only.
- Metrics: subagent transcripts are attributed to a ticket only when their first message names the project or the
  ticket id (concurrent unrelated subagents no longer land on an open window).
- Pack schema 1.9: `regulated: true` scaffolds the regulator-licence wizard at phase 10 and `gate release` blocks
  until `foundry.py release confirm --by <name>`. Packs retail-pos and trading-app complete (reference ≥120 lines each,
  glossaries 96/126 rows, sources with VERIFIED/UNVERIFIED); 6 eval variants per pack; evals loop over every fixture.
- Playwright in generated projects: `fullyParallel: false`, `workers: 2` (per-file groups that share PGlite state).
- generalisation fix: `tickets-skeleton` read the decision ledger as a dict and crashed before scaffolding the
  regulator-licence wizard (reason: trading-app run, phase 10).
- generalisation fix: an integration ticket is emitted when the API carries a webhook for a category even when no
  decision maps to `integrations.<cat>` (reason: trading-app `webhook_payments` had no owning ticket; gate 10 failed).
- generalisation fix: `stack_id` resolves pack `stack_default` values against stacks.csv by prefix and prefers the
  mobile stack for platform=mobile (reason: trading-app `nextjs` was not a stacks.csv id; gate 5 failed once).
- generalisation fix: packs declare `contexts: {name: [Entity…]}` and `offline_contexts`; domain, API, schema and
  tickets use them instead of the restaurant contexts (reason: both new packs landed Sale/Order in kitchen/menu/inventory).
- generalisation fix: `offline: forbidden` packs get no `offline_capable` operations, no `/sync/*` endpoints, no T-005
  offline ticket, no offline acceptance tests and no offline screen copy (reason: trading-app run, phases 6, 8, 10).
- fix: pack contexts reset to the restaurant defaults for packs that declare none (reason: after a trading-app fixture
  ran, the restaurant golden regen inherited trading contexts in the same process and the golden stage failed 2/3).
- generalisation fix: should-have tickets no longer depend on T-005 when it does not exist, the `sync` context is
  omitted without offline, and the Arabic copy column appears only for Arabic regions (reason: trading-app rerun,
  gate 10 `T-026 blocked by unknown T-005`; Urdu app carried an Arabic column).

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
- fix: reviewers are dispatched by SKILL.md path (reason: an implementer invoked Claude Code's built-in
  `/security-review`, a name collision, and got an error instead of a verdict).
- fix: evals probed the CLI's non-interactive mode with a real call before triggers/e2e (reason: its auth status
  reported ok while non-interactive runs answered "not logged in"); both stages reported the exact skip reason.
  (That path was removed in P10: subscription-only.)
- fix: release smoke/gate must not run while a dev server writes `.next` (reason: `next build` failed on a
  half-written nft.json); the release skill says so.
- dogfood: 12 more tickets (T-011…T-021, T-024) built by sonnet implementer subagents through the thin parent;
  0 escalations; deploy wizard `deploy-vps` scaffolded; cashier-flow video under docs/examples/restaurant-pos.
- Evals: `evals/thresholds.yaml` with regression ceilings; stages `golden` (artefact diffs against
  evals/expected/restaurant-pos with an allowlist), `triggers` (40 prompts → skill) and `e2e` (unattended phases
  0–10 + `/foundry-build --n 2` + release smoke), both through the CLI's non-interactive mode (replaced by
  `/foundry-eval` in P10); `--update-thresholds`, `--update-golden`.

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
