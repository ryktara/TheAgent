---
id: "T-006"
title: "Open account (kyc-capture, signup)"
type: "feature"
blockedBy: ["T-003", "T-004"]
jobs: ["open-account"]
screens: ["kyc-capture", "signup"]
operations: ["account_open_account"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/accounts/open-account.ts", "apps/api/src/accounts/open-account.test.ts", "apps/web/app/kyc-capture/page.tsx", "apps/web/app/signup/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the kyc-capture screen, When open account completes, Then the Account state and totals match the domain invariants"
  - "Given a cashier role, When open account is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Position.qty == sum of signed Fill.qty for its Account and Instrument; Position is never w' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'A withdrawal Transfer is paid only to a beneficiary in the name of the Account owner' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-006 — Open account (kyc-capture, signup)

## Slice

Vertical slice for job `open-account`: operations account_open_account; screens kyc-capture, signup; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the kyc-capture screen, When open account completes, Then the Account state and totals match the domain invariants
2. Given a cashier role, When open account is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Position.qty == sum of signed Fill.qty for its Account and Instrument; Position is never w' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'A withdrawal Transfer is paid only to a beneficiary in the name of the Account owner' is checked, Then it holds

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
