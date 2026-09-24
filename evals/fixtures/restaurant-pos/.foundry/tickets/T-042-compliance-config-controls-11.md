---
id: "T-042"
title: "Compliance: config controls (11)"
type: "compliance"
blockedBy: ["T-003"]
jobs: []
screens: []
operations: []
adrs: []
controls: ["SEC-CFG-01", "SEC-CFG-02", "SEC-CFG-03", "SEC-CFG-04", "SEC-CFG-06", "SEC-CFG-07", "SEC-CFG-08", "SEC-CFG2-01", "SEC-CFG2-02", "SEC-CFG2-03", "SEC-CFG2-04"]
estimate: "L"
files_likely_touched: ["apps/api/src/security/", "docs/compliance/", ".foundry/compliance.yaml"]
acceptance_tests:
  - "Given control SEC-CFG-01, When its verify method (review) runs, Then evidence is attached in compliance.yaml"
  - "Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link"
  - "Given a regression, When the config tests run in CI, Then a failing control blocks merge"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-042 — Compliance: config controls (11)

## Slice

Implement and evidence 11 config controls: SEC-CFG-01, SEC-CFG-02, SEC-CFG-03, SEC-CFG-04, SEC-CFG-06, SEC-CFG-07, SEC-CFG-08, SEC-CFG2-01, SEC-CFG2-02, SEC-CFG2-03, SEC-CFG2-04

## Acceptance tests

1. Given control SEC-CFG-01, When its verify method (review) runs, Then evidence is attached in compliance.yaml
2. Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link
3. Given a regression, When the config tests run in CI, Then a failing control blocks merge

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
