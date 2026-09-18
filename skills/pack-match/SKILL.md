---
name: pack-match
description: Match a brief to a domain pack and write .foundry/pack.yaml with confidence, alternates and brief-prefilled answers. Fall back to generic below threshold.
invocation: model
model: haiku
reads: [.foundry/brief.md, packs/index.csv]
writes: [.foundry/pack.yaml]
gate: python scripts/foundry.py gate pack-match
---

# pack-match — phase 1

Fully deterministic: the matcher scores, resolves ties by must_have overlap, and writes the
selection. This skill opens no pack.yaml and no reference/ file.

## Steps

1. **Score and write.**

   ```
   python scripts/foundry.py match --brief .foundry/brief.md --write
   ```

   Done when: `.foundry/pack.yaml` exists and the command printed `chosen:`.

2. **Gate.**

   ```
   python scripts/foundry.py gate pack-match
   ```

   Done when: the gate prints `pass`.

3. **Report one line** for the orchestrator's metrics note: `<slug> <confidence> <chosen_by>`
   plus any flags.
   Done when: the line is emitted.

## Reference

| Flag | Meaning for phase 2 |
|------|---------------------|
| no-questions-requested | brief asks for zero questions; grilling runs unattended |
| close-match | tie resolved by must_have overlap; alternates carry the runner-up |
| below-threshold | generic chosen; round 1 opens with the product-summary question |
| scope-sprawl | brief names many modules; PRD scopes one first slice, lists the rest as later |

`chosen_by`: `keywords` (top score at or above threshold), `must-have-overlap` (tie within
0.15), `fallback` (generic). Prefilled answers carry `source: brief`; phase 2 seeds the ledger
from them and asks a confirm only for irreversible ones.
