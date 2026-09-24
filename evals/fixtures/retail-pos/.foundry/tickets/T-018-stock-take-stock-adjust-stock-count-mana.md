---
id: "T-018"
title: "Stock take + stock adjust (stock-count, manager-pin)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-007", "T-008"]
jobs: ["stock-take", "stock-adjust"]
screens: ["stock-count", "manager-pin"]
operations: ["stock_count_stock_take", "stock_movement_stock_adjust"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/inventory/stock-take.ts", "apps/api/src/inventory/stock-take.test.ts", "apps/web/app/stock-count/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the stock-count screen, When stock take completes, Then the StockCount state and totals match the domain invariants"
  - "Given a cashier role, When stock take is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A StockCount posted writes exactly one StockMovement of kind count-variance per Variant with non-zero variance' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'Every state change on Sale, Tender, Return, CashDrawerSession, Promotion and StockCount writes one audit log event' is checked, Then it holds"
  - "Given the merged job stock-adjust, When stock adjust runs on the same screen, Then its operations respond and its screen states render"
  - "Given a posted StockCount, When it posts, Then exactly one count-variance StockMovement exists per Variant with non-zero variance"
  - "Given sales after the snapshot, When the count posts, Then those movements are reconciled and not double counted"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-018 — Stock take + stock adjust (stock-count, manager-pin)

## Slice

Vertical slice for job `stock-take`: operations stock_count_stock_take; screens stock-count; copy from copy.csv; a11y scan; screenshot. Merged job `stock-adjust`: operations stock_movement_stock_adjust.

## Acceptance tests

1. Given the stock-count screen, When stock take completes, Then the StockCount state and totals match the domain invariants
2. Given a cashier role, When stock take is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'A StockCount posted writes exactly one StockMovement of kind count-variance per Variant with non-zero variance' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'Every state change on Sale, Tender, Return, CashDrawerSession, Promotion and StockCount writes one audit log event' is checked, Then it holds
6. Given the merged job stock-adjust, When stock adjust runs on the same screen, Then its operations respond and its screen states render
7. Given a posted StockCount, When it posts, Then exactly one count-variance StockMovement exists per Variant with non-zero variance
8. Given sales after the snapshot, When the count posts, Then those movements are reconciled and not double counted

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
