# Restaurant POS — workflows

Notation: (S) server step; → state transition; ✗ failure path. Every transition on Order,
Payment, Refund, Shift, Discount writes an audit event (see compliance.md).

## 1. Dine-in: seat → order → kitchen → bill → pay

| Step | Actor | Action | Transition | Failure |
|-----:|-------|--------|------------|---------|
| 1 | waiter | Tap free table, set covers | Table free → seated; Order draft | table blocked ✗ pick another |
| 2 | waiter | Add items, modifiers, seats, courses | OrderLine pending | sold-out item ✗ "86'd" |
| 3 | waiter | Send | Order draft → sent; lines pending → fired (course 1); KitchenTicket new | offline ✗ queue SyncEvent, ticket prints locally |
| 4 | kitchen | Bump lines / ticket | KitchenTicket in-progress → ready; Order → ready | recall → in-progress |
| 5 | waiter | Serve, fire next course | lines ready → served; Course fired | held course stays held |
| 6 | waiter | Print bill | Order served → billed; Table → billed | reprint marks receipt |
| 7 | cashier | Tender (see 6) | Payment captured; Order → paid | declined ✗ other tender |
| 8 | system | Close | Order paid → closed; Table → dirty; StockMovement sale per line | |
| 9 | waiter | Mark clean | Table dirty → free | |

## 2. Quick-service counter

1. cashier: order-entry in counter mode (no table); order number auto-assigned.
2. Take payment first (tender) → Order paid → then fire to kitchen (KitchenTicket new).
3. kitchen bumps → Order ready → customer display or call-out shows number.
4. Handover → Order closed. ✗ Payment declined before firing: Order stays draft, nothing fires.

## 3. QR self-order

1. customer scans table QR → session bound to Table; language chosen.
2. Adds items → Order draft (channel qr) with seat "guest".
3. Pay now: hosted payment page (SAQ A scope) → Payment captured → Order sent and fired.
   Pay at table: Order sent unpaid → bill later via workflow 1.
4. ✗ Table closed by staff: session ends with message. ✗ Kitchen closed: ordering paused.
5. Staff can see qr lines in order-entry and void with reason.

## 4. Split bill

| Mode | Rule | Rounding |
|------|------|----------|
| by seat | lines grouped by seat tag; shared lines split equally | remainder to seat 1 |
| by item | drag lines to bills | none |
| equal n ways | total / n | remainder to last bill |
| custom | amounts typed; must sum to total | none |

Each bill becomes a Payment group; Order → paid only when remaining == 0. ✗ Assigned less than
total: Complete disabled with remaining shown.

## 5. Hold, void, comp

- Hold: line pending → held; not fired; release fires it.
- Void before fire: line pending → voided, reason required, no PIN under policy limit.
- Void after fire: reason + manager PIN; KitchenTicket recalled with strike-through.
- Comp: line → comped (price 0, cost still deducted); reason + PIN always.
- Whole order void: Order → void; all Payments must be zero or refunded first.

## 6. Tender and payment

1. Amount due shown tax-inclusive (AE, SA) or exclusive with tax line (PK).
2. Discount: pick Discount; over policy → manager PIN; Order.discount_total recomputed.
3. Service charge auto per Branch rule (hotel F&B 10%), removable with PIN.
4. Tip: percent chips or amount; recorded on Payment.
5. Tender rows: cash (numpad, change computed), card (push amount to terminal, wait for approval
   code), wallet (QR shown, poll), room charge (PMS folio lookup), khaata (Customer credit).
6. (S) Payment authorised → captured; Order → paid when sum == total.
7. ✗ Terminal timeout: cancel, retry, or mark cash. ✗ Offline: card via standalone terminal, enter
   approval code manually; flagged for reconciliation.

## 7. Receipt

1. Receipt issued with gapless Branch number; language per Customer or toggle.
2. Fiscal: AE prints TRN and VAT breakdown; SA embeds TLV QR (seller, VAT no, timestamp, total,
   VAT) and (S) reports XML within 24 h; PK sends invoice to FBR (S), prints FBR number + QR.
3. ✗ SA reporting fails: receipt still prints; SyncEvent retries until acked; alert after 20 h.
4. Reprint: same number, "REPRINT" watermark, audit event.

## 8. Refund

1. manager finds paid Order; selects lines or amount.
2. Reason + PIN → Refund requested → approved.
3. (S) Provider refund to original tender → processed; cash refund opens drawer.
4. Order → refunded (partial keeps paid with refund note). Stock returns only for unserved lines.
5. ✗ Provider fails: retry; cash fallback needs owner PIN.

## 9. Shift open and close

Open: cashier enters float → Shift open (device bound). ✗ Unclosed shift elsewhere: takeover with PIN.
Close:
1. Open orders listed → must be paid, void, or transferred. ✗ Blocked otherwise.
2. Count denominations → expected (float + cash sales − cash refunds − payouts) vs counted → variance.
3. Variance over policy → manager PIN and note.
4. Shift → closed; Z-report printed (X-report available any time without closing).
5. (S) Later reconciliation with provider settlement → Shift reconciled.

## 10. Offline → reconnect sync

| Rule | Detail |
|------|--------|
| Queue | Every write becomes a SyncEvent (device_id, seq monotonic, entity, payload) |
| Order identity | client_uuid; server never renumbers; receipt numbers reserved per device block (e.g. 1000 per device) so they stay gapless per branch |
| Replay | On reconnect, events sent in seq order; server acks each |
| Conflict | Same Order edited on two devices: last-writer-wins per field; Payments append-only; voids win over edits |
| Menu changes | Server-side price changes apply to new lines only; open orders keep their prices |
| Recovery target | Queue drained within 60 s of reconnect for 500 events |
| Failure | Unresolvable conflict → SyncEvent conflict → sync-status screen, manager resolves |

## 11. Aggregator order inbound

1. (S) Platform webhook or poll → Order draft (channel talabat/deliveroo/careem/noon-food).
2. Auto-accept if enabled with default prep time; else delivery-inbox shows card with timer.
3. Accept → Order sent; KitchenTicket new. Reject → Order void with platform reason.
4. Bump → ready → (S) status pushed to platform.
5. Rider arrives → handover → Order closed; payment recorded as platform tender (settled later).
6. ✗ Platform API down: tablet-fallback mode, staff key orders manually with platform ref.

## 12. End of day

1. Every device shift closed; unsynced devices listed → resolve.
2. Day totals per tender, tax, discounts, voids, comps, refunds.
3. (S) Post journal to accounting integration; retry on failure; skip with note allowed.
4. Lock day: no edits to Orders of that day without owner PIN; archive KitchenTickets.
5. Email Z summary to owner; WhatsApp optional.

## 13. Menu change with channel pricing

1. manager edits item price for channel delivery only.
2. Change scheduled or immediate; branches receive via central sync unless per-branch mode.
3. Open orders unaffected; new lines use new price; audit event menu.price_changed.

## 14. Multi-branch daily

1. Owner views consolidated reports across Branches.
2. Central menu push: draft → publish → each Branch device pulls; per-branch price overrides kept.
3. Stock transfer between branches recorded as paired StockMovements.
