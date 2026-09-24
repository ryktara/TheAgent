---
id: "T-009"
title: "View positions (positions)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006", "T-008"]
jobs: ["view-positions"]
screens: ["positions"]
operations: ["position_view_positions"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/trading/view-positions.ts", "apps/api/src/trading/view-positions.test.ts", "apps/web/app/positions/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the positions screen, When view positions completes, Then the Position state and totals match the domain invariants"
  - "Given a retail-trader role, When view positions is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Position.qty == sum of signed Fill.qty for its Account and Instrument; Position is never w' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-009 — View positions (positions)

## Slice

Vertical slice for job `view-positions`: operations position_view_positions; screens positions; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the positions screen, When view positions completes, Then the Position state and totals match the domain invariants
2. Given a retail-trader role, When view positions is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Position.qty == sum of signed Fill.qty for its Account and Instrument; Position is never w' is checked, Then it holds

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
