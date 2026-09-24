---
id: "T-018"
title: "Compliance case review (compliance-case-detail, surveillance-alerts)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006", "T-014"]
jobs: ["compliance-case-review"]
screens: ["compliance-case-detail", "surveillance-alerts"]
operations: ["compliance_case_compliance_case_review"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/compliance/compliance-case-review.ts", "apps/api/src/compliance/compliance-case-review.test.ts", "apps/web/app/compliance-case-detail/page.tsx", "apps/web/app/surveillance-alerts/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the compliance-case-detail screen, When compliance case review completes, Then the ComplianceCase state and totals match the domain invariants"
  - "Given a retail-trader role, When compliance case review is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A KycCase decision and every ComplianceCase closure record a reviewer Staff id different f' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-018 — Compliance case review (compliance-case-detail, surveillance-alerts)

## Slice

Vertical slice for job `compliance-case-review`: operations compliance_case_compliance_case_review; screens compliance-case-detail, surveillance-alerts; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the compliance-case-detail screen, When compliance case review completes, Then the ComplianceCase state and totals match the domain invariants
2. Given a retail-trader role, When compliance case review is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'A KycCase decision and every ComplianceCase closure record a reviewer Staff id different f' is checked, Then it holds

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
