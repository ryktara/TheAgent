---
name: foundry-build
description: Implement the ticket graph produced by /foundry as a thin parent: per ticket activate (the card), dispatch one implementer subagent with the card only, receive its ≤300-token return, complete, hand off. The parent never reads source files.
invocation: user
model: sonnet
reads: [.foundry/tickets/*.md, .foundry/build.yaml, .foundry/handoff.md, .foundry/tickets/T-xxx.progress.md]
writes: [.foundry/build.yaml, .foundry/handoff.md, .foundry/metrics.jsonl]
gate: python scripts/foundry.py gate tickets
---

# /foundry-build — thin parent, phases 11–12

Argument: optional `--n <count>` (default 4). Context isolation: the parent holds the card and
the return contracts, nothing else. The implementer subagent holds the code. Reviewers hold the
review pack. Requires codebase-memory-mcp.

## Steps

0. **Resume point and code graph.** Read `handoff.md` frontmatter. `python scripts/foundry.py
   doctor --build` (stop on FAIL and print its install lines). `index_repository` on the project
   root, then `python scripts/foundry.py build index --name <cbm project>`.
   Done when: doctor ok, `build.yaml` has `cbm_project`, the resume ticket (if any) is known.

1. **Scaffold when T-000 is not done.** `build activate --ticket T-000`, `scaffold --stack <ADR
   0001 web stack>`, `dod --ticket T-000`, commit `chore(T-000): scaffold`, `build complete`.
   Done when: T-000 is in `done` or a blocker is recorded.

2. **Loop** until `--n` tickets completed this session, `tickets next` prints nothing, or a blocker:

   ```
   python scripts/foundry.py tickets next --n 1 --done <comma list from build.yaml>
   python scripts/foundry.py build activate --ticket T-xxx      # prints the card
   ```

   Dispatch ONE implementer with the Agent tool, `model: sonnet`, `run_in_background: false`.
   The prompt is exactly: the card, the line `Skill: <plugin root>/skills/implement-ticket/SKILL.md
   (read it first; it dispatches the three reviewers itself with the models in their frontmatter)`,
   the line `Conventions: <plugin root>/CLAUDE.md`, the project root, and the return contract
   below. ≤3k tokens. When `.foundry/tickets/T-xxx.progress.md` exists (resume), add its ≤20 lines.
   Done when: the subagent returned the contract.

3. **Return contract** (the subagent's last message, ≤300 tokens):

   ```
   {"ticket": "T-xxx", "status": "done|blocked", "commit": "<sha or null>",
    "dod": "<tier runs, passed steps, skipped steps>", "blocking": "<count fixed / remaining>",
    "wizards": ["<slug>"], "escalated": false, "notes": "<≤2 lines>"}
   ```

   On `done`: `python scripts/foundry.py build complete --ticket T-xxx` and
   `python scripts/foundry.py metrics --ticket T-xxx --escalated <bool> ...` when the subagent
   did not record it. On `blocked` after three DoD loops: re-dispatch ONCE with `model: opus`,
   the same prompt plus the progress file; record `escalated: true`; a second `blocked` is final.
   Done when: `build.yaml` reflects the outcome.

4. **Metrics and handoff after each ticket.**

   ```
   python scripts/foundry.py metrics ingest
   python scripts/foundry.py handoff write --note "T-xxx <status>: <notes>"
   ```

   Done when: the report shows the ticket's transcript columns (subagent transcripts included).

5. **Report** (≤8 lines): `foundry.py status` output, escalations, blockers, next command.
   Done when: the report is sent.

## Reference

| Command | Purpose |
|---------|---------|
| `build activate --ticket` | stamps the window, prints the card (the implementer's spec) |
| `build complete --ticket` | stamps completion; `tickets next --done` skips it |
| `metrics ingest` | tokens per ticket from the session and its `<session>/subagents/*.jsonl` transcripts |
| `metrics report --by-model` | cost per model per ticket; `status` shows the blended cost per ticket |
| `handoff write` | frontmatter + note; the SessionStart hook injects it |

Hard guardrail: the parent never opens `apps/`, `packages/` or `tests/` files; a detail the card
lacks is the implementer's to fetch. Hooks guard shell commands, scope edits, record tool calls,
inject the handoff and run the fast tier on stop.
