---
name: threat-model
description: Model threats for phase 9: STRIDE per trust boundary, an authz matrix per operation, abuse cases for the riskiest workflows, and blocking findings on money-moving operations.
invocation: model
model: opus
reads: [.foundry/architecture.md, openapi.yaml, .foundry/decisions.yaml, data/threat-patterns.csv, data/security-controls.csv]
writes: [.foundry/threats.md, .foundry/compliance.yaml, .foundry/compliance-evidence-plan.md]
gate: python scripts/foundry.py gate security
---

# threat-model — phase 9a

Boundaries first, then operations, then abuse. The skeleton joins the boundaries named in
architecture.md to threat-patterns.csv and controls.csv filtered by this project's decisions;
the model writes the abuse cases and judges the residual risk.

## Steps

1. **Generate.**

   ```
   python scripts/foundry.py threat-skeleton
   ```

   Done when: `.foundry/threats.md`, `compliance.yaml` and `compliance-evidence-plan.md` exist
   and the command printed boundary, control and pci_scope counts.

2. **Abuse cases for the three riskiest workflows.** Open architecture.md "Data flows" only.
   For payment, refund and offline sync, rewrite the abuse-case table: actor, goal, path,
   the control id that stops it, residual risk. Add rows for any actor the skeleton missed
   (rider, aggregator, LAN attacker, insider owner).
   Done when: each workflow has at least two rows and every "Stopped by" cites a control id
   from security-controls.csv.

3. **Money-moving operations.** In the authz matrix, every row with Money = yes must name an
   exact role rule (never "any authenticated") and carry access, business-logic and error-log
   controls. Write any violation under "Blocking findings" with the operationId and the fix.
   Done when: "Blocking findings" lists every violation or reads "none" and the matrix has no
   money row with "any authenticated".

4. **Top-10 review.** Reorder the top-10 risks when this project's exposure differs from the
   default (for example a delivery-only operation has no terminal-print-bridge risk), and add one line
   of rationale under the table.
   Done when: the top-10 table reflects this project's boundaries and has a rationale line.

5. **Gate.**

   ```
   python scripts/foundry.py gate security
   ```

   Done when: the gate prints `pass`.

## Reference

| Score | Meaning |
|-------|---------|
| severity × exposure | severity low 1, medium 2, high 3; exposure internet-edge, edge-api, webhook 3; third-party, device, admin 2; db, print bridge 1 |

Trust boundary types map to threat-patterns.csv `boundary_type`: internet<->edge,
edge<->api, api<->db, api<->payment-provider (third-party), api<->delivery-platform (webhook),
terminal<->local-print-bridge, device<->offline-store, plus admin always.
