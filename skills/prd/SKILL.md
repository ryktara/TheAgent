---
name: prd
description: Write .foundry/prd.md from the chosen pack, the decision ledger and the brief. Cite every decision as [D:id] and list every default as an open assumption.
invocation: model
model: sonnet
reads: [.foundry/brief.md, .foundry/pack.yaml, .foundry/decisions.yaml, packs/<slug>/pack.yaml]
writes: [.foundry/prd.md]
gate: python scripts/foundry.py gate prd
---

# prd — phase 3

Single source of truth for scope. Inputs are three files plus one pack.yaml; the pack's
`reference/` folder stays closed in this phase. Template: PRD-TEMPLATE.md (sibling).

## Steps

1. **Load inputs.** Read `.foundry/pack.yaml` for `chosen`, then `packs/<chosen>/pack.yaml`,
   `.foundry/decisions.yaml`, `.foundry/brief.md`. Compute the ledger hash:

   ```
   python -c "import sys; sys.path.insert(0,'scripts'); import foundry as f, pathlib as p; print(f.decisions_hash(f.load_ledger(p.Path('.'))))"
   ```

   Done when: pack, ledger, brief and hash are in hand.

2. **Fill PRD-TEMPLATE.md section by section.** Rules that the gate checks:
   - Section 4 lists every pack `must_have` id in backticks, plus each `should_have` the ledger
     turns on (for example `multi-branch` when `[D:branches]` = multi).
   - Section 5 lists every remaining `should_have` id in backticks with a one-line reason.
   - Section 6 names offline, latency, devices and languages; languages include Arabic (RTL)
     for AE and SA, Urdu for PK.
   - Section 8 copies `regional[<region>]` and `compliance_must` for the region in `[D:region]`.
   - Section 10 lists every decision with source `pack-default` or `timeout-default` as
     `` `id` `` = value, one per line, marked changeable.
   - Every sentence derived from a decision ends with `[D:<id>]`.
   Done when: all ten sections are filled and no placeholder text remains.

3. **Write and gate.** Save `.foundry/prd.md` with frontmatter `pack`, `version: 1`,
   `decisions_hash`. Run:

   ```
   python scripts/foundry.py gate prd
   ```

   Done when: the gate prints `pass`.

## Reference

| Decision source | Where it appears |
|-----------------|------------------|
| human, brief, agent-fact | cited inline as [D:id] where it shapes scope or NFRs |
| pack-default, timeout-default | section 10 Open assumptions (and inline citation when used) |

Success metrics (section 9) are measurable: a number, a unit, and a time window each.
