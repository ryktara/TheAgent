---
name: foundry-build
description: Implement the ticket graph produced by /foundry. Run phases 11–14 (implement, review, wizard, release) under machine-verifiable done gates.
invocation: user
model: sonnet
reads: [.foundry/tickets/*.md, .foundry/architecture.md, .foundry/screens/*.md, .foundry/threats.md]
writes: [code, tests, .foundry/metrics.jsonl, .foundry/reviews/*.md, .foundry/wizard/*.ps1, .foundry/wizard/*.sh, CHANGELOG.md]
gate: python scripts/foundry.py gate 14
---

# /foundry-build — orchestrator, phases 11–14

STUB. Phase bodies land in P7–P8. Full table with reads, writes and gates: docs/pipeline.md.

## Phases

| Phase | Name | Skill | Status |
|------:|------|-------|--------|
| 11 | Implement | implement-ticket | not yet implemented |
| 12 | Review | code-review, ui-review, security-review | not yet implemented |
| 13 | Human-only | wizard | not yet implemented |
| 14 | Release | release | not yet implemented |

## Steps

1. **Pick the next unblocked ticket.** Topological order over `blockedBy` edges.
   Done when: a ticket with every blocker closed is selected, or the DAG is exhausted.

2. **Implement under red/green.** Failing test first, then code, then the machine DoD:
   typecheck, tests, lint, semgrep, axe, screenshot.
   Done when: every DoD command exits 0 and the screenshot path is recorded in metrics.

3. **Review, wizard, release.** Parallel review subagents return fixed-schema findings; human-only
   steps become wizard scripts; release runs the smoke test on the deployed URL.
   Done when: phase 14 gate passes.

Code intelligence: codebase-memory-mcp graph tools before grep once code exists.
