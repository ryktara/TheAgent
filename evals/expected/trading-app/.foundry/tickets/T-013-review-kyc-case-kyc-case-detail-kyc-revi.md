---
id: "T-013"
title: "Review kyc case (kyc-case-detail, kyc-review-queue)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006", "T-008"]
jobs: ["review-kyc-case"]
screens: ["kyc-case-detail", "kyc-review-queue"]
operations: ["kyc_case_review_kyc_case"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/accounts/review-kyc-case.ts", "apps/api/src/accounts/review-kyc-case.test.ts", "apps/web/app/kyc-case-detail/page.tsx", "apps/web/app/kyc-review-queue/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the kyc-case-detail screen, When review kyc case completes, Then the KycCase state and totals match the domain invariants"
  - "Given a retail-trader role, When review kyc case is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A Transfer of direction withdrawal requires KycCase approved at the tier covering the amou' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'A KycCase decision and every ComplianceCase closure record a reviewer Staff id different f' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-013 — Review kyc case (kyc-case-detail, kyc-review-queue)

## Slice

Vertical slice for job `review-kyc-case`: operations kyc_case_review_kyc_case; screens kyc-case-detail, kyc-review-queue; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the kyc-case-detail screen, When review kyc case completes, Then the KycCase state and totals match the domain invariants
2. Given a retail-trader role, When review kyc case is attempted without permission, Then the api returns 403 and logs authz.denied
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
