---
id: "T-028"
title: "Layaway (should-have)"
type: "feature"
blockedBy: ["T-005", "T-004"]
jobs: ["layaway"]
screens: ["layaway"]
operations: ["layaway_layaway"]
adrs: []
controls: ["SEC-ACC-01", "SEC-LOG-02"]
estimate: "M"
files_likely_touched: ["apps/api/src/customers/layaway.ts", "apps/web/app/layaway/page.tsx"]
acceptance_tests:
  - "Given the job is enabled, When layaway runs, Then its operations respond per openapi.yaml"
  - "Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation"
  - "Given the screen, When it renders in ar, Then axe reports zero serious violations"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-028 — Layaway (should-have)

## Slice

Should-have slice for `layaway`.

## Acceptance tests

1. Given the job is enabled, When layaway runs, Then its operations respond per openapi.yaml
2. Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation
3. Given the screen, When it renders in ar, Then axe reports zero serious violations

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
