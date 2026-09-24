---
id: "T-032"
title: "Compliance: agentic controls (12)"
type: "compliance"
blockedBy: ["T-003"]
jobs: []
screens: []
operations: []
adrs: []
controls: ["SEC-AGT-01", "SEC-AGT-02", "SEC-AGT-03", "SEC-AGT-04", "SEC-AGT-05", "SEC-AGT-06", "SEC-AGT-07", "SEC-AGT-08", "SEC-AGT-09", "SEC-AGT-10", "SEC-AGT-11", "SEC-AGT-12"]
estimate: "L"
files_likely_touched: ["apps/api/src/security/", "docs/compliance/", ".foundry/compliance.yaml"]
acceptance_tests:
  - "Given control SEC-AGT-01, When its verify method (review) runs, Then evidence is attached in compliance.yaml"
  - "Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link"
  - "Given a regression, When the agentic tests run in CI, Then a failing control blocks merge"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-032 — Compliance: agentic controls (12)

## Slice

Implement and evidence 12 agentic controls: SEC-AGT-01, SEC-AGT-02, SEC-AGT-03, SEC-AGT-04, SEC-AGT-05, SEC-AGT-06, SEC-AGT-07, SEC-AGT-08, SEC-AGT-09, SEC-AGT-10, SEC-AGT-11, SEC-AGT-12

## Acceptance tests

1. Given control SEC-AGT-01, When its verify method (review) runs, Then evidence is attached in compliance.yaml
2. Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link
3. Given a regression, When the agentic tests run in CI, Then a failing control blocks merge

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
