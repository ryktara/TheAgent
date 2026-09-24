# Hooks

Loaded automatically from `hooks/hooks.json` (the plugin manifest must not reference it again: Claude Code 2.1 reports a duplicate hooks file and refuses to load the plugin). Every hook is Python 3.11+
stdlib, reads the Claude Code JSON payload on stdin, writes JSON on stdout, and fails open
(any error → exit 0 with no output). `${CLAUDE_PLUGIN_ROOT}` resolves to this plugin.

| Hook | Event / matcher | Payload fields used | Output | Control |
|------|-----------------|---------------------|--------|---------|
| bash_guard.py | PreToolUse, `Bash` | `tool_name`, `tool_input.command` | `hookSpecificOutput.permissionDecision: deny` + reason for `rm -rf /`, force push, `curl \| sh`, writes to `.env*` or secrets files, `npm publish`, `git reset --hard`, `DROP TABLE`; nothing otherwise | SEC-AGT-02, SEC-AGT-03 |
| edit_guard.py | PreToolUse, `Edit\|Write\|MultiEdit` | `tool_name`, `tool_input.file_path`, `cwd` | `permissionDecision: allow` with `additionalContext` when the path is outside the active ticket's `files_likely_touched` and outside `tests/` or `.foundry/`; never denies | SEC-AGT-10 |
| metrics.py | PostToolUse, `.*` | `tool_name`, `tool_response`, `cwd` | none; appends `{ts, phase 11, event tool-call, tool, ticket, tool_calls 1, tokens_out ≈ chars/4, note}` to `.foundry/metrics.jsonl` | observability |
| session_start.py | SessionStart | `cwd` | `additionalContext` ≤15 lines: graph-first rule with the re-index check, handoff.md frontmatter (phase, active_ticket, done, blocked, wizards_pending, next_command, cbm_project, generation) | SEC-AGT-06 |
| stop_check.py (runs for the parent and every subagent; the parent has no active edits so it is a no-op there) | Stop | `cwd`, `stop_hook_active` | `systemMessage` with the tail of `foundry.py dod --ticket <active> --tier fast` (typecheck, lint, unit in parallel); never blocks | SEC-AGT-09 |

Active ticket and done list come from `.foundry/build.yaml` (written by `foundry.py build
activate|complete`). Hooks only act inside a project that has a `.foundry/` folder.

Test: `python -m unittest hooks/test_hooks.py` feeds sample payloads and asserts the contract.

P10 notes: hooks run identically inside the ticket-builder, ticket-finisher and reviewer subagents (each is its own
Claude Code agent). stop_check's fast tier is what a builder sees on every stop; the finisher and reviewers have no
active edits of their own beyond fixes, so the tail is short. No hook reads an API key or spawns the CLI: the plugin is
subscription-only and every hook is a stdin/stdout Python script.

Not yet wired: a PreToolUse wrapper for WebFetch that marks fetched content as data
(SEC-AGT-01); the skills carry the rule until then.
