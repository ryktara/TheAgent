---
name: foundry-build
description: Implement the ticket graph produced by /foundry: index the code graph, then run implement-ticket on the next unblocked tickets (default 4 per session) until done or blocked, and write the handoff.
invocation: user
model: sonnet
reads: [.foundry/tickets/*.md, .foundry/build.yaml, .foundry/handoff.md, .foundry/architecture.md]
writes: [code, tests, .foundry/build.yaml, .foundry/handoff.md, .foundry/metrics.jsonl, .foundry/reviews/*, .foundry/screenshots/]
gate: python scripts/foundry.py gate tickets
---

# /foundry-build — orchestrator, phases 11–12

Argument: optional `--n <count>` (default 4). Graph first; every ticket through implement-ticket;
reviews as parallel subagents from the review pack; handoff on every exit. Requires
codebase-memory-mcp.

## Steps

0. **Resume point and code graph.** Read `.foundry/handoff.md` frontmatter: when
   `active_ticket` is set, that ticket continues (its status.yaml tells which dod step failed
   last). Then:

   ```
   python scripts/foundry.py doctor --build
   ```

   Stop on FAIL and print the install command and MCP JSON the table shows. Call
   `index_repository` on the project root (incremental when already indexed) and record it:

   ```
   python scripts/foundry.py build index --name <cbm project name>
   ```

   Done when: doctor is ok, `build.yaml` has `cbm_project` and `indexed_at`, the resume ticket is known.

1. **Scaffold when T-000 is not done.** When `done` lacks T-000: `build activate --ticket T-000`,
   `python scripts/foundry.py scaffold --stack <ADR 0001 web stack>`, `dod --ticket T-000`;
   on PASS commit `chore(T-000): scaffold`, `build complete --ticket T-000`, `index_repository`.
   Done when: T-000 is in `done` or a blocker is recorded.

2. **Loop.** Repeat until `--n` tickets completed this session or a blocker:

   ```
   python scripts/foundry.py tickets next --n 1 --done <comma list from build.yaml>
   ```

   invoke implement-ticket on the printed ticket (it activates, indexes, builds, reviews,
   commits, completes and records metrics).
   Done when: the count is reached, `tickets next` prints nothing, or a blocker was written.

3. **Metrics from transcripts.**

   ```
   python scripts/foundry.py metrics ingest
   python scripts/foundry.py metrics report
   ```

   Done when: the report shows transcript columns for every ticket done this session.

4. **Handoff (every exit, including blockers).**

   ```
   python scripts/foundry.py handoff write --note "<tickets done this session; blockers; unreviewed copy ids>"
   ```

   Done when: `handoff.md` frontmatter has phase, active_ticket, done, blocked, wizards_pending,
   next_command, cbm_project, generation.

5. **Report** (≤8 lines): `foundry.py status` output, blockers, screenshots path, next command.
   Done when: the report is sent.

## Reference

| Command | Purpose |
|---------|---------|
| `build activate --ticket` | stamps the window, prints the ticket card (the spec) |
| `dod --ticket --tier fast\|full` | fast after each green; full once before reviews |
| `review-pack --ticket` | the only input reviewers receive |
| `build complete --ticket` | stamps completion; `tickets next --done` skips it |
| `metrics ingest` | real tokens from Claude Code transcripts per ticket window |
| `handoff write` | frontmatter + next_command; the SessionStart hook injects it |

Hooks guard shell commands (SEC-AGT-02), scope edits to the ticket, record tool calls, inject
the handoff on session start and run the fast tier on stop.
