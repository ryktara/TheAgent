---
id: "0005"
title: "Offline and sync"
status: accepted
decision_refs: []
date: "2026-09-24"
---

# ADR 0005: Offline and sync

## Context

Offline required: False (pack-default). Order entry is online-only; quotes go stale after a few seconds and must never be traded on; recovery target 60 s after reconnect.

## Decision

Event-sourced outbox on the device: every write is a SyncEvent (device_id, monotonic seq, entity, payload). Orders carry a client UUID; receipt numbers come from a per-device block reserved per branch so numbering stays gapless. On reconnect events replay in seq order and are acked individually. Conflicts: last-writer-wins per field, Payments append-only, voids beat edits; unresolvable conflicts surface on the sync-status screen. Server pushes menu and table state over websocket; devices pull on reconnect.

## Alternatives

| Alternative | Rejected because |
|-------------|------------------|
| CRDT document per order | harder to audit and to reason about for money; the outbox rule set from workflows.md is enough |
| Online-only with a queue | fails the offline gate |

## Consequences

- Device store is pglite (same SQL dialect as the server)
- Sync endpoints /sync/push and /sync/pull with per-device sequence
- Receipt block allocation is a server call made while online

## Revisit when

Two devices must edit the same order offline for long periods, or fiscal rules forbid device-side numbering.
