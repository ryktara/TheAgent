---
id: "T-041"
title: "Compliance: crypto controls (8)"
type: "compliance"
blockedBy: ["T-003"]
jobs: []
screens: []
operations: []
adrs: []
controls: ["SEC-CRY-01", "SEC-CRY-02", "SEC-CRY-03", "SEC-CRY-04", "SEC-CRY2-01", "SEC-CRY2-02", "SEC-CRY2-04", "SEC-CRY2-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/security/", "docs/compliance/", ".foundry/compliance.yaml"]
acceptance_tests:
  - "Given control SEC-CRY-01, When its verify method (scan) runs, Then evidence is attached in compliance.yaml"
  - "Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link"
  - "Given a regression, When the crypto tests run in CI, Then a failing control blocks merge"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-041 — Compliance: crypto controls (8)

## Slice

Implement and evidence 8 crypto controls: SEC-CRY-01, SEC-CRY-02, SEC-CRY-03, SEC-CRY-04, SEC-CRY2-01, SEC-CRY2-02, SEC-CRY2-04, SEC-CRY2-05

## Acceptance tests

1. Given control SEC-CRY-01, When its verify method (scan) runs, Then evidence is attached in compliance.yaml
2. Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link
3. Given a regression, When the crypto tests run in CI, Then a failing control blocks merge

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
