---
id: "T-039"
title: "Compliance: auth controls (10)"
type: "compliance"
blockedBy: ["T-003"]
jobs: []
screens: []
operations: []
adrs: []
controls: ["SEC-AUTH-01", "SEC-AUTH-02", "SEC-AUTH-03", "SEC-AUTH-04", "SEC-AUTH-07", "SEC-AUTH-08", "SEC-AUTH-09", "SEC-AUTH-12", "SEC-AUTH-13", "SEC-AUTH-14"]
estimate: "L"
files_likely_touched: ["apps/api/src/security/", "docs/compliance/", ".foundry/compliance.yaml"]
acceptance_tests:
  - "Given control SEC-AUTH-01, When its verify method (test) runs, Then evidence is attached in compliance.yaml"
  - "Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link"
  - "Given a regression, When the auth tests run in CI, Then a failing control blocks merge"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-039 — Compliance: auth controls (10)

## Slice

Implement and evidence 10 auth controls: SEC-AUTH-01, SEC-AUTH-02, SEC-AUTH-03, SEC-AUTH-04, SEC-AUTH-07, SEC-AUTH-08, SEC-AUTH-09, SEC-AUTH-12, SEC-AUTH-13, SEC-AUTH-14

## Acceptance tests

1. Given control SEC-AUTH-01, When its verify method (test) runs, Then evidence is attached in compliance.yaml
2. Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link
3. Given a regression, When the auth tests run in CI, Then a failing control blocks merge

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
