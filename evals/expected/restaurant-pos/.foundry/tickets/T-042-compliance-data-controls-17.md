---
id: "T-042"
title: "Compliance: data controls (17)"
type: "compliance"
blockedBy: ["T-003"]
jobs: []
screens: []
operations: []
adrs: []
controls: ["SEC-DATA-01", "SEC-DATA-02", "SEC-DATA-03", "SEC-DATA-04", "SEC-DATA-05", "SEC-DATA-06", "SEC-DATA-08", "SEC-DATA-09", "SEC-DATA-10", "SEC-OFF-02", "SEC-OFF-04", "SEC-OFF-05", "SEC-DATA2-01", "SEC-DATA2-02", "SEC-DATA2-03", "SEC-DATA2-04", "SEC-DATA2-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/security/", "docs/compliance/", ".foundry/compliance.yaml"]
acceptance_tests:
  - "Given control SEC-DATA-01, When its verify method (scan) runs, Then evidence is attached in compliance.yaml"
  - "Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link"
  - "Given a regression, When the data tests run in CI, Then a failing control blocks merge"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-042 — Compliance: data controls (17)

## Slice

Implement and evidence 17 data controls: SEC-DATA-01, SEC-DATA-02, SEC-DATA-03, SEC-DATA-04, SEC-DATA-05, SEC-DATA-06, SEC-DATA-08, SEC-DATA-09, SEC-DATA-10, SEC-OFF-02, SEC-OFF-04, SEC-OFF-05…

## Acceptance tests

1. Given control SEC-DATA-01, When its verify method (scan) runs, Then evidence is attached in compliance.yaml
2. Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link
3. Given a regression, When the data tests run in CI, Then a failing control blocks merge

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
