---
id: "0001"
title: "Stack"
status: accepted
decision_refs: ["D:platform"]
date: "2026-09-24"
---

# ADR 0001: Stack

## Context

Pack default stack: web nextjs, mobile expo, api hono-node, db postgres, realtime websocket, cache redis, ledger postgres-double-entry, queue postgres-outbox, charts lightweight-charts. Device breadth (desktop web, phones, tablets) and live market data and offline needs [D:platform] decide the web layer.

## Decision

Web/POS: expo. API: hono-node. Database: postgres. Offline store: pglite-event-sourced-sync. Realtime: websocket. Mobile companion: expo. Printing: escpos-local-bridge. Commands per layer come from data/stacks.csv.

## Alternatives

| Alternative | Rejected because |
|-------------|------------------|
| Native apps only (Expo everywhere) | no Windows POS terminal path; slower hardware iteration |
| NestJS API | heavier DI framework for a small team; hono covers the routing and middleware needed |

## Consequences

- One TypeScript language across web, api, bridge and mobile
- PWA install on tablets; store submission only for the companion app
- stacks.csv is the source of truth for scaffold, test, typecheck, lint and a11y commands

## Revisit when

A native-only device (kiosk hardware without a browser) enters scope, or team size passes 8 engineers.
