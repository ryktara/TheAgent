---
id: "T-009"
title: "Modify order (modifier-sheet, order-entry)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-006", "T-007"]
jobs: ["modify-order"]
screens: ["modifier-sheet", "order-entry"]
operations: ["order_line_modify_order"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/ordering/modify-order.ts", "apps/api/src/ordering/modify-order.test.ts", "apps/web/app/modifier-sheet/page.tsx", "apps/web/app/order-entry/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the modifier-sheet screen, When modify order completes, Then the OrderLine state and totals match the domain invariants"
  - "Given offline mode, When modify order runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Order.total == sum(OrderLine.line_total) - Order.discount_total + Order.service_charge + O' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'An OrderLine in state voided or comped carries a reason and an approver Staff id' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-009 — Modify order (modifier-sheet, order-entry)

## Slice

Vertical slice for job `modify-order`: operations order_line_modify_order; screens modifier-sheet, order-entry; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the modifier-sheet screen, When modify order completes, Then the OrderLine state and totals match the domain invariants
2. Given offline mode, When modify order runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Order.total == sum(OrderLine.line_total) - Order.discount_total + Order.service_charge + O' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'An OrderLine in state voided or comped carries a reason and an approver Staff id' is checked, Then it holds

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
