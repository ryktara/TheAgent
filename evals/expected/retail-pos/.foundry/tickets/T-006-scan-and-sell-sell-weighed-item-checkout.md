---
id: "T-006"
title: "Scan and sell + sell weighed item (checkout, product-search, weighed-item)"
type: "feature"
blockedBy: ["T-005", "T-004"]
jobs: ["scan-and-sell", "sell-weighed-item"]
screens: ["checkout", "product-search", "weighed-item"]
operations: ["sale_scan_and_sell", "sale_line_sell_weighed_item"]
adrs: ["0002"]
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01", "SEC-SESS-07", "SEC-API-01", "SEC-BL-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/sales/scan-and-sell.ts", "apps/api/src/sales/scan-and-sell.test.ts", "apps/web/app/checkout/page.tsx", "apps/web/app/product-search/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the checkout screen, When scan and sell completes, Then the Sale state and totals match the domain invariants"
  - "Given offline mode, When scan and sell runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Sale.total == sum(SaleLine.line_total) - Sale.discount_total + Sale.tax_total, computed on' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'A Sale in state paid has captured Tender amounts summing exactly to Sale.total; change is ' is checked, Then it holds"
  - "Given the merged job sell-weighed-item, When sell weighed item runs on the same screen, Then its operations respond and its screen states render"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-006 — Scan and sell + sell weighed item (checkout, product-search, weighed-item)

## Slice

Vertical slice for job `scan-and-sell`: operations sale_scan_and_sell; screens checkout, product-search; copy from copy.csv; a11y scan; screenshot. Merged job `sell-weighed-item`: operations sale_line_sell_weighed_item.

## Acceptance tests

1. Given the checkout screen, When scan and sell completes, Then the Sale state and totals match the domain invariants
2. Given offline mode, When scan and sell runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Sale.total == sum(SaleLine.line_total) - Sale.discount_total + Sale.tax_total, computed on' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'A Sale in state paid has captured Tender amounts summing exactly to Sale.total; change is ' is checked, Then it holds
6. Given the merged job sell-weighed-item, When sell weighed item runs on the same screen, Then its operations respond and its screen states render

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
