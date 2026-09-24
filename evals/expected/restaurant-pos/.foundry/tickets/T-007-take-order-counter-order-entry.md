---
id: "T-007"
title: "Take order counter (order-entry)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-006"]
jobs: ["take-order-counter"]
screens: ["order-entry"]
operations: ["order_take_order_counter"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/ordering/take-order-counter.ts", "apps/api/src/ordering/take-order-counter.test.ts", "apps/web/app/order-entry/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the order-entry screen, When take order counter completes, Then the Order state and totals match the domain invariants"
  - "Given offline mode, When take order counter runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Order.total == sum(OrderLine.line_total) - Order.discount_total + Order.service_charge + O' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'When TaxRule.inclusive is true, tax_total is extracted from tax-inclusive prices and round' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-007 — Take order counter (order-entry)

## Slice

Vertical slice for job `take-order-counter`: operations order_take_order_counter; screens order-entry; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the order-entry screen, When take order counter completes, Then the Order state and totals match the domain invariants
2. Given offline mode, When take order counter runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Order.total == sum(OrderLine.line_total) - Order.discount_total + Order.service_charge + O' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'When TaxRule.inclusive is true, tax_total is extracted from tax-inclusive prices and round' is checked, Then it holds

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
