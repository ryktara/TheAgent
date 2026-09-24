---
id: "T-036"
title: "Compliance: api controls (13)"
type: "compliance"
blockedBy: ["T-003"]
jobs: []
screens: []
operations: []
adrs: []
controls: ["SEC-API-02", "SEC-API-03", "SEC-API-07", "SEC-API-09", "SEC-API-10", "SEC-API-12", "SEC-API-13", "SEC-FIS-03", "SEC-FIS-04", "SEC-API2-02", "SEC-API2-03", "SEC-API2-04", "SEC-API2-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/security/", "docs/compliance/", ".foundry/compliance.yaml"]
acceptance_tests:
  - "Given control SEC-API-02, When its verify method (test) runs, Then evidence is attached in compliance.yaml"
  - "Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link"
  - "Given a regression, When the api tests run in CI, Then a failing control blocks merge"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-036 — Compliance: api controls (13)

## Slice

Implement and evidence 13 api controls: SEC-API-02, SEC-API-03, SEC-API-07, SEC-API-09, SEC-API-10, SEC-API-12, SEC-API-13, SEC-FIS-03, SEC-FIS-04, SEC-API2-02, SEC-API2-03, SEC-API2-04…

## Acceptance tests

1. Given control SEC-API-02, When its verify method (test) runs, Then evidence is attached in compliance.yaml
2. Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link
3. Given a regression, When the api tests run in CI, Then a failing control blocks merge

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
