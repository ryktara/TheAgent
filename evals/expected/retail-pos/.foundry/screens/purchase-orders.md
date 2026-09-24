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
| purchase-orders                                              |
+--------------------------------------------------------------+
| PO list by status             | editor with lines            |
| PO list by status             | editor with lines            |
| PO list by status             | editor with lines            |
+--------------------------------------------------------------+
| costs                                                        |
+--------------------------------------------------------------+
| expected date                                                |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| purchase-orders                  |
+----------------------------------+
| PO list by status                |
|                                  |
| editor with lines                |
|                                  |
| costs                            |
|                                  |
| expected date                    |
|                                  |
+----------------------------------+
```

Components from screens.md: PoList, PoEditor

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Suggest from reorder points, edit lines, send (PDF/email), cancel | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Nothing here yet. | لا يوجد شيء هنا بعد. <!-- unreviewed --> | copy.csv |
| loading | Loading… | جارٍ التحميل… <!-- unreviewed --> | copy.csv |
| error | Something went wrong. Retry, or contact the manager. | حدث خطأ ما. أعد المحاولة أو تواصل مع المدير. <!-- unreviewed --> | copy.csv |
| offline | Offline. Changes are saved on this device and sync when the connection returns. | غير متصل. تُحفظ التغييرات على هذا الجهاز وتُزامن عند عودة الاتصال. <!-- unreviewed --> | copy.csv |
| locked | A manager PIN is needed for this action. | هذا الإجراء يتطلب رمز المدير. <!-- unreviewed --> | copy.csv |
| success | Done. | تم. <!-- unreviewed --> | copy.csv |

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
