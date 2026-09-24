---
id: "cash-management"
jobs: ["cash-management"]
personas: ["cashier"]
route: "/cash-management"
routes: [{path: "/cash-management"}]
layout: "action-bar / high density"
components: ["button", "drawer", "empty-state", "numpad", "pin-pad", "skeleton", "toast", "virtual-list"]
data:
  reads: ["cash_drawer_session_get", "cash_drawer_session_list"]
  writes: ["cash_drawer_session_cash_management"]
  events: []
offline: true
print: false
---

# cash-management

## Purpose

Open drawer with float, cash drops, pickups, paid-outs, close with blind count

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| Cash drawer  Till 2  Open since 08:00        [ Close drawer ]|
+--------------------------------------------------------------+
| Session summary            | Denomination   Count   SAR      |
| Float        500.00        | 500            [  2 ] 1,000.00  |
| Cash sales 3,240.00        | 100            [ 14 ] 1,400.00  |
| Drops     -2,000.00        | 50             [  9 ]   450.00  |
+--------------------------------------------------------------+
| 10:42 Drop -2,000.00   11:05 Paid-out -35.00  [ Drop ] [Pick]|
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Cash drawer  Till 2   Open       |
+----------------------------------+
| Expected hidden (blind count)    |
| 500 [ 2 ]   100 [ 14 ]  50 [ 9 ] |
| [ numpad ]                       |
+----------------------------------+
| 10:42 Drop -2,000.00             |
| [ Drop ] [ Pickup ] [ Close ]    |
+----------------------------------+
```

Components from screens.md: DenominationGrid, Numpad

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Open with float | primary | `button` |
| Cash drop | secondary | `button` |
| Pickup or paid-out | secondary | `drawer` |
| Count by denomination | primary | `numpad` |
| Close drawer | primary | `button` |
| Approve variance | secondary | `pin-pad` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No drawer open. Enter the opening float to start. | لا يوجد درج مفتوح. أدخل الرصيد الافتتاحي للبدء. | copy.csv |
| loading | Loading drawer session… | جارٍ تحميل جلسة الدرج… | copy.csv |
| error | The count could not be saved. Recount and try again. | تعذّر حفظ العدّ. أعد العدّ ثم حاول مرة أخرى. | copy.csv |
| offline | Offline. Cash events are saved on this device and sync when the connection returns. | لا يوجد اتصال. تُحفظ حركات النقد على هذا الجهاز وتُزامن عند عودة الاتصال. | copy.csv |
| locked | Variance is above policy. A manager PIN is needed to close. | الفرق يتجاوز الحد المسموح. يلزم رمز المدير للإغلاق. | copy.csv |
| success | Drawer closed. Variance 0.00 SAR. | تم إغلاق الدرج. الفرق 0.00 ر.س. | copy.csv |

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
- Screen note: Totals announced

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Mirrors

## Telemetry

- `screen.cash-management.viewed` (persona, branch)
- `screen.cash-management.action` (action id, duration_ms)
- `screen.cash-management.error` (code)

## Open questions

- Drawer cash limit that triggers the drop prompt, and the variance policy amount, are not set.
