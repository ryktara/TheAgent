---
id: "T-017"
title: "Manage risk limits (risk-limits)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006", "T-014"]
jobs: ["manage-risk-limits"]
screens: ["risk-limits"]
operations: ["risk_limit_manage_risk_limits"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/trading/manage-risk-limits.ts", "apps/api/src/trading/manage-risk-limits.test.ts", "apps/web/app/risk-limits/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the risk-limits screen, When manage risk limits completes, Then the RiskLimit state and totals match the domain invariants"
  - "Given a retail-trader role, When manage risk limits is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'No Order moves to accepted without a passed buying-power or margin check against RiskLimit' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'Order leverage <= min(Instrument.max_leverage, RiskLimit.max_leverage for the Account juri' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-017 — Manage risk limits (risk-limits)

## Slice

Vertical slice for job `manage-risk-limits`: operations risk_limit_manage_risk_limits; screens risk-limits; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the risk-limits screen, When manage risk limits completes, Then the RiskLimit state and totals match the domain invariants
2. Given a retail-trader role, When manage risk limits is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'No Order moves to accepted without a passed buying-power or margin check against RiskLimit' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'Order leverage <= min(Instrument.max_leverage, RiskLimit.max_leverage for the Account juri' is checked, Then it holds

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
