---
id: "receipt-lookup"
jobs: ["return-exchange"]
personas: ["cashier"]
route: "/receipt-lookup"
routes: [{path: "/receipt-lookup"}]
layout: "action-bar / high density"
components: ["badge", "button", "chip", "date-picker", "empty-state", "receipt-preview", "search", "skeleton", "toast", "virtual-list"]
data:
  reads: ["sale_list", "sale_get", "receipt_list", "receipt_get"]
  writes: []
  events: []
offline: true
print: false
---

# receipt-lookup

## Purpose

Find the original Sale: scan receipt barcode/QR, receipt number, date + amount, customer phone, card last 4

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| [Scan receipt QR / number / phone ................] [Scan]   |
| (Receipt no.) (Date + amount) (Phone) (Card last 4)          |
| Date: [2026-09-01] to [2026-09-23]                           |
+--------------------------------------------------------------+
| #10234   2026-09-20  SAR 529.00  Mada **4411              >  |
| #10198   2026-09-18  SAR 180.00  Cash                     >  |
| #09877   2026-09-02  SAR  45.00  Cash   [Olaya branch]    >  |
| ...                                                          |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| [Scan / number / phone ] [Scan]  |
| (No.)(Date+amt)(Phone)(Card)     |
| [2026-09-01] - [2026-09-23]      |
+----------------------------------+
| #10234  09-20  529.00  Mada   >  |
| #10198  09-18  180.00  Cash   >  |
| #09877  09-02   45.00 [Olaya] >  |
+----------------------------------+
```

Components from screens.md: LookupModes, SaleResultRow

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Scan or type receipt, phone or card last 4 | primary | `search` |
| Pick lookup mode | secondary | `chip` |
| Filter date range | secondary | `date-picker` |
| Open sale | primary | `virtual-list` |
## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Not found. Try the date and amount. | لم يُعثر عليها. جرّب التاريخ والمبلغ. | reviewed |
| loading | Searching sales… | جارٍ البحث في المبيعات… | reviewed |
| error | Search failed. Try again. | تعذّر البحث. حاول مجددًا. | reviewed |
| offline | Offline. Only sales from this device are shown. | لا يوجد اتصال. تظهر مبيعات هذا الجهاز فقط. | reviewed |
| locked | Sales from other branches need a manager PIN. | مبيعات الفروع الأخرى تحتاج رمز المدير. | reviewed |
| success | Sale found. | تم العثور على العملية. | reviewed |
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
- `A11Y-13`
- `A11Y-14`
- `A11Y-16`
- Screen note: Results announce number, date, total

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Mirrors

## Telemetry

- `screen.receipt-lookup.viewed` (persona, branch)
- `screen.receipt-lookup.action` (action id, duration_ms)
- `screen.receipt-lookup.error` (code)

## Open questions

- none
