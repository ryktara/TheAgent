---
name: foundry-resume
description: Resume a Foundry run from .foundry/ alone in a fresh session. Find the last passed gate (0–8) and continue from the next phase.
invocation: user
model: sonnet
reads: [.foundry/brief.md, .foundry/pack.yaml, .foundry/decisions.yaml, .foundry/prd.md, .foundry/domain.yaml, .foundry/architecture.md, openapi.yaml, design-system/MASTER.md, .foundry/screens/*.md, .foundry/metrics.jsonl]
writes: [.foundry/metrics.jsonl]
gate: python scripts/foundry.py gate screens
---

# /foundry-resume — orchestrator

Phases 0–8 implemented; 9+ hand off to docs/pipeline.md pointers.

## Steps

1. **Locate the frontier.** Run gates in order and stop at the first failure:

   ```
   python scripts/foundry.py gate 0
   python scripts/foundry.py gate 1
   python scripts/foundry.py gate 2
   python scripts/foundry.py gate 3
   python scripts/foundry.py gate 4
   python scripts/foundry.py gate 5
   python scripts/foundry.py gate 6
   python scripts/foundry.py gate 7
   python scripts/foundry.py gate 8
   ```

   Done when: `next_phase` = the number of the first gate that failed, or 9 when all pass.

2. **Restore mode.** Read `mode` from `.foundry/decisions.yaml` when it exists; `unattended`
   sets `FOUNDRY_UNATTENDED=1` for the rest of the run.
   Done when: the mode is set.

3. **Continue.** Run the /foundry steps from `next_phase` onward (doctor before phase 4), each
   wrapped in `metrics --phase <n> --start` and `metrics --phase <n> --note "resumed"`, with the
   same retry rule and final report. When `next_phase` is 9, print the report and point to
   `/foundry-continue`.
   Done when: gate 8 passes or the run stopped with the failing gate printed.

## Reference

| First failing gate | Meaning | Action |
|--------------------|---------|--------|
| 0 | no brief | ask for the brief; this is the one question resume may ask |
| 1 | no or invalid selection | re-run pack-match |
| 2 | ledger incomplete | bounded-grilling picks up: `grill-plan` lists only unanswered questions |
| 3 | PRD missing or stale hash | re-run prd |
| 4 | domain.yaml or CONTEXT.md missing or incomplete | re-run domain-model |
| 5 | ADRs or architecture.md missing | re-run architecture |
| 6 | schema or openapi missing or failing | re-run data-model then api-contract |
| 7 | design-system files missing or design-check failing | re-run design-system |
| 8 | screens missing or bindings broken | re-run screen-spec |
