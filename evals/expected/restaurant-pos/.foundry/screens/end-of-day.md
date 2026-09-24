---
id: "end-of-day"
jobs: ["end-of-day"]
personas: ["manager"]
route: "/end-of-day"
routes: [{path: "/end-of-day"}]
layout: "action-bar / high density"
components: ["button", "empty-state", "skeleton", "toast", "virtual-list"]
data:
  reads: ["shift_get", "shift_list"]
  writes: ["shift_end_of_day"]
  events: []
offline: true
print: true
---

# end-of-day

## Purpose

Close the business day across devices, post to accounting, archive

Role access: manager.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| end-of-day                                                   |
+--------------------------------------------------------------+
| header                        | content                      |
| header                        | content                      |
| header                        | content                      |
+--------------------------------------------------------------+
| action bar                                                   |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| end-of-day                       |
+----------------------------------+
| header                           |
|                                  |
| content                          |
|                                  |
| action bar                       |
|                                  |
+----------------------------------+
```

Components from screens.md: ShiftList, DayTotals, SyncChecklist

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Review shift Zs, resolve open orders, post to accounting, lock day | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Fill in the fields to continue. | املأ الحقول للمتابعة. <!-- unreviewed --> | copy.csv |
| loading | Saving… | جارٍ الحفظ… <!-- unreviewed --> | copy.csv |
| error | accounting sync failed (retry, skip) | بعض الحقول تحتاج مراجعة. صحّحها واحفظ مرة أخرى. <!-- unreviewed --> | from screens.md |
| offline | Saved on this device. It will sync when online. | تم الحفظ على هذا الجهاز وسيُزامن عند الاتصال. <!-- unreviewed --> | copy.csv |
| locked | unsynced devices | رمز المدير مطلوب لتغيير هذا. <!-- unreviewed --> | from screens.md |
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
- `A11Y-08`
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- `A11Y-18`
- Screen note: Checklist items are checkboxes with status text

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.end-of-day.viewed` (persona, branch)
- `screen.end-of-day.action` (action id, duration_ms)
- `screen.end-of-day.error` (code)

## Open questions

- none
