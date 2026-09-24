---
id: "T-006"
title: "Scan and sell + sell weighed item (checkout, product-search, weighed-item)"
type: "feature"
blockedBy: ["T-005", "T-004"]
jobs: ["scan-and-sell", "sell-weighed-item"]
screens: ["checkout", "product-search", "weighed-item"]
operations: ["sale_scan_and_sell", "sale_line_sell_weighed_item"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/sales/scan-and-sell.ts", "apps/api/src/sales/scan-and-sell.test.ts", "apps/web/app/checkout/page.tsx", "apps/web/app/product-search/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the checkout screen, When scan and sell completes, Then the Sale state and totals match the domain invariants"
  - "Given offline mode, When scan and sell runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Sale.total == sum(SaleLine.line_total) - Sale.discount_total + Sale.tax_total, computed once in minor units at tender' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'A Sale in state paid has captured Tender amounts summing exactly to Sale.total; change is given only from cash' is checked, Then it holds"
  - "Given the merged job sell-weighed-item, When sell weighed item runs on the same screen, Then its operations respond and its screen states render"
  - "Given a basket of 3 variants at 49.99 SAR VAT-inclusive, When totals are computed, Then VAT is extracted once per sale and rounded to the nearest halala once"
  - "Given a Variant with on hand 0 and allow_negative false, When it is scanned, Then the line is blocked with the out-of-stock copy"
  - "Given the same barcode scanned twice, When the second scan lands, Then the existing SaleLine qty increments instead of a new line"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-006 — Scan and sell + sell weighed item (checkout, product-search, weighed-item)

## Slice

Vertical slice for job `scan-and-sell`: operations sale_scan_and_sell; screens checkout, product-search; copy from copy.csv; a11y scan; screenshot. Merged job `sell-weighed-item`: operations sale_line_sell_weighed_item.

## Acceptance tests

1. Given the checkout screen, When scan and sell completes, Then the Sale state and totals match the domain invariants
2. Given offline mode, When scan and sell runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Sale.total == sum(SaleLine.line_total) - Sale.discount_total + Sale.tax_total, computed once in minor units at tender' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'A Sale in state paid has captured Tender amounts summing exactly to Sale.total; change is given only from cash' is checked, Then it holds
6. Given the merged job sell-weighed-item, When sell weighed item runs on the same screen, Then its operations respond and its screen states render
7. Given a basket of 3 variants at 49.99 SAR VAT-inclusive, When totals are computed, Then VAT is extracted once per sale and rounded to the nearest halala once
8. Given a Variant with on hand 0 and allow_negative false, When it is scanned, Then the line is blocked with the out-of-stock copy
9. Given the same barcode scanned twice, When the second scan lands, Then the existing SaleLine qty increments instead of a new line

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
