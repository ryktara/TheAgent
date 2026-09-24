---
id: "customer-lookup"
jobs: ["loyalty-points"]
personas: ["cashier"]
route: "/customer-lookup"
routes: [{path: "/customer-lookup"}]
layout: "action-bar / high density"
components: ["bottom-sheet", "button", "empty-state", "search", "skeleton", "toast"]
data:
  reads: ["loyalty_account_get", "loyalty_account_list"]
  writes: ["loyalty_account_create", "loyalty_account_loyalty_points", "loyalty_account_update"]
  events: []
offline: true
print: false
---

# customer-lookup

## Purpose

Attach a customer by phone or loyalty card; show points, tier, khaata balance

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| customer-lookup                                              |
+--------------------------------------------------------------+
| Sheet: search                 | result card with points and  |
| Sheet: search                 | result card with points and  |
| Sheet: search                 | result card with points and  |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| customer-lookup                  |
+----------------------------------+
| Sheet: search                    |
|                                  |
| result card with points and bala |
|                                  |
+----------------------------------+
```

Components from screens.md: PhoneField, CustomerCard

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Search phone, scan card, quick-create (name + phone), attach | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No records yet. Create the first one. | لا توجد سجلات بعد. أنشئ السجل الأول. <!-- unreviewed --> | copy.csv |
| loading | Loading list… | جارٍ تحميل القائمة… <!-- unreviewed --> | copy.csv |
| error | The list could not be loaded. Retry. | تعذّر تحميل القائمة. أعد المحاولة. <!-- unreviewed --> | copy.csv |
| offline | Showing the last saved list. Edits are queued. | عرض آخر قائمة محفوظة. التعديلات في قائمة الانتظار. <!-- unreviewed --> | copy.csv |
| locked | warning | رمز المدير مطلوب لتعديل هذه القائمة. <!-- unreviewed --> | from screens.md |
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
- Screen note: Points and balance read out

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors; phone stays LTR

## Telemetry

- `screen.customer-lookup.viewed` (persona, branch)
- `screen.customer-lookup.action` (action id, duration_ms)
- `screen.customer-lookup.error` (code)

## Open questions

- none
