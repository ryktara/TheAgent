---
id: "receipt-preview"
jobs: ["issue-receipt"]
personas: ["cashier"]
route: "/receipt-preview"
routes: [{path: "/receipt-preview"}]
layout: "action-bar / high density"
components: ["button", "data-table", "empty-state", "receipt-preview", "select", "skeleton", "toast"]
data:
  reads: ["receipt_get", "receipt_list"]
  writes: ["receipt_issue_receipt"]
  events: []
offline: true
print: true
---

# receipt-preview

## Purpose

Show and print/send the receipt with fiscal fields (TRN, QR, FBR number)

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| receipt-preview                                              |
+--------------------------------------------------------------+
| 80 mm receipt mock left       | delivery options right       |
| 80 mm receipt mock left       | delivery options right       |
| 80 mm receipt mock left       | delivery options right       |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| receipt-preview                  |
+----------------------------------+
| 80 mm receipt mock left          |
|                                  |
| delivery options right           |
|                                  |
+----------------------------------+
```

Components from screens.md: ReceiptRender (bilingual), QrBlock, SendOptions

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Print, email, WhatsApp, gift receipt (no prices), reprint (marked) | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No receipt for this order yet. | لا يوجد إيصال لهذا الطلب بعد. <!-- unreviewed --> | copy.csv |
| loading | Preparing receipt… | جارٍ تجهيز الإيصال… <!-- unreviewed --> | copy.csv |
| error | Printer offline. Receipt queued; send an e-receipt instead. | الطابعة غير متصلة. الإيصال في قائمة الانتظار؛ أرسل إيصالًا إلكترونيًا. <!-- unreviewed --> | copy.csv |
| offline | Offline. Fiscal QR will be added when reported. | غير متصل. سيُضاف رمز QR الضريبي عند الإبلاغ. <!-- unreviewed --> | copy.csv |
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
- `A11Y-10`
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- Screen note: Receipt text selectable; send buttons labelled

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Arabic-first layout for SA; bilingual columns elsewhere

## Telemetry

- `screen.receipt-preview.viewed` (persona, branch)
- `screen.receipt-preview.action` (action id, duration_ms)
- `screen.receipt-preview.error` (code)

## Open questions

- none
