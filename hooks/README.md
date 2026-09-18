# Hooks (planned, P7)

Claude Code hooks that make token discipline and gates structural rather than requested.

| Hook | Event | Action | Writes |
|------|-------|--------|--------|
| metrics | PostToolUse | Append one record (tool, phase, ticket, wall_ms, token estimate) | .foundry/metrics.jsonl |
| gate | Stop | Run `foundry.py gate <current phase>`; block stop on failure with the failing criterion | stdout |
| graph-first | PreToolUse (Grep/Read on source) | Non-blocking reminder to prefer codebase-memory-mcp graph tools | none |

All hook scripts are Python 3.11+ stdlib, invoked through `foundry.ps1` / `foundry.sh`.
Records validate against `schemas/metrics.schema.json`.

Not implemented in P0.
