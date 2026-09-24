---
id: "open-orders"
jobs: ["amend-cancel-order"]
personas: ["retail-trader"]
route: "/open-orders"
routes: [{path: "/open-orders"}]
layout: "bottom-tabs / high density"
components: ["button", "empty-state", "pin-pad", "quantity-stepper", "skeleton", "tabs", "toast", "virtual-list"]
data:
  reads: ["order_get", "order_list"]
  writes: ["order_amend_cancel_order", "order_create", "order_update"]
  events: []
offline: false
print: false
---

# open-orders

## Purpose

Working and recent Order rows with amend and cancel

Role access: retail-trader.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| open-orders                                                  |
+--------------------------------------------------------------+
| Tabs Working / Filled / Cance | OCO and bracket children gro |
| Tabs Working / Filled / Cance | OCO and bracket children gro |
| Tabs Working / Filled / Cance | OCO and bracket children gro |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| open-orders                      |
+----------------------------------+
| Tabs Working / Filled / Cancelle |
|                                  |
| OCO and bracket children grouped |
|                                  |
+----------------------------------+
```

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Cancel, cancel all, amend price/qty, view Fill list | primary | `button` |

## States

| State | Copy (en) | Copy (ur) | Notes |
|-------|-----------|-----------|-------|
| empty | Nothing here yet. | ابھی یہاں کچھ نہیں ہے۔ <!-- unreviewed --> | copy.csv |
| loading | Loading… | لوڈ ہو رہا ہے… <!-- unreviewed --> | copy.csv |
| error | Something went wrong. Retry, or contact the manager. | کچھ غلط ہو گیا۔ دوبارہ کوشش کریں یا منیجر سے رابطہ کریں۔ <!-- unreviewed --> | copy.csv |
| offline | Offline. Changes are saved on this device and sync when the connection returns. | آف لائن۔ تبدیلیاں اس ڈیوائس پر محفوظ ہیں اور کنکشن واپس آنے پر سنک ہوں گی۔ <!-- unreviewed --> | copy.csv |
| locked | A manager PIN is needed for this action. | اس عمل کے لیے منیجر پن درکار ہے۔ <!-- unreviewed --> | copy.csv |
| success | Done. | ہو گیا۔ <!-- unreviewed --> | copy.csv |

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
- `A11Y-06`
- `A11Y-08`
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`

## Telemetry

- `screen.open-orders.viewed` (persona, branch)
- `screen.open-orders.action` (action id, duration_ms)
- `screen.open-orders.error` (code)

## Open questions

- none
