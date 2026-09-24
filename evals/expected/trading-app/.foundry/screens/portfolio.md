---
id: "portfolio"
jobs: ["view-portfolio"]
personas: ["retail-trader"]
route: "/portfolio"
routes: [{path: "/portfolio"}]
layout: "bottom-tabs / high density"
components: ["button", "data-table", "empty-state", "input", "skeleton", "switch", "toast"]
data:
  reads: ["account_get", "account_list"]
  writes: ["account_create", "account_update", "account_view_portfolio"]
  events: []
offline: false
print: false
---

# portfolio

## Purpose

Account-level view: allocation, performance, cash per currency

Role access: retail-trader.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| portfolio                                                    |
+--------------------------------------------------------------+
| Equity curve                  | allocation donut with labels |
| Equity curve                  | allocation donut with labels |
| Equity curve                  | allocation donut with labels |
+--------------------------------------------------------------+
| Wallet balances                                              |
+--------------------------------------------------------------+
| realised/unrealised table                                    |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| portfolio                        |
+----------------------------------+
| Equity curve                     |
|                                  |
| allocation donut with labels     |
|                                  |
| Wallet balances                  |
|                                  |
| realised/unrealised table        |
|                                  |
+----------------------------------+
```

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Switch period, switch account (live/paper), export | primary | `button` |

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
- `A11Y-10`
- `A11Y-11`
- `A11Y-12`
- `A11Y-14`

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`

## Telemetry

- `screen.portfolio.viewed` (persona, branch)
- `screen.portfolio.action` (action id, duration_ms)
- `screen.portfolio.error` (code)

## Open questions

- none
