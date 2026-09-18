# Domain packs

A pack is pre-baked industry knowledge that lets Foundry ask 3–7 questions instead of 40.
Folder: `packs/<slug>/pack.yaml` (at most 200 lines, the only file loaded) plus `reference/`
(pointed at, loaded one section at a time).

Create one with:

```
python scripts/foundry.py scaffold-pack <slug>
```

## Routing table

`packs/index.csv` is generated: `python scripts/foundry.py sync-index` rebuilds it from every
`pack.yaml` (`threshold` defaults to 0.7, generic 0.0) and `validate` fails on drift. Columns:

| Column | Meaning |
|--------|---------|
| slug | folder name under packs/ |
| name | display name |
| aliases | `;`-separated alternative names |
| keywords | `;`-separated confidence keywords |
| confidence_threshold | 0–1; below it the generic pack is used and extra questions are asked |

## YAML subset (no PyYAML)

Scripts are stdlib only, so `pack.yaml` is parsed by a minimal loader in `scripts/foundry.py`.
Stay inside this subset:

- Block mappings with 2-space indentation.
- Block lists (`- item`) and one-line flow lists (`[a, b, c]`).
- One-line flow mappings (`{k: v, k2: [a, b]}`), nestable one level inside a flow mapping.
- Block lists of flow mappings (`- {id: x, must: true}`).
- Scalars: bare strings, `"double quoted"`, `'single quoted'`, integers, floats, `true`/`false`.
- Comments with `#` at line start or after a space.

Outside the subset: anchors, multi-line strings (`|`, `>`), multi-line flow collections,
block mappings nested inside block lists. Validate catches parse errors with `file:line`.

## pack.yaml example (schema 1.2)

```yaml
version: "1.2"
threshold: 0.7
slug: restaurant-pos
name: Restaurant POS
aliases: [restaurant point of sale, cafe pos, qsr pos]
confidence_keywords: [restaurant, cafe, kitchen, table, menu, order, kds, bill]
personas: [cashier, waiter, kitchen, manager, owner]
jobs: [{id: take-order, must: true, screens: [order-entry, table-map]}]
must_have: [order-entry, modifiers, split-bill, kds, payments, shift-close]
should_have: [reservations, loyalty, multi-branch]
entities: {Order: {states: [draft, sent, ready, served, paid, void]}}
invariants: ["Order total == sum(lines) - discounts + tax"]
integrations: {payments: [stripe, tap], delivery: [talabat]}
regional: {AE: {tax: "VAT 5%", receipt_lang: [en, ar]}}
compliance_must: [PCI-DSS SAQ-A via hosted fields]
nfr_defaults: {offline: required, p95_order_entry_ms: 200}
stack_default: {web: nextjs, api: hono, db: postgres, mobile: expo}
ui_profile: {style: high-contrast-operational, density: high, touch: 48dp}
questions:
  - {id: service-model, rank: 1, ask: "Dine-in, quick-service, or both?", answer_type: choice, choices: [dine-in, quick-service, both], default: both, reversible: false, skip_if_brief_mentions: [dine-in, quick-service, qsr], brief_hints: {dine-in: [table service, waiters], quick-service: [qsr, counter]}, maps_to: service.model}
reference: {screens: reference/screens.md, workflows: reference/workflows.md, glossary: reference/glossary.csv, compliance: reference/compliance.md, ux_patterns: reference/ux-patterns.md}
```

Schema: `schemas/pack.schema.json`.

## Question bank (1.2)

`questions` is a ranked bank of at most 12. The 7/3 round budget is enforced at grill time by
`schemas/decisions.schema.json`, so a brief that pre-answers three questions still leaves enough
ranked questions to fill round 1.

| Field | Required | Meaning |
|-------|----------|---------|
| id | yes | stable key, kebab-case |
| rank | yes | 1 = ask first; unique within the pack |
| ask | yes | the sentence shown to the founder |
| answer_type | yes | choice, text, number, bool |
| choices | when choice | allowed values; `default` is one of them |
| default | yes | used when the founder is silent or the budget is spent |
| reversible | no | false marks a decision that is costly to change later |
| skip_if_brief_mentions | no | keywords; any hit pre-answers the question with `source: brief` |
| brief_hints | no | choice → keywords; a hit resolves the value to that choice |
| maps_to | no | dotted path into decisions, e.g. `region.country` |
| followups | no | up to 3 of `{when: <value or "*">, ask: [ids]}`; targets are round-2 only and never fill round 1 |

`foundry.py match` prefills: for a choice question, the value is the `brief_hints` choice whose
keyword hit, else the choice whose text matches, else the matched phrase. Bool questions become
`true` on any hit; text and number questions carry the matched phrase.

## reference/ folder

| File | Holds |
|------|-------|
| screens.md | per-screen layout, states, data bindings |
| workflows.md | end-to-end operational flows per persona |
| glossary.csv | term, definition, aliases (seeds CONTEXT.md) |
| compliance.md | regional and industry controls with sources |
| ux-patterns.md | domain UI patterns (numpad, split-bill, KDS, order ticket) |
