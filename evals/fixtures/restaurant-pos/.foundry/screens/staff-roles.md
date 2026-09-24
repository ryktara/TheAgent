---
id: "staff-roles"
jobs: ["staff-roles"]
personas: ["owner"]
route: "/staff-roles"
layout: "action-bar / high density"
components: ["button", "data-table", "empty-state", "pin-pad", "skeleton", "toast"]
data:
  reads: ["staff_get", "staff_list"]
  writes: ["staff_staff_roles"]
  events: []
offline: true
print: false
---

# staff-roles

## Purpose

Staff, PINs, roles, permissions, branch assignment

Role access: owner.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| staff-roles                                                  |
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
| staff-roles                      |
+----------------------------------+
| header                           |
|                                  |
| content                          |
|                                  |
| action bar                       |
|                                  |
+----------------------------------+
```

Components from screens.md: StaffTable, RoleMatrix

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Add staff, set PIN, assign role, suspend | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No records yet. Create the first one. | لا توجد سجلات بعد. أنشئ السجل الأول. <!-- unreviewed --> | copy.csv |
| loading | Loading list… | جارٍ تحميل القائمة… <!-- unreviewed --> | copy.csv |
| error | duplicate PIN within branch | تعذّر تحميل القائمة. أعد المحاولة. <!-- unreviewed --> | from screens.md |
| offline | Showing the last saved list. Edits are queued. | عرض آخر قائمة محفوظة. التعديلات في قائمة الانتظار. <!-- unreviewed --> | copy.csv |
| locked | Manager PIN needed to edit this list. | رمز المدير مطلوب لتعديل هذه القائمة. <!-- unreviewed --> | copy.csv |
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
- Screen note: Matrix cells are checkboxes with row and column headers

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.staff-roles.viewed` (persona, branch)
- `screen.staff-roles.action` (action id, duration_ms)
- `screen.staff-roles.error` (code)

## Open questions

- none
