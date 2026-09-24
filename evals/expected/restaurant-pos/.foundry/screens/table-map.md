---
id: "table-map"
jobs: ["take-order-table", "merge-transfer-tables", "manage-floor"]
personas: ["manager", "waiter"]
route: "/table-map"
routes: [{path: "/table-map"}]
layout: "action-bar / high density"
components: ["banner-offline", "button", "chip", "data-table", "empty-state", "floor-canvas", "pin-pad", "search", "skeleton", "table-map-tile", "tabs", "toast"]
data:
  reads: ["order_get", "order_list", "table_get", "table_list"]
  writes: ["order_create", "order_take_order_table", "order_update", "table_create", "table_manage_floor", "table_merge_transfer_tables", "table_update"]
  events: []
offline: true
print: false
---

# table-map

## Purpose

Seat guests, see table state at a glance, open or resume an order

Role access: waiter.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| table-map                                                    |
+--------------------------------------------------------------+
| Zone tabs (Indoor             | Terrace                      |
| Zone tabs (Indoor             | Terrace                      |
| Zone tabs (Indoor             | Terrace                      |
+--------------------------------------------------------------+
| Shisha)                                                      |
+--------------------------------------------------------------+
| floor canvas                                                 |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| table-map                        |
+----------------------------------+
| Zone tabs (Indoor                |
|                                  |
| Terrace                          |
|                                  |
| Shisha)                          |
|                                  |
| floor canvas                     |
|                                  |
+----------------------------------+
```

Components from screens.md: FloorCanvas, TableChip (number, covers, age, total), ZoneTabs, LegendBar

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Tap free table → new order | primary | `button` |
| tap seated table → resume | secondary | `button` |
| long-press → merge, transfer, mark dirty | secondary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | "No floor plan yet, open Floor editor" | لا توجد خريطة طاولات بعد. افتح محرر القاعة. <!-- unreviewed --> | from screens.md |
| loading | Loading tables… | جارٍ تحميل الطاولات… <!-- unreviewed --> | copy.csv |
| error | Table status could not be refreshed. | تعذّر تحديث حالة الطاولات. <!-- unreviewed --> | copy.csv |
| offline | banner, all actions allowed | غير متصل. حالات الطاولات من هذا الجهاز. <!-- unreviewed --> | from screens.md |
| locked | PIN for transfer | نقل الطاولة يتطلب رمز المدير. <!-- unreviewed --> | from screens.md |
| success | Table updated. | تم تحديث الطاولة. <!-- unreviewed --> | copy.csv |

## Validation and error copy

- `FRM-02` Error copy says what happened and how to fix it in one sentence.
- `FRM-01` Validate on blur; re-validate on change after the first error; summarise on submit.
- `FRM-03` Submit stays enabled; errors listed on attempt.

## Keyboard and shortcuts

| Key | Action |
|-----|--------|
| Arrows | move between tables |
| Enter | open order |

## Accessibility checklist

- `A11Y-01`
- `A11Y-02`
- `A11Y-03`
- `A11Y-06`
- `A11Y-08`
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- Screen note: Tables are buttons with label "Table 12, seated, 4 covers, 18 minutes"; zone tabs arrow-key navigable

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Canvas coordinates unchanged; header and tabs mirror

## Telemetry

- `screen.table-map.viewed` (persona, branch)
- `screen.table-map.action` (action id, duration_ms)
- `screen.table-map.error` (code)

## Open questions

- none
