---
id: "product-search"
jobs: ["scan-and-sell"]
personas: ["cashier"]
route: "/product-search"
routes: [{path: "/product-search"}]
layout: "action-bar / high density"
components: ["button", "chip", "empty-state", "search", "skeleton", "toast", "virtual-list"]
data:
  reads: ["sale_get", "sale_list"]
  writes: ["sale_create", "sale_scan_and_sell", "sale_update"]
  events: []
offline: true
print: false
---

# product-search

## Purpose

Find a product without a barcode: name, SKU, PLU, brand, category, in Arabic or English

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| product-search                                               |
+--------------------------------------------------------------+
| Full-height overlay: search f | category chips               |
| Full-height overlay: search f | category chips               |
| Full-height overlay: search f | category chips               |
+--------------------------------------------------------------+
| results grid with image                                      |
+--------------------------------------------------------------+
| price                                                        |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| product-search                   |
+----------------------------------+
| Full-height overlay: search fiel |
|                                  |
| category chips                   |
|                                  |
| results grid with image          |
|                                  |
| price                            |
|                                  |
+----------------------------------+
```

Components from screens.md: SearchField (debounced 80 ms, local index), CategoryChips, ResultCard, VariantMatrix

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Type, filter by category, pick variant from size/colour matrix, add to basket | primary | `button` |

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
| / | focus search |
| Enter | add to basket |
| Escape | back to checkout |

## Accessibility checklist

- `A11Y-01`
- `A11Y-02`
- `A11Y-03`
- `A11Y-08`
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- `A11Y-18`
- Screen note: Results are a listbox; arrow keys and Enter add

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Grid flows from the right; SKU and prices stay LTR

## Telemetry

- `screen.product-search.viewed` (persona, branch)
- `screen.product-search.action` (action id, duration_ms)
- `screen.product-search.error` (code)

## Open questions

- none
