---
id: "paper-mode"
jobs: ["paper-trade"]
personas: ["retail-trader"]
route: "/paper-mode"
routes: [{path: "/paper-mode"}]
layout: "bottom-tabs / high density"
components: ["button", "empty-state", "skeleton", "switch", "toast"]
data:
  reads: ["paper_account_get", "paper_account_list"]
  writes: ["paper_account_create", "paper_account_paper_trade", "paper_account_update"]
  events: []
offline: false
print: false
---

# paper-mode

## Purpose

Toggle into a PaperAccount with virtual funds for practice

Role access: retail-trader.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| paper-mode                                                   |
+--------------------------------------------------------------+
| Persistent "PAPER" watermark and amber-hatched header on eve |
| Persistent "PAPER" watermark and amber-hatched header on eve |
| Persistent "PAPER" watermark and amber-hatched header on eve |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| paper-mode                       |
+----------------------------------+
| Persistent "PAPER" watermark and |
|                                  |
+----------------------------------+
```

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Switch mode, reset balance, compare with live | primary | `button` |

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

- `screen.paper-mode.viewed` (persona, branch)
- `screen.paper-mode.action` (action id, duration_ms)
- `screen.paper-mode.error` (code)

## Open questions

- none
