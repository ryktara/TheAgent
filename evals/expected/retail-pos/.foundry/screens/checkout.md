---
id: "checkout"
jobs: ["scan-and-sell", "sell-weighed-item", "price-override"]
personas: ["cashier", "store-manager"]
route: "/checkout"
routes: [{path: "/checkout"}]
layout: "action-bar / high density"
components: ["badge", "banner-offline", "button", "drawer", "empty-state", "numpad", "pin-pad", "quantity-stepper", "search", "skeleton", "toast", "virtual-list"]
data:
  reads: ["sale_get", "sale_list"]
  writes: ["sale_create", "sale_line_price_override", "sale_line_sell_weighed_item", "sale_scan_and_sell", "sale_update"]
  events: []
offline: true
print: false
---

# checkout

## Purpose

Scan-first selling: barcode, PLU, weighed items, variants, promotions, customer, park and tender

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| checkout                                                     |
+--------------------------------------------------------------+
| Top: big search field with sc | left 60%: basket lines (newe |
| Top: big search field with sc | left 60%: basket lines (newe |
| Top: big search field with sc | left 60%: basket lines (newe |
+--------------------------------------------------------------+
| right 40%: totals                                            |
+--------------------------------------------------------------+
| promotions applied                                           |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| checkout                         |
+----------------------------------+
| Top: big search field with scan  |
|                                  |
| left 60%: basket lines (newest o |
|                                  |
| right 40%: totals                |
|                                  |
| promotions applied               |
|                                  |
+----------------------------------+
```

Components from screens.md: ScanField, BasketList, TotalsPanel, Numpad, PromoBadge, ActionBar, ParkedSalesDrawer

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Scan, type PLU/name, change qty (numpad), void line, price override (PIN), attach customer, park, recall, Pay | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | "Scan an item to start" | لا يوجد شيء هنا بعد. <!-- unreviewed --> | from screens.md |
| loading | Loading… | جارٍ التحميل… <!-- unreviewed --> | copy.csv |
| error | Something went wrong. Retry, or contact the manager. | حدث خطأ ما. أعد المحاولة أو تواصل مع المدير. <!-- unreviewed --> | copy.csv |
| offline | banner, selling continues | غير متصل. تُحفظ التغييرات على هذا الجهاز وتُزامن عند عودة الاتصال. <!-- unreviewed --> | from screens.md |
| locked | A manager PIN is needed for this action. | هذا الإجراء يتطلب رمز المدير. <!-- unreviewed --> | copy.csv |
| success | Done. | تم. <!-- unreviewed --> | copy.csv |

## Validation and error copy

- `FRM-02` Error copy says what happened and how to fix it in one sentence.
- `FRM-01` Validate on blur; re-validate on change after the first error; summarise on submit.
- `FRM-03` Submit stays enabled; errors listed on attempt.

## Keyboard and shortcuts

| Key | Action |
|-----|--------|
| digits | scan or type barcode |
| F2 | product search |
| Enter | add line |
| F12 | pay |

## Accessibility checklist

- `A11Y-01`
- `A11Y-02`
- `A11Y-03`
- `A11Y-06`
- `A11Y-08`
- `A11Y-12`
- `A11Y-13`
- `A11Y-14`
- Screen note: Each added line is announced "Added Milk 1 L, 6.50"; errors announced assertively

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Basket and totals swap sides; amounts right-aligned in both directions

## Telemetry

- `screen.checkout.viewed` (persona, branch)
- `screen.checkout.action` (action id, duration_ms)
- `screen.checkout.error` (code)

## Open questions

- none
