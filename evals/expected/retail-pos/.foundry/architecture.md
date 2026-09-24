---
pack: "retail-pos"
stack_id: "nextjs-pwa"
adr_ids: ["0001", "0002", "0003", "0004", "0005", "0006", "0007", "0008", "0009"]
trust_boundaries: ["internet<->edge", "edge<->api", "api<->db", "api<->payment-provider", "terminal<->local-print-bridge", "device<->offline-store"]
decisions_hash: "af8853fb0dac"
---

# Architecture — Retail POS

ADRs under .foundry/adr/. Containers follow C4 level 2.

## Containers

| Name | Tech | Responsibility | Talks to |
|------|------|----------------|----------|
| till-web | nextjs-pwa | Cashier and store manager screens; offline store; receipt and label jobs | api, print-bridge, offline-store |
| mobile-stock | expo | Handheld stock counts and goods receiving | api |
| api | hono-node | Domain services, authz, sync, adapters, webhooks | db, payment-provider, delivery-platform, accounting, fiscal |
| db | postgres | System of record with RLS | - |
| offline-store | pglite-event-sourced-sync | Device-local data and outbox | till-web |
| print-bridge | node escpos | LAN service driving printers and cash drawer | printers |
| realtime | websocket | Price and stock fan-out per branch | till-web |

## Trust boundaries

- **internet<->edge**: public clients to TLS edge; rate limits, WAF
- **edge<->api**: authenticated device or staff session; request ids
- **api<->db**: RLS by branch; app role has no DDL
- **api<->payment-provider**: outbound only; secrets in api env; idempotency keys
- **terminal<->local-print-bridge**: LAN, bridge token, print payloads only
- **device<->offline-store**: device-local; encrypted at rest on tablets

## Data flows (riskiest workflows)

1. **Payment**: till-web → api `POST /payments` (idempotency key) → network-intl terminal/gateway → approval code → api writes Payment captured, audit event → realtime → receipt job → print-bridge. Card data never crosses the till-web or api boundary.
2. **Refund**: manager PIN on till-web → api `POST /refunds` with approver → provider refund → Refund processed, audit event → receipt; cash refunds open the drawer via print-bridge.
3. **Offline sync**: till-web writes to offline-store outbox → on reconnect `POST /sync/push` in seq order → api applies conflict rules (LWW per field, payments append-only) → `GET /sync/pull` returns server changes and receipt blocks → conflicts to sync-status.

## Scaling and limits

- Concurrent terminals per branch: 4 minimum; websocket rooms per branch.
- One Postgres primary handles 100 branches at typical POS volume (hundreds of orders per branch per day).
- Sync push batches of 500 events; queue drains within 60 s on reconnect.
- Fiscal reporting queue is independent so a regulator outage never blocks ordering.

## Cost estimate

| Branches | Compute | Database | Other | Monthly (USD, order of magnitude) |
|---------:|---------|----------|-------|-----------------------------------|
| 1 | 1 small VM or Fly app | managed Postgres small | error tracking free tier | 40–80 |
| 10 | 2 VMs | managed Postgres medium + backups | error tracking, uptime | 200–400 |
| 100 | autoscaled api ×4, realtime ×2 | Postgres large + replica | observability, CDN | 1500–3000 |
