---
id: "T-028"
title: "Copy trade (should-have)"
type: "feature"
blockedBy: ["T-003", "T-004"]
jobs: ["copy-trade"]
screens: ["copy-leaders", "copy-settings"]
operations: ["copy_link_copy_trade"]
adrs: []
controls: ["SEC-ACC-01", "SEC-LOG-02"]
estimate: "M"
files_likely_touched: ["apps/api/src/growth/copy-trade.ts", "apps/web/app/copy-leaders/page.tsx", "apps/web/app/copy-settings/page.tsx"]
acceptance_tests:
  - "Given the job is enabled, When copy trade runs, Then its operations respond per openapi.yaml"
  - "Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation"
  - "Given the screen, When it renders in ar, Then axe reports zero serious violations"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-028 — Copy trade (should-have)

## Slice

Should-have slice for `copy-trade`.

## Acceptance tests

1. Given the job is enabled, When copy trade runs, Then its operations respond per openapi.yaml
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
