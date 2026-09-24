---
id: "T-024"
title: "Purchase orders (should-have)"
type: "feature"
blockedBy: ["T-005", "T-004"]
jobs: ["purchase-orders"]
screens: ["purchase-orders"]
operations: ["purchase_order_purchase_orders"]
adrs: []
controls: ["SEC-ACC-01", "SEC-LOG-02"]
estimate: "M"
files_likely_touched: ["apps/api/src/inventory/purchase-orders.ts", "apps/web/app/purchase-orders/page.tsx"]
acceptance_tests:
  - "Given the job is enabled, When purchase orders runs, Then its operations respond per openapi.yaml"
  - "Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation"
  - "Given the screen, When it renders in ar, Then axe reports zero serious violations"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-024 — Purchase orders (should-have)

## Slice

Should-have slice for `purchase-orders`.

## Acceptance tests

1. Given the job is enabled, When purchase orders runs, Then its operations respond per openapi.yaml
2. Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation
3. Given the screen, When it renders in ar, Then axe reports zero serious violations

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
