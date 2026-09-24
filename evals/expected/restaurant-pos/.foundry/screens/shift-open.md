---
id: "shift-open"
jobs: ["open-close-shift"]
personas: ["cashier"]
route: "/shift-open"
routes: [{path: "/shift-open"}]
layout: "action-bar / high density"
components: ["button", "empty-state", "numpad", "pin-pad", "skeleton", "toast"]
data:
  reads: ["shift_get", "shift_list"]
  writes: ["shift_open_close_shift"]
  events: []
offline: true
print: false
---

# shift-open

## Purpose

Start a shift on a device with an opening float

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| shift-open                                                   |
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
| shift-open                       |
+----------------------------------+
| header                           |
|                                  |
| content                          |
|                                  |
| action bar                       |
|                                  |
+----------------------------------+
```

Components from screens.md: Numpad, ShiftSummary

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Enter float (numpad), confirm | primary | `button` |
| resumes an unclosed shift if present | secondary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Fill in the fields to continue. | املأ الحقول للمتابعة. <!-- unreviewed --> | copy.csv |
| loading | Saving… | جارٍ الحفظ… <!-- unreviewed --> | copy.csv |
| error | unclosed shift on another device (offer takeover with PIN) | بعض الحقول تحتاج مراجعة. صحّحها واحفظ مرة أخرى. <!-- unreviewed --> | from screens.md |
| offline | Saved on this device. It will sync when online. | تم الحفظ على هذا الجهاز وسيُزامن عند الاتصال. <!-- unreviewed --> | copy.csv |
| locked | Manager PIN needed to change this. | رمز المدير مطلوب لتغيير هذا. <!-- unreviewed --> | copy.csv |
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
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- Screen note: Float field labelled with currency

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Numpad LTR

## Telemetry

- `screen.shift-open.viewed` (persona, branch)
- `screen.shift-open.action` (action id, duration_ms)
- `screen.shift-open.error` (code)

## Open questions

- none
