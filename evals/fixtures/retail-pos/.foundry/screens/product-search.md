---
id: "product-search"
jobs: ["scan-and-sell"]
personas: ["cashier"]
route: "/product-search"
routes: [{path: "/product-search"}]
layout: "action-bar / high density"
components: ["button", "chip", "empty-state", "search", "skeleton", "toast", "virtual-list"]
data:
  reads: ["product_list", "product_get", "variant_list"]
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
| [Search name / SKU / PLU / brand (AR or EN) .....]  [Close]  |
+--------------------------------------------------------------+
| (All) (Abayas) (Thobes) (Dresses) (Kids) (Shoes) (Accs)      |
+--------------------------------------------------------------+
| +-----------+ +-----------+ +-----------+ +-----------+      |
| | [image]   | | [image]   | | [image]   | | [image]   |      |
| | Abaya Blk | | Thobe Wht | | Dress Nvy | | Scarf Red |      |
| | 250.00    | | 180.00    | | 320.00    | | 45.00     |      |
| | Stock 12  | | Stock 4   | | Stock 0   | | Stock 30  |      |
| +-----------+ +-----------+ +-----------+ +-----------+      |
+--------------------------------------------------------------+
| Size \ Colour   Black   White   Navy     (variant matrix)    |
| S / M / L       [ 3 ]   [ 5 ]   [ 0 ]    [Add to basket]     |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| [Search name / SKU / PLU ] [X]   |
+----------------------------------+
| (All) (Abayas) (Thobes) (>)      |
+----------------------------------+
| [img] Abaya Black    250.00  12  |
| [img] Thobe White    180.00   4  |
| [img] Dress Navy     320.00   0  |
| ... first 50, refine to see more |
+----------------------------------+
| Size: (S)(M)(L)  Colour: (Blk)(W)|
| [        Add to basket         ] |
+----------------------------------+
```

Components from screens.md: SearchField (debounced 80 ms, local index), CategoryChips, ResultCard, VariantMatrix

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Search by name, SKU, PLU or brand | primary | `search` |
| Filter by category | secondary | `chip` |
| Pick size and colour | primary | `chip` |
| Add to basket | primary | `button` |
## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No match. Try the SKU or scan the barcode. | لا توجد نتيجة. جرّب رمز الصنف أو امسح الباركود. | reviewed |
| loading | Searching… | جارٍ البحث… | reviewed |
| error | Search failed. Try again or scan the barcode. | تعذّر البحث. حاول مجددًا أو امسح الباركود. | reviewed |
| offline | Offline. Searching this device's catalogue; stock may be out of date. | لا يوجد اتصال. البحث في كتالوج هذا الجهاز، وقد لا يكون المخزون محدّثًا. | reviewed |
| locked | This item is restricted. Ask a manager. | هذا الصنف مقيّد. راجع المدير. | reviewed |
| success | Added to basket. | أُضيف إلى السلة. | reviewed |
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
