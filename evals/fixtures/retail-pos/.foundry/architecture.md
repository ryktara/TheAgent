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
| pos-web | nextjs-pwa | Cashier, waiter and manager screens; offline store; print jobs | api, print-bridge, offline-store |
| kds-web | nextjs-pwa | Kitchen display per station | api (websocket) |
| mobile-waiter | expo | Handheld order taking | api |
| api | hono-node | Domain services, authz, sync, adapters, webhooks | db, payment-provider, delivery-platform, accounting, fiscal |
| db | postgres | System of record with RLS | - |
| offline-store | pglite-event-sourced-sync | Device-local data and outbox | pos-web |
| print-bridge | node escpos | LAN service driving printers and cash drawer | printers |
| realtime | websocket | Ticket and table state fan-out per branch | pos-web, kds-web |

## Trust boundaries

- **internet<->edge**: public clients to TLS edge; rate limits, WAF
- **edge<->api**: authenticated device or staff session; request ids
- **api<->db**: RLS by branch; app role has no DDL
- **api<->payment-provider**: outbound only; secrets in api env; idempotency keys
- **terminal<->local-print-bridge**: LAN, bridge token, print payloads only
- **device<->offline-store**: device-local; encrypted at rest on tablets

## Data flows (riskiest workflows)

1. **Payment** [D:payments]: pos-web -> api `POST /tenders` (idempotency key = client_uuid + tender seq) crossing edge<->api -> api pushes amount to the Network International terminal (semi-integrated) across api<->payment-provider -> approval code and last four only -> Tender captured, Sale paid when captured sum equals total, audit event -> fiscal-worker queues ZATCA report -> receipt job to print-bridge (terminal<->local-print-bridge, bridge token). Terminal timeout: status query before any retry, never double-charge. Card data never crosses pos-web or api.
2. **Refund / exchange**: cashier looks up receipt on pos-web -> Return requested -> store-manager PIN when outside the 7-day window -> api `POST /returns/{id}/approve` then refund to original tender via adapter (idempotency key = return id) or exchange credit on a new Sale -> StockMovement return (restock) -> loyalty points reversed -> ZATCA credit note queued -> audit event. Card refund with provider offline: queue or store credit per policy.
3. **Offline sync** [D:offline]: pos-web writes Sale, Tender (cash) and StockMovement events to the offline-store outbox (device<->offline-store, encrypted at rest) with client_uuid and monotonic device_seq -> on reconnect `POST /sync/push` in device_seq order across edge<->api -> api applies rules: Sales and Tenders append-only and deduplicated on client_uuid, stock applied as movements (never overwritten), catalog last-writer-wins per field from the server -> `GET /sync/pull` returns catalog, price and promotion changes plus a new receipt-number block -> conflicts shown on sync-status; queue drains within 60 s.

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
