---
id: "T-041"
title: "Compliance: input controls (14)"
type: "compliance"
blockedBy: ["T-003"]
jobs: []
screens: []
operations: []
adrs: []
controls: ["SEC-IN-01", "SEC-IN-02", "SEC-IN-03", "SEC-IN-07", "SEC-IN-08", "SEC-IN-09", "SEC-IN-10", "SEC-IN2-01", "SEC-IN2-02", "SEC-IN2-03", "SEC-IN2-05", "SEC-IN2-06", "SEC-IN2-07", "SEC-IN2-08"]
estimate: "L"
files_likely_touched: ["apps/api/src/security/", "docs/compliance/", ".foundry/compliance.yaml"]
acceptance_tests:
  - "Given control SEC-IN-01, When its verify method (test) runs, Then evidence is attached in compliance.yaml"
  - "Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link"
  - "Given a regression, When the input tests run in CI, Then a failing control blocks merge"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-041 — Compliance: input controls (14)

## Slice

Implement and evidence 14 input controls: SEC-IN-01, SEC-IN-02, SEC-IN-03, SEC-IN-07, SEC-IN-08, SEC-IN-09, SEC-IN-10, SEC-IN2-01, SEC-IN2-02, SEC-IN2-03, SEC-IN2-05, SEC-IN2-06…

## Acceptance tests

1. Given control SEC-IN-01, When its verify method (test) runs, Then evidence is attached in compliance.yaml
2. Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link
3. Given a regression, When the input tests run in CI, Then a failing control blocks merge

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
