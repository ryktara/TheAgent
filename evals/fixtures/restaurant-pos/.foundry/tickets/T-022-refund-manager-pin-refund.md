---
id: "T-022"
title: "Refund (manager-pin, refund)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-017", "T-018"]
jobs: ["refund"]
screens: ["manager-pin", "refund"]
operations: ["refund_refund"]
adrs: ["0002"]
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01", "SEC-SESS-07", "SEC-API-01", "SEC-BL-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/payments/refund.ts", "apps/api/src/payments/refund.test.ts", "apps/web/app/manager-pin/page.tsx", "apps/web/app/refund/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the manager-pin screen, When refund completes, Then the Refund state and totals match the domain invariants"
  - "Given a cashier role, When refund is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A Refund never exceeds the captured amount of its Payment minus prior Refunds' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'Every state change on Order, Payment, Refund, Shift and Discount writes one audit log even' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-022 — Refund (manager-pin, refund)

## Slice

Vertical slice for job `refund`: operations refund_refund; screens manager-pin, refund; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the manager-pin screen, When refund completes, Then the Refund state and totals match the domain invariants
2. Given a cashier role, When refund is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'A Refund never exceeds the captured amount of its Payment minus prior Refunds' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'Every state change on Order, Payment, Refund, Shift and Discount writes one audit log even' is checked, Then it holds

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
