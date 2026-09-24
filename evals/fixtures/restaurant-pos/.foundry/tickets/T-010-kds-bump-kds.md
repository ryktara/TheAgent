---
id: "T-010"
title: "Kds bump (kds)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-006", "T-007"]
jobs: ["kds-bump"]
screens: ["kds"]
operations: ["kitchen_ticket_kds_bump"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/kitchen/kds-bump.ts", "apps/api/src/kitchen/kds-bump.test.ts", "apps/web/app/kds/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the kds screen, When kds bump completes, Then the KitchenTicket state and totals match the domain invariants"
  - "Given offline mode, When kds bump runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A KitchenTicket is derived from fired OrderLines; it never holds lines that are not on the' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-010 — Kds bump (kds)

## Slice

Vertical slice for job `kds-bump`: operations kitchen_ticket_kds_bump; screens kds; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the kds screen, When kds bump completes, Then the KitchenTicket state and totals match the domain invariants
2. Given offline mode, When kds bump runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'A KitchenTicket is derived from fired OrderLines; it never holds lines that are not on the' is checked, Then it holds

## Definition of done

- typecheck
- unit
- integration
- e2e-smoke
- a11y-axe
- lint
- semgrep
- screenshot
- spec-review
- detect_changes_risk<=medium
