---
id: "T-008"
title: "View market data (chart, depth-ladder, instrument-detail)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006"]
jobs: ["view-market-data"]
screens: ["chart", "depth-ladder", "instrument-detail"]
operations: ["instrument_view_market_data"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/markets/view-market-data.ts", "apps/api/src/markets/view-market-data.test.ts", "apps/web/app/chart/page.tsx", "apps/web/app/depth-ladder/page.tsx", "apps/web/app/instrument-detail/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the chart screen, When view market data completes, Then the Instrument state and totals match the domain invariants"
  - "Given a cashier role, When view market data is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Position.qty == sum of signed Fill.qty for its Account and Instrument; Position is never w' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'Order leverage <= min(Instrument.max_leverage, RiskLimit.max_leverage for the Account juri' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-008 — View market data (chart, depth-ladder, instrument-detail)

## Slice

Vertical slice for job `view-market-data`: operations instrument_view_market_data; screens chart, depth-ladder, instrument-detail; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the chart screen, When view market data completes, Then the Instrument state and totals match the domain invariants
2. Given a cashier role, When view market data is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Position.qty == sum of signed Fill.qty for its Account and Instrument; Position is never w' is checked, Then it holds
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
