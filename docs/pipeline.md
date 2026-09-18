# Foundry pipeline

Phases 0–10 run under `/foundry`; 11–15 under `/foundry-build`. `/foundry-resume` re-enters at the
first phase whose gate fails. Every artifact lives under `.foundry/` in the target app repo.

| Phase | Name | Skill | Reads | Writes | Gate |
|------:|------|-------|-------|--------|------|
| 0 | Intake | /foundry | brief | .foundry/brief.md, .foundry/metrics.jsonl | `gate 0`: brief.md exists and is non-empty |
| 1 | Pack match | pack-match | brief, packs/index.csv | .foundry/pack.yaml | `gate 1`: selection validates; top confidence ≥ pack threshold (0.7 domain, 0.0 generic) else generic; ties within 0.15 resolved by must_have overlap inside `match` |
| 2 | Bounded grill | bounded-grilling | .foundry/pack.yaml, packs/<slug>/pack.yaml | .foundry/decisions.yaml | `gate 2`: `grill-plan` rounds 1 and 2 empty, ledger validates, every pack question has an entry; budget 7 (round 1, confirms first) / 3 (round 2 followups) |
| 3 | PRD | prd | decisions, pack, brief | .foundry/prd.md | `gate 3`: frontmatter hash matches ledger; every must_have in Scope IN; every should_have in IN or OUT; every decision cited [D:id] or in Open assumptions; NFR names offline, latency, devices, languages |
| 4 | Domain model | domain-model | prd, pack entities | CONTEXT.md, .foundry/domain.yaml | every PRD noun in glossary; every entity has invariants |
| 5 | Architecture | architecture | domain, nfrs | .foundry/architecture.md, .foundry/adr/*.md | ADRs for stack, auth, tenancy, data store, offline, integrations, deployment |
| 6 | Data + API | data-model, api-contract | domain, architecture | schema, openapi.yaml, .foundry/events.yaml | schema compiles; every endpoint has authz rule |
| 7 | Design system | design-system | pack ui_profile, brand answers | design-system/MASTER.md, tokens.json | contrast/type/spacing validator passes |
| 8 | Screens | screen-spec | prd, domain, design system | .foundry/screens/*.md | every job has a screen; every screen has empty/loading/error states |
| 9 | Security | threat-model, compliance | architecture, api, pack compliance | .foundry/threats.md, .foundry/compliance.yaml | every endpoint mapped to a control |
| 10 | Tickets | to-tickets | all | .foundry/tickets/*.md | DAG acyclic; every feature covered |
| 11 | Implement | /foundry-build → implement-ticket | ticket, code graph | code, tests, .foundry/metrics.jsonl | typecheck+tests+lint+semgrep+axe green; screenshot captured |
| 12 | Review | code-review, ui-review, security-review | diff, spec | .foundry/reviews/*.md | zero blocking findings |
| 13 | Human-only | wizard | architecture | .foundry/wizard/*.ps1 and *.sh | human confirms |
| 14 | Release | release | all | CHANGELOG.md, deploy config, runbook | smoke test on deployed URL |
| 15 | Handoff | handoff | .foundry/ | .foundry/handoff.md | fresh session resumes from file alone |

Gates 0–3 are enforced by `scripts/foundry.py gate <phase>` (number or name). Later gates arrive with
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
