---
name: foundry-resume
description: Resume a Foundry run from .foundry/ alone in a fresh session. Read handoff.md, find the last passed gate (0–10) or the active ticket (11+), and continue from the exact point.
invocation: user
model: sonnet
reads: [.foundry/handoff.md, .foundry/build.yaml, .foundry/brief.md, .foundry/pack.yaml, .foundry/decisions.yaml, .foundry/prd.md, .foundry/domain.yaml, .foundry/architecture.md, openapi.yaml, design-system/MASTER.md, .foundry/screens/*.md, .foundry/threats.md, .foundry/tickets/*.md, .foundry/metrics.jsonl]
writes: [.foundry/metrics.jsonl, .foundry/handoff.md]
gate: python scripts/foundry.py gate tickets
---

# /foundry-resume — orchestrator

Phases 0–10 continue here; phase 11+ delegates to /foundry-build at the exact ticket.

## Steps

1. **Read the handoff.** `python scripts/foundry.py handoff show`. Frontmatter fields:
   `phase`, `active_ticket`, `done`, `blocked`, `wizards_pending`, `next_command`,
   `cbm_project`, `generation`. When `next_command` names `/foundry-build`, go to step 4.
   Done when: the frontmatter is read, or its absence noted.

2. **Locate the frontier (phases 0–10).** Run gates in order and stop at the first failure:

   ```
   python scripts/foundry.py gate 0
   … through …
   python scripts/foundry.py gate 10
   ```

   Done when: `next_phase` = the first failing gate, or 11 when all pass.

3. **Continue phases.** Read `mode` from `.foundry/decisions.yaml` (`unattended` sets
   `FOUNDRY_UNATTENDED=1`). Run the /foundry steps from `next_phase` onward (doctor before
   phase 4), each wrapped in `metrics --phase <n> --start` / `--note "resumed"`, same retry
   rule and final report. When `next_phase` is 11, continue with step 4.
   Done when: gate 10 passes or the run stopped with the failing gate printed.

4. **Continue the build at the exact ticket.** With `active_ticket` set: `build activate
   --ticket <it>` (the window is kept), read `.foundry/tickets/<it>.status.yaml` `last` to see
   the failing dod step, and run implement-ticket from step 5 (GREEN) onward. Without an
   active ticket: run /foundry-build. Blocked tickets listed in `blocked` are retried once
   with their recorded failing output in context, then skipped with a note.
   Done when: implement-ticket or /foundry-build has taken over.

5. **Handoff on exit.** `python scripts/foundry.py handoff write --note "resumed at …"`.
   Done when: the frontmatter is current.

## Reference

| First failing gate | Meaning | Action |
|--------------------|---------|--------|
| 0 | no brief | ask for the brief; the one question resume may ask |
| 1 | no or invalid selection | re-run pack-match |
| 2 | ledger incomplete | bounded-grilling: `grill-plan` lists unanswered questions |
| 3 | PRD missing or stale hash | re-run prd |
| 4 | domain.yaml or CONTEXT.md incomplete | re-run domain-model |
| 5 | ADRs or architecture.md missing | re-run architecture |
| 6 | schema or openapi missing or failing | re-run data-model then api-contract |
| 7 | design-system files missing or design-check failing | re-run design-system |
| 8 | screens missing or bindings broken | re-run screen-spec |
| 9 | threats.md or compliance.yaml incomplete | re-run threat-model then compliance |
| 10 | tickets missing, cyclic or uncovered | re-run to-tickets |
| 11+ | tickets exist | /foundry-build from `active_ticket` |
