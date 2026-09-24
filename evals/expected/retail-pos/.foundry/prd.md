---
pack: retail-pos
version: 1
decisions_hash: af8853fb0dac
generated_by: prd-skeleton
---

# PRD — Retail POS

## 1. Product

A point-of-sale and stock system for a single clothing shop in Riyadh [D:region] [D:branches], used by cashiers at the till and by the manager and stock-keeper in the back office. It sells by barcode with stock held per size and colour variant [D:variants], handles returns and exchanges, earns and redeems loyalty points [D:loyalty], and takes card payments through Network International [D:payments]. Every sale produces a ZATCA phase-2 simplified tax invoice with a TLV QR code [D:einvoice], and the till keeps selling when the internet drops, syncing later [D:offline]. The one thing it must never fail at is completing a sale with a correct, compliant e-invoice and an exact stock decrement for the variant sold.

## 2. Personas

| Persona | Role in the product | Kept because |
|---------|---------------------|--------------|
| cashier | pack persona | pack |
| store-manager | pack persona | pack |
| owner | pack persona | pack |
| stock-keeper | pack persona | pack |
| accountant | pack persona | pack |
| customer | pack persona | pack |

## 3. Jobs to be done

| Id | Persona | Job | must/should | Screens |
|----|---------|-----|-------------|---------|
| `scan-and-sell` | cashier | scan and sell | must | checkout, product-search |
| `sell-weighed-item` | cashier | sell weighed item | must | checkout, weighed-item |
| `take-payment` | cashier | take payment | must | tender |
| `issue-receipt` | cashier | issue receipt | must | receipt-preview |
| `return-exchange` | cashier | return exchange | must | returns, receipt-lookup, manager-pin |
| `price-override` | store-manager | price override | must | checkout, manager-pin |
| `manage-promotions` | store-manager | manage promotions | must | promotions |
| `loyalty-points` | cashier | loyalty points | should | customer-lookup, tender |
| `gift-card-store-credit` | cashier | gift card store credit | should | gift-cards, tender |
| `layaway` | cashier | layaway | should | layaway |
| `manage-catalog` | store-manager | manage catalog | must | product-catalog |
| `purchase-orders` | stock-keeper | purchase orders | should | purchase-orders |
| `receive-goods` | stock-keeper | receive goods | must | goods-receipt |
| `stock-take` | stock-keeper | stock take | must | stock-count |
| `stock-adjust` | stock-keeper | stock adjust | must | stock-count, manager-pin |
| `stock-transfer` | stock-keeper | stock transfer | should | transfers |
| `manage-suppliers` | store-manager | manage suppliers | should | suppliers |
| `e-invoicing` | accountant | e invoicing | must | einvoice-status |
| `customer-display` | customer | customer display | should | customer-display |
| `cash-management` | cashier | cash management | must | cash-management, z-report |
| `reports-shrinkage` | owner | reports shrinkage | must | reports |
| `print-labels` | stock-keeper | print labels | must | labels |
| `staff-roles` | owner | staff roles | must | staff-roles |
| `multi-store` | owner | multi store | should | store-switcher |
| `offline-sync` | cashier | offline sync | must | sync-status |

## 4. Scope IN

- `checkout` — pack must-have
- `barcode-scan` — pack must-have
- `plu-lookup` — pack must-have
- `weighed-items` — pack must-have
- `variants` — pack must-have
- `tender-cash-card-wallet` — pack must-have
- `split-tender` — pack must-have
- `receipt-bilingual-qr` — pack must-have
- `returns-exchanges` — pack must-have
- `price-override` — pack must-have
- `promotions-engine` — pack must-have
- `catalog-management` — pack must-have
- `goods-receipt` — pack must-have
- `stock-count` — pack must-have
- `stock-adjustments` — pack must-have
- `label-printing` — pack must-have
- `cash-management` — pack must-have
- `z-report` — pack must-have
- `e-invoice` — pack must-have
- `reports-core` — pack must-have
- `shrinkage-report` — pack must-have
- `staff-roles` — pack must-have
- `offline-queue` — pack must-have
- `audit-log` — pack must-have
- `loyalty` — enabled by loyalty = true [D:loyalty]
- `stock-transfers` — enabled by stock-transfer = true [D:stock-transfer]

## 5. Scope OUT

- `gift-cards` — not enabled by any decision; later phase
- `store-credit` — not enabled by any decision; later phase
- `layaway` — not enabled by any decision; later phase
- `purchase-orders` — not enabled by any decision; later phase
- `supplier-management` — not enabled by any decision; later phase
- `multi-store` — not enabled by any decision; later phase
- `customer-display` — not enabled by any decision; later phase
- `accounting-sync` — not enabled by any decision; later phase
- `marketplace-sync` — not enabled by any decision; later phase
- `serial-warranty` — not enabled by any decision; later phase
- `khaata-credit` — not enabled by any decision; later phase
- `whatsapp-receipts` — not enabled by any decision; later phase

## 6. Non-functional requirements

- Offline: required [D:offline]
- Latency: scan to line p95 100 ms; search p95 200 ms; tender p95 500 ms
- Devices: scanners: ['usb-hid', 'camera', 'bluetooth']
- Languages: ar, en (RTL for ar/ur) [D:region]
- Other: sync_recovery_s 60; catalog_size_min 50000; concurrent_terminals_min 4; label_printer ['zebra-zpl', 'tsc-tspl']; receipt_printer thermal-80mm; scale ['ean13-prefix-2', 'serial']; rtl required; font_min_px 16; touch_min_dp 48; uptime 99.5%; backups daily

## 7. Integrations

| Category | Chosen | Source |
|----------|--------|--------|
| payments | network-intl | [D:payments] |
| accounting | zoho | pack default |
| marketplaces | noon | pack default |
| scanners | usb-hid | pack default |
| label_printers | zebra-zpl | pack default |
| scales | scale-ean13-prefix-2 | pack default |
| printers | escpos-network | pack default |
| hardware | cash-drawer | pack default |
| messaging | whatsapp-receipts | pack default |
| einvoicing | sa-zatca | pack default |

## 8. Regional and compliance

- Region: SA [D:region]
- tax: VAT 15%
- inclusive default: True
- receipt lang: ar, en
- einvoice: ZATCA Fatoora phase 2: simplified tax invoice with TLV QR, reported within 24h
- currency: SAR
- minor units: 2
- rounding: nearest halala, once per sale
- returns: 7-day return or exchange for unused goods; policy in clear Arabic
- Must controls: `C-ALL-01`, `C-ALL-02`, `C-ALL-03`, `C-ALL-04`, `C-ALL-05`, `C-ALL-06`, `C-ALL-07`, `C-ALL-08`, `C-SA-01`, `C-SA-02`, `C-SA-03`
- Should controls: `C-ALL-09`, `C-ALL-10`, `C-SA-04`

## 9. Success metrics

1. Scan-to-line latency p95 at or below 100 ms over each trading week (`scan-and-sell`).
2. 100% of sales reported to ZATCA within 24 hours, measured daily (`e-invoicing`).
3. Variant stock accuracy at or above 98% at each monthly stock take (`stock-take`).
4. A return or exchange completed in under 60 seconds median over each month (`return-exchange`).
5. Zero lost sales during offline periods; queue drained within 60 s of reconnect, measured per incident (`offline-sync`).

## 10. Open assumptions

Confirmed decisions (human, brief, derived):

- `region` = "SA" — brief: brief matched 'riyadh' [D:region]
- `branches` = "single" — brief: brief matched 'one store' [D:branches]
- `variants` = true — brief: brief matched 'colour' [D:variants]
- `loyalty` = true — brief: brief matched 'loyalty' [D:loyalty]
- `payment-provider-name` = "Network International" — agent-fact: derived from payments=network-intl [D:payment-provider-name]

Assumptions taken from pack defaults; each can be changed by editing `.foundry/decisions.yaml`:

- `einvoice` = true — timeout-default; changeable [D:einvoice]
- `payments` = "network-intl" — timeout-default; changeable [D:payments]
- `weighed-items` = false — timeout-default; changeable [D:weighed-items]
- `offline` = true — timeout-default; changeable [D:offline]
- `gift-cards` = false — timeout-default; changeable [D:gift-cards]
- `customer-credit` = false — pack-default; changeable [D:customer-credit]
- `stock-transfer` = true — pack-default; changeable [D:stock-transfer]
