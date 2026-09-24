---
id: "T-014"
title: "Cash management (cash-management, z-report)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-007", "T-008"]
jobs: ["cash-management"]
screens: ["cash-management", "z-report"]
operations: ["cash_drawer_session_cash_management"]
adrs: ["0002"]
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01", "SEC-SESS-07", "SEC-API-01", "SEC-BL-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/sales/cash-management.ts", "apps/api/src/sales/cash-management.test.ts", "apps/web/app/cash-management/page.tsx", "apps/web/app/z-report/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the cash-management screen, When cash management completes, Then the CashDrawerSession state and totals match the domain invariants"
  - "Given offline mode, When cash management runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A CashDrawerSession closes with expected == opening_float + cash Tender - cash refunds - p' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'Every state change on Sale, Tender, Return, CashDrawerSession, Promotion and StockCount wr' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-014 — Cash management (cash-management, z-report)

## Slice

Vertical slice for job `cash-management`: operations cash_drawer_session_cash_management; screens cash-management, z-report; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the cash-management screen, When cash management completes, Then the CashDrawerSession state and totals match the domain invariants
2. Given offline mode, When cash management runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'A CashDrawerSession closes with expected == opening_float + cash Tender - cash refunds - p' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'Every state change on Sale, Tender, Return, CashDrawerSession, Promotion and StockCount wr' is checked, Then it holds

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
