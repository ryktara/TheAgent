---
pack: "retail-pos"
decisions_hash: "af8853fb0dac"
boundaries: ["internet<->edge", "edge<->api", "api<->db", "api<->payment-provider", "terminal<->local-print-bridge", "device<->offline-store"]
---

# Threat model — Retail POS

STRIDE per trust boundary from data/threat-patterns.csv, controls from data/security-controls.csv
filtered by this project's decisions. Operation authz matrix from openapi.yaml `x-foundry`.

## Boundary: internet<->edge

| Id | STRIDE | Threat | Controls | Severity |
|----|--------|--------|----------|----------|
| TP-IE-01 | S | Attacker impersonates the web app via phishing domain to capture staff credentials | `SEC-AUTH-08`, `SEC-CRY-01`, `SEC-AUTH-13` | medium |
| TP-IE-02 | T | Request tampering in transit (downgrade, MITM on hotel wifi) | `SEC-CRY-01` | high |
| TP-IE-03 | R | Client denies sending a request; no request ids | `SEC-LOG-01` | low |
| TP-IE-04 | I | Verbose errors or debug endpoints leak stack traces and versions | `SEC-LOG-04`, `SEC-CFG-02`, `SEC-CFG-06` | medium |
| TP-IE-05 | D | Volumetric or credential-stuffing traffic exhausts the api | `SEC-AUTH-04`, `SEC-API-02` | medium |
| TP-IE-06 | E | Missing security headers enable clickjacking or script injection on back-office pages | `SEC-API-08`, `SEC-IN-03` | medium |

## Boundary: edge<->api

| Id | STRIDE | Threat | Controls | Severity |
|----|--------|--------|----------|----------|
| TP-EA-01 | S | Stolen device token reused from another network | `SEC-AUTH-06`, `SEC-SESS-08`, `SEC-API-11` | high |
| TP-EA-02 | T | Client sets server-owned fields (total, state, branch_id) in request bodies | `SEC-ACC-04`, `SEC-BL-01` | high |
| TP-EA-03 | R | Money-moving action without actor identity | `SEC-LOG-02`, `SEC-AUTH-11` | high |
| TP-EA-04 | I | List endpoints leak other branches' orders (BOLA) | `SEC-ACC-02`, `SEC-API-03` | high |
| TP-EA-05 | D | Unbounded pagination or bulk operations exhaust the api | `SEC-IN-10`, `SEC-API-02` | medium |
| TP-EA-06 | E | Cashier calls admin routes or refund operation directly | `SEC-ACC-01`, `SEC-ACC-03`, `SEC-SESS-07` | high |
| TP-EA-07 | T | Replay of a payment POST creates a duplicate charge | `SEC-API-01` | high |

## Boundary: api<->db

| Id | STRIDE | Threat | Controls | Severity |
|----|--------|--------|----------|----------|
| TP-AD-01 | S | App role used to bypass RLS with BYPASSRLS | `SEC-ACC-05` | medium |
| TP-AD-02 | T | SQL injection through string-built queries | `SEC-IN-04` | high |
| TP-AD-03 | R | Audit rows updated or deleted after the fact | `SEC-DATA-07`, `SEC-LOG-02` | high |
| TP-AD-04 | I | Backups unencrypted or exposed | `SEC-DATA-06`, `SEC-CRY-03` | medium |
| TP-AD-05 | D | Long-running report queries lock operational tables | `SEC-API-03` | low |
| TP-AD-06 | E | Migration run with superuser in production | `SEC-CFG-01`, `SEC-ACC-05` | medium |

## Boundary: api<->payment-provider

| Id | STRIDE | Threat | Controls | Severity |
|----|--------|--------|----------|----------|
| TP-AT-01 | S | Fake provider endpoint via DNS or SSRF | `SEC-API-06`, `SEC-CRY-01` | medium |
| TP-AT-02 | T | Provider response tampered or malformed leads to wrong Payment state | `SEC-API-12`, `SEC-PAY-05` | medium |
| TP-AT-03 | R | Payment captured at provider but not recorded locally | `SEC-PAY-05`, `SEC-API-05` | high |
| TP-AT-04 | I | Provider secrets leaked through logs or devices | `SEC-PAY-03`, `SEC-CRY-03`, `SEC-DATA-08` | high |
| TP-AT-05 | D | Provider outage blocks all tenders | `SEC-API-05`, `SEC-CFG-08` | medium |
| TP-AT-06 | E | Sandbox keys swapped for live keys without a human step | `SEC-CFG-08`, `SEC-AGT-12` | medium |

## Boundary: terminal<->local-print-bridge

| Id | STRIDE | Threat | Controls | Severity |
|----|--------|--------|----------|----------|
| TP-PB-01 | S | Rogue LAN device sends print jobs or opens the drawer | `SEC-CFG-07` | high |
| TP-PB-02 | T | Control bytes injected through item names into ESC/POS | `SEC-IN-07` | medium |
| TP-PB-03 | R | Drawer opened without a tender recorded | `SEC-LOG-02`, `SEC-BL-07` | medium |
| TP-PB-04 | I | Receipt data sniffed on the LAN | `SEC-CFG-07`, `SEC-CRY-01` | low |
| TP-PB-05 | D | Printer offline blocks tender completion | `SEC-API-05` | low |

## Boundary: device<->offline-store

| Id | STRIDE | Threat | Controls | Severity |
|----|--------|--------|----------|----------|
| TP-DO-01 | T | Duplicate or replayed outbox events create double orders | `SEC-BL-11`, `SEC-API-11` | high |
| TP-DO-02 | R | Receipt numbers reused across devices | `SEC-BL-08`, `SEC-OFF-04` | high |
| TP-DO-03 | I | PII persisted beyond the shift on the device | `SEC-OFF-02`, `SEC-DATA-03` | medium |
| TP-DO-04 | D | Sync storm after reconnect starves ordering | `SEC-OFF-05` | medium |
| TP-DO-05 | T | Conflicting edits resolved non-deterministically | `SEC-OFF-03` | medium |

## Boundary: admin

| Id | STRIDE | Threat | Controls | Severity |
|----|--------|--------|----------|----------|
| TP-AM-01 | S | Owner account taken over via password reuse | `SEC-AUTH-02`, `SEC-AUTH-08` | high |
| TP-AM-02 | T | Role matrix edited to grant refund rights to cashiers | `SEC-ACC-07`, `SEC-LOG-02` | high |
| TP-AM-03 | R | Settings changed without audit | `SEC-LOG-02` | medium |
| TP-AM-04 | I | Export of all customers by a non-owner | `SEC-ACC-03`, `SEC-ACC-09` | medium |
| TP-AM-05 | E | Last owner demoted, locking out the organisation | `SEC-ACC-06` | medium |

## Operation authz matrix

| operationId | Job | Personas | Authz | Audit | Idempotent | Money | Controls |
|-------------|-----|----------|-------|-------|------------|-------|----------|
| `product_list` | read | store-manager, owner | role in [store-manager, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `product_create` | create | store-manager, owner | role in [store-manager, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `product_get` | read | store-manager, owner | role in [store-manager, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `product_update` | update | store-manager, owner | role in [store-manager, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `product_archive` | archive | store-manager, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `variant_list` | read | system, owner | role in [system, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `variant_create` | create | system, owner | role in [system, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `variant_get` | read | system, owner | role in [system, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `variant_update` | update | system, owner | role in [system, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `variant_archive` | archive | system, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `sale_list` | read | cashier, owner | role in [cashier, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `sale_create` | create | cashier, owner | role in [cashier, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `sale_get` | read | cashier, owner | role in [cashier, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `sale_update` | update | cashier, owner | role in [cashier, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `sale_archive` | archive | cashier, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `tender_list` | read | cashier, owner | role in [cashier, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `tender_create` | create | cashier, owner | role in [cashier, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `tender_get` | read | cashier, owner | role in [cashier, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `tender_update` | update | cashier, owner | role in [cashier, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `tender_archive` | archive | cashier, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `return_list` | read | store-manager, owner | role in [store-manager, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `return_create` | create | store-manager, owner | role in [store-manager, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `return_get` | read | store-manager, owner | role in [store-manager, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `return_update` | update | store-manager, owner | role in [store-manager, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `return_archive` | archive | store-manager, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `promotion_list` | read | store-manager, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `promotion_get` | read | store-manager, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `loyalty_account_list` | read | store-manager, owner | role in [store-manager, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `loyalty_account_create` | create | store-manager, owner | role in [store-manager, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `loyalty_account_get` | read | store-manager, owner | role in [store-manager, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `loyalty_account_update` | update | store-manager, owner | role in [store-manager, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `loyalty_account_archive` | archive | store-manager, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `customer_list` | read | cashier, owner | role in [cashier, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `customer_create` | create | cashier, owner | role in [cashier, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `customer_get` | read | cashier, owner | role in [cashier, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `customer_update` | update | cashier, owner | role in [cashier, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `customer_archive` | archive | cashier, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `gift_card_list` | read | cashier, owner | role in [cashier, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `gift_card_create` | create | cashier, owner | role in [cashier, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `gift_card_get` | read | cashier, owner | role in [cashier, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `gift_card_update` | update | cashier, owner | role in [cashier, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `gift_card_archive` | archive | cashier, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `layaway_list` | read | cashier, owner | role in [cashier, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `layaway_create` | create | cashier, owner | role in [cashier, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `layaway_get` | read | cashier, owner | role in [cashier, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `layaway_update` | update | cashier, owner | role in [cashier, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `layaway_archive` | archive | cashier, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `purchase_order_list` | read | stock-keeper, owner | role in [stock-keeper, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `purchase_order_create` | create | stock-keeper, owner | role in [stock-keeper, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `purchase_order_get` | read | stock-keeper, owner | role in [stock-keeper, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `purchase_order_update` | update | stock-keeper, owner | role in [stock-keeper, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `purchase_order_archive` | archive | stock-keeper, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `goods_receipt_list` | read | stock-keeper, owner | role in [stock-keeper, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `goods_receipt_create` | create | stock-keeper, owner | role in [stock-keeper, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `goods_receipt_get` | read | stock-keeper, owner | role in [stock-keeper, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `goods_receipt_update` | update | stock-keeper, owner | role in [stock-keeper, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `goods_receipt_archive` | archive | stock-keeper, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `stock_count_list` | read | stock-keeper, owner | role in [stock-keeper, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `stock_count_create` | create | stock-keeper, owner | role in [stock-keeper, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `stock_count_get` | read | stock-keeper, owner | role in [stock-keeper, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `stock_count_update` | update | stock-keeper, owner | role in [stock-keeper, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `stock_count_archive` | archive | stock-keeper, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `transfer_list` | read | stock-keeper, owner | role in [stock-keeper, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `transfer_create` | create | stock-keeper, owner | role in [stock-keeper, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `transfer_get` | read | stock-keeper, owner | role in [stock-keeper, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `transfer_update` | update | stock-keeper, owner | role in [stock-keeper, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `transfer_archive` | archive | stock-keeper, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `supplier_list` | read | store-manager, owner | role in [store-manager, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `supplier_create` | create | store-manager, owner | role in [store-manager, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `supplier_get` | read | store-manager, owner | role in [store-manager, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `supplier_update` | update | store-manager, owner | role in [store-manager, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `supplier_archive` | archive | store-manager, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `cash_drawer_session_list` | read | cashier, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `cash_drawer_session_get` | read | cashier, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `receipt_list` | read | system, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `receipt_get` | read | system, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `sync_event_list` | read | system, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `sync_event_get` | read | system, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `tax_rule_list` | read | owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `tax_rule_get` | read | owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `staff_list` | read | owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `staff_get` | read | owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `store_list` | read | owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `store_get` | read | owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `sale_scan_and_sell` | scan-and-sell | cashier | role in [cashier, store-manager, owner]; store scope; no PIN | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `sale_line_sell_weighed_item` | sell-weighed-item | cashier | role in [cashier, store-manager, owner]; store scope; no PIN | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `tender_take_payment` | take-payment | cashier | role in [cashier, store-manager, owner]; store scope; no PIN; refund of a captured tender needs manager PIN | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `receipt_issue_receipt` | issue-receipt | cashier | role in [cashier, store-manager, owner]; store scope; reprint marks copy; no PIN | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `return_return_exchange` | return-exchange | cashier | role in [cashier, store-manager, owner]; store scope; manager PIN when outside the 7-day window, over auto-approve limit or no receipt | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `sale_line_price_override` | price-override | store-manager | role in [cashier, store-manager, owner]; store scope; manager PIN always; over override_limit_pct needs owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `promotion_manage_promotions` | manage-promotions | store-manager | role in [store-manager, owner]; store scope; no PIN | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `loyalty_account_loyalty_points` | loyalty-points | cashier | role in [cashier, store-manager, owner]; store scope; redeem over policy needs manager PIN | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `gift_card_gift_card_store_credit` | gift-card-store-credit | cashier | role in [cashier, store-manager, owner]; store scope; store credit issue needs manager PIN | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `layaway_layaway` | layaway | cashier | role in [cashier, store-manager, owner]; store scope; cancel needs manager PIN | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `product_manage_catalog` | manage-catalog | store-manager | role in [store-manager, owner]; store scope; no PIN | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `purchase_order_purchase_orders` | purchase-orders | stock-keeper | role in [stock-keeper, store-manager, owner]; store scope; send needs store-manager | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `goods_receipt_receive_goods` | receive-goods | stock-keeper | role in [stock-keeper, store-manager, owner]; store scope; over-tolerance receipt needs manager PIN | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `stock_count_stock_take` | stock-take | stock-keeper | role in [stock-keeper, store-manager, owner]; store scope; post needs store-manager approval | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `stock_movement_stock_adjust` | stock-adjust | stock-keeper | role in [stock-keeper, store-manager, owner]; store scope; manager PIN always | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `transfer_stock_transfer` | stock-transfer | stock-keeper | role in [stock-keeper, store-manager, owner]; store scope; discrepancy resolution needs owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `supplier_manage_suppliers` | manage-suppliers | store-manager | role in [store-manager, owner]; store scope; no PIN | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `receipt_e_invoicing` | e-invoicing | accountant | role in [accountant, owner]; store scope; no PIN | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `sale_customer_display` | customer-display | customer | device role customer-display; read-only; paired to one terminal | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `cash_drawer_session_cash_management` | cash-management | cashier | role in [cashier, store-manager, owner]; store scope; pickups, paid-outs and variance above policy need manager PIN | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `job_reports_shrinkage` | reports-shrinkage | owner | role in [owner, store-manager, accountant]; store scope; read-only | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `barcode_print_labels` | print-labels | stock-keeper | role in [stock-keeper, store-manager, owner]; store scope; no PIN | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `staff_staff_roles` | staff-roles | owner | role == owner; organisation scope; PIN resets audited | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `store_multi_store` | multi-store | owner | role == owner; organisation scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `sync_event_offline_sync` | offline-sync | cashier | device session bound to terminal; store scope; no PIN | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-API-11`, `SEC-OFF-01` |
| `sync_push` | offline-sync | cashier | device token; branch of the device | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-API-11`, `SEC-OFF-01` |
| `sync_pull` | offline-sync | cashier | device token; branch of the device | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-API-11`, `SEC-OFF-01` |
| `webhook_payments` | payments-webhook | system | provider signature verified; idempotent on (provider, event_id) | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06`, `SEC-API-04`, `SEC-CRY-06` |
| `webhook_einvoicing` | einvoicing-webhook | system | provider signature verified; idempotent on (provider, event_id) | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-API-04`, `SEC-CRY-06` |

## Top 10 risks

| Rank | Score | Boundary | Threat | Controls |
|-----:|------:|----------|--------|----------|
| 1 | 9 | edge<->api | Stolen device token reused from another network (TP-EA-01) | `SEC-AUTH-06`, `SEC-SESS-08`, `SEC-API-11` |
| 2 | 9 | edge<->api | Client sets server-owned fields (total, state, branch_id) in request bodies (TP-EA-02) | `SEC-ACC-04`, `SEC-BL-01` |
| 3 | 9 | edge<->api | Money-moving action without actor identity (TP-EA-03) | `SEC-LOG-02`, `SEC-AUTH-11` |
| 4 | 9 | edge<->api | List endpoints leak other branches' orders (BOLA) (TP-EA-04) | `SEC-ACC-02`, `SEC-API-03` |
| 5 | 9 | edge<->api | Cashier calls admin routes or refund operation directly (TP-EA-06) | `SEC-ACC-01`, `SEC-ACC-03`, `SEC-SESS-07` |
| 6 | 9 | edge<->api | Replay of a payment POST creates a duplicate charge (TP-EA-07) | `SEC-API-01` |
| 7 | 9 | internet<->edge | Request tampering in transit (downgrade, MITM on hotel wifi) (TP-IE-02) | `SEC-CRY-01` |
| 8 | 6 | admin | Owner account taken over via password reuse (TP-AM-01) | `SEC-AUTH-02`, `SEC-AUTH-08` |
| 9 | 6 | admin | Role matrix edited to grant refund rights to cashiers (TP-AM-02) | `SEC-ACC-07`, `SEC-LOG-02` |
| 10 | 6 | api<->payment-provider | Payment captured at provider but not recorded locally (TP-AT-03) | `SEC-PAY-05`, `SEC-API-05` |

Rationale: single Riyadh store, no delivery boundary and a semi-integrated terminal keep edge<->api and insider refund risks on top; the print bridge ranks low because it carries receipts and labels only.

## Abuse cases

| Workflow | Actor | Goal | Path | Stopped by | Residual |
|----------|-------|------|------|------------|----------|
| payment | cashier | pocket cash by marking a card tender paid | record tender kind card without a Network International approval code | `SEC-PAY-02` approval code from terminal required; `SEC-PAY-05` nightly settlement reconciliation | offline manual approval entry, audited and reconciled next day |
| payment | cashier | ring a lower total for a friend | price override or bogus promotion on a paid line | `SEC-ACC-04` server-owned totals; `SEC-BL-01` server recomputes price and promotions | override with manager PIN, visible in audit and shrinkage report |
| payment | LAN attacker | double-charge or divert terminal payment | replay the tender POST or spoof the terminal response | `SEC-API-01` idempotency key; `SEC-CRY-01` TLS on every hop | terminal pairing stolen with the device |
| refund | store-manager | refund to own card | refund to a tender not on the original sale | `SEC-PAY-04` refund only against the original tender token; `SEC-BL-04` refund capped at returnable amount | cash refund fallback needs owner review |
| refund | cashier | return an item never bought (no-receipt fraud) | no-receipt return of shelf stock for cash | `SEC-BL-03` returnable qty checked per SaleLine; `SEC-LOG-02` actor and approver logged | no-receipt returns to store credit only, reviewed weekly |
| refund | insider owner | erase a sale after ZATCA reporting | void a reported receipt | `SEC-LOG-02` append-only audit; `SEC-BL-05` void after report only by credit note | none beyond audit |
| offline sync | device | replay events to duplicate sales | resend outbox with reused device_seq | `SEC-API-11` monotonic seq per device; `SEC-BL-06` client_uuid dedupe | none beyond audit |
| offline sync | thief with stolen till | read customer phones and loyalty data | copy the offline store from the device | `SEC-CRY-06` device store encrypted at rest; `SEC-AUTH-06` device token revocable | data cached before revocation |

## Blocking findings

- none
