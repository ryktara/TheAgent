---
name: architecture
description: Decide the architecture for phase 5: write nine ADRs and .foundry/architecture.md with containers, trust boundaries, risky data flows, scaling and cost.
invocation: model
model: opus
reads: [.foundry/domain.yaml, .foundry/decisions.yaml, .foundry/prd.md, packs/<slug>/pack.yaml, data/stacks.csv]
writes: [.foundry/architecture.md, .foundry/adr/*.md]
gate: python scripts/foundry.py gate architecture
---

# architecture — phase 5

Decisions recorded as they are made. The skeleton writes every ADR from pack defaults and
ledger decisions; the model edits where the founder's answers or the domain model change the
trade-off. Template: ADR-TEMPLATE.md (sibling). Each ADR stays under 60 lines.

## Steps

1. **Generate.**

   ```
   python scripts/foundry.py arch-skeleton
   ```

   Done when: `.foundry/adr/0001..0009-*.md` and `.foundry/architecture.md` exist.

2. **Review each ADR against the ledger.** For each of the nine ids below, read the ADR and
   the decisions it cites. Where a decision changes the trade-off (offline off, multi-branch,
   provider choice, region), rewrite Decision and Consequences; keep the alternatives table
   honest with a real reason per rejected option. Cite every decision used as `[D:<id>]`; write
   `pack-default` where none applies.
   Done when: all nine ADRs read true for this project and each cites a decision or says
   pack-default.

3. **Check trust boundaries.** architecture.md lists at least the five that phase 9's threat
   model consumes: internet↔edge, edge↔api, api↔db, api↔payment-provider,
   device↔offline-store; add terminal↔local-print-bridge when printing is in scope and
   api↔delivery-platform when delivery is on.
   Done when: every boundary in the frontmatter has a bullet with its control summary.

4. **Rewrite the three risky data flows** (payment, refund, offline sync) so each names the
   containers crossed and the boundary controls applied, matching the chosen provider and the
   conflict rules in `packs/<slug>/reference/workflows.md` (open only the sync section).
   Done when: each flow lists containers, boundaries and the idempotency or conflict rule.

5. **Record in code memory** when `python scripts/foundry.py doctor` reports
   codebase-memory-mcp present: call `manage_adr` once per ADR (mode `update` or
   `set_sections`) with id, title, status and the Decision section. When absent, add
   "CBM absent, ADRs not mirrored" to the phase metrics note.
   Done when: nine ADRs mirrored, or the note is recorded.

6. **Gate.**

   ```
   python scripts/foundry.py gate architecture
   ```

   Done when: the gate prints `pass`.

## Reference

| Id | ADR | Cites |
|----|-----|-------|
| 0001 | Stack | offline, platform |
| 0002 | Auth and sessions | service-model, branches |
| 0003 | Tenancy and branches | branches, central-menu-sync |
| 0004 | Data store and migrations | region |
| 0005 | Offline and sync | offline |
| 0006 | Integrations boundary | payments, delivery, kds |
| 0007 | Deployment and environments | branches |
| 0008 | Observability | offline |
| 0009 | Internationalisation and RTL | region |

Stack ids and their commands come from `data/stacks.csv`; `foundry.py query stacks --layer api`
lists the options for a layer.
