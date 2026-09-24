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
| Staff and roles                               [Add staff]    |
+--------------------------------------------------------------+
| List (data-table)             | Editor                       |
|  Name | Role | Status         |  Name                        |
|  Sara | Cashier | Active      |  Role [select]               |
|  Omar | Manager | Suspended   |  Override limit SAR [    ]   |
|                               |  [Set PIN]  [Suspend] [Save] |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Staff              [Add]         |
+----------------------------------+
| List (virtual-list)              |
|  Name - Role - Status            |
+----------------------------------+
| Editor (on tap)                  |
|  Role / limit / PIN              |
+----------------------------------+
```

Components from screens.md: StaffTable, RoleSelect

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Add staff | primary | `button` |
| Set PIN | secondary | `pin-pad` |
| Set role and override limit | secondary | `select` |
| Suspend | destructive | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No staff yet. Add the first staff member. | لا يوجد موظفون بعد. أضف أول موظف. | copy.csv |
| loading | Loading staff… | جارٍ تحميل الموظفين… | copy.csv |
| error | Staff list could not be loaded. Retry. | تعذّر تحميل قائمة الموظفين. أعد المحاولة. | copy.csv |
| offline | Showing the last saved list. Changes are queued until the connection returns. | نعرض آخر قائمة محفوظة. تُحفظ التعديلات حتى يعود الاتصال. | copy.csv |
| locked | Only the owner can change staff and roles. | تعديل الموظفين والأدوار متاح للمالك فقط. | copy.csv |
| success | Staff saved. | تم حفظ بيانات الموظف. | copy.csv |

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

- Purpose lists per-staff store access, but multi-store is out of PRD scope: hide the store-access field?
