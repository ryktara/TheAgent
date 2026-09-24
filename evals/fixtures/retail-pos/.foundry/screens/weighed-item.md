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
| Sell by weight                                      [Close]  |
+-------------------------------+------------------------------+
| PLU grid                      |  Weight (kg)                 |
| [img][img][img]               |        1.250                 |
| [img][img][img]               |  Tare: (None)(Bag)(Box)      |
| [img][img][img]               |  Price/kg        40.00       |
|                               |  Price           50.00       |
| or scan scale label           |  [ 7 ][ 8 ][ 9 ] ...         |
+-------------------------------+------------------------------+
|                                    [Cancel]   [  Accept  ]   |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Sell by weight              [X]  |
+----------------------------------+
| [img][img][img]  (PLU grid)      |
+----------------------------------+
| Weight kg          1.250         |
| Tare: (None)(Bag)(Box)           |
| 40.00 /kg      Price 50.00       |
+----------------------------------+
| [Cancel]         [   Accept   ]  |
+----------------------------------+
```

Components from screens.md: PluGrid, ScaleReadout, TareChips, Numpad

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Pick PLU | primary | `button` |
| Choose tare | secondary | `chip` |
| Enter weight manually (manager PIN) | secondary | `pin-pad` |
| Key in weight | secondary | `numpad` |
| Accept | primary | `button` |
## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Pick an item or scan a scale label. | اختر صنفًا أو امسح ملصق الميزان. | reviewed |
| loading | Reading the scale… | جارٍ قراءة الميزان… | reviewed |
| error | Weight is unstable or zero. Wait, then try again. | الوزن غير مستقر أو صفر. انتظر ثم حاول مجددًا. | reviewed |
| offline | Scale offline. Manual weight needs a manager PIN. | الميزان غير متصل. إدخال الوزن يدويًا يحتاج رمز المدير. | reviewed |
| locked | A manager PIN is needed to enter weight by hand. | إدخال الوزن يدويًا يحتاج رمز المدير. | reviewed |
| success | Added {item}, {weight} kg, {price}. | أُضيف {item}، {weight} كغ، {price}. | reviewed |
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

- A clothing shop in Riyadh likely sells nothing by weight; confirm whether this screen stays in scope.
