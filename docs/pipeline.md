# Foundry pipeline

Phases 0–10 run under `/foundry`; 11–15 under `/foundry-build`. `/foundry-resume` re-enters at the
first phase whose gate fails. Every artifact lives under `.foundry/` in the target app repo.

| Phase | Name | Skill | Reads | Writes | Gate |
|------:|------|-------|-------|--------|------|
| 0 | Intake | /foundry | brief | .foundry/brief.md | brief non-empty |
| 1 | Pack match | pack-match | brief, packs/index.csv | .foundry/pack.yaml | top confidence ≥ its index.csv threshold (0.7 for domain packs, 0.0 for generic) else generic; ties within 0.15 resolved by must_have overlap |
| 2 | Bounded grill | bounded-grilling | pack defaults, brief | .foundry/decisions.yaml | frontier empty AND questions ≤ 7 (round 1) / 3 (round 2) |
| 3 | PRD | prd | decisions, pack | .foundry/prd.md | every pack must_have present or explicitly excluded |
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

Gates are enforced by `scripts/foundry.py gate <phase>` (P7+). Until then each skill states its
gate in frontmatter and checks it by hand.

## Phase 1 confidence formula (`foundry.py match`, matcher 1.0)

For each index.csv row: `raw = (3.0 × alias phrase hits + 1.0 × keyword hits + 0.5 × stem hits) / (1 + ln(1 + keyword count))`.
Then `confidence = (raw / max raw) × min(1, distinct hits / 3) × (1 − overlap²)` where `overlap` is the
best other domain pack's raw divided by this pack's raw (generic is exempt). The saturation term keeps a
single stray word such as "shop" below threshold; the overlap term sends a brief that names every
module at once ("POS, inventory, accounting, HR, CRM") to generic with the `scope-sprawl` flag.
