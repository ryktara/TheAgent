---
id: "T-023"
title: "Price alerts (alerts)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006", "T-014"]
jobs: ["price-alerts"]
screens: ["alerts"]
operations: ["alert_price_alerts"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/trading/price-alerts.ts", "apps/api/src/trading/price-alerts.test.ts", "apps/web/app/alerts/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the alerts screen, When price alerts completes, Then the Alert state and totals match the domain invariants"
  - "Given a retail-trader role, When price alerts is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'An Alert fires once per crossing: it re-arms only after the Quote returns across the thres' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-023 — Price alerts (alerts)

## Slice

Vertical slice for job `price-alerts`: operations alert_price_alerts; screens alerts; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the alerts screen, When price alerts completes, Then the Alert state and totals match the domain invariants
2. Given a retail-trader role, When price alerts is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'An Alert fires once per crossing: it re-arms only after the Quote returns across the thres' is checked, Then it holds

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
