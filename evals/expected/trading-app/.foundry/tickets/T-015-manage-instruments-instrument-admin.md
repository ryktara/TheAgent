---
id: "T-015"
title: "Manage instruments (instrument-admin)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006", "T-014"]
jobs: ["manage-instruments"]
screens: ["instrument-admin"]
operations: ["instrument_manage_instruments"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/markets/manage-instruments.ts", "apps/api/src/markets/manage-instruments.test.ts", "apps/web/app/instrument-admin/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the instrument-admin screen, When manage instruments completes, Then the Instrument state and totals match the domain invariants"
  - "Given a retail-trader role, When manage instruments is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Position.qty == sum of signed Fill.qty for its Account and Instrument; Position is never w' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'Order leverage <= min(Instrument.max_leverage, RiskLimit.max_leverage for the Account juri' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-015 — Manage instruments (instrument-admin)

## Slice

Vertical slice for job `manage-instruments`: operations instrument_manage_instruments; screens instrument-admin; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the instrument-admin screen, When manage instruments completes, Then the Instrument state and totals match the domain invariants
2. Given a retail-trader role, When manage instruments is attempted without permission, Then the api returns 403 and logs authz.denied
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
