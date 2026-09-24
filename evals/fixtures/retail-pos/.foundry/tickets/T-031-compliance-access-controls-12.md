---
id: "T-031"
title: "Compliance: access controls (12)"
type: "compliance"
blockedBy: ["T-003"]
jobs: []
screens: []
operations: []
adrs: []
controls: ["SEC-ACC-03", "SEC-ACC-04", "SEC-ACC-06", "SEC-ACC-07", "SEC-ACC-09", "SEC-ACC-10", "SEC-ACC2-01", "SEC-ACC2-02", "SEC-ACC2-03", "SEC-ACC2-04", "SEC-ACC2-05", "SEC-ACC2-06"]
estimate: "L"
files_likely_touched: ["apps/api/src/security/", "docs/compliance/", ".foundry/compliance.yaml"]
acceptance_tests:
  - "Given control SEC-ACC-03, When its verify method (test) runs, Then evidence is attached in compliance.yaml"
  - "Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link"
  - "Given a regression, When the access tests run in CI, Then a failing control blocks merge"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-031 — Compliance: access controls (12)

## Slice

Implement and evidence 12 access controls: SEC-ACC-03, SEC-ACC-04, SEC-ACC-06, SEC-ACC-07, SEC-ACC-09, SEC-ACC-10, SEC-ACC2-01, SEC-ACC2-02, SEC-ACC2-03, SEC-ACC2-04, SEC-ACC2-05, SEC-ACC2-06

## Acceptance tests

1. Given control SEC-ACC-03, When its verify method (test) runs, Then evidence is attached in compliance.yaml
2. Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link
3. Given a regression, When the access tests run in CI, Then a failing control blocks merge

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
