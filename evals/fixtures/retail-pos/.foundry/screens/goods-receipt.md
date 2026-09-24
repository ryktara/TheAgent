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
| Goods receipt   PO [ PO-1042 v ]  Supplier   [ Post GRN ]    |
+--------------------------------------------------------------+
| SKU / size / colour    | Ordered | Received | Var  | Scan    |
| TSH-01  M  Navy        |   24    |   24     |  0   | [____]  |
| TSH-01  L  Navy        |   24    |   20     | -4 ! | Qty [-+]|
| ABY-07  52 Black       |   10    |   11     | +1 ! | Damaged |
+--------------------------------------------------------------+
| Variance: 2 lines outside tolerance   Supplier invoice [___] |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Goods receipt       PO-1042 v    |
+----------------------------------+
| Scan barcode [______________]    |
+----------------------------------+
| TSH-01 L Navy   24 / 20   -4 !   |
| ABY-07 52 Black 10 / 11   +1 !   |
+----------------------------------+
| 2 variances    [ Post GRN ]      |
+----------------------------------+
```

Components from screens.md: ScanField, ReceiveTable, VarianceChip

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Pick purchase order | secondary | `data-table` |
| Scan item | primary | `button` |
| Set received qty | secondary | `quantity-stepper` |
| Flag damaged | secondary | `chip` |
| Post GRN | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No purchase orders are open. Pick a PO or start a blind receipt. | لا توجد أوامر شراء مفتوحة. اختر أمر شراء أو ابدأ استلامًا دون أمر. | copy.csv |
| loading | Loading purchase order lines… | جارٍ تحميل بنود أمر الشراء… | copy.csv |
| error | The receipt could not be posted. Check the variances and try again. | تعذّر ترحيل الاستلام. راجع الفروقات ثم أعد المحاولة. | copy.csv |
| offline | Offline. Scans are saved on this device and post when the connection returns. | لا يوجد اتصال. تُحفظ عمليات المسح على هذا الجهاز وتُرحَّل عند عودة الاتصال. | copy.csv |
| locked | A line is over tolerance. A store manager must approve before posting. | يوجد بند يتجاوز الحد المسموح. يلزم اعتماد مدير المتجر قبل الترحيل. | copy.csv |
| success | Goods received. Stock updated for 12 lines. | تم استلام البضاعة وتحديث المخزون لـ 12 بندًا. | copy.csv |

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

- Over-tolerance percentage per line (global or per supplier) is not decided.
- Unknown barcode: may the stock-keeper create a new size/colour variant, or only skip?
