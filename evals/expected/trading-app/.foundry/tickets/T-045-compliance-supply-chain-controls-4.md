---
id: "T-045"
title: "Compliance: supply-chain controls (4)"
type: "compliance"
blockedBy: ["T-003"]
jobs: []
screens: []
operations: []
adrs: []
controls: ["SEC-SC-02", "SEC-SC-03", "SEC-SC-04", "SEC-SC-05"]
estimate: "M"
files_likely_touched: ["apps/api/src/security/", "docs/compliance/", ".foundry/compliance.yaml"]
acceptance_tests:
  - "Given control SEC-SC-02, When its verify method (review) runs, Then evidence is attached in compliance.yaml"
  - "Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link"
  - "Given a regression, When the supply-chain tests run in CI, Then a failing control blocks merge"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-045 — Compliance: supply-chain controls (4)

## Slice

Implement and evidence 4 supply-chain controls: SEC-SC-02, SEC-SC-03, SEC-SC-04, SEC-SC-05

## Acceptance tests

1. Given control SEC-SC-02, When its verify method (review) runs, Then evidence is attached in compliance.yaml
2. Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link
3. Given a regression, When the supply-chain tests run in CI, Then a failing control blocks merge

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
