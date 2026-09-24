# Foundry quickstart

For a founder with an idea and a Claude Code subscription. Install first:
[INSTALL-WINDOWS.md](INSTALL-WINDOWS.md) or [INSTALL-MAC-LINUX.md](INSTALL-MAC-LINUX.md).

## 1. Type one line

Open an empty folder for your app, start `claude`, and type:

```
/foundry "A POS for my two cafes in Dubai, Arabic and English receipts"
```

One sentence is enough. Name the business, the city or country, and anything you already know
(languages, payment provider, offline use). Every fact you give is a question you will not be asked.

## 2. Answer at most 10 questions

Foundry matches your brief to a domain pack (restaurant, retail, trading, or generic) and asks
**at most 7 questions**, then **at most 3 follow-ups**. Each question shows a default; press
Enter to accept it. Questions that are hard to change later (country, service model) come first.

After the answers, Foundry runs without you until the ticket plan is ready.

## 3. What you get

| Command | You receive |
|---------|-------------|
| `/foundry` | Product spec, domain model, architecture decisions, database schema, API contract, design system, one spec per screen, threat model, compliance list, ticket plan (at most 60 tickets) |
| `/foundry-build` | Working code, ticket by ticket: installable web app (PWA), API, Postgres database, tests, screenshots in light and dark, left-to-right and right-to-left |
| `/release` | Dockerfiles, deploy config, runbook, smoke test, user guides |

Mobile apps (Expo) are on the roadmap. Today every app is web-first.

## 4. Where files live

Everything Foundry writes about your app lives in the `.foundry/` folder of your app repo:
`brief.md`, `prd.md`, `decisions.yaml`, `adr/`, `screens/`, `tickets/`, `wizard/`, `handoff.md`.
The code sits beside it in `apps/` and `packages/`. Nothing is stored anywhere else.

## 5. Build and resume

```
/foundry-build            implements the next 4 tickets
/foundry-build --n 10     implements the next 10
/foundry-resume           continues exactly where the last session stopped
```

Close the terminal whenever you like. `.foundry/handoff.md` records the phase, the active ticket
and the next command; a new session shows it on start, and `/foundry-resume` continues from it.

## 6. Read the dashboard

Run it from your app folder; `<foundry>` is the folder you passed to `claude plugin marketplace add`:

```
python <foundry>/scripts/foundry.py status
```

```
FOUNDRY STATUS  cafe-pos
phase: 11   tickets: 12/49 done   active: T-013   generation: 3
dod: 30/34 runs passed (88%)   blockers: 0   wizards pending: 1 (payments-tap)
tokens so far: ...   cost $41.20 (blended $3.43/ticket; ...)   est. remaining 37 tickets ...
escalations: 0
next: T-014   command: /foundry-build
```

| Field | Meaning |
|-------|---------|
| phase | 0 to 10 = planning, 11 = building |
| tickets | done out of total; `active` = in progress now |
| dod | automated checks (types, lint, tests, accessibility, screenshots) passed per attempt |
| blockers | problems that stopped the build; each prints on its own `blocker:` line |
| wizards pending | human steps you still owe (section 7) |
| cost, est. remaining | usage so far and the projection for the rest |
| next, command | the next ticket and what to type |

## 7. Wizards: the steps only you can do

Some tickets need a secret or an account only a person can get: a payment provider key, a
domain name, a regulator licence. Foundry builds the feature behind a switch and writes a wizard:

- `.foundry/wizard/<name>.md`: why it is needed and the exact steps.
- `.foundry/wizard/<name>.ps1` (Windows) or `.sh` (Mac, Linux): run it and paste each value when
  asked. It checks the format, writes `.env.local` (never committed) and tests the values.

Until you run it, the feature works with a stub. `status` lists every wizard still pending.

## 8. Release confirm (regulated apps)

For regulated domains (a trading app, for example), release stays blocked until a named person
confirms the licence and compliance steps are done. After the `regulator-licence` wizard:

```
python <foundry>/scripts/foundry.py release confirm --by "Your Name"
```

This records who approved going live. Only a person runs it; no agent runs it for you.

## Good to know

- Foundry runs only inside your logged-in Claude Code session. There is no API key to set.
- Builds need the code-graph tool codebase-memory-mcp; `/foundry-setup` checks and registers it.
