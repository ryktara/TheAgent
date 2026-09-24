---
id: "T-011"
title: "Handle margin call (margin-call, positions)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006", "T-008"]
jobs: ["handle-margin-call"]
screens: ["margin-call", "positions"]
operations: ["margin_call_handle_margin_call"]
adrs: ["0002"]
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01", "SEC-SESS-07", "SEC-API-01", "SEC-BL-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/trading/handle-margin-call.ts", "apps/api/src/trading/handle-margin-call.test.ts", "apps/web/app/margin-call/page.tsx", "apps/web/app/positions/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the margin-call screen, When handle margin call completes, Then the MarginCall state and totals match the domain invariants"
  - "Given a retail-trader role, When handle margin call is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A MarginCall opens when Account equity < maintenance margin and at most one MarginCall per' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-011 — Handle margin call (margin-call, positions)

## Slice

Vertical slice for job `handle-margin-call`: operations margin_call_handle_margin_call; screens margin-call, positions; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the margin-call screen, When handle margin call completes, Then the MarginCall state and totals match the domain invariants
2. Given a retail-trader role, When handle margin call is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'A MarginCall opens when Account equity < maintenance margin and at most one MarginCall per' is checked, Then it holds

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
