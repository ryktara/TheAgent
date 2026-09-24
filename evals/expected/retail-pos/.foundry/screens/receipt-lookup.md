---
id: "receipt-lookup"
jobs: ["return-exchange"]
personas: ["cashier"]
route: "/receipt-lookup"
routes: [{path: "/receipt-lookup"}]
layout: "action-bar / high density"
components: ["badge", "button", "chip", "date-picker", "empty-state", "receipt-preview", "search", "skeleton", "toast", "virtual-list"]
data:
  reads: ["return_get", "return_list"]
  writes: ["return_create", "return_return_exchange", "return_update"]
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
| receipt-lookup                                               |
+--------------------------------------------------------------+
| Search bar with mode chips    | results list                 |
| Search bar with mode chips    | results list                 |
| Search bar with mode chips    | results list                 |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| receipt-lookup                   |
+----------------------------------+
| Search bar with mode chips       |
|                                  |
| results list                     |
|                                  |
+----------------------------------+
```

Components from screens.md: LookupModes, SaleResultRow

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Scan, type, filter date range, open sale | primary | `button` |

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
