# How Foundry was built

Foundry was built in numbered steps (P0 to P11) by an orchestrator session that wrote one prompt
per step, dispatched it to an executing session, and read back a fixed-format report. This file
records the method so the next pack or version runs the same way. Detail per step:
[CHANGELOG.md](../CHANGELOG.md).

## The steps

**P0 Scaffold.** Plugin manifest, house style (CLAUDE.md), orchestrator stubs, schemas,
`validate`, `scaffold-pack`, tests, CI, golden briefs. Gate: validate green on an empty pipeline.

**P1 Pack schema 1.1 and pack-match.** Ranked question bank, the generic pack, three scaffolded
domain packs with real aliases, the deterministic `match` scorer, eval stage `match` (5/5).

**P2 Bounded grilling.** Schema 1.2 (`threshold`, `followups`), `grill-plan` with the 7/3 budget,
the decision ledger, `decide`, gates 0 to 3, the PRD skill, `/foundry` real for phases 0 to 3.

**P3 restaurant-pos pack.** The first complete pack (27 jobs, 25 entities, 104 glossary terms,
sources split VERIFIED/UNVERIFIED), the pack lint, `prd-skeleton`, rematch on free-text answers,
6 variant briefs.

**P4 Domain to API.** `doctor`, `data/stacks.csv`, skeletons for domain, architecture (9 ADRs),
schema and OpenAPI 3.1; gates 4 to 6.

**P5 Design and screens.** The design CSVs (ux-rules, palettes, typography, components),
`design-check` (WCAG contrast), design and screen skeletons, gates 7 and 8; entity `exposure`
cut the API to 87 operations.

**P6 Security and tickets.** Security-control and threat-pattern data, copy.csv (en/ar/ur),
threat and ticket skeletons, gates 9 and 10; `/foundry` complete through phase 10.

**P7a Build machinery.** `build activate|complete`, the 10-step `dod`, the nextjs-pwa + hono +
prisma scaffold (T-000), hooks, implement-ticket and the three reviewers.

**P7b Build on real tickets.** Ten fixes found only by building (Tailwind source scan, screenshot
waits, duplicate timestamps, stale tickets), metrics per ticket.

**P8 Efficiency and hand-off.** Fast/full DoD tiers, one Playwright run for axe and screenshots,
transcript-based token metrics, wizard and release skills, `gate release`, handoff/resume and the
`status` dashboard.

**P9 Isolation and evals.** Thin-parent `/foundry-build`, model routing (docs/models.md), per-model
cost, `thresholds.yaml` regression ceilings, golden/triggers/e2e eval stages, 12 dogfood tickets
with 0 escalations.

**P10 Subscription-only and generalisation.** No API key, no headless mode, `/foundry-eval` for
model stages; builder/finisher context split; schema 1.9 `regulated`; retail-pos and trading-app
packs; pack `contexts`/`offline_contexts`; embedded Postgres with `FOUNDRY_PG_PORT`; six
generalisation fixes and one context-reset fix, each with its failing run as the reason.

**P11 Budgets and docs.** Builder turn budget (120 tool calls, then a fresh builder from the
progress file), finisher skips unchanged passing review families, schema 2.0 `vocabulary`,
`/foundry-setup`, and these docs (quickstart en/ar, install, pack authoring, this file).

## Report template

Every step ends with this report, in this order. The orchestrator reads nothing else.

```
## P<n> report
Status: done | partial | blocked
Commits: <sha> <subject>, one per line
Delivered: bullet per deliverable, with the file path
Gate results: command -> result (validate, unittest, evals/run.py, gate <phase>, dod)
Deviations: what differs from the prompt, and why
Decisions made without asking: decision; reversible y/n
Open questions: question; recommended answer
Token/time: tokens or cost, wall time, notable escalations
Next-step readiness: what P<n+1> can assume; what it must not
```

Criteria: every Delivered item is a path; every Gate result is a command with its output
summary; every Open question carries a recommended answer so the orchestrator can reply "yes".

## Answers are binding

The orchestrator answers Open questions at the top of the next prompt as a numbered list
("P7a answer 4: screenshot cookie URL uses WEB_PORT"). An answer is a requirement for every later
step until a later answer replaces it. Executing sessions cite the answer number in the commit
or changelog entry that applies it. A decision reported as reversible: n is reviewed before the
next prompt goes out.

## Thin parent, subagents with contracts

The pattern that keeps long runs inside context, used by Foundry itself and by the orchestrator:

- **Parent holds pointers, not content.** It passes a card (the spec, at most 80 lines), a skill
  path and the project root. It never reads source files.
- **Each subagent returns a contract.** Builder: at most 150 tokens (status, files, dod tier
  result, budget). Finisher: at most 300 tokens (verdicts, commit sha). Reviewers: JSON only.
- **State lives in files.** `T-xxx.progress.md`, `build.yaml`, `handoff.md`. A fresh subagent
  resumes from the file, not from the parent's memory.
- **Budgets are explicit.** 120 tool calls per builder; three DoD fix loops; one escalation slot
  (a second sonnet builder), opus only after it.
- **Review input is bounded.** `review-pack` header at most 600 tokens; re-reviews see changed
  hunks plus their own previous blocking list.

## Driving the next pack or version

1. Write P<n>'s prompt: goal, deliverables as paths, gates as commands, binding answers from
   P<n-1>, and "report in the template".
2. For a pack: follow [PACK-AUTHORING.md](PACK-AUTHORING.md); the generalisation run is the step's
   real test. Every fix it forces becomes a `generalisation fix:` changelog line with its reason.
3. For a version: bump the schema only when a skeleton needs a new field; add the field to
   packs/README.md and the schema in the same commit; migrate every pack.
4. Isolate parallel work in git worktrees (one branch per workstream, docs-only branches write
   only under `docs/`); the orchestrator merges.
5. Close the step when validate, unittest and every deterministic eval stage pass, and
   `/foundry-eval` results (triggers, e2e) stay inside `evals/thresholds.yaml`.
