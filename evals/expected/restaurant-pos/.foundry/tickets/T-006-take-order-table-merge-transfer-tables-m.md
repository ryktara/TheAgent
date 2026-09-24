---
id: "T-006"
title: "Take order table + merge transfer tables + manage floor (order-entry, table-map, floor-editor)"
type: "feature"
blockedBy: ["T-005", "T-004"]
jobs: ["take-order-table", "merge-transfer-tables", "manage-floor"]
screens: ["order-entry", "table-map", "floor-editor"]
operations: ["order_take_order_table", "table_merge_transfer_tables", "table_manage_floor"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/ordering/take-order-table.ts", "apps/api/src/ordering/take-order-table.test.ts", "apps/web/app/order-entry/page.tsx", "apps/web/app/table-map/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the order-entry screen, When take order table completes, Then the Order state and totals match the domain invariants"
  - "Given offline mode, When take order table runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Order.total == sum(OrderLine.line_total) - Order.discount_total + Order.service_charge + O' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'When TaxRule.inclusive is true, tax_total is extracted from tax-inclusive prices and round' is checked, Then it holds"
  - "Given the merged job merge-transfer-tables, When merge transfer tables runs on the same screen, Then its operations respond and its screen states render"
  - "Given the merged job manage-floor, When manage floor runs on the same screen, Then its operations respond and its screen states render"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-006 — Take order table + merge transfer tables + manage floor (order-entry, table-map, floor-editor)

## Slice

Vertical slice for job `take-order-table`: operations order_take_order_table; screens order-entry, table-map; copy from copy.csv; a11y scan; screenshot. Merged job `merge-transfer-tables`: operations table_merge_transfer_tables. Merged job `manage-floor`: operations table_manage_floor.

## Acceptance tests

1. Given the order-entry screen, When take order table completes, Then the Order state and totals match the domain invariants
2. Given offline mode, When take order table runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Order.total == sum(OrderLine.line_total) - Order.discount_total + Order.service_charge + O' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'When TaxRule.inclusive is true, tax_total is extracted from tax-inclusive prices and round' is checked, Then it holds
6. Given the merged job merge-transfer-tables, When merge transfer tables runs on the same screen, Then its operations respond and its screen states render
7. Given the merged job manage-floor, When manage floor runs on the same screen, Then its operations respond and its screen states render

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
