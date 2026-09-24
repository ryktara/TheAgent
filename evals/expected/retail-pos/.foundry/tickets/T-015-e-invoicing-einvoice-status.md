---
id: "T-015"
title: "E invoicing (einvoice-status)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-007", "T-008"]
jobs: ["e-invoicing"]
screens: ["einvoice-status"]
operations: ["receipt_e_invoicing"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/sales/e-invoicing.ts", "apps/api/src/sales/e-invoicing.test.ts", "apps/web/app/einvoice-status/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the einvoice-status screen, When e invoicing completes, Then the Receipt state and totals match the domain invariants"
  - "Given offline mode, When e invoicing runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Receipt numbers are gapless and increasing per Store; a reprint reuses the number and mark' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-015 — E invoicing (einvoice-status)

## Slice

Vertical slice for job `e-invoicing`: operations receipt_e_invoicing; screens einvoice-status; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the einvoice-status screen, When e invoicing completes, Then the Receipt state and totals match the domain invariants
2. Given offline mode, When e invoicing runs, Then the write lands in the outbox and syncs without duplicates
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
