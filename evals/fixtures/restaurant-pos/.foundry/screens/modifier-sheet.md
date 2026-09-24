---
id: "modifier-sheet"
jobs: ["modify-order"]
personas: ["waiter"]
route: "/modifier-sheet"
layout: "action-bar / high density"
components: ["bottom-sheet", "button", "chip", "empty-state", "modifier-sheet", "select", "skeleton", "toast"]
data:
  reads: []
  writes: ["order_line_modify_order"]
  events: []
offline: true
print: false
---

# modifier-sheet

## Purpose

Required and optional modifiers, notes, allergens, course, seat for one line

Role access: waiter.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| modifier-sheet                                               |
+--------------------------------------------------------------+
| Bottom sheet 70% height: grou | sticky Done with running lin |
| Bottom sheet 70% height: grou | sticky Done with running lin |
| Bottom sheet 70% height: grou | sticky Done with running lin |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| modifier-sheet                   |
+----------------------------------+
| Bottom sheet 70% height: groups  |
|                                  |
| sticky Done with running line to |
|                                  |
+----------------------------------+
```

Components from screens.md: ModifierGroup (chips or steppers), NoteField, AllergenChips, CourseSelect, SeatSelect

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Select modifiers (min/max enforced), type note, tag allergen, set course, set seat, Done | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Fill in the fields to continue. | املأ الحقول للمتابعة. <!-- unreviewed --> | copy.csv |
| loading | Saving… | جارٍ الحفظ… <!-- unreviewed --> | copy.csv |
| error | "Choose at least one size" | بعض الحقول تحتاج مراجعة. صحّحها واحفظ مرة أخرى. <!-- unreviewed --> | from screens.md |
| offline | Saved on this device. It will sync when online. | تم الحفظ على هذا الجهاز وسيُزامن عند الاتصال. <!-- unreviewed --> | copy.csv |
| locked | none | رمز المدير مطلوب لتغيير هذا. <!-- unreviewed --> | from screens.md |
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
- `A11Y-10`
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- Screen note: Each group is a fieldset with legend and min/max in description

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Sheet mirrors; chips wrap from the right

## Telemetry

- `screen.modifier-sheet.viewed` (persona, branch)
- `screen.modifier-sheet.action` (action id, duration_ms)
- `screen.modifier-sheet.error` (code)

## Open questions

- none
