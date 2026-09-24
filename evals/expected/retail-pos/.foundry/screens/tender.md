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
| tender                                                       |
+--------------------------------------------------------------+
| Amount due 48 px top          | tender tiles                 |
| Amount due 48 px top          | tender tiles                 |
| Amount due 48 px top          | tender tiles                 |
+--------------------------------------------------------------+
| tendered list                                                |
+--------------------------------------------------------------+
| remaining bar                                                |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| tender                           |
+----------------------------------+
| Amount due 48 px top             |
|                                  |
| tender tiles                     |
|                                  |
| tendered list                    |
|                                  |
| remaining bar                    |
|                                  |
+----------------------------------+
```

Components from screens.md: TenderTile, Numpad, QuickCash, RemainingBar, TerminalStatus

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Pick tender, enter amount (numpad), quick cash notes, redeem points, scan gift card, complete | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Choose a tender to take payment. | اختر طريقة الدفع. <!-- unreviewed --> | copy.csv |
| loading | Waiting for the card terminal… | بانتظار جهاز الدفع… <!-- unreviewed --> | copy.csv |
| error | Payment declined. Try another tender. | تم رفض الدفع. جرّب طريقة أخرى. <!-- unreviewed --> | copy.csv |
| offline | card only if terminal standalone, else cash/gift card | جهاز الدفع غير متصل. اقبل نقدًا أو أدخل رمز الموافقة. <!-- unreviewed --> | from screens.md |
| locked | Discount over policy needs a manager PIN. | الخصم فوق السياسة يتطلب رمز المدير. <!-- unreviewed --> | copy.csv |
| success | Paid. Change {change}. | تم الدفع. الباقي {change}. <!-- unreviewed --> | copy.csv |

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

- none
