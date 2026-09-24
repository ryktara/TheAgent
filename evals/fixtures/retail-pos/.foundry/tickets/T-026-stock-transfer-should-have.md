---
id: "T-026"
title: "Stock transfer (should-have)"
type: "feature"
blockedBy: ["T-005", "T-004"]
jobs: ["stock-transfer"]
screens: ["transfers"]
operations: ["transfer_stock_transfer"]
adrs: []
controls: ["SEC-ACC-01", "SEC-LOG-02"]
estimate: "M"
files_likely_touched: ["apps/api/src/inventory/stock-transfer.ts", "apps/web/app/transfers/page.tsx"]
acceptance_tests:
  - "Given the job is enabled, When stock transfer runs, Then its operations respond per openapi.yaml"
  - "Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation"
  - "Given the screen, When it renders in ar, Then axe reports zero serious violations"
  - "Given a Transfer dispatched with 5 units, When 4 are scanned on arrival, Then the Transfer moves to discrepancy for owner review"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-026 — Stock transfer (should-have)

## Slice

Should-have slice for `stock-transfer`.

## Acceptance tests

1. Given the job is enabled, When stock transfer runs, Then its operations respond per openapi.yaml
2. Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation
3. Given the screen, When it renders in ar, Then axe reports zero serious violations
4. Given a Transfer dispatched with 5 units, When 4 are scanned on arrival, Then the Transfer moves to discrepancy for owner review

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
