---
id: "T-013"
title: "Return exchange (manager-pin, receipt-lookup, returns)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-007", "T-008"]
jobs: ["return-exchange"]
screens: ["manager-pin", "receipt-lookup", "returns"]
operations: ["return_return_exchange"]
adrs: ["0002"]
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01", "SEC-SESS-07", "SEC-API-01", "SEC-BL-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/sales/return-exchange.ts", "apps/api/src/sales/return-exchange.test.ts", "apps/web/app/manager-pin/page.tsx", "apps/web/app/receipt-lookup/page.tsx", "apps/web/app/returns/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the manager-pin screen, When return exchange completes, Then the Return state and totals match the domain invariants"
  - "Given offline mode, When return exchange runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Returned qty per SaleLine never exceeds sold qty minus prior Return qty on that SaleLine' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'A Return refunds to the original Tender kind unless the approver Staff id authorises store credit on a GiftCard' is checked, Then it holds"
  - "Given a SaleLine sold qty 2 with 1 already returned, When 2 are returned, Then the return is blocked (returned qty never exceeds sold minus prior returns)"
  - "Given a return on day 8, When submitted, Then manager PIN is required (7-day window, C-SA-03)"
  - "Given a refund of a card sale, When approved, Then the refund goes to the original tender, includes VAT, loyalty points earned are reversed and a credit note is queued for ZATCA"
  - "Given an exchange of size M for size L, When completed, Then a StockMovement return for M and sale for L are written and the difference is paid or refunded"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-013 — Return exchange (manager-pin, receipt-lookup, returns)

## Slice

Vertical slice for job `return-exchange`: operations return_return_exchange; screens manager-pin, receipt-lookup, returns; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the manager-pin screen, When return exchange completes, Then the Return state and totals match the domain invariants
2. Given offline mode, When return exchange runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Returned qty per SaleLine never exceeds sold qty minus prior Return qty on that SaleLine' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'A Return refunds to the original Tender kind unless the approver Staff id authorises store credit on a GiftCard' is checked, Then it holds
6. Given a SaleLine sold qty 2 with 1 already returned, When 2 are returned, Then the return is blocked (returned qty never exceeds sold minus prior returns)
7. Given a return on day 8, When submitted, Then manager PIN is required (7-day window, C-SA-03)
8. Given a refund of a card sale, When approved, Then the refund goes to the original tender, includes VAT, loyalty points earned are reversed and a credit note is queued for ZATCA
9. Given an exchange of size M for size L, When completed, Then a StockMovement return for M and sale for L are written and the difference is paid or refunded

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
