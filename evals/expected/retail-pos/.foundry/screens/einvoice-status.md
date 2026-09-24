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
| einvoice-status                                              |
+--------------------------------------------------------------+
| Counters (reported            | pending                      |
| Counters (reported            | pending                      |
| Counters (reported            | pending                      |
+--------------------------------------------------------------+
| failed)                                                      |
+--------------------------------------------------------------+
| table of Receipts                                            |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| einvoice-status                  |
+----------------------------------+
| Counters (reported               |
|                                  |
| pending                          |
|                                  |
| failed)                          |
|                                  |
| table of Receipts                |
|                                  |
+----------------------------------+
```

Components from screens.md: StatusCounters, ReceiptTable

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Filter by status, retry, view payload and response | primary | `button` |

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
