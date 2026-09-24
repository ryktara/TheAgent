---
id: "T-022"
title: "Staff roles (staff-roles)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006", "T-014"]
jobs: ["staff-roles"]
screens: ["staff-roles"]
operations: ["staff_staff_roles"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/people/staff-roles.ts", "apps/api/src/people/staff-roles.test.ts", "apps/web/app/staff-roles/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the staff-roles screen, When staff roles completes, Then the Staff state and totals match the domain invariants"
  - "Given a retail-trader role, When staff roles is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A KycCase decision and every ComplianceCase closure record a reviewer Staff id different f' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-022 — Staff roles (staff-roles)

## Slice

Vertical slice for job `staff-roles`: operations staff_staff_roles; screens staff-roles; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the staff-roles screen, When staff roles completes, Then the Staff state and totals match the domain invariants
2. Given a retail-trader role, When staff roles is attempted without permission, Then the api returns 403 and logs authz.denied
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
