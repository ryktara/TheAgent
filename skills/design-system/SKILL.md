---
name: design-system
description: Produce the design system for phase 7: MASTER.md, tokens.json and tailwind.tokens.css from the pack profile, product type and brand answers; make it deliberate, not templated.
invocation: model
model: sonnet
reads: [.foundry/pack.yaml, .foundry/decisions.yaml, packs/<slug>/pack.yaml, data/product-types.csv, data/palettes.csv, data/typography.csv, data/styles.csv, data/components.csv, data/ux-rules.csv]
writes: [design-system/MASTER.md, design-system/tokens.json, design-system/tailwind.tokens.css, design-system/pages/README.md]
gate: python scripts/foundry.py gate design
---

# design-system — phase 7

Reference is data. Palette, typography, style and rules come from `data/*.csv` through the
skeleton and `foundry.py query`; no CSV is opened whole. The model writes the intent and
adjusts for brand; the validator guards contrast and scales.

## Steps

1. **Generate.**

   ```
   python scripts/foundry.py design-skeleton
   ```

   Done when: `design-system/MASTER.md`, `tokens.json`, `tailwind.tokens.css` and
   `pages/README.md` exist and the command named palette, typography, style and product type.

2. **Brand branch.** When the ledger has a brand answer (logo or colours provided): set
   `color.light.primary` in tokens.json to the brand primary, then run

   ```
   python scripts/foundry.py design-check
   ```

   and, while `primary_fg/primary` fails, move the primary lightness in 4% steps until it
   passes; record the original and adjusted hex under "Brand input" in MASTER.md. Keep the
   palette's neutrals and semantics.
   Done when: design-check reports 0 token issues and the adjustment (or "none") is written.

3. **Write the intent.** Replace the model comment under `## Intent` with at most five
   sentences that make this product look deliberate: name the one accent and why, the density
   and why, the typographic hierarchy (two weights), the motion purpose, and what stays flat.
   Leading words: deliberate, operational, calm, dense.
   Done when: `## Intent` has 1–5 sentences and no `<!--` remains.

4. **Positive guardrails.** Confirm each holds in MASTER.md and tokens: one accent; radius
   scale of at most 3 used values; two type weights carry hierarchy; motion only signals state
   change (100–400 ms, reduced-motion variant); icons from Lucide, text for meaning; tabular
   numerals wherever money or counts appear.
   Done when: each of the six guardrails maps to a line in `## Do and avoid` or `## Scales`.

5. **Gate.**

   ```
   python scripts/foundry.py design-check
   python scripts/foundry.py gate design
   ```

   Done when: both print no failures and the gate prints `pass`.

## Reference

| Selection | Rule in the skeleton |
|-----------|----------------------|
| product type | `product-types.csv` row with id == pack slug, else best tag overlap with pack aliases |
| palette | highest overlap of `industry_tags` with product tags + default_palette_tag (+ dark when ui_profile.dark is default) |
| typography | overlap of use_case and mood with product tags; Arabic-capable pairs boosted for RTL regions |
| style | `ui_profile.style` when it is a styles.csv id, else the product type default |
| rules | priority ≤ 5 rules whose applies_to hits the product's key screens, 15 max |
| components | base set + operational set (pack `vocabulary.design_defaults.component_set`) for high-density POS and work-queue screens + charts for analytics |

`foundry.py query palettes --industry_tags pos` lists alternatives when the founder rejects the pick.
