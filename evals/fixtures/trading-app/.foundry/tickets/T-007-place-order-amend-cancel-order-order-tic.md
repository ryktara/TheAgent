---
id: "T-007"
title: "Place order + amend cancel order (order-ticket, risk-warning, open-orders)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006"]
jobs: ["place-order", "amend-cancel-order"]
screens: ["order-ticket", "risk-warning", "open-orders"]
operations: ["order_place_order", "order_amend_cancel_order"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/trading/place-order.ts", "apps/api/src/trading/place-order.test.ts", "apps/web/app/order-ticket/page.tsx", "apps/web/app/risk-warning/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the order-ticket screen, When place order completes, Then the Order state and totals match the domain invariants"
  - "Given a cashier role, When place order is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'No Order moves to accepted without a passed buying-power or margin check against RiskLimit' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'Sum of Fill.qty for an Order never exceeds Order.qty; filled_qty == sum(Fill.qty)' is checked, Then it holds"
  - "Given the merged job amend-cancel-order, When amend cancel order runs on the same screen, Then its operations respond and its screen states render"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-007 — Place order + amend cancel order (order-ticket, risk-warning, open-orders)

## Slice

Vertical slice for job `place-order`: operations order_place_order; screens order-ticket, risk-warning; copy from copy.csv; a11y scan; screenshot. Merged job `amend-cancel-order`: operations order_amend_cancel_order.

## Acceptance tests

1. Given the order-ticket screen, When place order completes, Then the Order state and totals match the domain invariants
2. Given a cashier role, When place order is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'No Order moves to accepted without a passed buying-power or margin check against RiskLimit' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'Sum of Fill.qty for an Order never exceeds Order.qty; filled_qty == sum(Fill.qty)' is checked, Then it holds
6. Given the merged job amend-cancel-order, When amend cancel order runs on the same screen, Then its operations respond and its screen states render

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
