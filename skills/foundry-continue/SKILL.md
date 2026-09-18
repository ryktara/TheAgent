---
name: foundry-continue
description: Continue a Foundry run past the PRD into phases 4–10 (domain model through tickets). Stub until P4.
invocation: user
model: opus
reads: [.foundry/prd.md, .foundry/decisions.yaml, .foundry/pack.yaml]
writes: []
gate: python scripts/foundry.py gate prd
---

# /foundry-continue — orchestrator, phases 4–10

STUB. Phase bodies land in P4–P6. Table: docs/pipeline.md.

## Steps

1. **Check the PRD gate.** `python scripts/foundry.py gate prd`.
   Done when: the gate prints `pass`; otherwise point to `/foundry-resume`.

2. **Report.** Print: "Phases 4–10 arrive in P4+. PRD is ready at .foundry/prd.md."
   Done when: the message is sent.
