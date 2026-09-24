---
id: "T-022"
title: "Inventory basic (inventory, recipe-editor)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006", "T-007"]
jobs: ["inventory-basic"]
screens: ["inventory", "recipe-editor"]
operations: ["inventory_item_inventory_basic"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/inventory/inventory-basic.ts", "apps/api/src/inventory/inventory-basic.test.ts", "apps/web/app/inventory/page.tsx", "apps/web/app/recipe-editor/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the inventory screen, When inventory basic completes, Then the InventoryItem state and totals match the domain invariants"
  - "Given a cashier role, When inventory basic is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'InventoryItem.on_hand == sum(StockMovement.qty) for that item since the last count' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-022 — Inventory basic (inventory, recipe-editor)

## Slice

Vertical slice for job `inventory-basic`: operations inventory_item_inventory_basic; screens inventory, recipe-editor; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the inventory screen, When inventory basic completes, Then the InventoryItem state and totals match the domain invariants
2. Given a cashier role, When inventory basic is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'InventoryItem.on_hand == sum(StockMovement.qty) for that item since the last count' is checked, Then it holds

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
