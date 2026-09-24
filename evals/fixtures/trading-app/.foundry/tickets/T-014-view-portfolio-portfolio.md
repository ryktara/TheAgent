---
id: "T-014"
title: "View portfolio (portfolio)"
type: "feature"
blockedBy: ["T-003", "T-004"]
jobs: ["view-portfolio"]
screens: ["portfolio"]
operations: ["account_view_portfolio"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/accounts/view-portfolio.ts", "apps/api/src/accounts/view-portfolio.test.ts", "apps/web/app/portfolio/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the portfolio screen, When view portfolio completes, Then the Account state and totals match the domain invariants"
  - "Given a cashier role, When view portfolio is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Position.qty == sum of signed Fill.qty for its Account and Instrument; Position is never w' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'A withdrawal Transfer is paid only to a beneficiary in the name of the Account owner' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-014 — View portfolio (portfolio)

## Slice

Vertical slice for job `view-portfolio`: operations account_view_portfolio; screens portfolio; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the portfolio screen, When view portfolio completes, Then the Account state and totals match the domain invariants
2. Given a cashier role, When view portfolio is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Position.qty == sum of signed Fill.qty for its Account and Instrument; Position is never w' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'A withdrawal Transfer is paid only to a beneficiary in the name of the Account owner' is checked, Then it holds

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
