---
id: "T-025"
title: "Set leverage (should-have)"
type: "feature"
blockedBy: ["T-017", "T-004"]
jobs: ["set-leverage"]
screens: ["leverage-settings", "risk-warning"]
operations: ["risk_limit_set_leverage"]
adrs: []
controls: ["SEC-ACC-01", "SEC-LOG-02"]
estimate: "M"
files_likely_touched: ["apps/api/src/trading/set-leverage.ts", "apps/web/app/leverage-settings/page.tsx", "apps/web/app/risk-warning/page.tsx"]
acceptance_tests:
  - "Given the job is enabled, When set leverage runs, Then its operations respond per openapi.yaml"
  - "Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation"
  - "Given the screen, When it renders in ar, Then axe reports zero serious violations"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-025 — Set leverage (should-have)

## Slice

Should-have slice for `set-leverage`.

## Acceptance tests

1. Given the job is enabled, When set leverage runs, Then its operations respond per openapi.yaml
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
