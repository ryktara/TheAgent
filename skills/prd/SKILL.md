---
name: prd
description: Write .foundry/prd.md from the chosen pack, the decision ledger and the brief. Generate sections 2–8 and 10 deterministically, then write sections 1 and 9.
invocation: model
model: sonnet
reads: [.foundry/brief.md, .foundry/pack.yaml, .foundry/decisions.yaml, packs/<slug>/pack.yaml]
writes: [.foundry/prd.md]
gate: python scripts/foundry.py gate prd
---

# prd — phase 3

Single source of truth for scope. The skeleton carries every table, feature id and `[D:id]`
citation; the model writes two sections. The pack's `reference/` folder stays closed here.
Template for the two model sections: PRD-TEMPLATE.md (sibling).

## Steps

1. **Generate the skeleton.**

   ```
   python scripts/foundry.py prd-skeleton --out .foundry/prd.md
   ```

   Done when: `.foundry/prd.md` exists with frontmatter and two `<!-- model: write -->` blocks.

2. **Write section 1, Product.** One paragraph from the brief and the confirmed decisions in
   section 10: what it is, for whom, where it runs, the one thing it must never fail at. Each
   sentence that rests on a decision ends with `[D:<id>]`. Replace the model block and its
   comment.
   Done when: section 1 has one paragraph and no `<!--` remains in it.

3. **Write section 9, Success metrics.** Three to five lines, each with a number, a unit and a
   time window, tied to the must-have jobs in section 3. Replace the model block.
   Done when: section 9 has 3–5 numbered metrics and no `<!--` remains in it.

4. **Review sections 4 and 5.** The skeleton enables a should-have when a decision shares a
   token with it. Move an id between IN and OUT only with a citation, keeping every id in
   exactly one of the two sections.
   Done when: every pack `should_have` id appears once across sections 4 and 5.

5. **Gate.**

   ```
   python scripts/foundry.py gate prd
   ```

   Done when: the gate prints `pass`.

## Reference

| Skeleton section | Source |
|------------------|--------|
| 2 Personas, 3 Jobs | pack personas, jobs (id, persona, must, screens) |
| 4 IN / 5 OUT | must_have always IN; should_have by decision token overlap |
| 6 NFR | nfr_defaults, offline decision, regional languages |
| 7 Integrations | pack integrations, decisions whose maps_to names the category |
| 8 Regional | regional[region decision], compliance_must / should ids |
| 10 Assumptions | every ledger entry: confirmed (human, brief, agent-fact) then defaults |
