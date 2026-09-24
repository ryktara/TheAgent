---
id: "T-046"
title: "Compliance: session controls (10)"
type: "compliance"
blockedBy: ["T-003"]
jobs: []
screens: []
operations: []
adrs: []
controls: ["SEC-SESS-02", "SEC-SESS-03", "SEC-SESS-04", "SEC-SESS-05", "SEC-SESS-06", "SEC-SESS-08", "SEC-SESS2-01", "SEC-SESS2-02", "SEC-SESS2-03", "SEC-SESS2-04"]
estimate: "L"
files_likely_touched: ["apps/api/src/security/", "docs/compliance/", ".foundry/compliance.yaml"]
acceptance_tests:
  - "Given control SEC-SESS-02, When its verify method (test) runs, Then evidence is attached in compliance.yaml"
  - "Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link"
  - "Given a regression, When the session tests run in CI, Then a failing control blocks merge"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-046 — Compliance: session controls (10)

## Slice

Implement and evidence 10 session controls: SEC-SESS-02, SEC-SESS-03, SEC-SESS-04, SEC-SESS-05, SEC-SESS-06, SEC-SESS-08, SEC-SESS2-01, SEC-SESS2-02, SEC-SESS2-03, SEC-SESS2-04

## Acceptance tests

1. Given control SEC-SESS-02, When its verify method (test) runs, Then evidence is attached in compliance.yaml
2. Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link
3. Given a regression, When the session tests run in CI, Then a failing control blocks merge

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
