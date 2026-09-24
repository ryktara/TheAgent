---
id: "T-009"
title: "Take payment (tender)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-007", "T-008"]
jobs: ["take-payment"]
screens: ["tender"]
operations: ["tender_take_payment"]
adrs: ["0002"]
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01", "SEC-SESS-07", "SEC-API-01", "SEC-BL-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/sales/take-payment.ts", "apps/api/src/sales/take-payment.test.ts", "apps/web/app/tender/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the tender screen, When take payment completes, Then the Tender state and totals match the domain invariants"
  - "Given offline mode, When take payment runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A Sale in state paid has captured Tender amounts summing exactly to Sale.total; change is ' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'A Return refunds to the original Tender kind unless the approver Staff id authorises store' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-009 — Take payment (tender)

## Slice

Vertical slice for job `take-payment`: operations tender_take_payment; screens tender; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the tender screen, When take payment completes, Then the Tender state and totals match the domain invariants
2. Given offline mode, When take payment runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'A Sale in state paid has captured Tender amounts summing exactly to Sale.total; change is ' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'A Return refunds to the original Tender kind unless the approver Staff id authorises store' is checked, Then it holds

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
