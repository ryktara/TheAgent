---
id: "kds"
jobs: ["send-to-kitchen", "kds-bump", "delivery-orders"]
personas: ["kitchen", "waiter"]
route: "/kds"
layout: "action-bar / high density"
components: ["banner-offline", "button", "empty-state", "kds-ticket", "skeleton", "tabs", "toast"]
data:
  reads: ["order_get", "order_list"]
  writes: ["kitchen_ticket_kds_bump", "order_create", "order_delivery_orders", "order_send_to_kitchen", "order_update"]
  events: []
offline: true
print: true
---

# kds

## Purpose

Kitchen sees fired tickets per station and bumps them

Role access: kitchen.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| kds                                                          |
+--------------------------------------------------------------+
| Ticket rail (newest right     | oldest left                  |
| Ticket rail (newest right     | oldest left                  |
| Ticket rail (newest right     | oldest left                  |
+--------------------------------------------------------------+
| 4–6 visible)                                                 |
+--------------------------------------------------------------+
| station tabs                                                 |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| kds                              |
+----------------------------------+
| Ticket rail (newest right        |
|                                  |
| oldest left                      |
|                                  |
| 4–6 visible)                     |
|                                  |
| station tabs                     |
|                                  |
+----------------------------------+
```

Components from screens.md: TicketCard, BumpBar (keyboard: 1–9 bump ticket n, R recall, S station), AgeTimer

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Bump line, bump ticket, recall, mark item 86, filter by station | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | "No open tickets" | لا توجد تذاكر مفتوحة. <!-- unreviewed --> | from screens.md |
| loading | Connecting to the kitchen feed… | جارٍ الاتصال بقناة المطبخ… <!-- unreviewed --> | copy.csv |
| error | printer fallback | انقطع اتصال المطبخ. تُطبع التذاكر كبديل. <!-- unreviewed --> | from screens.md |
| offline | tickets from local queue, banner | غير متصل. عرض التذاكر من هذا الجهاز. <!-- unreviewed --> | from screens.md |
| locked | Recall needs a manager PIN after 10 minutes. | الاستدعاء بعد 10 دقائق يتطلب رمز المدير. <!-- unreviewed --> | copy.csv |
| success | Bumped. | تم الإنجاز. <!-- unreviewed --> | copy.csv |

## Validation and error copy

- `FRM-02` Error copy says what happened and how to fix it in one sentence.
- `FRM-01` Validate on blur; re-validate on change after the first error; summarise on submit.
- `FRM-03` Submit stays enabled; errors listed on attempt.

## Keyboard and shortcuts

| Key | Action |
|-----|--------|
| 1–9 | bump ticket in slot |
| R | recall last bump |
| S | cycle station |

## Accessibility checklist

- `A11Y-01`
- `A11Y-02`
- `A11Y-03`
- `A11Y-08`
- `A11Y-12`
- `A11Y-13`
- `A11Y-14`
- `A11Y-16`
- Screen note: Dark theme 7:1 contrast; ticket cards announce age; bump bar keys documented on screen

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Ticket rail order stays chronological left→right; text mirrors

## Telemetry

- `screen.kds.viewed` (persona, branch)
- `screen.kds.action` (action id, duration_ms)
- `screen.kds.error` (code)

## Open questions

- none
