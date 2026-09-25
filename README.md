# FOUNDRY

Foundry is a Claude Code plugin that turns a one-line brief into a designed, architected,
implemented and tested web application, asking the founder at most 7 questions plus 3 follow-ups.
It runs inside your logged-in Claude Code session and writes everything to `.foundry/` in your app repo.

## Install

Base tools (Git, Node LTS, Python 3.11+), then Claude Code:

```
winget install --id Git.Git -e; winget install --id OpenJS.NodeJS.LTS -e; winget install --id Python.Python.3.12 -e   # Windows
brew install git node python@3.12                                                                                    # macOS
npm install -g @anthropic-ai/claude-code
```

Then the plugin, from GitHub:

```
claude plugin marketplace add ryktara/TheAgent
claude plugin install foundry@theagent
```

Dev path (a local checkout; the marketplace is still named `theagent`, it was `foundry-local` before 1.0):

```
claude plugin marketplace add /path/to/foundry
claude plugin install foundry@theagent
```

In a `claude` session, run `/foundry-setup`; done when the last line starts with `setup: ready`.
Step by step, with troubleshooting: [docs/INSTALL-WINDOWS.md](docs/INSTALL-WINDOWS.md),
[docs/INSTALL-MAC-LINUX.md](docs/INSTALL-MAC-LINUX.md).

## Quickstart

Full guide: [docs/QUICKSTART.md](docs/QUICKSTART.md) ([Arabic](docs/QUICKSTART.ar.md)).
From an empty app folder:

```
/foundry "<one line: what the business is, where, what you already know>"
/foundry-build
/foundry-resume
/release
```

`/foundry` plans (phases 0 to 10), `/foundry-build` implements the next 4 tickets (`--n 10` for more),
`/foundry-resume` continues in a new session, `/release` produces deploy files and a smoke-tested build.

## Packs available

| Pack | Status | Covers |
|------|--------|--------|
| restaurant-pos | complete | restaurants and cafes: tables, kitchen display, offline tills, bilingual receipts |
| retail-pos | complete | shops and supermarkets: barcodes, stock, returns, e-invoicing |
| trading-app | complete, regulated | brokerage and trading apps: orders, portfolio, KYC; release needs a licence confirm |
| generic | fallback | any brief no domain pack matches with confidence 0.7 or more |

Write a new pack in a day: [docs/PACK-AUTHORING.md](docs/PACK-AUTHORING.md).

## Pipeline

Phases 0 to 15; gates, inputs and outputs per phase: [docs/pipeline.md](docs/pipeline.md).

```
+-----------+   +-----------+   +---------------------+   +-----------+   +-----------+
| 0 brief   |-->| 1 match   |-->| 2 grill             |-->| 3 PRD     |-->| 4 domain  |
|           |   |   pack    |   |   <=7 + 3 questions |   |           |   |           |
+-----------+   +-----------+   +---------------------+   +-----------+   +-----------+
                                                                                |
+-----------+   +-----------+   +---------------------+   +-----------+         |
| 8 screens |<--| 7 design  |<--| 6 data + API        |<--| 5 archi-  |<--------+
|           |   |   system  |   |                     |   |   tecture |
+-----------+   +-----------+   +---------------------+   +-----------+
      |
      v
+-----------+   +-----------+   +------------------------------------------------+
| 9 threats |-->| 10 tickets|-->| 11-12 build loop, per ticket                   |
| + comply  |   |   (DAG)   |   |   builder -> finisher -> 3 reviewers           |
+-----------+   +-----------+   |   (code, ui, security)                         |
                                +------------------------------------------------+
                                                   |
                +-----------+   +-----------+   +-----------+
                | 15 handoff|<--| 14 release|<--| 13 wizards|
                +-----------+   +-----------+   +-----------+
```

## Cost expectations

Measured on the reference app (restaurant-pos, 49 tickets, P8–P11 transcripts), subscription usage
priced at public list prices: sonnet for builder, finisher and reviewers, haiku for ui-review, the
parent's own turns at the opus tier. Full table: docs/examples/restaurant-pos/COST.md.

| Measure | Value |
|---------|-------|
| Per feature ticket, median | $21.20 |
| Per compliance ticket, median | $10.16 |
| Per integration ticket, median | $5.21 |
| Full reference app, total (49 tickets) | $1,059.64 (sonnet $473.57, haiku $7.67, parent $578.39) |
| Wall time, sum of ticket windows | 46 h |
| Design pipeline, phases 0–10 (retail-pos run) | $4.29, under 30 min |

Your own numbers, from the app folder: `python <foundry>/scripts/foundry.py metrics report --by-model`.

## Limits

- Web-first: every app is nextjs-pwa + hono + postgres. Expo mobile is on the roadmap.
- Subscription-only: no API key, no non-interactive CLI, no headless mode. Model evals run through `/foundry-eval` in a session.
- Human-only steps (provider keys, domains, licences) are handed to you as wizards; the feature ships stubbed until you run it.
- Regulated packs block release until a named person runs `release confirm --by <name>`.
- DoD runs (Playwright, embedded Postgres, parallel test runners) need a quiet machine; close other heavy work while building.

## Roadmap

- Expo stack for native mobile apps.
- More domain packs.
- Preview environments per ticket.
- Cross-project intelligence: lessons from one app's build feeding the next.

## Layout

```
.claude-plugin/   plugin manifest and marketplace (theagent)
skills/           one SKILL.md folder per skill and subagent
packs/            domain packs, packs/index.csv, packs/README.md (schema 2.0)
data/             CSV knowledge the scripts query
schemas/          JSON Schema draft 2020-12
scripts/          foundry.py CLI, wrappers, tests
hooks/            session start, guards, metrics, stop check
evals/            briefs, expected outcomes, fixtures, thresholds, run.py
docs/             install, quickstart, pipeline, models, pack authoring, orchestrator, examples
CHANGELOG.md      step-by-step history (P0 to P11)
```

## Licence

Copyright (c) 2026 Al Sadq IT Solutions LLC. All rights reserved. See [LICENSE](LICENSE).

Source-available, not open-source: you may read and evaluate the code here; any other use needs the
owner's written permission until Al Sadq IT Solutions LLC says otherwise. See [CONTRIBUTING.md](CONTRIBUTING.md)
and [SECURITY.md](SECURITY.md).
