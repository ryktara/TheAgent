---
id: "T-029"
title: "Refer friend (should-have)"
type: "feature"
blockedBy: ["T-003", "T-004"]
jobs: ["refer-friend"]
screens: ["referrals"]
operations: ["referral_refer_friend"]
adrs: []
controls: ["SEC-ACC-01", "SEC-LOG-02"]
estimate: "M"
files_likely_touched: ["apps/api/src/growth/refer-friend.ts", "apps/web/app/referrals/page.tsx"]
acceptance_tests:
  - "Given the job is enabled, When refer friend runs, Then its operations respond per openapi.yaml"
  - "Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation"
  - "Given the screen, When it renders in ar, Then axe reports zero serious violations"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-029 — Refer friend (should-have)

## Slice

Should-have slice for `refer-friend`.

## Acceptance tests

1. Given the job is enabled, When refer friend runs, Then its operations respond per openapi.yaml
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
