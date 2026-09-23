# Model routing (P9)

Every `SKILL.md` carries `model:`; orchestrators pass it to the Agent tool when they dispatch the
skill as a subagent. The matrix is the source of truth; `foundry.py validate` checks each skill's
value is one of haiku, sonnet, opus.

| Skill | Model | Reason |
|-------|-------|--------|
| foundry (phases 0–10 orchestrator) | opus | long multi-phase plan with retries; judgement across artefacts |
| pack-match | haiku | deterministic matcher does the work; the skill only reports |
| bounded-grilling | sonnet | writes seven questions and reads answers; no deep reasoning |
| prd | sonnet | prose from a skeleton |
| domain-model | sonnet | fills invariants from pack workflows |
| architecture | opus | ADR trade-offs shape every later phase; the costliest place to be wrong |
| data-model, api-contract | sonnet | skeleton-driven, gate-checked |
| design-system, screen-spec | sonnet | data-driven from CSVs |
| threat-model | opus | STRIDE per boundary with control selection; security judgement |
| compliance | haiku | maps controls to owners and evidence from CSV rows |
| to-tickets | haiku | tickets-skeleton produces the DAG; the skill validates and labels |
| foundry-build (parent) | sonnet | thin loop: activate, dispatch, complete, handoff; never reads source |
| ticket-builder (first half subagent) | sonnet | card → RED → GREEN → fast tier; holds the code, never the reviews |
| ticket-builder, second dispatch | sonnet | the escalation slot: a fresh context from the progress file after `blocked` |
| ticket-builder, third dispatch | opus | only when the second builder also returns `blocked`; `escalated: true` |
| ticket-finisher (second half subagent) | sonnet | full tier, review pack, fixes at file+line, hunk-only re-review, commit |
| implement-ticket (human in-session) | sonnet | the two halves performed in order by a person |
| foundry-eval | sonnet | answers the 40 trigger prompts and drives the unattended e2e run in a session |
| code-review | sonnet | spec conformance needs the acceptance tests in mind |
| ui-review | haiku | checklist against screenshots and states; cheap and frequent |
| security-review | sonnet | SYNC-RULES parity and authz reasoning |
| wizard | sonnet | exact human steps and validation scripts |
| release | sonnet | generated artefacts reviewed once |
| foundry-resume, foundry-continue | sonnet | reads state, delegates |

Prices: `data/model-prices.csv` (public list prices, `as_of` per row). `metrics ingest` attributes
each assistant turn to its model; `metrics report --by-model` breaks a ticket's cost down per
model and `status` shows the blended cost per ticket.

Escalation is recorded as `escalated: true` on the ticket-end metrics row and the parent notes
it in the handoff.
