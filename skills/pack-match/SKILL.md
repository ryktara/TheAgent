---
name: pack-match
description: Match a brief to a domain pack and write .foundry/pack.yaml with confidence, alternates and brief-prefilled answers. Fall back to generic below threshold.
invocation: model
model: haiku
reads: [.foundry/brief.md, packs/index.csv]
writes: [.foundry/pack.yaml]
gate: python scripts/foundry.py validate
---

# pack-match — phase 1

Deterministic first, judgement only on a tie. Pack vocabulary comes from the matcher output;
`pack.yaml` bodies stay closed except in the tie branch. Reference folders stay closed here.

## Steps

1. **Score.** Run:

   ```
   python scripts/foundry.py match --brief .foundry/brief.md --json
   ```

   Done when: JSON with `candidates` (top 3), `prefilled`, `flags`, `unmatched_brief_terms`
   is in hand.

2. **Choose.** Let `top` be `candidates[0]` and `threshold` its index.csv value.
   - `top.confidence >= threshold` and no other candidate within 0.15 → accept `top`,
     `chosen_by: matcher`.
   - Two candidates within 0.15 of each other and both at or above their thresholds → open
     ONLY `name`, `personas`, `must_have` of those two `packs/<slug>/pack.yaml`; count brief
     nouns that overlap each `must_have` list; the larger overlap wins, `chosen_by:
     must-have-overlap`, flag `close-match`.
   - `top.confidence < threshold` → `chosen: generic`, `chosen_by: fallback`, flag
     `below-threshold`.

   Done when: exactly one `chosen` slug and one `chosen_by` value are decided.

3. **Write.** Emit `.foundry/pack.yaml` with: `chosen`, `confidence`, `threshold`,
   `alternates` (the other candidates with slug and confidence), `matched_terms`,
   `unmatched_aspects` (every brief noun the matcher listed as unmatched), `prefilled`
   (copied from the matcher, only for the chosen pack), `flags`, `matcher_version`,
   `chosen_by`. Schema: schemas/pack-selection.schema.json.

   Done when: `python scripts/foundry.py validate` passes with the file present.

4. **Account for every noun.** Each brief noun appears in `matched_terms` or in
   `unmatched_aspects`.

   Done when: the two lists together cover every noun in `unmatched_brief_terms` plus the
   matcher's matched terms, and the file re-validates.

## Reference

| Flag | Meaning for phase 2 |
|------|---------------------|
| no-questions-requested | brief asks for zero questions; grill still asks anything without a pack default |
| close-match | tie resolved by must_have overlap; the alternate pack is a candidate for round 2 |
| below-threshold | generic chosen; round 1 spends its first question on product category |
| scope-sprawl | brief names many modules; PRD scopes one first slice, lists the rest as later |

Prefilled answers carry `source: brief`; phase 2 logs them in the ledger without asking.
