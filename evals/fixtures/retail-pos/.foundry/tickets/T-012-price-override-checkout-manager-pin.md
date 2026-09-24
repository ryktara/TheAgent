---
id: "T-012"
title: "Price override (checkout, manager-pin)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-007", "T-008"]
jobs: ["price-override"]
screens: ["checkout", "manager-pin"]
operations: ["sale_line_price_override"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/sales/price-override.ts", "apps/api/src/sales/price-override.test.ts", "apps/web/app/checkout/page.tsx", "apps/web/app/manager-pin/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the checkout screen, When price override completes, Then the SaleLine state and totals match the domain invariants"
  - "Given offline mode, When price override runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Sale.total == sum(SaleLine.line_total) - Sale.discount_total + Sale.tax_total, computed once in minor units at tender' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'Returned qty per SaleLine never exceeds sold qty minus prior Return qty on that SaleLine' is checked, Then it holds"
  - "Given a price override above the manager's override_limit_pct, When submitted, Then it is refused with Needs owner"
  - "Given an override, When saved, Then SaleLine.override_by holds the approver Staff id and an audit event is written"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-012 — Price override (checkout, manager-pin)

## Slice

Vertical slice for job `price-override`: operations sale_line_price_override; screens checkout, manager-pin; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the checkout screen, When price override completes, Then the SaleLine state and totals match the domain invariants
2. Given offline mode, When price override runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Sale.total == sum(SaleLine.line_total) - Sale.discount_total + Sale.tax_total, computed once in minor units at tender' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'Returned qty per SaleLine never exceeds sold qty minus prior Return qty on that SaleLine' is checked, Then it holds
6. Given a price override above the manager's override_limit_pct, When submitted, Then it is refused with Needs owner
7. Given an override, When saved, Then SaleLine.override_by holds the approver Staff id and an audit event is written

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
