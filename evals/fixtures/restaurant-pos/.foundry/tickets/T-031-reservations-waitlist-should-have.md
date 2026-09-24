---
id: "T-031"
title: "Reservations waitlist (should-have)"
type: "feature"
blockedBy: ["T-005", "T-004"]
jobs: ["reservations-waitlist"]
screens: ["reservations"]
operations: ["reservation_reservations_waitlist"]
adrs: []
controls: ["SEC-ACC-01", "SEC-LOG-02"]
estimate: "M"
files_likely_touched: ["apps/api/src/ordering/reservations-waitlist.ts", "apps/web/app/reservations/page.tsx"]
acceptance_tests:
  - "Given the job is enabled, When reservations waitlist runs, Then its operations respond per openapi.yaml"
  - "Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation"
  - "Given the screen, When it renders in ar, Then axe reports zero serious violations"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-031 — Reservations waitlist (should-have)

## Slice

Should-have slice for `reservations-waitlist`.

## Acceptance tests

1. Given the job is enabled, When reservations waitlist runs, Then its operations respond per openapi.yaml
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
