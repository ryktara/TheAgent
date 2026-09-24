---
id: "T-021"
title: "End of day (end-of-day)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-017", "T-018"]
jobs: ["end-of-day"]
screens: ["end-of-day"]
operations: ["shift_end_of_day"]
adrs: ["0002"]
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01", "SEC-SESS-07", "SEC-API-01", "SEC-BL-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/ordering/end-of-day.ts", "apps/api/src/ordering/end-of-day.test.ts", "apps/web/app/end-of-day/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the end-of-day screen, When end of day completes, Then the Shift state and totals match the domain invariants"
  - "Given offline mode, When end of day runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A Shift closes only when every Order opened on its device is paid, void or transferred' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'Every state change on Order, Payment, Refund, Shift and Discount writes one audit log even' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-021 — End of day (end-of-day)

## Slice

Vertical slice for job `end-of-day`: operations shift_end_of_day; screens end-of-day; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the end-of-day screen, When end of day completes, Then the Shift state and totals match the domain invariants
2. Given offline mode, When end of day runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'A Shift closes only when every Order opened on its device is paid, void or transferred' is checked, Then it holds
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
