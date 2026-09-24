---
id: "T-045"
title: "Compliance: error-log controls (11)"
type: "compliance"
blockedBy: ["T-003"]
jobs: []
screens: []
operations: []
adrs: []
controls: ["SEC-LOG-01", "SEC-LOG-03", "SEC-LOG-04", "SEC-LOG-05", "SEC-LOG-06", "SEC-LOG-07", "SEC-LOG-08", "SEC-LOG2-01", "SEC-LOG2-02", "SEC-LOG2-03", "SEC-LOG2-04"]
estimate: "L"
files_likely_touched: ["apps/api/src/security/", "docs/compliance/", ".foundry/compliance.yaml"]
acceptance_tests:
  - "Given control SEC-LOG-01, When its verify method (review) runs, Then evidence is attached in compliance.yaml"
  - "Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link"
  - "Given a regression, When the error-log tests run in CI, Then a failing control blocks merge"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-045 — Compliance: error-log controls (11)

## Slice

Implement and evidence 11 error-log controls: SEC-LOG-01, SEC-LOG-03, SEC-LOG-04, SEC-LOG-05, SEC-LOG-06, SEC-LOG-07, SEC-LOG-08, SEC-LOG2-01, SEC-LOG2-02, SEC-LOG2-03, SEC-LOG2-04

## Acceptance tests

1. Given control SEC-LOG-01, When its verify method (review) runs, Then evidence is attached in compliance.yaml
2. Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link
3. Given a regression, When the error-log tests run in CI, Then a failing control blocks merge

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
