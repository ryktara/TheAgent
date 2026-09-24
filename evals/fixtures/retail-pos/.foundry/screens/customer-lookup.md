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
| Attach customer (sheet)                          [x] close   |
+--------------------------------------------------------------+
| [+966 5x xxx xxxx        ] [Search]   [Scan loyalty card]    |
+--------------------------------------------------------------+
| CustomerCard                                                 |
|  Noura A.   +966 55 123 4567   Tier: Gold                    |
|  Points 1,240 (= SAR 12.40)    Balance SAR 0.00              |
|  ! Blocked customer warning (when flagged)                   |
+--------------------------------------------------------------+
| Not found?  Name [        ]  [ ] Marketing consent           |
+--------------------------------------------------------------+
| [Quick create]                                   [Attach]    |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Attach customer              [x] |
+----------------------------------+
| [+966 5x xxx xxxx]  [Scan card]  |
+----------------------------------+
| Noura A.  +966 55 123 4567       |
| Gold  Points 1,240               |
| Balance SAR 0.00                 |
+----------------------------------+
| Name [          ]                |
| [ ] Marketing consent            |
+----------------------------------+
| [Quick create]       [Attach]    |
+----------------------------------+
```

Components from screens.md: PhoneField, CustomerCard

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Search by phone | primary | `search` |
| Scan loyalty card | secondary | `button` |
| Quick-create (name + phone) | secondary | `button` |
| Attach to sale | primary | `button` |
| Close sheet | tertiary | `bottom-sheet` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Enter a phone number or scan a loyalty card. | أدخل رقم الجوال أو امسح بطاقة الولاء. | reviewed |
| loading | Searching… | جارٍ البحث… | reviewed |
| error | No customer found for this number. Create one. | لا يوجد عميل بهذا الرقم. أنشئ عميلًا جديدًا. | reviewed |
| offline | Offline. Searching saved customers; points update after sync. | غير متصل. البحث في العملاء المحفوظين؛ تُحدَّث النقاط بعد المزامنة. | reviewed |
| locked | This customer is blocked. Ask the manager. | هذا العميل محظور. راجع المدير. | reviewed |
| success | Customer attached. {points} points. | تم ربط العميل. {points} نقطة. | reviewed |

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

- Reads cover loyalty_account only; confirm whether phone search should also bind customer_list / customer_create.
- Customer credit (khaata) balance: in scope for Riyadh stores or hide the field.
