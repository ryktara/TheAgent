---
id: "layaway"
jobs: ["layaway"]
personas: ["cashier"]
route: "/layaway"
routes: [{path: "/layaway"}]
layout: "action-bar / high density"
components: ["button", "date-picker", "empty-state", "skeleton", "toast", "virtual-list"]
data:
  reads: ["layaway_get", "layaway_list"]
  writes: ["layaway_create", "layaway_layaway", "layaway_update"]
  events: []
offline: true
print: false
---

# layaway

## Purpose

Reserve items for a customer against a deposit, take instalments, release on full payment

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| layaway                                                      |
+--------------------------------------------------------------+
| List by due date              | detail with items            |
| List by due date              | detail with items            |
| List by due date              | detail with items            |
+--------------------------------------------------------------+
| deposit                                                      |
+--------------------------------------------------------------+
| balance                                                      |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| layaway                          |
+----------------------------------+
| List by due date                 |
|                                  |
| detail with items                |
|                                  |
| deposit                          |
|                                  |
| balance                          |
|                                  |
+----------------------------------+
```

Components from screens.md: LayawayList, PaymentSchedule

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Create from basket, take payment, collect, cancel (refund per policy) | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Nothing here yet. | لا يوجد شيء هنا بعد. <!-- unreviewed --> | copy.csv |
| loading | Loading… | جارٍ التحميل… <!-- unreviewed --> | copy.csv |
| error | Something went wrong. Retry, or contact the manager. | حدث خطأ ما. أعد المحاولة أو تواصل مع المدير. <!-- unreviewed --> | copy.csv |
| offline | Offline. Changes are saved on this device and sync when the connection returns. | غير متصل. تُحفظ التغييرات على هذا الجهاز وتُزامن عند عودة الاتصال. <!-- unreviewed --> | copy.csv |
| locked | A manager PIN is needed for this action. | هذا الإجراء يتطلب رمز المدير. <!-- unreviewed --> | copy.csv |
| success | Done. | تم. <!-- unreviewed --> | copy.csv |

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
- Screen note: Due dates spoken in full

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.layaway.viewed` (persona, branch)
- `screen.layaway.action` (action id, duration_ms)
- `screen.layaway.error` (code)

## Open questions

- none
