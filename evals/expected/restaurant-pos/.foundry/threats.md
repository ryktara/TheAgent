---
pack: "restaurant-pos"
decisions_hash: "ceb231ab5069"
boundaries: ["internet<->edge", "edge<->api", "api<->db", "api<->payment-provider", "terminal<->local-print-bridge", "device<->offline-store"]
---

# Threat model — Restaurant POS

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
| `order_list` | read | waiter, owner, kitchen | role in [waiter, owner] and branch scope; or role == kitchen (read only, states sent, in-progress, ready) | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_create` | create | waiter, owner | role in [waiter, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_get` | read | waiter, owner, kitchen | role in [waiter, owner] and same branch; or role == kitchen (read only, states sent, in-progress, ready) | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_update` | update | waiter, owner | role in [waiter, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_archive` | archive | waiter, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `table_list` | read | waiter, owner | role in [waiter, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `table_create` | create | waiter, owner | role in [waiter, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `table_get` | read | waiter, owner | role in [waiter, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `table_update` | update | waiter, owner | role in [waiter, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `table_archive` | archive | waiter, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `shift_list` | read | cashier, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `shift_get` | read | cashier, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `payment_list` | read | cashier, owner | role in [cashier, owner] and branch scope | no | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `payment_create` | create | cashier, owner | role in [cashier, owner] and branch scope | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `payment_get` | read | cashier, owner | role in [cashier, owner] and same branch | no | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `payment_update` | update | cashier, owner | role in [cashier, owner] and same branch; state guards per domain.yaml | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `payment_archive` | archive | cashier, owner | role == owner | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `tender_list` | read | manager, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `tender_get` | read | manager, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `refund_list` | read | manager, owner | role == owner | no | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `refund_get` | read | manager, owner | role == owner | no | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `receipt_list` | read | manager, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `receipt_get` | read | manager, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `menu_item_list` | read | manager, owner | role in [manager, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `menu_item_create` | create | manager, owner | role in [manager, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `menu_item_get` | read | manager, owner | role in [manager, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `menu_item_update` | update | manager, owner | role in [manager, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `menu_item_archive` | archive | manager, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `reservation_list` | read | cashier, owner | role in [cashier, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `reservation_create` | create | cashier, owner | role in [cashier, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `reservation_get` | read | cashier, owner | role in [cashier, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `reservation_update` | update | cashier, owner | role in [cashier, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `reservation_archive` | archive | cashier, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `customer_list` | read | cashier, owner | role in [cashier, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `customer_create` | create | cashier, owner | role in [cashier, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `customer_get` | read | cashier, owner | role in [cashier, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `customer_update` | update | cashier, owner | role in [cashier, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `customer_archive` | archive | cashier, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `discount_list` | read | manager, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `discount_get` | read | manager, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `tax_rule_list` | read | manager, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `tax_rule_get` | read | manager, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `branch_list` | read | manager, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `branch_get` | read | manager, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `staff_list` | read | manager, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `staff_get` | read | manager, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `role_list` | read | cashier, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `role_get` | read | cashier, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `inventory_item_list` | read | manager, owner | role in [manager, owner] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `inventory_item_create` | create | manager, owner | role in [manager, owner] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `inventory_item_get` | read | manager, owner | role in [manager, owner] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `inventory_item_update` | update | manager, owner | role in [manager, owner] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `inventory_item_archive` | archive | manager, owner | role == owner | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `sync_event_list` | read | cashier, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `sync_event_get` | read | cashier, owner | role == owner | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_take_order_table` | take-order-table | waiter | role == waiter or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_take_order_counter` | take-order-counter | cashier | role == cashier or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_take_order_qr` | take-order-qr | customer | role == customer or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_line_modify_order` | modify-order | waiter | role == waiter or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_send_to_kitchen` | send-to-kitchen | waiter | role == waiter or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `kitchen_ticket_kds_bump` | kds-bump | kitchen | role == kitchen or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_line_hold_void_comp` | hold-void-comp | manager | role == manager or role == owner; branch scope; manager PIN when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `order_split_bill` | split-bill | cashier | role == cashier or role == owner; branch scope; manager PIN when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `table_merge_transfer_tables` | merge-transfer-tables | waiter | role == waiter or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_apply_discount` | apply-discount | cashier | role == cashier or role == owner; branch scope; manager PIN when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `order_tips_service_charge` | tips-service-charge | cashier | role == cashier or role == owner; branch scope; manager PIN when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `payment_take_payment` | take-payment | cashier | role == cashier or role == owner; branch scope; manager PIN when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `receipt_print_receipt` | print-receipt | cashier | role == cashier or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `refund_refund` | refund | manager | role == manager or role == owner; branch scope; manager PIN when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `shift_open_close_shift` | open-close-shift | cashier | role == cashier or role == owner; branch scope; manager PIN when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `shift_end_of_day` | end-of-day | manager | role == manager or role == owner; branch scope; manager PIN when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `menu_item_manage_menu` | manage-menu | manager | role == manager or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `table_manage_floor` | manage-floor | manager | role == manager or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `reservation_reservations_waitlist` | reservations-waitlist | waiter | role == waiter or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `inventory_item_inventory_basic` | inventory-basic | manager | role == manager or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `inventory_item_purchasing` | purchasing | manager | role == manager or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_delivery_orders` | delivery-orders | kitchen | role == kitchen or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `job_reports` | reports | owner | role == owner or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `staff_staff_roles` | staff-roles | owner | role == owner or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `branch_multi_branch` | multi-branch | owner | role == owner or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `customer_loyalty` | loyalty | cashier | role == cashier or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `sync_event_offline_sync` | offline-sync | cashier | role == cashier or role == owner; branch scope; manager PIN when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-API-11`, `SEC-OFF-01` |
| `sync_push` | offline-sync | cashier | device token; branch of the device | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-API-11`, `SEC-OFF-01` |
| `sync_pull` | offline-sync | cashier | device token; branch of the device | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-API-11`, `SEC-OFF-01` |
| `webhook_payments` | payments-webhook | system | provider signature verified; idempotent on (provider, event_id) | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06`, `SEC-API-04`, `SEC-CRY-06` |
| `webhook_delivery` | delivery-webhook | system | provider signature verified; idempotent on (provider, event_id) | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-API-04`, `SEC-CRY-06` |
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

## Abuse cases

<!-- model: write one table per risky workflow (payment, refund, offline sync): actor, goal, path, control that stops it, residual risk -->

| Workflow | Actor | Goal | Path | Stopped by | Residual |
|----------|-------|------|------|------------|----------|
| payment | cashier | pocket cash by marking card paid | mark tender card without terminal approval | `SEC-PAY-02` approval code required; `SEC-PAY-05` nightly reconciliation | manual approval-code entry offline, audited |
| refund | manager | refund to own card | refund to a tender not on the order | `SEC-PAY-04` refund via provider token of the original payment; `SEC-BL-04` cap | cash refund fallback needs owner PIN |
| offline sync | device | replay events to duplicate orders | resend outbox with reused seq | `SEC-API-11` monotonic seq; `SEC-BL-11` client UUID dedupe | none beyond audit |

## Blocking findings

- none
