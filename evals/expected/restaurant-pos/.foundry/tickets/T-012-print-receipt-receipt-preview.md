---
id: "T-012"
title: "Print receipt (receipt-preview)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-006", "T-007"]
jobs: ["print-receipt"]
screens: ["receipt-preview"]
operations: ["receipt_print_receipt"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/payments/print-receipt.ts", "apps/api/src/payments/print-receipt.test.ts", "apps/web/app/receipt-preview/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the receipt-preview screen, When print receipt completes, Then the Receipt state and totals match the domain invariants"
  - "Given a cashier role, When print receipt is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Receipt numbers are gapless and increasing per Branch; a reprint reuses the number and mar' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'Receipt.language is one of the Branch receipt languages and defaults to the Customer prefe' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-012 — Print receipt (receipt-preview)

## Slice

Vertical slice for job `print-receipt`: operations receipt_print_receipt; screens receipt-preview; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the receipt-preview screen, When print receipt completes, Then the Receipt state and totals match the domain invariants
2. Given a cashier role, When print receipt is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Receipt numbers are gapless and increasing per Branch; a reprint reuses the number and mar' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'Receipt.language is one of the Branch receipt languages and defaults to the Customer prefe' is checked, Then it holds

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
