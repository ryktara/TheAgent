---
id: "T-027"
title: "Take order qr (should-have)"
type: "feature"
blockedBy: ["T-006", "T-004"]
jobs: ["take-order-qr"]
screens: ["qr-self-order"]
operations: ["order_take_order_qr"]
adrs: []
controls: ["SEC-ACC-01", "SEC-LOG-02"]
estimate: "M"
files_likely_touched: ["apps/api/src/ordering/take-order-qr.ts", "apps/web/app/qr-self-order/page.tsx"]
acceptance_tests:
  - "Given the job is enabled, When take order qr runs, Then its operations respond per openapi.yaml"
  - "Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation"
  - "Given the screen, When it renders in ar, Then axe reports zero serious violations"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-027 — Take order qr (should-have)

## Slice

Should-have slice for `take-order-qr`.

## Acceptance tests

1. Given the job is enabled, When take order qr runs, Then its operations respond per openapi.yaml
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
