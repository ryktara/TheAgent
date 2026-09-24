---
id: "tender"
jobs: ["apply-discount", "tips-service-charge", "take-payment", "loyalty"]
personas: ["cashier"]
route: "/tender"
layout: "action-bar / high density"
components: ["banner-offline", "button", "chip", "empty-state", "numpad", "pin-pad", "select", "skeleton", "split-bill", "tender-keypad", "toast", "virtual-list"]
data:
  reads: ["customer_get", "customer_list", "order_get", "order_list", "payment_get", "payment_list"]
  writes: ["customer_create", "customer_loyalty", "customer_update", "order_apply_discount", "order_create", "order_tips_service_charge", "order_update", "payment_create", "payment_take_payment", "payment_update"]
  events: []
offline: true
print: false
---

# tender

## Purpose

Take payment with one or more tenders, apply discount, tip, service charge, loyalty

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| tender                                                       |
+--------------------------------------------------------------+
| Left: amount due              | tender list with paid amount |
| Left: amount due              | tender list with paid amount |
| Left: amount due              | tender list with paid amount |
+--------------------------------------------------------------+
| right: numpad and quick chips                                |
+--------------------------------------------------------------+
| footer: Complete                                             |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| tender                           |
+----------------------------------+
| Left: amount due                 |
|                                  |
| tender list with paid amounts    |
|                                  |
| right: numpad and quick chips    |
|                                  |
| footer: Complete                 |
|                                  |
+----------------------------------+
```

Components from screens.md: AmountDue, TenderRow, Numpad, QuickCash (exact, 50, 100, 200), TipSelector, DiscountPicker

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Cash (numpad, quick amounts), card (terminal push), wallet QR, room charge, khaata, split tender, discount, tip | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Choose a tender to take payment. | اختر طريقة الدفع. <!-- unreviewed --> | copy.csv |
| loading | Waiting for the card terminal… | بانتظار جهاز الدفع… <!-- unreviewed --> | copy.csv |
| error | Payment declined. Try another tender. | تم رفض الدفع. جرّب طريقة أخرى. <!-- unreviewed --> | copy.csv |
| offline | "Terminal offline, take cash or queue" | جهاز الدفع غير متصل. اقبل نقدًا أو أدخل رمز الموافقة. <!-- unreviewed --> | from screens.md |
| locked | discount over policy | الخصم فوق السياسة يتطلب رمز المدير. <!-- unreviewed --> | from screens.md |
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
- `A11Y-10`
- `A11Y-12`
- `A11Y-14`
- Screen note: Amount due is a live region; tender rows are buttons with paid state

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Numpad LTR; tender list mirrors

## Telemetry

- `screen.tender.viewed` (persona, branch)
- `screen.tender.action` (action id, duration_ms)
- `screen.tender.error` (code)

## Open questions

- none
