---
id: "T-010"
title: "Issue receipt (receipt-preview)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-007", "T-008"]
jobs: ["issue-receipt"]
screens: ["receipt-preview"]
operations: ["receipt_issue_receipt"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/sales/issue-receipt.ts", "apps/api/src/sales/issue-receipt.test.ts", "apps/web/app/receipt-preview/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the receipt-preview screen, When issue receipt completes, Then the Receipt state and totals match the domain invariants"
  - "Given offline mode, When issue receipt runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Receipt numbers are gapless and increasing per Store; a reprint reuses the number and mark' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-010 — Issue receipt (receipt-preview)

## Slice

Vertical slice for job `issue-receipt`: operations receipt_issue_receipt; screens receipt-preview; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the receipt-preview screen, When issue receipt completes, Then the Receipt state and totals match the domain invariants
2. Given offline mode, When issue receipt runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Receipt numbers are gapless and increasing per Store; a reprint reuses the number and mark' is checked, Then it holds

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
