# Foundry pipeline

Phases 0–10 run under `/foundry`; 11–15 under `/foundry-build`. `/foundry-resume` re-enters at the
first phase whose gate fails. Every artifact lives under `.foundry/` in the target app repo.

| Phase | Name | Skill | Reads | Writes | Gate |
|------:|------|-------|-------|--------|------|
| 0 | Intake | /foundry | brief | .foundry/brief.md, .foundry/metrics.jsonl | `gate 0`: brief.md exists and is non-empty |
| 1 | Pack match | pack-match | brief, packs/index.csv | .foundry/pack.yaml | `gate 1`: selection validates; top confidence ≥ pack threshold (0.7 domain, 0.0 generic) else generic; ties within 0.15 resolved by must_have overlap inside `match` |
| 2 | Bounded grill | bounded-grilling | .foundry/pack.yaml, packs/<slug>/pack.yaml | .foundry/decisions.yaml | `gate 2`: `grill-plan` rounds 1 and 2 empty, ledger validates, every pack question has an entry; budget 7 (round 1, confirms first) / 3 (round 2 followups) |
| 3 | PRD | prd (`prd-skeleton` + model sections 1 and 9) | decisions, pack, brief | .foundry/prd.md | `gate 3`: no unfilled model block; frontmatter hash matches ledger; every must_have in Scope IN; every should_have in IN or OUT; every decision cited [D:id] or in Open assumptions; NFR names offline, latency, devices, languages |
| 4 | Domain model | domain-model (`domain-skeleton` + workflow walk) | prd, pack entities, workflows.md sections in scope | CONTEXT.md, .foundry/domain.yaml | `gate 4`: schema; every PRD job and feature id resolves in CONTEXT.md; every entity has an invariant and a transition; every transition names a persona; every event has a consumer or is external |
| 5 | Architecture | architecture (`arch-skeleton`) | domain, ledger, stacks.csv | .foundry/architecture.md, .foundry/adr/0001–0009 | `gate 5`: nine ADRs exist, validate, accepted, cite [D:] or pack-default, ≤60 lines; architecture.md frontmatter validates, ≥5 trust boundaries, stack_id in stacks.csv |
| 6 | Data + API | data-model (`schema-skeleton`), api-contract (`api-skeleton`) | domain, architecture | prisma/schema.prisma, openapi.yaml, .foundry/events.yaml | `gate 6`: model per entity and enum per state list (`npx prisma validate` when available); OpenAPI 3.1 with unique operationIds, x-foundry.authz and 2xx/4xx on every operation, a path per entity, an operation per job; events.yaml validates |
| 7 | Design system | design-system (`design-skeleton`) | pack ui_profile, product-types.csv, palettes/typography/styles/components/ux-rules.csv, brand answers | design-system/MASTER.md, tokens.json, tailwind.tokens.css, pages/README.md | `gate 7`: files exist; `design-check` passes (palette contrast, token scales); MASTER.md has Intent, Palette, Typography, Scales, Components, Do and avoid, RTL, Print; every component in components.csv |
| 8 | Screens | screen-spec (`screens-skeleton`) | PRD §3, pack screens.md sections, openapi.yaml, components.csv, ux-rules.csv | .foundry/screens/<id>.md | `gate 8`: every PRD job has a screen; six states with copy; components, operationIds and rule ids exist; ≥3 a11y rules and ≥1 RTL rule (RTL regions); unique routes |
| 9 | Security | threat-model, compliance (`threat-skeleton`) | architecture.md boundaries, openapi.yaml, decisions, threat-patterns.csv, security-controls.csv | .foundry/threats.md, compliance.yaml, compliance-evidence-plan.md | `gate 9`: ≥4 STRIDE rows per boundary; authz row per operation; money operations carry access, business-logic and error-log controls and never 'any authenticated'; PRD §8 controls in compliance.yaml; pci_scope set; no high threat without a control |
| 10 | Tickets | to-tickets (`tickets-skeleton`) | all phase 0–9 artifacts, stacks.csv | .foundry/tickets/T-*.md, compliance.yaml owners | `gate 10`: DAG acyclic; every must-have job, public job operation and screen covered; every planned control owned; ≥3 acceptance tests per ticket; T-000 unblocked; ≤60 tickets |
| 11 | Implement | /foundry-build (thin parent: card → ticket-builder subagent, sonnet → ticket-finisher subagent, sonnet; second builder is the escalation slot, opus only after it); builder: `build activate`, red/green, `run --tail 30`, `dod --tier fast`, progress file; finisher: `dod --tier full`, reviews, commit | ticket, code graph (codebase-memory-mcp, mandatory), screen specs, copy.csv | code, tests, .foundry/tickets/T-xxx.status.yaml, .foundry/screenshots/, metrics.jsonl | `dod`: typecheck, lint, unit, integration, e2e-smoke, a11y-axe (serious/critical fail), screenshot (light/dark × ltr/rtl), semgrep, detect_changes_risk ≤ medium, spec-review; max 3 fix loops |
| 12 | Review | code-review, ui-review, security-review (parallel subagents dispatched by ticket-finisher; re-review with `review-pack --hunks-since last`: changed hunks + own previous blocking list) | `.foundry/reviews/T-xxx.pack.md` (≤600 tokens), `.diff`, screenshots, semgrep | .foundry/reviews/T-xxx.{code,ui,sec}.json (verdict, blocking[], nonblocking[]) | zero blocking findings across the three; `dod` spec-review reads code.json |
| 13 | Human-only | wizard (`wizard scaffold`, triggered by implement-ticket) | ticket, ADR 0006, .env.example | .foundry/wizard/<slug>.md, .ps1, .sh; stub adapter behind FEATURE_<SLUG> | `wizard status`: every variable present in .env.local and the validation command exits 0; until then the ticket ships stubbed |
| 14 | Release | /release (`release-skeleton`) | ticket commits, ADR 0007, screens, copy.csv, wizards | CHANGELOG.md, apps/*/Dockerfile, compose.prod.yml + Caddyfile or fly.toml, runbook.md, scripts/smoke.mjs, user-docs/ | `gate release`: for `regulated: true` packs a human `release confirm --by <name>` after the regulator-licence wizard; files present; `pnpm run build`; prod api+web started on 3101/3100; smoke.mjs passes /health, enrol + whoami, the pack `vocabulary.smoke` route, / |
| 15 | Handoff | every user-invoked skill on exit (`handoff write`) | build.yaml, wizards, metrics | .foundry/handoff.md with frontmatter phase, active_ticket, done[], blocked[], wizards_pending[], next_command, cbm_project, generation | SessionStart hook injects the frontmatter + next_command (≤15 lines); /foundry-resume continues at the exact ticket |

Gates 0–10 are enforced by `scripts/foundry.py gate <phase>` (number or name). `doctor` runs before phase 4; `design-check` runs inside gate 7; `tickets next` feeds phase 11. Later gates arrive with
their phases; until then each skill states its gate in frontmatter.

## Phase 2 mechanics

`grill-plan --round 1` = confirms for every prefilled answer whose question is `reversible: false`
(in rank order), then unanswered questions by rank, excluding questions that only a `followups`
entry can unlock, capped at 7. `grill-plan --round 2` = followups unlocked by answered values
(`when: *` or an exact value), minus answered, capped at 3. Unattended mode (`FOUNDRY_UNATTENDED=1`,
`/foundry --unattended`, or the `no-questions-requested` flag) records every would-be question with
`source: timeout-default`; confirms keep the brief value. `decide --apply-defaults` closes the rest
with `source: pack-default`.

## Phase 1 confidence formula (`foundry.py match`, matcher 1.0)

For each index.csv row: `raw = (3.0 × alias phrase hits + 1.0 × keyword hits + 0.5 × stem hits) / (1 + ln(1 + keyword count))`.
Then `confidence = (raw / max raw) × min(1, distinct hits / 3) × (1 − overlap²)` where `overlap` is the
best other domain pack's raw divided by this pack's raw (generic is exempt). The saturation term keeps a
single stray word such as "shop" below threshold; the overlap term sends a brief that names every
module at once ("POS, inventory, accounting, HR, CRM") to generic with the `scope-sprawl` flag.

## Build loop commands

All run as `python scripts/foundry.py <command>` from the app folder (`--dir` defaults to the cwd).

| Command | What it does |
|---------|--------------|
| `build activate --ticket T-xxx` | stamps the ticket window and prints the ticket card (the spec, at most 80 lines) |
| `dod --ticket T-xxx --tier fast\|full` | fast = typecheck, lint, unit in parallel; full = every step, one Playwright run for smoke, axe and screenshots |
| `review-pack --ticket T-xxx [--hunks-since <sha>\|last]` | `.foundry/reviews/T-xxx.pack.md` (at most 600 tokens) + `.diff`, the only reviewer inputs; a re-review sees changed hunks plus each family's previous blocking list |
| `run --tail 30 -- <cmd>` | full log to `.foundry/logs/`, only the last 30 lines printed |
| `wizard status\|scaffold` | human-only prerequisites: md + ps1 + sh that prompt, validate, write `.env.local` |
| `release-skeleton`, `gate release` | release files; smoke on a local production build |
| `release confirm --by <name>` | human confirmation for `regulated: true` packs; `gate release` stays red until it exists |
| `metrics ingest [--since ts]`, `metrics report [--phases] [--by-model]` | real tokens per ticket from Claude Code transcripts, priced by `data/model-prices.csv` |
| `status` | one-screen dashboard |
| `handoff write\|show` | `.foundry/handoff.md` frontmatter for `/foundry-resume` |
