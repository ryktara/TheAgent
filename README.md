# FOUNDRY

Foundry is a Claude Code plugin that turns a one-line brief into a designed, architected,
implemented and tested application while asking the founder at most seven questions.
It is built for non-technical founders: type `/foundry "I need a restaurant POS"` and let the
pipeline run.

## Install

```
claude plugins install ./foundry
```

For a local checkout you can also register the folder as a local marketplace and install from
it. Confirm the install by checking that `/foundry` appears in the slash-command list.

Requirements: Claude Code, Python 3.11+ (stdlib only). Windows, macOS and Linux are supported;
use `scripts/foundry.ps1` or `scripts/foundry.sh`. Implementation phases depend on the
codebase-memory-mcp server for code intelligence.

**Subscription-only, by design.** Foundry runs inside your logged-in Claude Code session and nowhere
else. It never reads or asks for an API key, never drives the CLI non-interactively, and has no
headless mode. The two evals that need a model (trigger accuracy and the unattended end-to-end
run) are run by a human typing `/foundry-eval` in a session; CI runs `python evals/run.py`, which is
deterministic (skeletons, gates, golden artefact diffs, and the latest `/foundry-eval` results).

## Pipeline overview

`/foundry` takes the brief, matches it against a domain pack (industry knowledge shipped as YAML
and CSV), asks a bounded set of questions to close the decision frontier, then produces a PRD,
domain model with glossary, architecture with ADRs, data and API contracts, a design system,
screen specs, threat model and compliance map, and a DAG of tracer-bullet tickets.
`/foundry-build` implements each ticket under typecheck, test, lint, semgrep and axe gates with
screenshots, runs code, UI and security reviews, hands human-only steps to a wizard, releases,
and writes a handoff file that a fresh session can resume from with `/foundry-resume`.
Full table: [docs/pipeline.md](docs/pipeline.md).

## Status

| Step | Deliverable | Status |
|------|-------------|--------|
| P0 | Scaffold + house style, validate, scaffold-pack, tests, CI | done |
| P1 | Pack schema 1.1 + generic pack + pack-match skill + deterministic matcher | done |
| P2 | Bounded grilling + decision ledger + PRD + /foundry phases 0–3 | done |
| P3 | restaurant-pos pack (full reference), prd-skeleton, rematch, pack lint | done |
| P4 | Domain model, architecture + 9 ADRs, data model, API contract, doctor, query | done |
| P5 | Design layer: 7 data CSVs, design-check, design-system, screen specs | done |
| P6 | Security controls, threat model, compliance, tickets; /foundry ends at phase 10 | done |
| P7a | Build loop machinery: CBM mandatory, DoD runner, hooks, implement-ticket + review skills, T-000 scaffold executed | done |
| P7b | T-001…T-008 built through the loop on the Sharjah brief; 7 plugin fixes; examples in docs/examples | done |
| P8 | Loop efficiency (tiers, one Playwright run, ticket card, review pack), transcript metrics + cost, wizard, release, handoff/resume, status dashboard | done |
| P9 | Context isolation (thin parent + implementer subagent), model routing (docs/models.md), evals with thresholds (golden diffs, e2e, trigger test), 12 more dogfood tickets | done |
| P10 | Subscription-only rule, ticket-builder/ticket-finisher context split with hunk-only re-review, `/foundry-eval`, pack schema 1.9 (`regulated`), retail-pos + trading-app packs, generalisation proof | done |
| P11 | Packaging | planned |

## Build loop commands (P8–P10)

| Command | What it does |
|---------|--------------|
| `build activate --ticket T-xxx` | stamps the ticket window and prints the ticket card (the spec, ≤80 lines) |
| `dod --ticket T-xxx --tier fast\|full` | fast = typecheck+lint+unit in parallel (≤30 s); full = every step, one Playwright run for smoke+axe+shots |
| `review-pack --ticket T-xxx [--hunks-since <sha>\|last]` | `.foundry/reviews/T-xxx.pack.md` (≤600-token header) + `.diff`: the only inputs reviewers get; on re-review only the hunks changed since the last pack plus each family's previous blocking list |
| `run --tail 30 -- <cmd>` | run a test runner or pnpm command, keep the full log in `.foundry/logs/`, print the last 30 lines only (builder and finisher use it for every noisy command) |
| `release confirm --by <name>` | human confirmation for `regulated: true` packs; `gate release` stays red until it exists |
| `metrics ingest [--since ts] [--transcripts dir]` | real tokens per ticket from Claude Code transcripts (`~/.claude/projects/<cwd-encoded>/*.jsonl`, incl. `<session>/subagents/`), priced by `data/model-prices.csv` |
| `metrics report [--phases] [--compare a.jsonl b.jsonl] [--by-model]` | self-reported and transcript columns, cache read, context peak, cost (per model with --by-model), escalations; before/after diff |
| `status` | one-screen dashboard: phase, tickets, dod pass rate, blockers, wizards, tokens, estimate |
| `wizard status\|scaffold` | human-only prerequisites: md + ps1 + sh that prompt, validate, write .env.local, verify |
| `release-skeleton`, `gate release` | CHANGELOG, Dockerfiles, compose+Caddy or fly.toml, runbook, smoke, user docs; smoke on a local prod build |
| `handoff write\|show` | handoff.md frontmatter (phase, active_ticket, done, blocked, wizards_pending, next_command, cbm_project, generation) |

Subagent transcripts live under `<session>/subagents/<agent>.jsonl` next to the session file and are attributed to the ticket window like any other turn (`subagent_turns` on the ingest row). Transcript path: Claude Code writes `~/.claude/projects/<session cwd with every non-alphanumeric as "-">/<session>.jsonl`
and subagent transcripts under `<session>/subagents/`. `metrics ingest` scans every folder, keeps files modified since the
earliest ticket window and attributes each assistant turn by timestamp to the ticket whose activate/complete stamps
(`.foundry/build.yaml` `stamps`) enclose it. Windows for tickets built before stamps existed are back-filled from their
ticket-end record.

## Layout

```
.claude-plugin/plugin.json   plugin manifest
skills/                      SKILL.md folders (at most 150 lines each)
packs/                       domain packs + index.csv
data/                        CSV knowledge queried by scripts
schemas/                     JSON Schema draft 2020-12
scripts/                     foundry.py CLI + wrappers + tests
hooks/                       planned PostToolUse / Stop hooks
evals/                       golden briefs + expected outcomes
docs/pipeline.md             16-row phase table (0–15)
```
