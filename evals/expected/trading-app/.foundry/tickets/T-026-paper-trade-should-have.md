---
id: "T-026"
title: "Paper trade (should-have)"
type: "feature"
blockedBy: ["T-003", "T-004"]
jobs: ["paper-trade"]
screens: ["order-ticket", "paper-mode"]
operations: ["paper_account_paper_trade"]
adrs: []
controls: ["SEC-ACC-01", "SEC-LOG-02"]
estimate: "M"
files_likely_touched: ["apps/api/src/trading/paper-trade.ts", "apps/web/app/order-ticket/page.tsx", "apps/web/app/paper-mode/page.tsx"]
acceptance_tests:
  - "Given the job is enabled, When paper trade runs, Then its operations respond per openapi.yaml"
  - "Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation"
  - "Given the screen, When it renders in ar, Then axe reports zero serious violations"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-026 — Paper trade (should-have)

## Slice

Should-have slice for `paper-trade`.

## Acceptance tests

1. Given the job is enabled, When paper trade runs, Then its operations respond per openapi.yaml
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
