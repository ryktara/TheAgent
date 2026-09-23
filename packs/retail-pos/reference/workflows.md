# Retail POS — workflows

Notation: (S) server step; → state transition; ✗ failure path. Every transition on Sale, Tender,
Return, CashDrawerSession, Promotion and StockCount writes an audit event (see compliance.md).

## 1. Cashier: scan and sell

| Step | Actor | Action | Transition | Failure |
|-----:|-------|--------|------------|---------|
| 1 | cashier | First scan or PLU | Sale open; SaleLine active | unknown barcode ✗ toast, product-search |
| 2 | cashier | Keep scanning; same barcode increments qty | SaleLine qty +1 | discontinued ✗ blocked |
| 3 | system | Evaluate promotions after every line | Promotion applied, badges shown | conflicting promos ✗ priority rule |
| 4 | cashier | Weighed item: PLU + scale, or scan prefix-2 label | SaleLine weight_g set | unstable scale ✗ wait |
| 5 | cashier | Attach customer (optional) | LoyaltyAccount linked | new customer ✗ quick-create |
| 6 | cashier | Pay | Sale open → tendering | |
| 7 | cashier | Tender(s) until remaining == 0 | Tender captured; Sale → paid | declined ✗ other tender |
| 8 | system | Receipt number, fiscal QR, stock out | Receipt issued; StockMovement sale per line | fiscal offline ✗ queue SyncEvent |
| 9 | (S) | Fiscal report (ZATCA/FBR/ETA) | Receipt → reported | failed ✗ retry, alert at 20 h |

Park and recall: Sale open → parked; recall on any till of the store → open.

## 2. Cashier: split tender and gift card

1. Amount due shown; cashier taps Gift card, scans code → balance shown.
2. Redeem min(balance, due) → Tender gift-card captured; GiftCard.balance decremented atomically.
3. Remaining paid by card terminal → Tender card captured with approval code.
4. ✗ Terminal timeout: status query before retry; never double-charge.

## 3. Cashier: return and exchange

| Step | Actor | Action | Transition | Failure |
|-----:|-------|--------|------------|---------|
| 1 | cashier | Receipt lookup (scan receipt QR, number, phone, date+amount) | Sale found | not found ✗ no-receipt policy |
| 2 | cashier | Pick lines and qty | Return requested | qty > returnable ✗ blocked |
| 3 | cashier | Reason, restock y/n | | outside window ✗ manager-pin |
| 4 | store-manager | Approve if required | Return → approved | deny → rejected |
| 5 | cashier | Refund to original tender or store credit | Return → refunded; Tender refunded; StockMovement return | card refund offline ✗ store credit or queue |
| 6 | cashier | Exchange: new items to checkout with return credit | Return → exchanged; new Sale | difference paid or refunded |
| 7 | system | Loyalty points reversed; fiscal credit note reported | LoyaltyAccount updated | |

## 4. Store manager: price override and promotions

- Override: cashier taps line → new price → manager-pin → SaleLine override_by set, reason stored.
  Over the manager's override_limit_pct ✗ "Needs owner".
- Promotions: create (BOGO, mix-and-match group, tiered spend, percent/amount), schedule, preview
  on sample basket → scheduled → active at start → expired at end. Shelf labels reprinted on start.

## 5. Stock keeper: purchase order to goods receipt

1. Reorder suggestions (on hand below reorder_point) → PurchaseOrder draft → sent to Supplier.
2. Delivery: goods-receipt, pick PO, scan items; received ≤ ordered + tolerance.
3. Post → GoodsReceipt posted; StockMovement receive per line; PO partially-received or received.
4. Damaged or wrong items → return to vendor (RTV) StockMovement with Supplier reference.
5. Print labels for received items (labels queue prefilled).

## 6. Stock keeper: stock take and adjustment

1. Plan count (full or cycle: category, bin, ABC class) → StockCount planned → counting (snapshot).
2. Scan and count with numpad; selling continues; movements after snapshot reconciled.
3. Review variance by value → store-manager approves → posted.
4. One StockMovement count-variance per Variant with non-zero variance; shrinkage report updated.
5. Ad-hoc adjustment (damage, expiry, theft, sample) with reason and manager PIN.

## 7. Stock keeper: transfer between stores

1. Create Transfer draft at source → dispatch → StockMovement out; Transfer in-transit.
2. Target scans on arrival → received; StockMovement in. Short/over → discrepancy for owner review.

## 8. Cashier: cash management

1. Shift start: open drawer with float (denominations) → CashDrawerSession open.
2. Drawer above limit → prompt cash drop to safe; pickups by manager; paid-outs with reason.
3. Close: blind count by denomination → expected vs counted → variance; above policy needs PIN.
4. Store manager prints Z once all sessions closed → day locked.

## 9. Accountant: e-invoicing and sync

1. Watch einvoice-status daily; failed rows retried; ZATCA/ETA pending older than 20 h escalated.
2. Export sales, tax and tender totals to accounting (Zoho, QuickBooks, Xero, Odoo) nightly.
3. Month end: stock valuation report; shrinkage posted to expense.

## 10. Owner: reports and staff

1. Daily: sales, margin, top items, staff performance; weekly: dead stock and shrinkage.
2. Staff: add, set role and override limit, suspend; PIN resets are audited.
3. Multi-store: store switcher, cross-store stock view, transfers.

## 11. Cashier: layaway

1. Basket → Layaway with deposit ≥ policy percent → stock reserved.
2. Instalments via tender screen; balance decreases.
3. Balance 0 → collect → Sale paid and receipt; expired → reservation released, refund per policy.

## 12. Cashier: khaata / udhaar (PK, baqala)

1. Customer attached; tender kind khaata; allowed only up to credit_limit.
2. Customer pays later → payment against khaata_balance with receipt.
3. Statement printable or sent by WhatsApp.

## 13. Customer: customer display

1. Idle: store promotions slideshow.
2. Each scan shows the line large and the running total; promotions shown as savings.
3. At tender: amount due, QR for wallet pay where supported; after: thank you, points earned.

## 14. Offline

- Scanning, pricing, promotions and cash/gift-card tenders work offline from the local catalog.
- Receipt numbers come from a per-device block; fiscal submission queued; card needs terminal.
- On reconnect SyncEvents replay in device_seq order; conflicts shown on sync-status.

## 15. Stock keeper: label printing

| Step | Actor | Action | Transition | Failure |
|-----:|-------|--------|------------|---------|
| 1 | system | Price change, promotion start or GRN adds items to the label queue | queue item | |
| 2 | stock-keeper | Review queue, pick template (shelf edge, sticker, jewellery tag) | | template missing field ✗ fix product |
| 3 | stock-keeper | Set copies (default = received qty for stickers, 1 for shelf edge) | | |
| 4 | stock-keeper | Print to Zebra (ZPL), TSC (TSPL) or Dymo | queue item printed | printer offline ✗ keep in queue |
| 5 | stock-keeper | Walk the aisle, replace shelf labels; scan label to confirm | label confirmed | mismatch ✗ reprint |
