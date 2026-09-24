---
id: "weighed-item"
jobs: ["sell-weighed-item"]
personas: ["cashier"]
route: "/weighed-item"
routes: [{path: "/weighed-item"}]
layout: "action-bar / high density"
components: ["banner-offline", "button", "chip", "data-table", "dialog", "empty-state", "numpad", "pin-pad", "skeleton", "toast"]
data:
  reads: []
  writes: ["sale_line_sell_weighed_item"]
  events: []
offline: true
print: true
---

# weighed-item

## Purpose

Sell items priced per kg: live scale read or scale-printed EAN-13 prefix 2 label

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| weighed-item                                                 |
+--------------------------------------------------------------+
| Modal: PLU picture grid left  | live weight readout (3 decim |
| Modal: PLU picture grid left  | live weight readout (3 decim |
| Modal: PLU picture grid left  | live weight readout (3 decim |
+--------------------------------------------------------------+
| tare chips                                                   |
+--------------------------------------------------------------+
| price per kg                                                 |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| weighed-item                     |
+----------------------------------+
| Modal: PLU picture grid left     |
|                                  |
| live weight readout (3 decimals  |
|                                  |
| tare chips                       |
|                                  |
| price per kg                     |
|                                  |
+----------------------------------+
```

Components from screens.md: PluGrid, ScaleReadout, TareChips, Numpad

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Pick PLU (fruit grid), read weight, tare, accept | primary | `button` |
| or scan scale label (weight/price decoded) | secondary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Nothing here yet. | لا يوجد شيء هنا بعد. <!-- unreviewed --> | copy.csv |
| loading | Loading… | جارٍ التحميل… <!-- unreviewed --> | copy.csv |
| error | Something went wrong. Retry, or contact the manager. | حدث خطأ ما. أعد المحاولة أو تواصل مع المدير. <!-- unreviewed --> | copy.csv |
| offline | manual weight entry needs manager PIN | غير متصل. تُحفظ التغييرات على هذا الجهاز وتُزامن عند عودة الاتصال. <!-- unreviewed --> | from screens.md |
| locked | A manager PIN is needed for this action. | هذا الإجراء يتطلب رمز المدير. <!-- unreviewed --> | copy.csv |
| success | Done. | تم. <!-- unreviewed --> | copy.csv |

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
- `A11Y-14`
- Screen note: Weight announced on stable; large 48 px readout

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Grid mirrors; readout stays LTR

## Telemetry

- `screen.weighed-item.viewed` (persona, branch)
- `screen.weighed-item.action` (action id, duration_ms)
- `screen.weighed-item.error` (code)

## Open questions

- none
