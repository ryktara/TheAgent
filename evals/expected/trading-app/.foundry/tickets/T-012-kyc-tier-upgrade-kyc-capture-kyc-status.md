---
id: "T-012"
title: "Kyc tier upgrade (kyc-capture, kyc-status)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006", "T-008"]
jobs: ["kyc-tier-upgrade"]
screens: ["kyc-capture", "kyc-status"]
operations: ["kyc_case_kyc_tier_upgrade"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/accounts/kyc-tier-upgrade.ts", "apps/api/src/accounts/kyc-tier-upgrade.test.ts", "apps/web/app/kyc-capture/page.tsx", "apps/web/app/kyc-status/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the kyc-capture screen, When kyc tier upgrade completes, Then the KycCase state and totals match the domain invariants"
  - "Given a retail-trader role, When kyc tier upgrade is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A Transfer of direction withdrawal requires KycCase approved at the tier covering the amou' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'A KycCase decision and every ComplianceCase closure record a reviewer Staff id different f' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-012 — Kyc tier upgrade (kyc-capture, kyc-status)

## Slice

Vertical slice for job `kyc-tier-upgrade`: operations kyc_case_kyc_tier_upgrade; screens kyc-capture, kyc-status; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the kyc-capture screen, When kyc tier upgrade completes, Then the KycCase state and totals match the domain invariants
2. Given a retail-trader role, When kyc tier upgrade is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'A Transfer of direction withdrawal requires KycCase approved at the tier covering the amou' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'A KycCase decision and every ComplianceCase closure record a reviewer Staff id different f' is checked, Then it holds

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
