---
name: foundry-build
description: Implement the ticket graph produced by /foundry as a thin parent: per ticket activate (the card), dispatch ticket-builder then ticket-finisher as subagents with the card and a skill pointer only, receive their short contracts, complete, hand off. The parent never reads source files.
invocation: user
model: sonnet
reads: [.foundry/tickets/*.md, .foundry/build.yaml, .foundry/handoff.md, .foundry/tickets/T-xxx.progress.md]
writes: [.foundry/build.yaml, .foundry/handoff.md, .foundry/metrics.jsonl]
gate: python scripts/foundry.py gate tickets
---

# /foundry-build — thin parent, phases 11–12

Argument: optional `--n <count>` (default 4). Context isolation: the parent holds the card and
the return contracts, nothing else. The builder holds the code, the finisher holds the reviews,
reviewers hold the pack. Requires codebase-memory-mcp.

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

   **Builder.** Agent tool, `model: sonnet`, `run_in_background: false`. Prompt, ≤3k tokens:
   the card; `Skill: <plugin root>/skills/ticket-builder/SKILL.md (read it first)`;
   `Conventions: <project root>/CLAUDE.md`; the project root; "run every command in the
   foreground, never background a monitor"; the builder contract (below). When
   `.foundry/tickets/T-xxx.progress.md` exists, append its ≤20 lines.
   Builder returns `budget` (120 tool calls spent) → dispatch a fresh builder with the progress
   file, as often as needed; it is not an escalation. Builder returns `blocked` → dispatch a
   **second builder** once, same prompt plus the progress file (the escalation slot). Second
   `blocked` → one **opus builder**, then record `escalated: true`; a third `blocked` is final.

   **Finisher.** Agent tool, `model: sonnet`, `run_in_background: false`. Prompt: the ticket id
   and title; `Skill: <plugin root>/skills/ticket-finisher/SKILL.md (read it first; it dispatches
   the three reviewers itself by SKILL.md path with their frontmatter models)`; the project root;
   the builder's JSON; the finisher contract (below).
   Done when: the finisher returned its contract.

3. **Contracts.** Builder (≤150 tokens):

   ```
   {"ticket": "T-xxx", "status": "green|blocked|budget", "loops": 1, "tool_calls": 84, "files_changed": 6, "tests_added": 4,
    "wizards": [], "progress": ".foundry/tickets/T-xxx.progress.md", "notes": "<≤2 lines>"}
   ```

   Finisher (≤300 tokens):

   ```
   {"ticket": "T-xxx", "status": "done|blocked", "commit": "<sha or null>",
    "dod": "<tier runs, passed steps, skipped steps>", "blocking": "<fixed>/<remaining>",
    "rereviews": 1, "wizards": ["<slug>"], "escalated": false, "notes": "<≤2 lines>"}
   ```

   On `done` without a metrics row: `python scripts/foundry.py metrics --ticket T-xxx --escalated <bool>`.
   On `blocked`: the note goes to `build.yaml` `blockers`; the loop continues with the next ticket.
   Done when: `build.yaml` reflects the outcome.

4. **Metrics and handoff after each ticket.**

   ```
   python scripts/foundry.py metrics ingest
   python scripts/foundry.py handoff write --note "T-xxx <status>: <notes>"
   ```

   Done when: the report shows the ticket's transcript columns (builder, finisher and reviewer
   subagent transcripts are attributed by the ticket id in their first message).

5. **Report** (≤8 lines): `foundry.py status` output, escalations, blockers, next command.
   Done when: the report is sent.

## Reference

| Command | Purpose |
|---------|---------|
| `build activate --ticket` | stamps the window, prints the card (the builder's spec) |
| `build complete --ticket` | stamps completion; `tickets next --done` skips it |
| `metrics ingest` | tokens per ticket from the session and its `<session>/subagents/*.jsonl` transcripts |
| `metrics report --by-model` | cost per model per ticket; `status` shows the blended cost per ticket |
| `handoff write` | frontmatter + note; the SessionStart hook injects it |

Hard guardrail: the parent never opens `apps/`, `packages/` or `tests/` files; a detail the card
lacks is the builder's to fetch. Hooks guard shell commands, scope edits, record tool calls,
inject the handoff and run the fast tier on stop.
