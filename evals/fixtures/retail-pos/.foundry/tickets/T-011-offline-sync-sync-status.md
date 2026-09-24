---
id: "T-011"
title: "Offline sync (sync-status)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-007", "T-008"]
jobs: ["offline-sync"]
screens: ["sync-status"]
operations: ["sync_event_offline_sync", "sync_push", "sync_pull"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/sync/offline-sync.ts", "apps/api/src/sync/offline-sync.test.ts", "apps/web/app/sync-status/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the sync-status screen, When offline sync completes, Then the SyncEvent state and totals match the domain invariants"
  - "Given a cashier role, When offline sync is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'Every offline Sale carries a client_uuid and a device_seq monotonic per device; each SyncEvent acks exactly once' is checked, Then it holds"
  - "Given two offline tills, When both replay their outboxes, Then SyncEvents apply in device_seq order and each client_uuid is acked exactly once"
  - "Given a duplicate SyncEvent, When it is pushed, Then it is acked without creating a second Sale or StockMovement"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-011 — Offline sync (sync-status)

## Slice

Vertical slice for job `offline-sync`: operations sync_event_offline_sync, sync_push, sync_pull; screens sync-status; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the sync-status screen, When offline sync completes, Then the SyncEvent state and totals match the domain invariants
2. Given a cashier role, When offline sync is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'Every offline Sale carries a client_uuid and a device_seq monotonic per device; each SyncEvent acks exactly once' is checked, Then it holds
5. Given two offline tills, When both replay their outboxes, Then SyncEvents apply in device_seq order and each client_uuid is acked exactly once
6. Given a duplicate SyncEvent, When it is pushed, Then it is acked without creating a second Sale or StockMovement

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
