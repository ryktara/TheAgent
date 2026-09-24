---
id: "manager-pin"
jobs: ["return-exchange", "price-override", "stock-adjust"]
personas: ["cashier", "stock-keeper", "store-manager"]
route: "/manager-pin"
routes: [{path: "/manager-pin"}]
layout: "action-bar / high density"
components: ["badge", "button", "chip", "dialog", "drawer", "empty-state", "numpad", "pin-pad", "skeleton", "toast"]
data:
  reads: ["return_get", "return_list"]
  writes: ["return_create", "return_return_exchange", "return_update", "sale_line_price_override", "stock_movement_stock_adjust"]
  events: []
offline: true
print: false
---

# manager-pin

## Purpose

Approve guarded actions: price override, return outside policy, void, drawer variance, stock adjustment

Role access: store-manager.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| manager-pin                                                  |
+--------------------------------------------------------------+
| Modal: action summary (old pr | reason chips                 |
| Modal: action summary (old pr | reason chips                 |
| Modal: action summary (old pr | reason chips                 |
+--------------------------------------------------------------+
| numpad                                                       |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| manager-pin                      |
+----------------------------------+
| Modal: action summary (old price |
|                                  |
| reason chips                     |
|                                  |
| numpad                           |
|                                  |
+----------------------------------+
```

Components from screens.md: Numpad, ReasonChips, ApprovalSummary

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Enter PIN or tap badge, choose reason, approve/deny | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Choose a tender to take payment. | اختر طريقة الدفع. <!-- unreviewed --> | copy.csv |
| loading | Waiting for the card terminal… | بانتظار جهاز الدفع… <!-- unreviewed --> | copy.csv |
| error | Payment declined. Try another tender. | تم رفض الدفع. جرّب طريقة أخرى. <!-- unreviewed --> | copy.csv |
| offline | Card terminal offline. Take cash or enter the approval code. | جهاز الدفع غير متصل. اقبل نقدًا أو أدخل رمز الموافقة. <!-- unreviewed --> | copy.csv |
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
- Screen note: PIN digits masked; count announced

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Summary mirrors; numpad unchanged

## Telemetry

- `screen.manager-pin.viewed` (persona, branch)
- `screen.manager-pin.action` (action id, duration_ms)
- `screen.manager-pin.error` (code)

## Open questions

- none
