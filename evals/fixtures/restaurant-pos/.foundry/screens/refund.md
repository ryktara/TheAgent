---
id: "refund"
jobs: ["refund"]
personas: ["manager"]
route: "/refund"
layout: "action-bar / high density"
components: ["banner-offline", "button", "dialog", "empty-state", "pin-pad", "receipt-preview", "search", "select", "skeleton", "toast"]
data:
  reads: ["refund_get", "refund_list"]
  writes: ["refund_refund"]
  events: []
offline: true
print: true
---

# refund

## Purpose

Refund a paid order fully or partly to the original tender

Role access: manager.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| refund                                                       |
+--------------------------------------------------------------+
| Search bar                    | order summary                |
| Search bar                    | order summary                |
| Search bar                    | order summary                |
+--------------------------------------------------------------+
| line selector                                                |
+--------------------------------------------------------------+
| refund summary                                               |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| refund                           |
+----------------------------------+
| Search bar                       |
|                                  |
| order summary                    |
|                                  |
| line selector                    |
|                                  |
| refund summary                   |
|                                  |
+----------------------------------+
```

Components from screens.md: OrderSearch, LineSelector, RefundSummary

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Find order (receipt number, scan QR), select lines or amount, reason, PIN, process | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Choose a tender to take payment. | اختر طريقة الدفع. <!-- unreviewed --> | copy.csv |
| loading | Waiting for the card terminal… | بانتظار جهاز الدفع… <!-- unreviewed --> | copy.csv |
| error | exceeds captured | تم رفض الدفع. جرّب طريقة أخرى. <!-- unreviewed --> | from screens.md |
| offline | cash only | جهاز الدفع غير متصل. اقبل نقدًا أو أدخل رمز الموافقة. <!-- unreviewed --> | from screens.md |
| locked | Discount over policy needs a manager PIN. | الخصم فوق السياسة يتطلب رمز المدير. <!-- unreviewed --> | copy.csv |
| success | Paid. Change {change}. | تم الدفع. الباقي {change}. <!-- unreviewed --> | copy.csv |

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
- `A11Y-04`
- `A11Y-06`
- `A11Y-08`
- `A11Y-10`
- `A11Y-12`
- Screen note: Line checkboxes with amounts announced

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Mirrors

## Telemetry

- `screen.refund.viewed` (persona, branch)
- `screen.refund.action` (action id, duration_ms)
- `screen.refund.error` (code)

## Open questions

- none
