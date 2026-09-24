---
id: "T-014"
title: "Apply discount (manager-pin, tender)"
type: "feature"
blockedBy: ["T-005", "T-004"]
jobs: ["apply-discount"]
screens: ["manager-pin", "tender"]
operations: ["order_apply_discount"]
adrs: ["0002"]
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01", "SEC-SESS-07", "SEC-API-01", "SEC-BL-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/ordering/apply-discount.ts", "apps/api/src/ordering/apply-discount.test.ts", "apps/web/app/manager-pin/page.tsx", "apps/web/app/tender/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the manager-pin screen, When apply discount completes, Then the Order state and totals match the domain invariants"
  - "Given offline mode, When apply discount runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Order.total == sum(OrderLine.line_total) - Order.discount_total + Order.service_charge + O' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'When TaxRule.inclusive is true, tax_total is extracted from tax-inclusive prices and round' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-014 — Apply discount (manager-pin, tender)

## Slice

Vertical slice for job `apply-discount`: operations order_apply_discount; screens manager-pin, tender; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the manager-pin screen, When apply discount completes, Then the Order state and totals match the domain invariants
2. Given offline mode, When apply discount runs, Then the write lands in the outbox and syncs without duplicates
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
