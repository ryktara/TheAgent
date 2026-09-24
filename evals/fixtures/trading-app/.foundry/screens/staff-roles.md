---
id: "staff-roles"
jobs: ["staff-roles"]
personas: ["admin"]
route: "/staff-roles"
routes: [{path: "/staff-roles"}]
layout: "bottom-tabs / high density"
components: ["button", "empty-state", "skeleton", "toast"]
data:
  reads: ["staff_get", "staff_list"]
  writes: ["staff_staff_roles"]
  events: []
offline: false
print: false
---

# staff-roles

## Purpose

Staff accounts, roles, MFA status, four-eyes groups

Role access: admin.

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

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Invite, suspend, change role (four-eyes) | primary | `button` |

## States

| State | Copy (en) | Copy (ur) | Notes |
|-------|-----------|-----------|-------|
| empty | No records yet. Create the first one. | ابھی کوئی ریکارڈ نہیں۔ پہلا ریکارڈ بنائیں۔ <!-- unreviewed --> | copy.csv |
| loading | Loading list… | فہرست لوڈ ہو رہی ہے… <!-- unreviewed --> | copy.csv |
| error | The list could not be loaded. Retry. | فہرست لوڈ نہیں ہو سکی۔ دوبارہ کوشش کریں۔ <!-- unreviewed --> | copy.csv |
| offline | Showing the last saved list. Edits are queued. | آخری محفوظ فہرست دکھائی جا رہی ہے۔ ترامیم قطار میں ہیں۔ <!-- unreviewed --> | copy.csv |
| locked | Manager PIN needed to edit this list. | اس فہرست میں ترمیم کے لیے منیجر پن درکار ہے۔ <!-- unreviewed --> | copy.csv |
| success | Saved. | محفوظ ہو گیا۔ <!-- unreviewed --> | copy.csv |

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

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`

## Telemetry

- `screen.staff-roles.viewed` (persona, branch)
- `screen.staff-roles.action` (action id, duration_ms)
- `screen.staff-roles.error` (code)

## Open questions

- none
