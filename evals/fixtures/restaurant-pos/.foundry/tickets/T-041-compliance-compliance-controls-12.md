---
id: "T-041"
title: "Compliance: compliance controls (12)"
type: "compliance"
blockedBy: ["T-003"]
jobs: []
screens: []
operations: []
adrs: []
controls: ["C-AE-01", "C-AE-02", "C-AE-03", "C-AE-04", "C-ALL-01", "C-ALL-02", "C-ALL-03", "C-ALL-04", "C-ALL-05", "C-ALL-06", "C-ALL-07", "C-ALL-08"]
estimate: "L"
files_likely_touched: ["apps/api/src/security/", "docs/compliance/", ".foundry/compliance.yaml"]
acceptance_tests:
  - "Given control C-AE-01, When its verify method (review) runs, Then evidence is attached in compliance.yaml"
  - "Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link"
  - "Given a regression, When the compliance tests run in CI, Then a failing control blocks merge"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-041 — Compliance: compliance controls (12)

## Slice

Implement and evidence 12 compliance controls: C-AE-01, C-AE-02, C-AE-03, C-AE-04, C-ALL-01, C-ALL-02, C-ALL-03, C-ALL-04, C-ALL-05, C-ALL-06, C-ALL-07, C-ALL-08

## Acceptance tests

1. Given control C-AE-01, When its verify method (review) runs, Then evidence is attached in compliance.yaml
2. Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link
3. Given a regression, When the compliance tests run in CI, Then a failing control blocks merge

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
