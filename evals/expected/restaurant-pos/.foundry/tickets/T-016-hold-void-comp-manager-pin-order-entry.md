---
id: "T-016"
title: "Hold void comp (manager-pin, order-entry)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-006", "T-007"]
jobs: ["hold-void-comp"]
screens: ["manager-pin", "order-entry"]
operations: ["order_line_hold_void_comp"]
adrs: ["0002"]
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01", "SEC-SESS-07", "SEC-API-01", "SEC-BL-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/ordering/hold-void-comp.ts", "apps/api/src/ordering/hold-void-comp.test.ts", "apps/web/app/manager-pin/page.tsx", "apps/web/app/order-entry/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the manager-pin screen, When hold void comp completes, Then the OrderLine state and totals match the domain invariants"
  - "Given offline mode, When hold void comp runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Order.total == sum(OrderLine.line_total) - Order.discount_total + Order.service_charge + O' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'An OrderLine in state voided or comped carries a reason and an approver Staff id' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-016 — Hold void comp (manager-pin, order-entry)

## Slice

Vertical slice for job `hold-void-comp`: operations order_line_hold_void_comp; screens manager-pin, order-entry; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the manager-pin screen, When hold void comp completes, Then the OrderLine state and totals match the domain invariants
2. Given offline mode, When hold void comp runs, Then the write lands in the outbox and syncs without duplicates
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
