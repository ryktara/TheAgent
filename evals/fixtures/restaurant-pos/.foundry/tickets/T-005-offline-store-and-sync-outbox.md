---
id: "T-005"
title: "Offline store and sync outbox"
type: "feature"
blockedBy: ["T-003", "T-004"]
jobs: []
screens: []
operations: ["sync_push", "sync_pull"]
adrs: ["0005"]
controls: ["SEC-API-11", "SEC-OFF-01", "SEC-OFF-03", "SEC-BL-08", "SEC-BL-11"]
estimate: "L"
files_likely_touched: ["apps/web/src/offline/store.ts", "apps/web/src/offline/outbox.ts", "apps/api/src/sync/push.ts", "apps/api/src/sync/pull.ts"]
acceptance_tests:
  - "Given the device offline, When an order is created, Then it is stored locally with a client UUID and a monotonic seq"
  - "Given 500 queued events, When the connection returns, Then the queue drains within 60 s and every event is acked once"
  - "Given the same event replayed, When push runs, Then the server returns the first result and creates no duplicate"
  - "Given two devices editing one order, When both sync, Then last-writer-wins per field and payments append"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-005 — Offline store and sync outbox

## Slice

pglite store, outbox, push/pull endpoints with seq validation, receipt block allocation, conflict rules from ADR 0005.

## Acceptance tests

1. Given the device offline, When an order is created, Then it is stored locally with a client UUID and a monotonic seq
2. Given 500 queued events, When the connection returns, Then the queue drains within 60 s and every event is acked once
3. Given the same event replayed, When push runs, Then the server returns the first result and creates no duplicate
4. Given two devices editing one order, When both sync, Then last-writer-wins per field and payments append

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
