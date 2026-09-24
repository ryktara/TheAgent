---
pack: restaurant-pos
version: 1
decisions_hash: ceb231ab5069
generated_by: prd-skeleton
---

# PRD — Restaurant POS

## 1. Product

A tablet point of sale for a dine-in restaurant in Sharjah [D:region] [D:service-model]. Waiters take orders at the table and the kitchen sees them on a display or printed ticket [D:kds]. Bills settle by card through Network International or in cash [D:payments] [D:payment-provider-name]. Order-taking must never stop when the internet drops [D:offline].

## 2. Personas

| Persona | Role in the product | Kept because |
|---------|---------------------|--------------|
| cashier | pack persona | pack |
| waiter | pack persona | pack |
| kitchen | pack persona | pack |
| manager | pack persona | pack |
| owner | pack persona | pack |
| accountant | pack persona | pack |
| customer | pack persona | pack |
| delivery-rider | pack persona | pack |

## 3. Jobs to be done

| Id | Persona | Job | must/should | Screens |
|----|---------|-----|-------------|---------|
| `take-order-table` | waiter | take order table | must | table-map, order-entry |
| `take-order-counter` | cashier | take order counter | must | order-entry |
| `take-order-qr` | customer | take order qr | should | qr-self-order |
| `modify-order` | waiter | modify order | must | order-entry, modifier-sheet |
| `send-to-kitchen` | waiter | send to kitchen | must | order-entry, kds |
| `kds-bump` | kitchen | kds bump | must | kds |
| `hold-void-comp` | manager | hold void comp | must | order-entry, manager-pin |
| `split-bill` | cashier | split bill | must | split-bill |
| `merge-transfer-tables` | waiter | merge transfer tables | must | table-map |
| `apply-discount` | cashier | apply discount | must | tender, manager-pin |
| `tips-service-charge` | cashier | tips service charge | must | tender |
| `take-payment` | cashier | take payment | must | tender |
| `print-receipt` | cashier | print receipt | must | receipt-preview |
| `refund` | manager | refund | must | refund, manager-pin |
| `open-close-shift` | cashier | open close shift | must | shift-open, shift-close |
| `end-of-day` | manager | end of day | must | end-of-day |
| `manage-menu` | manager | manage menu | must | menu-management |
| `manage-floor` | manager | manage floor | must | floor-editor, table-map |
| `reservations-waitlist` | waiter | reservations waitlist | should | reservations |
| `inventory-basic` | manager | inventory basic | must | inventory, recipe-editor |
| `purchasing` | manager | purchasing | should | purchasing |
| `delivery-orders` | kitchen | delivery orders | should | delivery-inbox, kds |
| `reports` | owner | reports | must | reports |
| `staff-roles` | owner | staff roles | must | staff-roles |
| `multi-branch` | owner | multi branch | should | branch-switcher, menu-management |
| `loyalty` | cashier | loyalty | should | tender, customer-lookup |
| `offline-sync` | cashier | offline sync | must | sync-status |

## 4. Scope IN

- `order-entry` — pack must-have
- `table-map` — pack must-have
- `modifiers` — pack must-have
- `course-firing` — pack must-have
- `send-to-kitchen` — pack must-have
- `kds` — pack must-have
- `hold-void-comp` — pack must-have
- `split-bill` — pack must-have
- `merge-transfer` — pack must-have
- `discounts` — pack must-have
- `tips-service-charge` — pack must-have
- `tender-cash-card-wallet` — pack must-have
- `split-tender` — pack must-have
- `receipt-bilingual-qr` — pack must-have
- `refunds` — pack must-have
- `shift-cash-count` — pack must-have
- `z-report` — pack must-have
- `end-of-day` — pack must-have
- `menu-management` — pack must-have
- `floor-management` — pack must-have
- `inventory-basic` — pack must-have
- `reports-core` — pack must-have
- `staff-roles` — pack must-have
- `offline-queue` — pack must-have
- `audit-log` — pack must-have

## 5. Scope OUT

- `qr-self-order` — not enabled by any decision; later phase
- `room-charge` — not enabled by any decision; later phase
- `reservations` — not enabled by any decision; later phase
- `waitlist` — not enabled by any decision; later phase
- `purchasing` — not enabled by any decision; later phase
- `delivery-integration` — not enabled by any decision; later phase
- `multi-branch` — not enabled by any decision; later phase
- `loyalty` — not enabled by any decision; later phase
- `whatsapp-receipts` — not enabled by any decision; later phase
- `accounting-sync` — not enabled by any decision; later phase
- `customer-display` — not enabled by any decision; later phase
- `e-invoicing` — not enabled by any decision; later phase

## 6. Non-functional requirements

- Offline: required [D:offline]
- Latency: add line p95 100 ms; send to kitchen p95 300 ms; tender p95 500 ms
- Devices: tablets: ['ipad-10th-gen', 'android-10in', 'windows-pos-terminal']; kitchen_screen: 15in; printers: thermal-80mm
- Languages: en, ar (RTL for ar/ur) [D:region]
- Other: sync_recovery_s 60; concurrent_terminals_min 3; rtl required; font_min_px 16; touch_min_dp 48; uptime 99.5%; backups daily

## 7. Integrations

| Category | Chosen | Source |
|----------|--------|--------|
| payments | network-intl | [D:payments] |
| delivery | talabat | [D:delivery-platforms] |
| accounting | zoho | pack default |
| printers | escpos-network | pack default |
| hardware | cash-drawer | pack default |
| messaging | whatsapp-receipts | pack default |
| einvoicing | ae-fta | pack default |

## 8. Regional and compliance

- Region: AE [D:region]
- tax: VAT 5%
- inclusive default: True
- receipt lang: en, ar
- einvoice: FTA e-invoicing B2B/B2G from 2027; B2C receipts exempt until further notice
- rounding: nearest fils, once per order
- currency: AED
- minor units: 2
- fiscal: VAT tax invoice fields; TRN on receipt
- fees: hotel F&B: 7% municipality fee (Dubai), 10% service charge; Tourism Dirham on rooms only
- Must controls: `C-ALL-01`, `C-ALL-02`, `C-ALL-03`, `C-ALL-04`, `C-ALL-05`, `C-ALL-06`, `C-AE-01`, `C-AE-02`, `C-AE-03`
- Should controls: `C-ALL-07`, `C-ALL-08`, `C-AE-04`

## 9. Success metrics

1. Median order entry under 45 seconds per table within 30 days of go-live
2. 99% of fired tickets visible on the KDS within 1 second during service hours, first 90 days
3. Zero lost orders during measured connectivity drops in the first 90 days
4. Shift close reconciled within 5 minutes on 95% of shifts from month two

## 10. Open assumptions

Confirmed decisions (human, brief, derived):

- `region` = "AE" — brief: brief matched 'sharjah' [D:region]
- `payments` = "network-intl" — brief: brief matched 'network international' [D:payments]
- `payment-provider-name` = "Network International" — agent-fact: derived from payments=network-intl [D:payment-provider-name]

Assumptions taken from pack defaults; each can be changed by editing `.foundry/decisions.yaml`:

- `service-model` = "dine-in" — timeout-default; changeable [D:service-model]
- `branches` = "single" — timeout-default; changeable [D:branches]
- `kds` = "both" — timeout-default; changeable [D:kds]
- `delivery` = false — timeout-default; changeable [D:delivery]
- `offline` = true — timeout-default; changeable [D:offline]
- `reservations` = false — timeout-default; changeable [D:reservations]
- `qr-self-order` = false — pack-default; changeable [D:qr-self-order]
- `delivery-platforms` = "talabat" — pack-default; changeable [D:delivery-platforms]
- `central-menu-sync` = "central" — pack-default; changeable [D:central-menu-sync]
