---
name: to-tickets
description: Slice the build into tracer-bullet tickets for phase 10: scaffold, auth, tenancy, schema, design shell, offline sync, one vertical slice per must-have job, integrations, compliance, release.
invocation: model
model: sonnet
reads: [.foundry/prd.md, .foundry/domain.yaml, openapi.yaml, .foundry/screens/*.md, .foundry/architecture.md, .foundry/compliance.yaml, data/stacks.csv]
writes: [.foundry/tickets/*.md, .foundry/compliance.yaml]
gate: python scripts/foundry.py gate tickets
---

# to-tickets — phase 10

Tracer bullets: every ticket is a vertical slice with API, screen, tests, a11y scan and copy.
A slice is never split into backend and frontend halves. The skeleton orders slices by the
entity graph; the model sharpens acceptance tests where invariants imply edge cases.

## Steps

1. **Generate.**

   ```
   python scripts/foundry.py tickets-skeleton
   ```

   Done when: `.foundry/tickets/T-*.md` exist and the command printed counts by type.

2. **Sharpen acceptance tests.** For each feature ticket, read its entity's invariants in
   `domain.yaml` and add Given/When/Then rows for the edge cases they imply: rounding once
   per order, split-tender remainder, offline duplicate, void after fire, refund cap, shift
   close with open orders. Keep at least three tests per ticket.
   Done when: every invariant of the ticket's entity maps to at least one acceptance test.

3. **Predict files.** Adjust `files_likely_touched` to the repo layout convention
   (`apps/api/src/<context>/…`, `apps/web/app/<route>/…`, `packages/db/prisma/…`) and keep
   the list under eight entries.
   Done when: every path follows the convention and no ticket lists more than eight files.

4. **Budget.** When the count exceeds 60, merge should-have-adjacent jobs into their parent
   ticket (same entity) and note the merge in the parent's slice; never merge two must-have
   jobs.
   Done when: the count is at most 60 and every must-have job still has its own ticket.

5. **Gate.**

   ```
   python scripts/foundry.py gate tickets
   python scripts/foundry.py tickets next --n 3
   ```

   Done when: the gate prints `pass` and `tickets next` lists T-000 first.

## Reference

| Ticket | Type | Blocked by |
|--------|------|------------|
| T-000 scaffold | scaffold | none |
| T-001 auth, T-002 tenancy, T-003 schema | feature | previous |
| T-004 design shell | feature | T-000 |
| T-005 offline sync | feature | T-003, T-004 |
| T-006… one per must-have job | feature | T-005 or T-003, T-004, upstream entity tickets |
| integrations | integration | T-005 (+ payment job) |
| compliance per family | compliance | T-003 |
| T-900 release | release | last six feature and integration tickets |

DoD on every ticket: typecheck, unit, integration, e2e-smoke, a11y-axe, lint, semgrep,
screenshot, spec-review, detect_changes risk at most medium.
