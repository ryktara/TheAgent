---
id: "T-019"
title: "Print labels (labels)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-007"]
jobs: ["print-labels"]
screens: ["labels"]
operations: ["barcode_print_labels"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/catalog/print-labels.ts", "apps/api/src/catalog/print-labels.test.ts", "apps/web/app/labels/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the labels screen, When print labels completes, Then the Barcode state and totals match the domain invariants"
  - "Given offline mode, When print labels runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A weighed SaleLine takes weight_g from the scale or an embedded Barcode; price == unit_pri' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-019 — Print labels (labels)

## Slice

Vertical slice for job `print-labels`: operations barcode_print_labels; screens labels; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the labels screen, When print labels completes, Then the Barcode state and totals match the domain invariants
2. Given offline mode, When print labels runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'A weighed SaleLine takes weight_g from the scale or an embedded Barcode; price == unit_pri' is checked, Then it holds

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
