---
id: "watchlist"
jobs: ["manage-watchlist"]
personas: ["retail-trader"]
route: "/watchlist"
routes: [{path: "/watchlist"}]
layout: "bottom-tabs / high density"
components: ["badge", "button", "empty-state", "search", "skeleton", "switch", "tabs", "toast", "virtual-list"]
data:
  reads: ["watchlist_get", "watchlist_list"]
  writes: ["watchlist_create", "watchlist_manage_watchlist", "watchlist_update"]
  events: []
offline: false
print: false
---

# watchlist

## Purpose

Home screen: user Watchlist rows with live Quote per Instrument

Role access: retail-trader.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| watchlist                                                    |
+--------------------------------------------------------------+
| List tabs                     | rows: symbol                 |
| List tabs                     | rows: symbol                 |
| List tabs                     | rows: symbol                 |
+--------------------------------------------------------------+
| name                                                         |
+--------------------------------------------------------------+
| last                                                         |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| watchlist                        |
+----------------------------------+
| List tabs                        |
|                                  |
| rows: symbol                     |
|                                  |
| name                             |
|                                  |
| last                             |
|                                  |
+----------------------------------+
```

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Add/remove symbol, reorder, switch list, tap row → instrument-detail, swipe → quick trade | primary | `button` |

## States

| State | Copy (en) | Copy (ur) | Notes |
|-------|-----------|-----------|-------|
| empty | suggested lists | ابھی یہاں کچھ نہیں ہے۔ <!-- unreviewed --> | from screens.md |
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
| Arrows | move between instruments |
| Enter | open instrument |

## Accessibility checklist

- `A11Y-01`
- `A11Y-02`
- `A11Y-03`
- `A11Y-08`
- `A11Y-12`
- `A11Y-13`
- `A11Y-14`
- `A11Y-16`

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`

## Telemetry

- `screen.watchlist.viewed` (persona, branch)
- `screen.watchlist.action` (action id, duration_ms)
- `screen.watchlist.error` (code)

## Open questions

- none
