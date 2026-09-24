---
id: "T-016"
title: "Manage promotions (promotions)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-007", "T-008"]
jobs: ["manage-promotions"]
screens: ["promotions"]
operations: ["promotion_manage_promotions"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/sales/manage-promotions.ts", "apps/api/src/sales/manage-promotions.test.ts", "apps/web/app/promotions/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the promotions screen, When manage promotions completes, Then the Promotion state and totals match the domain invariants"
  - "Given offline mode, When manage promotions runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Promotion evaluation is deterministic: best non-stackable Promotion per line by priority, stackable ones applied after' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'Every state change on Sale, Tender, Return, CashDrawerSession, Promotion and StockCount writes one audit log event' is checked, Then it holds"
  - "Given two stackable promotions, When both match, Then priority decides order and the shelf label price equals the charged price"
  - "Given a promotion with ends_at in the past, When a basket is evaluated, Then it does not apply"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-016 — Manage promotions (promotions)

## Slice

Vertical slice for job `manage-promotions`: operations promotion_manage_promotions; screens promotions; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the promotions screen, When manage promotions completes, Then the Promotion state and totals match the domain invariants
2. Given offline mode, When manage promotions runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Promotion evaluation is deterministic: best non-stackable Promotion per line by priority, stackable ones applied after' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'Every state change on Sale, Tender, Return, CashDrawerSession, Promotion and StockCount writes one audit log event' is checked, Then it holds
6. Given two stackable promotions, When both match, Then priority decides order and the shelf label price equals the charged price
7. Given a promotion with ends_at in the past, When a basket is evaluated, Then it does not apply

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
