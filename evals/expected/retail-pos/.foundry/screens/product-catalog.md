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
| product-catalog                                              |
+--------------------------------------------------------------+
| Table with filters            | editor with tabs (details    |
| Table with filters            | editor with tabs (details    |
| Table with filters            | editor with tabs (details    |
+--------------------------------------------------------------+
| variants                                                     |
+--------------------------------------------------------------+
| barcodes                                                     |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| product-catalog                  |
+----------------------------------+
| Table with filters               |
|                                  |
| editor with tabs (details        |
|                                  |
| variants                         |
|                                  |
| barcodes                         |
|                                  |
+----------------------------------+
```

Components from screens.md: ProductTable, VariantMatrix, BarcodeList, CsvImport

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Create product, generate variant matrix, add barcodes, bulk import CSV, bulk price change | primary | `button` |

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

- none
