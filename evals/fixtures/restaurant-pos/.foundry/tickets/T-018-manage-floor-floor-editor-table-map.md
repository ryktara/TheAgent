---
id: "T-018"
title: "Manage floor (floor-editor, table-map)"
type: "feature"
blockedBy: ["T-005", "T-004"]
jobs: ["manage-floor"]
screens: ["floor-editor", "table-map"]
operations: ["table_manage_floor"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/ordering/manage-floor.ts", "apps/api/src/ordering/manage-floor.test.ts", "apps/web/app/floor-editor/page.tsx", "apps/web/app/table-map/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the floor-editor screen, When manage floor completes, Then the Table state and totals match the domain invariants"
  - "Given offline mode, When manage floor runs, Then the write lands in the outbox and syncs without duplicates"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A Table in state seated or ordered references exactly one open Order' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'Merging Tables moves every OrderLine to one surviving Order and voids the others with reas' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-018 — Manage floor (floor-editor, table-map)

## Slice

Vertical slice for job `manage-floor`: operations table_manage_floor; screens floor-editor, table-map; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the floor-editor screen, When manage floor completes, Then the Table state and totals match the domain invariants
2. Given offline mode, When manage floor runs, Then the write lands in the outbox and syncs without duplicates
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'A Table in state seated or ordered references exactly one open Order' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'Merging Tables moves every OrderLine to one surviving Order and voids the others with reas' is checked, Then it holds

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
