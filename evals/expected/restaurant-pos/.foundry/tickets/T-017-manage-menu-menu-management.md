---
id: "T-017"
title: "Manage menu (menu-management)"
type: "feature"
blockedBy: ["T-005", "T-004", "T-006", "T-007"]
jobs: ["manage-menu"]
screens: ["menu-management"]
operations: ["menu_item_manage_menu"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/menu/manage-menu.ts", "apps/api/src/menu/manage-menu.test.ts", "apps/web/app/menu-management/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the menu-management screen, When manage menu completes, Then the MenuItem state and totals match the domain invariants"
  - "Given offline mode, When manage menu runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'StockMovement of kind sale is written once per served OrderLine using the Recipe of its Me' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'MenuItem in state sold-out cannot be added to a new OrderLine on any channel' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-017 — Manage menu (menu-management)

## Slice

Vertical slice for job `manage-menu`: operations menu_item_manage_menu; screens menu-management; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the menu-management screen, When manage menu completes, Then the MenuItem state and totals match the domain invariants
2. Given offline mode, When manage menu runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'StockMovement of kind sale is written once per served OrderLine using the Recipe of its Me' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'MenuItem in state sold-out cannot be added to a new OrderLine on any channel' is checked, Then it holds

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
