---
id: "reservations"
jobs: ["reservations-waitlist"]
personas: ["waiter"]
route: "/reservations"
routes: [{path: "/reservations"}]
layout: "action-bar / high density"
components: ["banner-offline", "button", "data-table", "empty-state", "input", "skeleton", "toast", "virtual-list"]
data:
  reads: ["reservation_get", "reservation_list"]
  writes: ["reservation_create", "reservation_reservations_waitlist", "reservation_update"]
  events: []
offline: true
print: false
---

# reservations

## Purpose

Bookings and walk-in waitlist

Role access: waiter.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| reservations                                                 |
+--------------------------------------------------------------+
| Timeline by table             | waitlist column              |
| Timeline by table             | waitlist column              |
| Timeline by table             | waitlist column              |
+--------------------------------------------------------------+
| booking form                                                 |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| reservations                     |
+----------------------------------+
| Timeline by table                |
|                                  |
| waitlist column                  |
|                                  |
| booking form                     |
|                                  |
+----------------------------------+
```

Components from screens.md: Timeline, WaitlistColumn, BookingForm

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Add booking, assign table, seat, no-show, notify by WhatsApp | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No records yet. Create the first one. | لا توجد سجلات بعد. أنشئ السجل الأول. <!-- unreviewed --> | copy.csv |
| loading | Loading list… | جارٍ تحميل القائمة… <!-- unreviewed --> | copy.csv |
| error | The list could not be loaded. Retry. | تعذّر تحميل القائمة. أعد المحاولة. <!-- unreviewed --> | copy.csv |
| offline | read-only | عرض آخر قائمة محفوظة. التعديلات في قائمة الانتظار. <!-- unreviewed --> | from screens.md |
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
- `A11Y-10`
- `A11Y-11`
- `A11Y-12`
- `A11Y-14`
- Screen note: Timeline slots are buttons with time and table

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Timeline mirrors

## Telemetry

- `screen.reservations.viewed` (persona, branch)
- `screen.reservations.action` (action id, duration_ms)
- `screen.reservations.error` (code)

## Open questions

- none
