---
id: "T-022"
title: "Loyalty points (should-have)"
type: "feature"
blockedBy: ["T-005", "T-004"]
jobs: ["loyalty-points"]
screens: ["customer-lookup", "tender"]
operations: ["loyalty_account_loyalty_points"]
adrs: []
controls: ["SEC-ACC-01", "SEC-LOG-02"]
estimate: "M"
files_likely_touched: ["apps/api/src/customers/loyalty-points.ts", "apps/web/app/customer-lookup/page.tsx", "apps/web/app/tender/page.tsx"]
acceptance_tests:
  - "Given the job is enabled, When loyalty points runs, Then its operations respond per openapi.yaml"
  - "Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation"
  - "Given the screen, When it renders in ar, Then axe reports zero serious violations"
  - "Given a sale of 200 SAR with a later return of 50 SAR, When points are recalculated, Then points reflect the 150 SAR net paid amount"
  - "Given a LoyaltyAccount, When balance is read, Then points == earned minus redeemed"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-022 — Loyalty points (should-have)

## Slice

Should-have slice for `loyalty-points`.

## Acceptance tests

1. Given the job is enabled, When loyalty points runs, Then its operations respond per openapi.yaml
2. Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation
3. Given the screen, When it renders in ar, Then axe reports zero serious violations
4. Given a sale of 200 SAR with a later return of 50 SAR, When points are recalculated, Then points reflect the 150 SAR net paid amount
5. Given a LoyaltyAccount, When balance is read, Then points == earned minus redeemed

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
