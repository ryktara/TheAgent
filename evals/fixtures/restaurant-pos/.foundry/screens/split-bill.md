---
id: "split-bill"
jobs: ["split-bill"]
personas: ["cashier"]
route: "/split-bill"
layout: "action-bar / high density"
components: ["banner-offline", "button", "empty-state", "select", "skeleton", "split-bill", "tabs", "toast"]
data:
  reads: ["order_get", "order_list"]
  writes: ["order_create", "order_split_bill", "order_update"]
  events: []
offline: true
print: false
---

# split-bill

## Purpose

Split one order into bills by seat, by item, equally, or by custom amount

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| split-bill                                                   |
+--------------------------------------------------------------+
| Mode tabs                     | columns per bill with totals |
| Mode tabs                     | columns per bill with totals |
| Mode tabs                     | columns per bill with totals |
+--------------------------------------------------------------+
| remaining balance bar                                        |
+--------------------------------------------------------------+
| Pay button per column                                        |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| split-bill                       |
+----------------------------------+
| Mode tabs                        |
|                                  |
| columns per bill with totals     |
|                                  |
| remaining balance bar            |
|                                  |
| Pay button per column            |
|                                  |
+----------------------------------+
```

Components from screens.md: ModeTabs, BillColumn, ItemDraggable, RemainingBar

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Choose mode, drag items to bill columns, set n ways, edit amount, pay each bill | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Choose a tender to take payment. | اختر طريقة الدفع. <!-- unreviewed --> | copy.csv |
| loading | Waiting for the card terminal… | بانتظار جهاز الدفع… <!-- unreviewed --> | copy.csv |
| error | "Remaining 12.50 not assigned" | تم رفض الدفع. جرّب طريقة أخرى. <!-- unreviewed --> | from screens.md |
| offline | allowed | جهاز الدفع غير متصل. اقبل نقدًا أو أدخل رمز الموافقة. <!-- unreviewed --> | from screens.md |
| locked | none | الخصم فوق السياسة يتطلب رمز المدير. <!-- unreviewed --> | from screens.md |
| success | Paid. Change {change}. | تم الدفع. الباقي {change}. <!-- unreviewed --> | copy.csv |

## Validation and error copy

- `FRM-02` Error copy says what happened and how to fix it in one sentence.
- `FRM-01` Validate on blur; re-validate on change after the first error; summarise on submit.
- `FRM-03` Submit stays enabled; errors listed on attempt.

## Keyboard and shortcuts

| Key | Action |
|-----|--------|
| Tab / Shift+Tab | move focus |
| Enter | activate |
| Escape | close dialog or sheet |

## Accessibility checklist

- `A11Y-01`
- `A11Y-02`
- `A11Y-03`
- `A11Y-08`
- `A11Y-10`
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- Screen note: Drag has keyboard alternative: select item then "Move to bill 2"

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Columns mirror; amounts right-aligned

## Telemetry

- `screen.split-bill.viewed` (persona, branch)
- `screen.split-bill.action` (action id, duration_ms)
- `screen.split-bill.error` (code)

## Open questions

- none
