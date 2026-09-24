---
id: "T-020"
title: "Open close shift (shift-close, shift-open)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-017", "T-018"]
jobs: ["open-close-shift"]
screens: ["shift-close", "shift-open"]
operations: ["shift_open_close_shift"]
adrs: ["0002"]
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01", "SEC-SESS-07", "SEC-API-01", "SEC-BL-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/ordering/open-close-shift.ts", "apps/api/src/ordering/open-close-shift.test.ts", "apps/web/app/shift-close/page.tsx", "apps/web/app/shift-open/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the shift-close screen, When open close shift completes, Then the Shift state and totals match the domain invariants"
  - "Given offline mode, When open close shift runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A Shift closes only when every Order opened on its device is paid, void or transferred' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'Every state change on Order, Payment, Refund, Shift and Discount writes one audit log even' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-020 — Open close shift (shift-close, shift-open)

## Slice

Vertical slice for job `open-close-shift`: operations shift_open_close_shift; screens shift-close, shift-open; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the shift-close screen, When open close shift completes, Then the Shift state and totals match the domain invariants
2. Given offline mode, When open close shift runs, Then the write lands in the outbox and syncs without duplicates
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
