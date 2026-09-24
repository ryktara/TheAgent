---
id: "qr-self-order"
jobs: ["take-order-qr"]
personas: ["customer"]
route: "/qr-self-order"
routes: [{path: "/qr-self-order"}]
layout: "action-bar / high density"
components: ["button", "chip", "data-table", "drawer", "empty-state", "skeleton", "toast", "virtual-list"]
data:
  reads: ["order_get", "order_list"]
  writes: ["order_create", "order_take_order_qr", "order_update"]
  events: []
offline: true
print: false
---

# qr-self-order

## Purpose

Guest orders from a phone after scanning the table QR

Role access: customer (no login).

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| qr-self-order                                                |
+--------------------------------------------------------------+
| Sticky header (table          | language toggle)             |
| Sticky header (table          | language toggle)             |
| Sticky header (table          | language toggle)             |
+--------------------------------------------------------------+
| category chips                                               |
+--------------------------------------------------------------+
| item list                                                    |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| qr-self-order                    |
+----------------------------------+
| Sticky header (table             |
|                                  |
| language toggle)                 |
|                                  |
| category chips                   |
|                                  |
| item list                        |
|                                  |
+----------------------------------+
```

Components from screens.md: LanguageToggle en/ar, ItemList, CartDrawer, HostedPaymentRedirect

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Browse menu, add items, pay now or pay at table, call waiter | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Tap an item to start the order. | اضغط على صنف لبدء الطلب. <!-- unreviewed --> | copy.csv |
| loading | Loading menu… | جارٍ تحميل القائمة… <!-- unreviewed --> | copy.csv |
| error | The menu could not be loaded. Retry. | تعذّر تحميل القائمة. أعد المحاولة. <!-- unreviewed --> | copy.csv |
| offline | Offline. Orders are saved here and sent to the kitchen when online. | غير متصل. تُحفظ الطلبات هنا وتُرسل للمطبخ عند الاتصال. <!-- unreviewed --> | copy.csv |
| locked | Void over the limit needs a manager PIN. | الإلغاء فوق الحد يتطلب رمز المدير. <!-- unreviewed --> | copy.csv |
| success | Sent to kitchen. | أُرسل إلى المطبخ. <!-- unreviewed --> | copy.csv |

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
- Screen note: WCAG AA, works without JS-heavy interactions, 200% zoom safe

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Full mirror; Arabic names from MenuItem.name_ar

## Telemetry

- `screen.qr-self-order.viewed` (persona, branch)
- `screen.qr-self-order.action` (action id, duration_ms)
- `screen.qr-self-order.error` (code)

## Open questions

- none
