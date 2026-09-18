---
name: foundry-build
description: Implement the ticket graph produced by /foundry: index the code graph, then run implement-ticket on the next unblocked tickets (default 4 per session) until done or blocked, and write the handoff.
invocation: user
model: sonnet
reads: [.foundry/tickets/*.md, .foundry/build.yaml, .foundry/architecture.md, .foundry/screens/*.md, .foundry/threats.md]
writes: [code, tests, .foundry/build.yaml, .foundry/handoff.md, .foundry/metrics.jsonl, .foundry/reviews/*.json, .foundry/screenshots/]
gate: python scripts/foundry.py gate tickets
---

# /foundry-build — orchestrator, phases 11–12

Argument: optional `--n <count>` (default 4). Graph first; every ticket through implement-ticket;
reviews as parallel subagents; handoff at the end. Requires codebase-memory-mcp.

## Steps

0. **Code graph.**

   ```
   python scripts/foundry.py doctor --build
   ```

   Stop on FAIL and print the install command and MCP JSON the table shows. Then call
   `index_repository` on the project root and `get_architecture` once; record the project:

   ```
   python scripts/foundry.py build index --name <cbm project name>
   ```

   Done when: doctor is ok and `.foundry/build.yaml` has `cbm_project` and `indexed_at`.

1. **Scaffold when T-000 is not done.** When `.foundry/build.yaml` `done` lacks T-000:
   `build activate --ticket T-000`, then `python scripts/foundry.py scaffold --stack <ADR 0001
   web stack>`, then `dod --ticket T-000`; on PASS commit `chore(T-000): scaffold` and
   `build complete --ticket T-000`; re-run `index_repository`.
   Done when: T-000 is in `done` or a blocker is recorded.

2. **Loop.** Repeat until `--n` tickets completed this session or a blocker:

   ```
   python scripts/foundry.py tickets next --n 1 --done <comma list from build.yaml>
   ```

   invoke implement-ticket on the printed ticket; after each ticket call `detect_changes` and
   re-index when generation changes.
   Done when: the count is reached, `tickets next` prints nothing, or implement-ticket wrote a
   blocker.

3. **Handoff.** Write `.foundry/handoff.md`: tickets done this session and overall, active
   ticket, blockers with the failing dod steps, unreviewed copy ids used, and the next command
   (`/foundry-build` or `/foundry-resume`).
   Done when: the file exists and a fresh session could continue from it alone.

4. **Report** (≤8 lines): tickets done / total, dod pass rate, blockers, screenshots path,
   next command.
   Done when: the report is sent.

## Reference

| Command | Purpose |
|---------|---------|
| `build activate --ticket` | set active ticket; hooks scope edits to its predicted files |
| `dod --ticket` | run the definition of done; writes `T-xxx.status.yaml` |
| `build complete --ticket` | mark done; `tickets next --done` skips it |
| `tickets next --n 1 --done …` | next unblocked ticket in topological order |

Hooks in this plugin guard shell commands (SEC-AGT-02), scope edits to the ticket, record
metrics, inject the handoff on session start and run typecheck+lint on stop.
