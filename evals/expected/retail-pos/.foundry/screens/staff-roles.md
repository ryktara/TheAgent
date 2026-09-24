---
id: "staff-roles"
jobs: ["staff-roles"]
personas: ["owner"]
route: "/staff-roles"
routes: [{path: "/staff-roles"}]
layout: "action-bar / high density"
components: ["button", "data-table", "empty-state", "pin-pad", "select", "skeleton", "toast", "virtual-list"]
data:
  reads: ["staff_get", "staff_list"]
  writes: ["staff_staff_roles"]
  events: []
offline: true
print: false
---

# staff-roles

## Purpose

Staff, PINs, roles, override limits, store access

Role access: owner.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| staff-roles                                                  |
+--------------------------------------------------------------+
| List                          | editor                       |
| List                          | editor                       |
| List                          | editor                       |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| staff-roles                      |
+----------------------------------+
| List                             |
|                                  |
| editor                           |
|                                  |
+----------------------------------+
```

Components from screens.md: StaffTable, RoleSelect

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Add staff, set PIN, set role and override limit, suspend | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No records yet. Create the first one. | لا توجد سجلات بعد. أنشئ السجل الأول. <!-- unreviewed --> | copy.csv |
| loading | Loading list… | جارٍ تحميل القائمة… <!-- unreviewed --> | copy.csv |
| error | The list could not be loaded. Retry. | تعذّر تحميل القائمة. أعد المحاولة. <!-- unreviewed --> | copy.csv |
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
- `A11Y-10`
- `A11Y-12`
- `A11Y-14`
- Screen note: Labels

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
