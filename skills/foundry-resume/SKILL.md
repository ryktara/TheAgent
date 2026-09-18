---
name: foundry-resume
description: Resume a Foundry run from .foundry/ alone in a fresh session. Find the last passed gate and continue from the next phase.
invocation: user
model: sonnet
reads: [.foundry/brief.md, .foundry/pack.yaml, .foundry/decisions.yaml, .foundry/prd.md, .foundry/metrics.jsonl]
writes: [.foundry/metrics.jsonl]
gate: python scripts/foundry.py gate prd
---

# /foundry-resume — orchestrator

Phases 0–3 implemented; 4+ hand off to docs/pipeline.md pointers.

## Steps

1. **Locate the frontier.** Run gates in order and stop at the first failure:

   ```
   python scripts/foundry.py gate 0
   python scripts/foundry.py gate 1
   python scripts/foundry.py gate 2
   python scripts/foundry.py gate 3
   ```

   Done when: `next_phase` = the number of the first gate that failed, or 4 when all pass.

2. **Restore mode.** Read `mode` from `.foundry/decisions.yaml` when it exists; `unattended`
   sets `FOUNDRY_UNATTENDED=1` for the rest of the run.
   Done when: the mode is set.

3. **Continue.** Run the /foundry steps from `next_phase` onward (pack-match for 1,
   bounded-grilling for 2, prd for 3), each wrapped in `metrics --phase <n> --start` and
   `metrics --phase <n> --note "resumed"`, with the same retry rule and final six-line report.
   When `next_phase` is 4, print the report and point to `/foundry-continue`.
   Done when: gate 3 passes or the run stopped with the failing gate printed.

## Reference

| First failing gate | Meaning | Action |
|--------------------|---------|--------|
| 0 | no brief | ask for the brief; this is the one question resume may ask |
| 1 | no or invalid selection | re-run pack-match |
| 2 | ledger incomplete | bounded-grilling picks up: `grill-plan` only lists unanswered questions |
| 3 | PRD missing or stale hash | re-run prd |
