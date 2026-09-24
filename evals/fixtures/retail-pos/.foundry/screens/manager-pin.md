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
| Approval needed                                   [x] close  |
+--------------------------------------------------------------+
| ApprovalSummary: Price override - Jeans M/Blue               |
|   Old SAR 199.00  ->  New SAR 149.00   (-25%)  [limit 30%]   |
+--------------------------------------------------------------+
| Reason chips: (Damaged) (Price match) (Loyalty) (Other)      |
+------------------------------+-------------------------------+
| PIN  * * * _   (2 of 3 left) |  [7] [8] [9]                  |
| or tap staff badge           |  [4] [5] [6]                  |
|                              |  [1] [2] [3]                  |
|                              |  [<] [0] [OK]                 |
+------------------------------+-------------------------------+
| [Deny]                                          [Approve]    |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Approval needed              [x] |
+----------------------------------+
| Price override - Jeans M/Blue    |
| SAR 199.00 -> SAR 149.00 (-25%)  |
+----------------------------------+
| (Damaged) (Price match) (Other)  |
+----------------------------------+
| PIN * * * _   tap badge          |
|  [7] [8] [9]                     |
|  [4] [5] [6]                     |
|  [1] [2] [3]                     |
|  [<] [0] [OK]                    |
+----------------------------------+
| [Deny]              [Approve]    |
+----------------------------------+
```

Components from screens.md: Numpad, ReasonChips, ApprovalSummary

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Enter PIN | primary | `pin-pad` |
| Tap staff badge to identify approver | secondary | `badge` |
| Choose reason | secondary | `chip` |
| Approve | primary | `button` |
| Deny | secondary | `button` |
| Close without deciding | tertiary | `dialog` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No guarded action pending. | لا يوجد إجراء بانتظار الموافقة. | reviewed |
| loading | Checking PIN… | جارٍ التحقق من الرمز… | reviewed |
| error | Wrong PIN. {left} tries left. | رمز غير صحيح. تبقّى {left} محاولات. | reviewed |
| offline | Offline. PIN checked on this device; approval syncs later. | غير متصل. يُتحقق من الرمز على هذا الجهاز وتُزامن الموافقة لاحقًا. | reviewed |
| locked | Too many tries. Locked for 5 minutes. Over your limit: needs owner. | محاولات كثيرة. القفل لمدة 5 دقائق. يتجاوز حدّك: يلزم المالك. | reviewed |
| success | Approved by {approver}. | تمت الموافقة من {approver}. | reviewed |

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

- Offline approval: may a PIN be verified against a cached hash when offline, and for which actions (price override yes, stock adjust?).
