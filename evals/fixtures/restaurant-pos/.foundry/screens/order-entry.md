---
id: "order-entry"
jobs: ["take-order-table", "take-order-counter", "modify-order", "send-to-kitchen", "hold-void-comp"]
personas: ["cashier", "manager", "waiter"]
route: "/order-entry"
layout: "action-bar / high density"
components: ["banner-offline", "bottom-sheet", "button", "chip", "empty-state", "modifier-sheet", "numpad", "order-card", "quantity-stepper", "search", "skeleton", "toast"]
data:
  reads: ["order_get", "order_list"]
  writes: ["order_create", "order_line_hold_void_comp", "order_line_modify_order", "order_send_to_kitchen", "order_take_order_counter", "order_take_order_table", "order_update"]
  events: []
offline: true
print: false
---

# order-entry

## Purpose

Build the order fast: categories, items, variants, modifiers, seats, courses

Role access: waiter (counter mode: cashier).

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| order-entry                                                  |
+--------------------------------------------------------------+
| Left 60%: category rail + ite | right 40%: ticket (lines gro |
| Left 60%: category rail + ite | right 40%: ticket (lines gro |
| Left 60%: category rail + ite | right 40%: ticket (lines gro |
+--------------------------------------------------------------+
| totals                                                       |
+--------------------------------------------------------------+
| action bar                                                   |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| order-entry                      |
+----------------------------------+
| Left 60%: category rail + item g |
|                                  |
| right 40%: ticket (lines grouped |
|                                  |
| totals                           |
|                                  |
| action bar                       |
|                                  |
+----------------------------------+
```

Components from screens.md: CategoryRail, ItemGrid (PLU search), TicketPanel, QtyChips, Numpad, ActionBar

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Add item, set qty (chips 1–9, numpad), open modifier sheet, assign seat, fire course, hold, send, bill | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | "Tap an item to start" | اضغط على صنف لبدء الطلب. <!-- unreviewed --> | from screens.md |
| loading | Loading menu… | جارٍ تحميل القائمة… <!-- unreviewed --> | copy.csv |
| error | The menu could not be loaded. Retry. | تعذّر تحميل القائمة. أعد المحاولة. <!-- unreviewed --> | copy.csv |
| offline | send queues locally | غير متصل. تُحفظ الطلبات هنا وتُرسل للمطبخ عند الاتصال. <!-- unreviewed --> | from screens.md |
| locked | void over limit | الإلغاء فوق الحد يتطلب رمز المدير. <!-- unreviewed --> | from screens.md |
| success | Sent to kitchen. | أُرسل إلى المطبخ. <!-- unreviewed --> | copy.csv |

## Validation and error copy

- `FRM-02` Error copy says what happened and how to fix it in one sentence.
- `FRM-01` Validate on blur; re-validate on change after the first error; summarise on submit.
- `FRM-03` Submit stays enabled; errors listed on attempt.

## Keyboard and shortcuts

| Key | Action |
|-----|--------|
| digits | PLU search |
| Enter | add highlighted item |
| Escape | close sheet |

## Accessibility checklist

- `A11Y-01`
- `A11Y-02`
- `A11Y-03`
- `A11Y-08`
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- `A11Y-18`
- Screen note: Item cards announce name, price, allergens; qty chips are a radiogroup

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Item grid and ticket swap sides; ticket amounts right-aligned in both directions

## Telemetry

- `screen.order-entry.viewed` (persona, branch)
- `screen.order-entry.action` (action id, duration_ms)
- `screen.order-entry.error` (code)

## Open questions

- none
