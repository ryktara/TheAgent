---
id: "T-013"
title: "Split bill (split-bill)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-006"]
jobs: ["split-bill"]
screens: ["split-bill"]
operations: ["order_split_bill"]
adrs: ["0002"]
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01", "SEC-SESS-07", "SEC-API-01", "SEC-BL-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/ordering/split-bill.ts", "apps/api/src/ordering/split-bill.test.ts", "apps/web/app/split-bill/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the split-bill screen, When split bill completes, Then the Order state and totals match the domain invariants"
  - "Given offline mode, When split bill runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Order.total == sum(OrderLine.line_total) - Order.discount_total + Order.service_charge + O' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'When TaxRule.inclusive is true, tax_total is extracted from tax-inclusive prices and round' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-013 — Split bill (split-bill)

## Slice

Vertical slice for job `split-bill`: operations order_split_bill; screens split-bill; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the split-bill screen, When split bill completes, Then the Order state and totals match the domain invariants
2. Given offline mode, When split bill runs, Then the write lands in the outbox and syncs without duplicates
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
