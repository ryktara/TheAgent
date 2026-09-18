---
name: foundry-resume
description: Resume a Foundry run from .foundry/ alone in a fresh session. Re-enter at the first phase whose gate fails.
invocation: user
model: sonnet
reads: [.foundry/handoff.md, .foundry/decisions.yaml, .foundry/metrics.jsonl]
writes: [.foundry/handoff.md]
gate: python scripts/foundry.py gate resume
---

# /foundry-resume — orchestrator

STUB. Body lands in P8. Full table: docs/pipeline.md.

## Steps

1. **Load handoff.** Read `.foundry/handoff.md` and the decision ledger.
   Done when: the last completed phase and its artifacts are listed.

2. **Find the first failing gate.** Run gates 0–15 in order.
   Done when: the first non-passing phase number is known.

3. **Hand off to the right orchestrator.** Phases 0–10 continue under /foundry; 11–14 under
   /foundry-build; 15 writes the handoff.
   Done when: the next orchestrator is invoked with the phase number, or all gates pass.
