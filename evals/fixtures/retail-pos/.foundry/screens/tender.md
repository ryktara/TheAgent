---
id: "tender"
jobs: ["take-payment", "loyalty-points", "gift-card-store-credit"]
personas: ["cashier"]
route: "/tender"
routes: [{path: "/tender"}]
layout: "action-bar / high density"
components: ["banner-offline", "button", "empty-state", "numpad", "pin-pad", "skeleton", "split-bill", "tender-keypad", "toast", "virtual-list"]
data:
  reads: ["gift_card_get", "gift_card_list", "loyalty_account_get", "loyalty_account_list", "tender_get", "tender_list"]
  writes: ["gift_card_create", "gift_card_gift_card_store_credit", "gift_card_update", "loyalty_account_create", "loyalty_account_loyalty_points", "loyalty_account_update", "tender_create", "tender_take_payment", "tender_update"]
  events: []
offline: true
print: false
---

# tender

## Purpose

Take payment: cash, card terminal, wallet, SoftPOS, gift card, store credit, loyalty points, khaata; split tender

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
|                                       Amount due  SAR 529.00 |
+--------------------------------------------------------------+
| [Cash] [Mada/Card] [Apple Pay] [Gift card] [Store credit]    |
| [Loyalty points]                                             |
+-----------------------------------+--------------------------+
| Tendered                          | [ 7 ][ 8 ][ 9 ]          |
| Mada            300.00            | [ 4 ][ 5 ][ 6 ]          |
| Points (1,000)   50.00            | [ 1 ][ 2 ][ 3 ]          |
| Terminal: waiting for card...     | Quick: [200][500][Exact] |
+-----------------------------------+--------------------------+
| Remaining  [#########-----]  179.00      Change due  0.00    |
| [Split]                                   [   Complete   ]   |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
|           Amount due SAR 529.00  |
+----------------------------------+
| [Cash][Mada][Apple Pay][More v]  |
+----------------------------------+
| Mada 300.00  Points 50.00        |
| Remaining 179.00  Change 0.00    |
+----------------------------------+
| [ 7 ][ 8 ][ 9 ]  [200][500]      |
| [ 4 ][ 5 ][ 6 ]  [Exact]         |
| [ 1 ][ 2 ][ 3 ]                  |
| [         Complete           ]   |
+----------------------------------+
```

Components from screens.md: TenderTile, Numpad, QuickCash, RemainingBar, TerminalStatus

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Pick tender | primary | `tender-keypad` |
| Enter amount | primary | `numpad` |
| Quick cash note | secondary | `button` |
| Redeem loyalty points | secondary | `button` |
| Scan gift card | secondary | `button` |
| Split payment | secondary | `split-bill` |
| Approve over-limit discount (manager PIN) | secondary | `pin-pad` |
| Complete sale | primary | `button` |
## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Choose a payment method. | اختر طريقة الدفع. | reviewed |
| loading | Waiting for the card terminal… | بانتظار جهاز الدفع… | reviewed |
| error | Payment declined. Try again or use another method. | رُفضت العملية. حاول مجددًا أو استخدم طريقة أخرى. | reviewed |
| offline | Offline. Take cash or gift card; card only on a standalone terminal. | لا يوجد اتصال. اقبل النقد أو بطاقة الهدايا، والبطاقة فقط عبر جهاز مستقل. | reviewed |
| locked | A discount over policy needs a manager PIN. | الخصم فوق الحد المسموح يحتاج رمز المدير. | reviewed |
| success | Paid. Change {change}. | تم الدفع. الباقي {change}. | reviewed |
## Validation and error copy

- `FRM-02` Error copy says what happened and how to fix it in one sentence.
- `FRM-01` Validate on blur; re-validate on change after the first error; summarise on submit.
- `FRM-03` Submit stays enabled; errors listed on attempt.

## Keyboard and shortcuts

| Key | Action |
|-----|--------|
| digits | amount |
| Enter | complete |
| Escape | cancel card wait |

## Accessibility checklist

- `A11Y-01`
- `A11Y-02`
- `A11Y-03`
- `A11Y-06`
- `A11Y-08`
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- Screen note: Change due announced; tender tiles labelled with kind and limit

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Amount due top-right; numpad unchanged

## Telemetry

- `screen.tender.viewed` (persona, branch)
- `screen.tender.action` (action id, duration_ms)
- `screen.tender.error` (code)

## Open questions

- Customer credit (khaata) is listed in the pack; confirm whether the shop offers it or it is dropped.
