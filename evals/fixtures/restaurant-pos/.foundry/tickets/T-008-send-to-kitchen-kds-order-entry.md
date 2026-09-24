---
id: "T-008"
title: "Send to kitchen (kds, order-entry)"
type: "feature"
blockedBy: ["T-005", "T-004"]
jobs: ["send-to-kitchen"]
screens: ["kds", "order-entry"]
operations: ["order_send_to_kitchen"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/ordering/send-to-kitchen.ts", "apps/api/src/ordering/send-to-kitchen.test.ts", "apps/web/app/kds/page.tsx", "apps/web/app/order-entry/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the kds screen, When send to kitchen completes, Then the Order state and totals match the domain invariants"
  - "Given offline mode, When send to kitchen runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Order.total == sum(OrderLine.line_total) - Order.discount_total + Order.service_charge + O' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'When TaxRule.inclusive is true, tax_total is extracted from tax-inclusive prices and round' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-008 — Send to kitchen (kds, order-entry)

## Slice

Vertical slice for job `send-to-kitchen`: operations order_send_to_kitchen; screens kds, order-entry; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the kds screen, When send to kitchen completes, Then the Order state and totals match the domain invariants
2. Given offline mode, When send to kitchen runs, Then the write lands in the outbox and syncs without duplicates
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
