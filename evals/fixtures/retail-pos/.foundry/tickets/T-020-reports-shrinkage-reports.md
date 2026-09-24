---
id: "T-020"
title: "Reports shrinkage (reports)"
type: "feature"
blockedBy: ["T-003", "T-004"]
jobs: ["reports-shrinkage"]
screens: ["reports"]
operations: ["job_reports_shrinkage"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/reporting/reports-shrinkage.ts", "apps/api/src/reporting/reports-shrinkage.test.ts", "apps/web/app/reports/page.tsx"]
acceptance_tests:
  - "Given the reports screen, When reports shrinkage runs, Then the result matches the PRD job"
  - "Given a cashier role, When reports shrinkage is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-020 — Reports shrinkage (reports)

## Slice

Vertical slice for job `reports-shrinkage`: operations job_reports_shrinkage; screens reports; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the reports screen, When reports shrinkage runs, Then the result matches the PRD job
2. Given a cashier role, When reports shrinkage is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations

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
