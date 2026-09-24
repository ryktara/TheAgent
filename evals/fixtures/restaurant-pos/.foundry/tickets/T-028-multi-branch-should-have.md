---
id: "T-028"
title: "Multi branch (should-have)"
type: "feature"
blockedBy: ["T-005", "T-004"]
jobs: ["multi-branch"]
screens: ["branch-switcher", "menu-management"]
operations: ["branch_multi_branch"]
adrs: []
controls: ["SEC-ACC-01", "SEC-LOG-02"]
estimate: "M"
files_likely_touched: ["apps/api/src/people/multi-branch.ts", "apps/web/app/branch-switcher/page.tsx", "apps/web/app/menu-management/page.tsx"]
acceptance_tests:
  - "Given the job is enabled, When multi branch runs, Then its operations respond per openapi.yaml"
  - "Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation"
  - "Given the screen, When it renders in ar, Then axe reports zero serious violations"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-028 — Multi branch (should-have)

## Slice

Should-have slice for `multi-branch`.

## Acceptance tests

1. Given the job is enabled, When multi branch runs, Then its operations respond per openapi.yaml
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
