---
id: "receipt-preview"
jobs: ["print-receipt"]
personas: ["cashier"]
route: "/receipt-preview"
routes: [{path: "/receipt-preview"}]
layout: "action-bar / high density"
components: ["banner-offline", "bottom-sheet", "button", "date-picker", "empty-state", "receipt-preview", "skeleton", "toast", "virtual-list"]
data:
  reads: ["receipt_get", "receipt_list"]
  writes: ["receipt_print_receipt"]
  events: []
offline: true
print: true
---

# receipt-preview

## Purpose

Preview, print, email, WhatsApp the receipt in the chosen language

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| receipt-preview                                              |
+--------------------------------------------------------------+
| Receipt facsimile (80 mm)     | actions row                  |
| Receipt facsimile (80 mm)     | actions row                  |
| Receipt facsimile (80 mm)     | actions row                  |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| receipt-preview                  |
+----------------------------------+
| Receipt facsimile (80 mm)        |
|                                  |
| actions row                      |
|                                  |
+----------------------------------+
```

Components from screens.md: ReceiptRenderer (ESC/POS and HTML), LanguageToggle, SendSheet

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Language toggle, print, reprint (marked), send e-receipt, no receipt | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No receipt for this order yet. | لا يوجد إيصال لهذا الطلب بعد. <!-- unreviewed --> | copy.csv |
| loading | Preparing receipt… | جارٍ تجهيز الإيصال… <!-- unreviewed --> | copy.csv |
| error | fiscal QR unavailable (SA: retry within 24 h) | الطابعة غير متصلة. الإيصال في قائمة الانتظار؛ أرسل إيصالًا إلكترونيًا. <!-- unreviewed --> | from screens.md |
| offline | queue print, offer e-receipt | غير متصل. سيُضاف رمز QR الضريبي عند الإبلاغ. <!-- unreviewed --> | from screens.md |
| locked | Reprint needs a manager PIN. | إعادة الطباعة تتطلب رمز المدير. <!-- unreviewed --> | copy.csv |
| success | Printed. | تمت الطباعة. <!-- unreviewed --> | copy.csv |

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
- Screen note: Facsimile has a text alternative listing lines

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Arabic receipt right-aligned, numerals Western by default with Arabic-Indic option

## Telemetry

- `screen.receipt-preview.viewed` (persona, branch)
- `screen.receipt-preview.action` (action id, duration_ms)
- `screen.receipt-preview.error` (code)

## Open questions

- none
