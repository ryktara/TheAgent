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
| [Scan / PLU / name ..................... ] (o) scanner ready  |
+--------------------------------------+-----------------------+
| Basket (newest on top)               | Subtotal       460.00 |
| 1  Abaya Black / M     -300- 250.00 %| VAT 15%         69.00 |
| 2  T-shirt White / L          210.00 | Promotions     -40.00 |
| ...                                  | Total SAR      529.00 |
|                                      | Loyalty: 1,250 pts    |
|                                      | [ 7 ][ 8 ][ 9 ]       |
|                                      | [ 4 ][ 5 ][ 6 ]       |
|                                      | [ 1 ][ 2 ][ 3 ]       |
+--------------------------------------+-----------------------+
| [Customer] [Void line] [Override] [Park] [Recall] [   PAY   ] |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| [Scan / PLU / name ....] (o)     |
+----------------------------------+
| 1 Abaya Black / M  -300- 250.00 %|
| 2 T-shirt White / L      210.00  |
| ...                              |
+----------------------------------+
| VAT 15% 69.00   Promos -40.00    |
| Total SAR 529.00   1,250 pts     |
+----------------------------------+
| [Qty] [Void] [More v]            |
| [            PAY               ] |
+----------------------------------+
```

Components from screens.md: ScanField, BasketList, TotalsPanel, Numpad, PromoBadge, ActionBar, ParkedSalesDrawer

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Scan or type barcode, PLU or name | primary | `search` |
| Change quantity | secondary | `quantity-stepper` |
| Enter quantity or price | secondary | `numpad` |
| Void line | secondary | `button` |
| Price override (manager PIN) | secondary | `pin-pad` |
| Attach customer | secondary | `button` |
| Park sale | secondary | `button` |
| Recall parked sale | secondary | `drawer` |
| Pay | primary | `button` |
## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Scan an item to start. | امسح أول قطعة للبدء. | reviewed |
| loading | Loading the basket… | جارٍ تحميل السلة… | reviewed |
| error | Barcode not found. Scan again or search by name. | الباركود غير موجود. امسحه مجددًا أو ابحث بالاسم. | reviewed |
| offline | Offline. Selling continues; sales sync when the connection returns. | لا يوجد اتصال. البيع مستمر، وتُزامن المبيعات عند عودة الاتصال. | reviewed |
| locked | A manager PIN is needed to change this price. | تعديل هذا السعر يحتاج رمز المدير. | reviewed |
| success | Added {item} {size}/{colour}, {price}. | أُضيف {item} {size}/{colour}، {price}. | reviewed |
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

- Out-of-stock variant: block the sale or warn only? Depends on `Store.allow_negative_stock` per store.
