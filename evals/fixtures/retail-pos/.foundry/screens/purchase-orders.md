---
id: "purchase-orders"
jobs: ["purchase-orders"]
personas: ["stock-keeper"]
route: "/purchase-orders"
routes: [{path: "/purchase-orders"}]
layout: "action-bar / high density"
components: ["button", "date-picker", "empty-state", "skeleton", "toast", "virtual-list"]
data:
  reads: ["purchase_order_get", "purchase_order_list"]
  writes: ["purchase_order_create", "purchase_order_purchase_orders", "purchase_order_update"]
  events: []
offline: true
print: false
---

# purchase-orders

## Purpose

Raise purchase orders from reorder suggestions, send to supplier

Role access: stock-keeper.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| Purchase orders   [Status v]  [Suggest from reorder] [+ New] |
+-------------------------+------------------------------------+
| PoList (by status)      | PoEditor: PO-0107  Supplier: Nada  |
| PO-0107 Draft           | Variant       Qty  Cost   Total    |
| PO-0104 Sent            | Tee M/Red     24   18.00  432.00   |
| PO-0099 Partly received | Jeans 32/Blue 12   75.00  900.00   |
| PO-0091 Overdue         | Expected [12/10/2026]  VAT 15%     |
|                         | Total SAR 1,531.80                 |
+-------------------------+------------------------------------+
| [Cancel PO]                     [Save draft]  [Send PDF]     |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Purchase orders   [Suggest]      |
+----------------------------------+
| PO-0107 Draft                    |
| PO-0099 Partly received          |
| PO-0091 Overdue                  |
+----------------------------------+
| PO-0107  Supplier: Nada          |
| Tee M/Red      24 x 18.00        |
| Expected [12/10/2026]            |
| Total SAR 1,531.80               |
+----------------------------------+
| [Cancel]     [Save] [Send PDF]   |
+----------------------------------+
```

Components from screens.md: PoList, PoEditor

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Suggest from reorder points | primary | `button` |
| Send to supplier (PDF/email) | primary | `button` |
| Save draft / edit lines | secondary | `button` |
| Set expected date | secondary | `date-picker` |
| Open PO from list | secondary | `virtual-list` |
| Cancel PO | destructive | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No purchase orders. Suggest one from reorder points. | لا توجد أوامر شراء. اقترح أمرًا من حدود إعادة الطلب. | reviewed |
| loading | Loading purchase orders… | جارٍ تحميل أوامر الشراء… | reviewed |
| error | The order could not be sent. Check the supplier email and retry. | تعذّر إرسال الأمر. تحقق من بريد المورد وأعد المحاولة. | reviewed |
| offline | Offline. Drafts are saved; sending waits for connection. | غير متصل. تُحفظ المسودات؛ الإرسال بانتظار الاتصال. | reviewed |
| locked | Cancelling a sent order needs a manager PIN. | إلغاء أمر مُرسل يتطلب رمز المدير. | reviewed |
| success | Order sent to {supplier}. | تم إرسال الأمر إلى {supplier}. | reviewed |

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
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- `A11Y-18`
- Screen note: Status as text, not colour only

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.purchase-orders.viewed` (persona, branch)
- `screen.purchase-orders.action` (action id, duration_ms)
- `screen.purchase-orders.error` (code)

## Open questions

- none
