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
| Receipt                                                      |
+----------------------------+---------------------------------+
| +------------------------+ | Send                            |
| | Store name  / VAT no.  | | [Print]                         |
| | Simplified tax invoice | | [Email]                         |
| | Abaya Blk/M     250.00 | | [WhatsApp]                      |
| | VAT 15%          69.00 | | [Gift receipt (no prices)]      |
| | Total SAR       529.00 | | [Reprint (marked COPY)]         |
| | [ZATCA QR]             | |                                 |
| +------------------------+ | ZATCA: reported / pending       |
+----------------------------+---------------------------------+
```

Phone:

```
+----------------------------------+
| Receipt                          |
+----------------------------------+
| Store / VAT no.                  |
| Abaya Blk/M          250.00      |
| Total SAR            529.00      |
| [ZATCA QR]   ZATCA: pending      |
+----------------------------------+
| [Print] [Email] [WhatsApp]       |
| [Gift receipt] [Reprint]         |
+----------------------------------+
```

Components from screens.md: ReceiptRender (bilingual), QrBlock, SendOptions

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Print | primary | `button` |
| Choose send channel (email, WhatsApp) | secondary | `select` |
| Gift receipt | secondary | `button` |
| Reprint (manager PIN) | secondary | `button` |
## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No receipt for this sale yet. | لا يوجد إيصال لهذه العملية بعد. | reviewed |
| loading | Preparing receipt… | جارٍ تجهيز الإيصال… | reviewed |
| error | Printer offline. Receipt queued; send it by WhatsApp or email. | الطابعة غير متصلة. الإيصال في الانتظار؛ أرسله عبر واتساب أو البريد. | reviewed |
| offline | Offline. The ZATCA QR is ready; reporting happens when the connection returns. | لا يوجد اتصال. رمز QR جاهز، ويتم الإبلاغ لهيئة الزكاة عند عودة الاتصال. | reviewed |
| locked | Reprint needs a manager PIN. | إعادة الطباعة تحتاج رمز المدير. | reviewed |
| success | Printed. | تمت الطباعة. | reviewed |
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

- Reprint is locked but `pin-pad` is not in this screen's components; confirm the PIN is collected by the manager-pin screen.
