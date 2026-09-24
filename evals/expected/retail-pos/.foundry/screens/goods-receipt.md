---
id: "goods-receipt"
jobs: ["receive-goods"]
personas: ["stock-keeper"]
route: "/goods-receipt"
routes: [{path: "/goods-receipt"}]
layout: "action-bar / high density"
components: ["button", "chip", "data-table", "empty-state", "quantity-stepper", "receipt-preview", "skeleton", "toast"]
data:
  reads: ["goods_receipt_get", "goods_receipt_list"]
  writes: ["goods_receipt_create", "goods_receipt_receive_goods", "goods_receipt_update"]
  events: []
offline: true
print: false
---

# goods-receipt

## Purpose

Receive stock (GRN) against a PO or blind; scan to count; record supplier invoice

Role access: stock-keeper.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| goods-receipt                                                |
+--------------------------------------------------------------+
| Ordered vs received columns   | scan field                   |
| Ordered vs received columns   | scan field                   |
| Ordered vs received columns   | scan field                   |
+--------------------------------------------------------------+
| variance highlight                                           |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| goods-receipt                    |
+----------------------------------+
| Ordered vs received columns      |
|                                  |
| scan field                       |
|                                  |
| variance highlight               |
|                                  |
+----------------------------------+
```

Components from screens.md: ScanField, ReceiveTable, VarianceChip

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Pick PO, scan items, enter qty, flag damaged, post | primary | `button` |

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
- Screen note: Variance announced

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Mirrors

## Telemetry

- `screen.goods-receipt.viewed` (persona, branch)
- `screen.goods-receipt.action` (action id, duration_ms)
- `screen.goods-receipt.error` (code)

## Open questions

- none
