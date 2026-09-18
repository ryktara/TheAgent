---
pack: <slug>
version: 1
decisions_hash: <from foundry.decisions_hash>
---

# PRD — <product name>

## 1. Product

One paragraph: what it is, for whom, where it runs, the one thing it must never fail at.
Derived facts end with [D:<id>].

## 2. Personas

| Persona | Role in the product | Kept because |
|---------|---------------------|--------------|
| <from pack.personas, pruned by decisions> | | [D:<id>] or pack |

## 3. Jobs to be done

| Id | Persona | Job | must/should | Screens |
|----|---------|-----|-------------|---------|
| <pack.jobs[].id> | | | | |

## 4. Scope IN

- `<must_have id>` — one line
- `<should_have id turned on>` — one line [D:<id>]

## 5. Scope OUT

- `<should_have id>` — reason (not chosen [D:<id>] / later phase / out of budget)

## 6. Non-functional requirements

- Offline: <required|optional|forbidden> [D:offline]
- Latency: <p95 targets from nfr_defaults>
- Devices: <from nfr_defaults and platform decisions>
- Languages: <en + ar (RTL) for AE/SA, ur for PK> [D:region]
- Uptime, backups, security baseline: <from nfr_defaults and compliance_must>

## 7. Integrations

| Category | Chosen | Source |
|----------|--------|--------|
| payments | <provider> | [D:payments] |

## 8. Regional and compliance

- Region: <country> [D:region]
- Tax, receipt languages, e-invoicing: <pack.regional[region]>
- Must controls: <pack.compliance_must, one per line>

## 9. Success metrics

1. <metric, number, unit, window>
2. ...

## 10. Open assumptions

Decisions taken from pack defaults; each can be changed by editing `.foundry/decisions.yaml`.

- `<id>` = <value> — <one line on what changes if it flips>
