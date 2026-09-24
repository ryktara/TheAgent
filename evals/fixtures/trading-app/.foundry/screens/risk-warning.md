---
id: "risk-warning"
jobs: ["place-order", "set-leverage"]
personas: ["retail-trader"]
route: "/risk-warning"
routes: [{path: "/risk-warning"}]
layout: "bottom-tabs / high density"
components: ["bottom-sheet", "button", "empty-state", "skeleton", "toast"]
data:
  reads: ["order_get", "order_list", "risk_limit_get", "risk_limit_list"]
  writes: ["order_create", "order_place_order", "order_update", "risk_limit_set_leverage"]
  events: []
offline: false
print: false
---

# risk-warning

## Purpose

Interstitial before first leveraged/complex product trade and after each warning version change

Role access: retail-trader.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| risk-warning                                                 |
+--------------------------------------------------------------+
| Full-screen sheet             | loss statistic               |
| Full-screen sheet             | loss statistic               |
| Full-screen sheet             | loss statistic               |
+--------------------------------------------------------------+
| plain-language bullets                                       |
+--------------------------------------------------------------+
| checkbox                                                     |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| risk-warning                     |
+----------------------------------+
| Full-screen sheet                |
|                                  |
| loss statistic                   |
|                                  |
| plain-language bullets           |
|                                  |
| checkbox                         |
|                                  |
+----------------------------------+
```

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Read, answer knowledge check, acknowledge | primary | `button` |

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
- `A11Y-08`
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- `A11Y-18`

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`

## Telemetry

- `screen.risk-warning.viewed` (persona, branch)
- `screen.risk-warning.action` (action id, duration_ms)
- `screen.risk-warning.error` (code)

## Open questions

- none
