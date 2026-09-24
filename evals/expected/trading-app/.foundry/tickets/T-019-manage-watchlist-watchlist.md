---
id: "T-019"
title: "Manage watchlist (watchlist)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006", "T-014"]
jobs: ["manage-watchlist"]
screens: ["watchlist"]
operations: ["watchlist_manage_watchlist"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/markets/manage-watchlist.ts", "apps/api/src/markets/manage-watchlist.test.ts", "apps/web/app/watchlist/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the watchlist screen, When manage watchlist completes, Then the Watchlist state and totals match the domain invariants"
  - "Given a retail-trader role, When manage watchlist is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Watchlist has exactly one state at a time' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-019 — Manage watchlist (watchlist)

## Slice

Vertical slice for job `manage-watchlist`: operations watchlist_manage_watchlist; screens watchlist; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the watchlist screen, When manage watchlist completes, Then the Watchlist state and totals match the domain invariants
2. Given a retail-trader role, When manage watchlist is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Watchlist has exactly one state at a time' is checked, Then it holds

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
