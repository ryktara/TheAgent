---
id: "T-015"
title: "Tips service charge (tender)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-006"]
jobs: ["tips-service-charge"]
screens: ["tender"]
operations: ["order_tips_service_charge"]
adrs: ["0002"]
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01", "SEC-SESS-07", "SEC-API-01", "SEC-BL-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/ordering/tips-service-charge.ts", "apps/api/src/ordering/tips-service-charge.test.ts", "apps/web/app/tender/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the tender screen, When tips service charge completes, Then the Order state and totals match the domain invariants"
  - "Given offline mode, When tips service charge runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Order.total == sum(OrderLine.line_total) - Order.discount_total + Order.service_charge + O' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'When TaxRule.inclusive is true, tax_total is extracted from tax-inclusive prices and round' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-015 — Tips service charge (tender)

## Slice

Vertical slice for job `tips-service-charge`: operations order_tips_service_charge; screens tender; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the tender screen, When tips service charge completes, Then the Order state and totals match the domain invariants
2. Given offline mode, When tips service charge runs, Then the write lands in the outbox and syncs without duplicates
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
