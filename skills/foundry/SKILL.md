---
name: foundry
description: Build an app from a one-line brief. Run phases 0–10 (intake through tickets) with at most 7 questions asked; resume with /foundry-resume; implement with /foundry-build.
invocation: user
model: opus
reads: [brief]
writes: [.foundry/brief.md, .foundry/pack.yaml, .foundry/decisions.yaml, .foundry/prd.md, CONTEXT.md, .foundry/domain.yaml, .foundry/architecture.md, .foundry/adr/*.md, openapi.yaml, .foundry/events.yaml, design-system/MASTER.md, tokens.json, .foundry/screens/*.md, .foundry/threats.md, .foundry/compliance.yaml, .foundry/tickets/*.md]
gate: python scripts/foundry.py gate 10
---

# /foundry — orchestrator, phases 0–10

STUB. Phase bodies land in P2–P6. Full table with reads, writes and gates: docs/pipeline.md.

## Phases

| Phase | Name | Skill | Status |
|------:|------|-------|--------|
| 0 | Intake | (inline) | not yet implemented |
| 1 | Pack match | pack-match | not yet implemented |
| 2 | Bounded grill | bounded-grilling | not yet implemented |
| 3 | PRD | prd | not yet implemented |
| 4 | Domain model | domain-model | not yet implemented |
| 5 | Architecture | architecture | not yet implemented |
| 6 | Data + API | data-model, api-contract | not yet implemented |
| 7 | Design system | design-system | not yet implemented |
| 8 | Screens | screen-spec | not yet implemented |
| 9 | Security | threat-model, compliance | not yet implemented |
| 10 | Tickets | to-tickets | not yet implemented |

## Steps

1. **Intake.** Write the brief verbatim to `.foundry/brief.md`.
   Done when: `.foundry/brief.md` exists and is non-empty.

2. **Run phases 1–10 in order.** Each phase calls its model-invoked skill and stops on a failed
   gate.
   Done when: every phase's gate in docs/pipeline.md passes, or the failing phase is reported.

Question budget: 7 in round 1, 3 in round 2, 0 after. Unanswered questions take the pack
default after the configured timeout.
