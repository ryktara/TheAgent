---
id: "delivery-inbox"
jobs: ["delivery-orders"]
personas: ["kitchen"]
route: "/delivery-inbox"
routes: [{path: "/delivery-inbox"}]
layout: "action-bar / high density"
components: ["button", "data-table", "empty-state", "input", "kds-ticket", "skeleton", "tabs", "toast"]
data:
  reads: ["order_get", "order_list"]
  writes: ["order_create", "order_delivery_orders", "order_update"]
  events: []
offline: true
print: false
---

# delivery-inbox

## Purpose

Aggregator orders land here, get accepted, and fire to KDS

Role access: kitchen.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| delivery-inbox                                               |
+--------------------------------------------------------------+
| Platform tabs                 | order cards with timer       |
| Platform tabs                 | order cards with timer       |
| Platform tabs                 | order cards with timer       |
+--------------------------------------------------------------+
| detail pane                                                  |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| delivery-inbox                   |
+----------------------------------+
| Platform tabs                    |
|                                  |
| order cards with timer           |
|                                  |
| detail pane                      |
|                                  |
+----------------------------------+
```

Components from screens.md: PlatformTabs, DeliveryOrderCard, RiderHandover

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Accept (prep time), reject with reason, mark ready, hand over to rider | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No open tickets. | لا توجد تذاكر مفتوحة. <!-- unreviewed --> | copy.csv |
| loading | Connecting to the kitchen feed… | جارٍ الاتصال بقناة المطبخ… <!-- unreviewed --> | copy.csv |
| error | Kitchen feed lost. Tickets print as fallback. | انقطع اتصال المطبخ. تُطبع التذاكر كبديل. <!-- unreviewed --> | copy.csv |
| offline | Offline. Showing tickets from this device. | غير متصل. عرض التذاكر من هذا الجهاز. <!-- unreviewed --> | copy.csv |
| locked | Recall needs a manager PIN after 10 minutes. | الاستدعاء بعد 10 دقائق يتطلب رمز المدير. <!-- unreviewed --> | copy.csv |
| success | Bumped. | تم الإنجاز. <!-- unreviewed --> | copy.csv |

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
- `A11Y-13`
- Screen note: New order sound plus visual flash; cards announce platform and ETA

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.delivery-inbox.viewed` (persona, branch)
- `screen.delivery-inbox.action` (action id, duration_ms)
- `screen.delivery-inbox.error` (code)

## Open questions

- none
