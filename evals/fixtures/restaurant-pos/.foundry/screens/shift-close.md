---
id: "shift-close"
jobs: ["open-close-shift"]
personas: ["cashier"]
route: "/shift-close"
layout: "action-bar / high density"
components: ["badge", "banner-offline", "button", "data-table", "empty-state", "input", "pin-pad", "skeleton", "toast", "virtual-list"]
data:
  reads: ["shift_get", "shift_list"]
  writes: ["shift_open_close_shift"]
  events: []
offline: true
print: true
---

# shift-close

## Purpose

Count cash, reconcile tenders, close the shift, print X/Z

Role access: cashier (variance over policy needs manager PIN).

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| shift-close                                                  |
+--------------------------------------------------------------+
| Denomination grid             | expected vs counted          |
| Denomination grid             | expected vs counted          |
| Denomination grid             | expected vs counted          |
+--------------------------------------------------------------+
| variance                                                     |
+--------------------------------------------------------------+
| open orders warning                                          |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| shift-close                      |
+----------------------------------+
| Denomination grid                |
|                                  |
| expected vs counted              |
|                                  |
| variance                         |
|                                  |
| open orders warning              |
|                                  |
+----------------------------------+
```

Components from screens.md: DenominationGrid, ReconcileTable, VarianceBadge

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Count by denomination, compare with expected, note variance, close, print Z | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Fill in the fields to continue. | املأ الحقول للمتابعة. <!-- unreviewed --> | copy.csv |
| loading | Saving… | جارٍ الحفظ… <!-- unreviewed --> | copy.csv |
| error | Some fields need attention. Fix them and save again. | بعض الحقول تحتاج مراجعة. صحّحها واحفظ مرة أخرى. <!-- unreviewed --> | copy.csv |
| offline | close allowed, Z queued | تم الحفظ على هذا الجهاز وسيُزامن عند الاتصال. <!-- unreviewed --> | from screens.md |
| locked | open orders listed with jump links | رمز المدير مطلوب لتغيير هذا. <!-- unreviewed --> | from screens.md |
| success | Saved. | تم الحفظ. <!-- unreviewed --> | copy.csv |

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
- `A11Y-10`
- `A11Y-11`
- `A11Y-12`
- Screen note: Denomination inputs labelled with value

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Grid mirrors

## Telemetry

- `screen.shift-close.viewed` (persona, branch)
- `screen.shift-close.action` (action id, duration_ms)
- `screen.shift-close.error` (code)

## Open questions

- none
