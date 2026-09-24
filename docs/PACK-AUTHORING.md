# Pack authoring

A pack turns 40 questions into at most 7. Budget: one day. Order: scaffold, research, pack.yaml,
reference/, lint, variant eval, fixture + golden, generalisation run. Every step ends on a
command that exits 0.

## Day plan

| Block | Output | Done when |
|-------|--------|-----------|
| 1. Scaffold | `packs/<slug>/` | `python scripts/foundry.py scaffold-pack <slug>` then `sync-index` |
| 2. Research | `reference/sources.md` | every fact that drives a control, tax or question is a row with VERIFIED + URL or UNVERIFIED |
| 3. pack.yaml | fields below | `python scripts/foundry.py validate` passes with `complete: false` |
| 4. reference/ | screens, workflows, glossary, compliance, ux-patterns | `validate` passes with `complete: true` |
| 5. Variant eval | 6 briefs + 6 expected yaml | `python evals/run.py --stage match` all pass |
| 6. Fixture + golden | `evals/fixtures/<slug>/`, `evals/expected/<slug>/` | `python evals/run.py --stage golden` passes |
| 7. Generalisation run | fixes with a reason | unattended `/foundry` reaches gate 10 and T-000 + T-001 pass `dod` |

## Schema 2.0, field by field

`pack.yaml` is at most 200 lines in the YAML subset of [packs/README.md](../packs/README.md)
(no anchors, no multi-line strings). Schema: `schemas/pack.schema.json`.

### Identity and routing

| Field | Rule |
|-------|------|
| version | `"2.0"` |
| complete | `true` turns on the pack lint |
| threshold | 0.7 domain, 0.0 generic; feeds `packs/index.csv` |
| slug, name | folder name; display name |
| aliases | whole phrases a founder types ("cafe pos"); weight 3.0 in the matcher |
| confidence_keywords | single words; weight 1.0. Leave out payment-provider and generic commerce words ("shop", "stripe"): they tie packs |
| regulated | `true` when go-live needs a licence; scaffolds the `regulator-licence` wizard and blocks `gate release` until `release confirm --by <name>` |

### Domain

| Field | Rule |
|-------|------|
| personas | every role that performs or reads a job |
| jobs[] | `{id, must, screens, persona, priority 1-9, entity, extra_readers?, merge_into?}`; `entity` required for complete packs (`none` allowed) |
| must_have, should_have | feature ids; every should_have is reachable by an `enables` or stays OUT |
| entities | `{Name: {states: [...], exposure: public|internal|derived}}` |
| invariants | strings; every CamelCase word is an entity |
| contexts | `{context: [Entity, ...]}`; every entity in exactly one context |
| offline_contexts | contexts that sync offline; `[]` for online-only packs |
| integrations | `{category: [provider, ...]}` |
| regional | `{CC: {currency, tax, languages, compliance_must, compliance_should, tax_by_province?}}` |
| compliance_must, compliance_should | control ids present in `reference/compliance.md` |
| nfr_defaults | at least `offline: required|optional|forbidden` and one latency budget |
| stack_default | `{web, api, db, mobile?}`; values resolve by prefix against `data/stacks.csv` |
| ui_profile | `{style, density, touch, palette?, typography?, themes?}`; pins are `data/*.csv` ids |
| questions | ranked bank, at most 12; fields in packs/README.md (rank, answer_type, default, reversible, skip_if_brief_mentions, brief_hints, maps_to, followups, enables, derive_from) |
| reference | paths to the five reference files |

### vocabulary (new in 2.0)

Everything a skeleton used to hard-code from the restaurant pack. Required on `complete: true`
packs; every key inside is optional and falls back to generic wording. Full table:
[packs/README.md](../packs/README.md#vocabulary-20); a complete example:
[packs/restaurant-pos/pack.yaml](../packs/restaurant-pos/pack.yaml).

```yaml
vocabulary:
  scaffold_ticket_titles: {auth: "Staff sign-in and roles", tenancy: "Stores and branches", schema: "Catalogue and stock schema", tokens: "Design tokens", offline: "Offline till sync"}
  adr_hints: {"0003": "Ledger in Postgres, double entry", "0006": "Payments behind an adapter per provider"}
  design_defaults: {key_screens: [checkout, product-search, shift-close], component_set: [numpad, pin-pad], theme_names: {default: <palette id>}}
  glossary_hint_terms: [SKU, barcode, shrinkage, khaata, float]
  copy_overrides: {cart.empty: {en: "No items yet", ar: "لا توجد أصناف بعد"}}
  money_tokens: [sell, refund, void, discount, tender, settle]
  terms: {catalog: catalogue, catalog_items: products}
  smoke: {route: /checkout, pattern: "Checkout|الدفع", label: checkout}
```

| Key | Consumer | Rule |
|-----|----------|------|
| scaffold_ticket_titles | tickets-skeleton, T-001 to T-005 | keys auth, tenancy, schema, tokens, offline only; `offline` used only when the pack has offline contexts |
| adr_hints | arch-skeleton | key is an ADR id 0001 to 0009; 1 to 2 sentences each |
| adr_refs | arch-skeleton | ADR id to extra decision (question) ids that ADR cites |
| design_defaults | design-skeleton, screens-skeleton | key_screens are job screen ids; component_set are component ids; theme_names is `{default: <palette id>, ...}`; also screen_types, screen_components, component_hints, keyboard, list_routes |
| glossary_hint_terms | domain-skeleton (CONTEXT.md) | glossary terms always kept |
| copy_overrides | screens-skeleton, release | copy id to `{en, ar, ur}`; wins over `reference/copy.csv`, which wins over `data/copy.csv` |
| money_tokens | threat-skeleton, tickets | substrings of job ids that mark money-moving operations (access, business-logic and error-log controls) |
| terms | arch, tickets | noun phrases for catalog, catalog_items, canvas, live_state |
| operator_role, user_docs, smoke, seed_note | release, scaffold | front-line role (names `user-docs/<role>-quick-start.*`), user-doc buttons and routine, the smoke route and pattern, the seed note |
| authz_guard, containers, event_consumers | api, arch, domain | x-foundry.authz tail; architecture container rows; extra event consumers per context |

### reference/*.csv overrides

A pack may ship `reference/<name>.csv` for components, copy, palettes, product-types, ux-rules,
security-controls, threat-patterns and stacks. For that pack only, the file merges over
`data/<name>.csv`: a row whose id exists in `data/` replaces it in place; a new row goes after the
row named in its optional `after` column. Put domain-only rows (a kitchen display component, a
table-map rule) here, never in `data/`. Example: `packs/restaurant-pos/reference/`.

## Pack lint (`complete: true`)

`validate` fails with `file:line` unless: every job screen has a `## <screen-id>` heading in
screens.md; every invariant CamelCase name is an entity and every entity appears in an invariant
or screens.md; every `compliance_must` and regional control id is in compliance.md; glossary.csv
has at least 80 rows; `vocabulary` is present; sources.md exists and every VERIFIED row carries a URL; every `maps_to` is
unique; every `enables` target is a should_have id. P10 packs landed at 96 and 126 glossary rows
and 120+ reference lines each; treat those as the working floor.

## Research discipline

`reference/sources.md`: one table per region, columns Fact, Status, Source, an access date at the
top.

- **VERIFIED**: read on the linked page during research. The URL is in the row.
- **UNVERIFIED**: from prior knowledge or market practice. It may seed a default; it never drives
  a `compliance_must` control until verified.
- Tax rates, e-invoicing mandates and regulator names change: cite the authority page first,
  a secondary summary second.

Done when: every compliance id, every `regional.*.tax` and every `regulated`-related fact traces to
a row.

## Variant-brief eval

Six briefs per pack under `evals/briefs/<slug>-variants/<name>.md`, each with an expected file
`evals/expected/<slug>-variants/<name>.yaml`:

```yaml
brief: retail-pos-variants/baqala-deira
expected_pack: retail-pos
min_confidence: 0.8
max_questions: 7
required_artifacts:
  - .foundry/pack.yaml
```

Cover: two regions, one small and one multi-branch business, one brief in local vocabulary
("baqala", "khaata"), one brief that mentions a neighbouring pack's words. Run
`python evals/run.py --stage match`. Done when: all six select the pack at or above
`min_confidence`, and the existing packs' variants still pass (no stolen briefs).

## Fixture and golden

Run an unattended `/foundry` on the pack's main brief (`evals/briefs/<slug>.md`) in a temp
directory, copy the deterministic artefacts (CONTEXT.md, openapi.yaml, prisma/, design-system/,
migrations) to `evals/fixtures/<slug>/`, then:

```
python evals/run.py --stage golden --update-golden
python evals/run.py
```

Done when: every deterministic stage passes for every fixture in one process (the P10 context-reset
bug surfaced only there).

## Generalisation checklist

Every item below came from a P10 or P11 run where a new pack broke a restaurant assumption.

- [ ] `contexts` declared and cover every entity; `offline_contexts` lists only what syncs.
- [ ] `nfr_defaults.offline: forbidden` for online-only domains: then no `/sync/*`, no T-005,
      no offline copy. Check gate 6, 8 and 10 output for the word "offline".
- [ ] `regulated: true` when a licence gates go-live; confirm the wizard appears at phase 10.
- [ ] `regional[CC].languages` per region; Arabic copy only where a region lists `ar`, Urdu
      where it lists `ur`.
- [ ] `stack_default` values resolve against `data/stacks.csv` by prefix; web-first
      (nextjs-pwa + hono + postgres); `mobile: expo` is recorded, not built.
- [ ] Every webhook category in the API has an owning integration ticket (gate 10).
- [ ] Money tokens mark every money operation; none is authorised as "any authenticated".
- [ ] `vocabulary` filled so no ticket title, ADR or screen says "kitchen", "table" or "menu"
      outside restaurant-pos.
- [ ] Unattended run: gates 0 to 10 pass, ticket count within `evals/thresholds.yaml`
      (35 to 60), T-000 and T-001 pass `dod`.
- [ ] Each fix lands in CHANGELOG.md as `generalisation fix: ... (reason: <pack> run, <phase>)`.
