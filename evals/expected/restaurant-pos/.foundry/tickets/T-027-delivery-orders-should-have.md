---
id: "T-027"
title: "Delivery orders (should-have)"
type: "feature"
blockedBy: ["T-006", "T-004"]
jobs: ["delivery-orders"]
screens: ["delivery-inbox", "kds"]
operations: ["order_delivery_orders"]
adrs: []
controls: ["SEC-ACC-01", "SEC-LOG-02"]
estimate: "M"
files_likely_touched: ["apps/api/src/ordering/delivery-orders.ts", "apps/web/app/delivery-inbox/page.tsx", "apps/web/app/kds/page.tsx"]
acceptance_tests:
  - "Given the job is enabled, When delivery orders runs, Then its operations respond per openapi.yaml"
  - "Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation"
  - "Given the screen, When it renders in ar, Then axe reports zero serious violations"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-027 — Delivery orders (should-have)

## Slice

Should-have slice for `delivery-orders`.

## Acceptance tests

1. Given the job is enabled, When delivery orders runs, Then its operations respond per openapi.yaml
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
