---
id: "T-007"
title: "Manage catalog (product-catalog)"
type: "feature"
blockedBy: ["T-005", "T-004"]
jobs: ["manage-catalog"]
screens: ["product-catalog"]
operations: ["product_manage_catalog"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/catalog/manage-catalog.ts", "apps/api/src/catalog/manage-catalog.test.ts", "apps/web/app/product-catalog/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the product-catalog screen, When manage catalog completes, Then the Product state and totals match the domain invariants"
  - "Given offline mode, When manage catalog runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A Product in state discontinued or a Variant out-of-stock with no allow_negative cannot be added to a new SaleLine' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-007 — Manage catalog (product-catalog)

## Slice

Vertical slice for job `manage-catalog`: operations product_manage_catalog; screens product-catalog; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the product-catalog screen, When manage catalog completes, Then the Product state and totals match the domain invariants
2. Given offline mode, When manage catalog runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'A Product in state discontinued or a Variant out-of-stock with no allow_negative cannot be added to a new SaleLine' is checked, Then it holds

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
