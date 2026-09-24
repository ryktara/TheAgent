---
id: "T-038"
title: "Compliance: business-logic controls (17)"
type: "compliance"
blockedBy: ["T-003"]
jobs: []
screens: []
operations: []
adrs: []
controls: ["SEC-BL-02", "SEC-BL-03", "SEC-BL-04", "SEC-BL-06", "SEC-BL-07", "SEC-BL-09", "SEC-BL-10", "SEC-BL-12", "SEC-BL-13", "SEC-BL-14", "SEC-BL-16", "SEC-BL2-01", "SEC-BL2-02", "SEC-BL2-03", "SEC-BL2-04", "SEC-BL2-05", "SEC-BL2-06"]
estimate: "L"
files_likely_touched: ["apps/api/src/security/", "docs/compliance/", ".foundry/compliance.yaml"]
acceptance_tests:
  - "Given control SEC-BL-02, When its verify method (test) runs, Then evidence is attached in compliance.yaml"
  - "Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link"
  - "Given a regression, When the business-logic tests run in CI, Then a failing control blocks merge"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-038 — Compliance: business-logic controls (17)

## Slice

Implement and evidence 17 business-logic controls: SEC-BL-02, SEC-BL-03, SEC-BL-04, SEC-BL-06, SEC-BL-07, SEC-BL-09, SEC-BL-10, SEC-BL-12, SEC-BL-13, SEC-BL-14, SEC-BL-16, SEC-BL2-01…

## Acceptance tests

1. Given control SEC-BL-02, When its verify method (test) runs, Then evidence is attached in compliance.yaml
2. Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link
3. Given a regression, When the business-logic tests run in CI, Then a failing control blocks merge

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
