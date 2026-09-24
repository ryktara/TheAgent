---
id: "product-catalog"
jobs: ["manage-catalog"]
personas: ["store-manager"]
route: "/product-catalog"
routes: [{path: "/product-catalog"}]
layout: "action-bar / high density"
components: ["button", "data-table", "empty-state", "skeleton", "tabs", "toast", "virtual-list"]
data:
  reads: ["product_get", "product_list"]
  writes: ["product_create", "product_manage_catalog", "product_update"]
  events: []
offline: true
print: false
---

# product-catalog

## Purpose

Maintain products, variants (size/colour matrix), barcodes, prices, tax, cost, MRP

Role access: store-manager.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| Products   [Search] [Category v] [Import CSV] [+ New]        |
+--------------------------------------------------------------+
| ProductTable: SKU | Name EN / AR | Price | VAT 15% | Stock   |
| TSH-01 | Basic tee / تيشيرت | 59.00 | Std | 124              |
+--------------------------------------------------------------+
| Tabs: [Details] [Variants] [Barcodes] [Stock] [Pricing]      |
| VariantMatrix       S     M     L     XL                     |
|   Red              [x]   [x]   [x]   [ ]                     |
|   Blue             [x]   [x]   [x]   [x]                     |
| ! Missing Arabic name   ! Duplicate barcode blocked          |
+--------------------------------------------------------------+
| [Bulk price change]          [Generate variants]   [Save]    |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Products        [Search] [+ New] |
+----------------------------------+
| TSH-01 Basic tee   SAR 59.00     |
| JNS-04 Slim jeans  SAR 199.00    |
+----------------------------------+
| [Details|Variants|Barcodes|...]  |
| Colour Red: S M L                |
| Colour Blue: S M L XL            |
| ! Missing Arabic name            |
+----------------------------------+
| [Generate variants]    [Save]    |
+----------------------------------+
```

Components from screens.md: ProductTable, VariantMatrix, BarcodeList, CsvImport

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Create / save product | primary | `button` |
| Browse and filter products | secondary | `data-table` |
| Switch editor tab (details, variants, barcodes, stock, pricing) | secondary | `tabs` |
| Generate variant matrix | secondary | `button` |
| Bulk import CSV | secondary | `button` |
| Bulk price change | secondary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No products yet. Add one or import a CSV. | لا توجد منتجات بعد. أضف منتجًا أو استورد ملف CSV. | reviewed |
| loading | Loading products… | جارٍ تحميل المنتجات… | reviewed |
| error | Barcode already used by another variant. | الباركود مستخدم لصنف آخر. | reviewed |
| offline | Offline. Edits are saved here and sync later. | غير متصل. تُحفظ التعديلات هنا وتُزامن لاحقًا. | reviewed |
| locked | Price and tax changes need a store manager. | تغيير السعر والضريبة يتطلب مدير المتجر. | reviewed |
| success | Product saved with {count} variants. | تم حفظ المنتج مع {count} صنفًا. | reviewed |

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
- Screen note: Matrix cells labelled "Size M, colour red"

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.product-catalog.viewed` (persona, branch)
- `screen.product-catalog.action` (action id, duration_ms)
- `screen.product-catalog.error` (code)

## Open questions

- MRP field comes from the pack; KSA has no MRP. Hide it or repurpose as compare-at price.
