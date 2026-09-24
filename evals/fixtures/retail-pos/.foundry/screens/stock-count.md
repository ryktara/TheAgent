---
id: "stock-count"
jobs: ["stock-take", "stock-adjust"]
personas: ["stock-keeper"]
route: "/stock-count"
routes: [{path: "/stock-count"}]
layout: "action-bar / high density"
components: ["button", "data-table", "empty-state", "numpad", "skeleton", "toast", "virtual-list"]
data:
  reads: ["stock_count_get", "stock_count_list"]
  writes: ["stock_count_create", "stock_count_stock_take", "stock_count_update", "stock_movement_stock_adjust"]
  events: []
offline: true
print: false
---

# stock-count

## Purpose

Full stock take or cycle count, plus manual adjustments (damage, theft, expiry)

Role access: stock-keeper (post: store-manager).

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| Stock count  Scope [ Category: Abayas v ]  [ Start count ]   |
+--------------------------------------------------------------+
| Count list                 | Variance review               |
| Scan [______________]      | SKU        Exp  Cnt  SAR      |
| ABY-07 52 Black   11 [123] | ABY-07 52   12   11   -180.00  |
| ABY-07 54 Black    8 [123] | TSH-01 L    20   22   +90.00   |
+--------------------------------------------------------------+
| Reason [ Damage | Theft | Expiry ]  Total -90.00  [ Post ]   |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Stock count   Abayas   Counting  |
+----------------------------------+
| Scan [__________________]        |
| ABY-07 52 Black     11  [numpad] |
| ABY-07 54 Black      8  [numpad] |
+----------------------------------+
| Variance -90.00 SAR  [ Review ]  |
| Reason [ Damage v ]  [ Post ]    |
+----------------------------------+
```

Components from screens.md: ScanField, CountRow, VarianceTable

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Start count | primary | `button` |
| Enter counted qty | primary | `numpad` |
| Review variance | secondary | `data-table` |
| Post count | primary | `button` |
| Adjust with reason | secondary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No count in progress. Start a full or cycle count. | لا يوجد جرد قيد التنفيذ. ابدأ جردًا كاملًا أو جزئيًا. | copy.csv |
| loading | Loading count lines… | جارٍ تحميل بنود الجرد… | copy.csv |
| error | The count could not be posted. Check your connection and try again. | تعذّر ترحيل الجرد. تحقّق من الاتصال ثم أعد المحاولة. | copy.csv |
| offline | Offline. Counts are saved on this device and sync when the connection returns. | لا يوجد اتصال. تُحفظ الكميات على هذا الجهاز وتُزامن عند عودة الاتصال. | copy.csv |
| locked | Only a store manager can post this count. | ترحيل هذا الجرد متاح لمدير المتجر فقط. | copy.csv |
| success | Count posted. Stock adjusted by -90.00 SAR. | تم ترحيل الجرد وتعديل المخزون بقيمة -90.00 ر.س. | copy.csv |

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
- Screen note: Counts entered with numpad

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Mirrors

## Telemetry

- `screen.stock-count.viewed` (persona, branch)
- `screen.stock-count.action` (action id, duration_ms)
- `screen.stock-count.error` (code)

## Open questions

- Variance value above which an adjustment needs a store-manager PIN is not set.
