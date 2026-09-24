---
id: "manager-pin"
jobs: ["hold-void-comp", "apply-discount", "refund"]
personas: ["cashier", "manager"]
route: "/manager-pin"
layout: "action-bar / high density"
components: ["badge", "banner-offline", "button", "chip", "dialog", "empty-state", "numpad", "pin-pad", "skeleton", "toast"]
data:
  reads: ["order_get", "order_list", "refund_get", "refund_list"]
  writes: ["order_apply_discount", "order_create", "order_line_hold_void_comp", "order_update", "refund_refund"]
  events: []
offline: true
print: false
---

# manager-pin

## Purpose

Approve a guarded action: void over limit, comp, discount over policy, refund, price override

Role access: manager.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| manager-pin                                                  |
+--------------------------------------------------------------+
| Modal: action summary         | reason chips                 |
| Modal: action summary         | reason chips                 |
| Modal: action summary         | reason chips                 |
+--------------------------------------------------------------+
| numpad                                                       |
+--------------------------------------------------------------+
| approver name after PIN                                      |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| manager-pin                      |
+----------------------------------+
| Modal: action summary            |
|                                  |
| reason chips                     |
|                                  |
| numpad                           |
|                                  |
| approver name after PIN          |
|                                  |
+----------------------------------+
```

Components from screens.md: ReasonChips, Numpad, ApproverBadge

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Enter 4–6 digit PIN or tap NFC card | primary | `button` |
| reason picker | secondary | `button` |
| confirm | secondary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Choose a tender to take payment. | اختر طريقة الدفع. <!-- unreviewed --> | copy.csv |
| loading | Waiting for the card terminal… | بانتظار جهاز الدفع… <!-- unreviewed --> | copy.csv |
| error | wrong PIN (3 tries then 60 s lock) | تم رفض الدفع. جرّب طريقة أخرى. <!-- unreviewed --> | from screens.md |
| offline | allowed, logged as pending-audit | جهاز الدفع غير متصل. اقبل نقدًا أو أدخل رمز الموافقة. <!-- unreviewed --> | from screens.md |
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
- `A11Y-12`
- `A11Y-13`
- Screen note: PIN field masked, announces digits entered count only

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Numpad stays LTR

## Telemetry

- `screen.manager-pin.viewed` (persona, branch)
- `screen.manager-pin.action` (action id, duration_ms)
- `screen.manager-pin.error` (code)

## Open questions

- none
