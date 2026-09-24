---
id: "T-017"
title: "Receive goods (goods-receipt)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-007", "T-008"]
jobs: ["receive-goods"]
screens: ["goods-receipt"]
operations: ["goods_receipt_receive_goods"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/inventory/receive-goods.ts", "apps/api/src/inventory/receive-goods.test.ts", "apps/web/app/goods-receipt/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the goods-receipt screen, When receive goods completes, Then the GoodsReceipt state and totals match the domain invariants"
  - "Given a cashier role, When receive goods is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'GoodsReceipt qty per line <= PurchaseOrder ordered qty minus received qty plus the Supplie' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-017 — Receive goods (goods-receipt)

## Slice

Vertical slice for job `receive-goods`: operations goods_receipt_receive_goods; screens goods-receipt; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the goods-receipt screen, When receive goods completes, Then the GoodsReceipt state and totals match the domain invariants
2. Given a cashier role, When receive goods is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'GoodsReceipt qty per line <= PurchaseOrder ordered qty minus received qty plus the Supplie' is checked, Then it holds

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
