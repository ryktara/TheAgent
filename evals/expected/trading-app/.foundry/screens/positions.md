---
id: "positions"
jobs: ["view-positions", "handle-margin-call"]
personas: ["retail-trader"]
route: "/positions"
routes: [{path: "/positions"}]
layout: "bottom-tabs / high density"
components: ["button", "empty-state", "skeleton", "toast"]
data:
  reads: ["margin_call_get", "margin_call_list"]
  writes: ["margin_call_create", "margin_call_handle_margin_call", "margin_call_update", "position_view_positions"]
  events: []
offline: false
print: false
---

# positions

## Purpose

Open Position rows with live P&L and close actions

Role access: retail-trader.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| positions                                                    |
+--------------------------------------------------------------+
| Totals strip (equity          | used margin                  |
| Totals strip (equity          | used margin                  |
| Totals strip (equity          | used margin                  |
+--------------------------------------------------------------+
| free margin                                                  |
+--------------------------------------------------------------+
| margin level %)                                              |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| positions                        |
+----------------------------------+
| Totals strip (equity             |
|                                  |
| used margin                      |
|                                  |
| free margin                      |
|                                  |
| margin level %)                  |
|                                  |
+----------------------------------+
```

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Close, partial close, add stop/take-profit, reverse | primary | `button` |

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

- `screen.positions.viewed` (persona, branch)
- `screen.positions.action` (action id, duration_ms)
- `screen.positions.error` (code)

## Open questions

- none
