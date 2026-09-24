---
id: "T-027"
title: "Multi store (should-have)"
type: "feature"
blockedBy: ["T-005", "T-004"]
jobs: ["multi-store"]
screens: ["store-switcher"]
operations: ["store_multi_store"]
adrs: []
controls: ["SEC-ACC-01", "SEC-LOG-02"]
estimate: "M"
files_likely_touched: ["apps/api/src/people/multi-store.ts", "apps/web/app/store-switcher/page.tsx"]
acceptance_tests:
  - "Given the job is enabled, When multi store runs, Then its operations respond per openapi.yaml"
  - "Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation"
  - "Given the screen, When it renders in ar, Then axe reports zero serious violations"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-027 — Multi store (should-have)

## Slice

Should-have slice for `multi-store`.

## Acceptance tests

1. Given the job is enabled, When multi store runs, Then its operations respond per openapi.yaml
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
