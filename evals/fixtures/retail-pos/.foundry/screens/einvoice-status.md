---
id: "einvoice-status"
jobs: ["e-invoicing"]
personas: ["accountant"]
route: "/einvoice-status"
routes: [{path: "/einvoice-status"}]
layout: "action-bar / high density"
components: ["button", "data-table", "empty-state", "receipt-preview", "skeleton", "toast"]
data:
  reads: ["receipt_get", "receipt_list"]
  writes: ["receipt_e_invoicing"]
  events: []
offline: true
print: false
---

# einvoice-status

## Purpose

Monitor fiscal reporting: ZATCA, FBR, ETA; retry failures

Role access: accountant.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| E-invoice status (ZATCA)    Filter [ All v ]   [ Retry all ] |
+--------------------------------------------------------------+
| Reported 1,284   | Pending 6    | Failed 2 !                 |
+--------------------------------------------------------------+
| Receipt   Time   Status     ZATCA ref     |                  |
| R-88121   09:14  Failed !   -             | [ Retry ]        |
| R-88120   09:12  Pending    -             | [ View payload ] |
| R-88119   09:10  Reported   a1b2c3...     | [ View payload ] |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| E-invoice status   Failed v      |
+----------------------------------+
| Reported 1,284 Pend 6 Failed 2 ! |
+----------------------------------+
| R-88121  09:14  Failed !         |
|   [ Retry ]  [ View payload ]    |
| R-88120  09:12  Pending          |
+----------------------------------+
```

Components from screens.md: StatusCounters, ReceiptTable

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Filter by status | secondary | `data-table` |
| Retry reporting | primary | `button` |
| View payload and response | secondary | `receipt-preview` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | All receipts are reported to ZATCA. Nothing to review. | تم إبلاغ هيئة الزكاة والضريبة والجمارك بجميع الفواتير. لا يوجد ما يتطلب المراجعة. | copy.csv |
| loading | Loading e-invoice status… | جارٍ تحميل حالة الفواتير الإلكترونية… | copy.csv |
| error | ZATCA rejected this invoice. Open the response, fix the cause, then retry. | رفضت الهيئة هذه الفاتورة. افتح الرد وعالج السبب ثم أعد المحاولة. | copy.csv |
| offline | Offline. Invoices are queued and report when the connection returns. | لا يوجد اتصال. الفواتير في قائمة الانتظار وستُبلَّغ عند عودة الاتصال. | copy.csv |
| locked | Only an accountant can retry reporting. | إعادة الإبلاغ متاحة للمحاسب فقط. | copy.csv |
| success | Invoice reported to ZATCA. | تم إبلاغ الهيئة بالفاتورة. | copy.csv |

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
- Screen note: Status text

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Mirrors

## Telemetry

- `screen.einvoice-status.viewed` (persona, branch)
- `screen.einvoice-status.action` (action id, duration_ms)
- `screen.einvoice-status.error` (code)

## Open questions

- none
