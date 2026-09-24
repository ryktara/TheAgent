---
id: "customer-lookup"
jobs: ["loyalty"]
personas: ["cashier"]
route: "/customer-lookup"
routes: [{path: "/customer-lookup"}]
layout: "action-bar / high density"
components: ["button", "empty-state", "search", "skeleton", "toast", "virtual-list"]
data:
  reads: ["customer_get", "customer_list"]
  writes: ["customer_create", "customer_loyalty", "customer_update"]
  events: []
offline: true
print: false
---

# customer-lookup

## Purpose

Find or create a customer for loyalty, khaata, allergens

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| customer-lookup                                              |
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
| customer-lookup                  |
+----------------------------------+
| header                           |
|                                  |
| content                          |
|                                  |
| action bar                       |
|                                  |
+----------------------------------+
```

Components from screens.md: PhoneSearch, CustomerCard

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Search by phone, create, attach to order, redeem points | primary | `button` |

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
- `A11Y-08`
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- `A11Y-18`
- Screen note: Search results as a listbox

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.customer-lookup.viewed` (persona, branch)
- `screen.customer-lookup.action` (action id, duration_ms)
- `screen.customer-lookup.error` (code)

## Open questions

- none
