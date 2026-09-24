---
id: "T-024"
title: "Reports (reports)"
type: "feature"
blockedBy: ["T-003", "T-004"]
jobs: ["reports"]
screens: ["reports"]
operations: ["job_reports"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/reporting/reports.ts", "apps/api/src/reporting/reports.test.ts", "apps/web/app/reports/page.tsx"]
acceptance_tests:
  - "Given the reports screen, When reports runs, Then the result matches the PRD job"
  - "Given a cashier role, When reports is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-024 — Reports (reports)

## Slice

Vertical slice for job `reports`: operations job_reports; screens reports; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the reports screen, When reports runs, Then the result matches the PRD job
2. Given a cashier role, When reports is attempted without permission, Then the api returns 403 and logs authz.denied
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
