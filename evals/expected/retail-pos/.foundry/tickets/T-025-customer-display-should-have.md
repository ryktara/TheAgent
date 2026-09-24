---
id: "T-025"
title: "Customer display (should-have)"
type: "feature"
blockedBy: ["T-006", "T-004"]
jobs: ["customer-display"]
screens: ["customer-display"]
operations: ["sale_customer_display"]
adrs: []
controls: ["SEC-ACC-01", "SEC-LOG-02"]
estimate: "M"
files_likely_touched: ["apps/api/src/sales/customer-display.ts", "apps/web/app/customer-display/page.tsx"]
acceptance_tests:
  - "Given the job is enabled, When customer display runs, Then its operations respond per openapi.yaml"
  - "Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation"
  - "Given the screen, When it renders in ar, Then axe reports zero serious violations"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-025 — Customer display (should-have)

## Slice

Should-have slice for `customer-display`.

## Acceptance tests

1. Given the job is enabled, When customer display runs, Then its operations respond per openapi.yaml
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
