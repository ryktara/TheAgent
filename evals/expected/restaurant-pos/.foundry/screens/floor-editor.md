---
id: "floor-editor"
jobs: ["manage-floor"]
personas: ["manager"]
route: "/floor-editor"
routes: [{path: "/floor-editor"}]
layout: "action-bar / high density"
components: ["button", "data-table", "empty-state", "floor-canvas", "skeleton", "table-map-tile", "toast"]
data:
  reads: ["table_get", "table_list"]
  writes: ["table_create", "table_manage_floor", "table_update"]
  events: []
offline: true
print: false
---

# floor-editor

## Purpose

Draw zones and tables

Role access: manager.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| floor-editor                                                 |
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
| floor-editor                     |
+----------------------------------+
| header                           |
|                                  |
| content                          |
|                                  |
| action bar                       |
|                                  |
+----------------------------------+
```

Components from screens.md: FloorCanvas (edit mode), TableInspector

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Add zone, drag table, set number and seats, shape, save | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No floor plan yet. Open the floor editor. | لا توجد خريطة طاولات بعد. افتح محرر القاعة. <!-- unreviewed --> | copy.csv |
| loading | Loading tables… | جارٍ تحميل الطاولات… <!-- unreviewed --> | copy.csv |
| error | duplicate table number | تعذّر تحديث حالة الطاولات. <!-- unreviewed --> | from screens.md |
| offline | Offline. Table states are from this device. | غير متصل. حالات الطاولات من هذا الجهاز. <!-- unreviewed --> | copy.csv |
| locked | Transfer needs a manager PIN. | نقل الطاولة يتطلب رمز المدير. <!-- unreviewed --> | copy.csv |
| success | Table updated. | تم تحديث الطاولة. <!-- unreviewed --> | copy.csv |

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
- Screen note: Keyboard nudge for table position

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Canvas unchanged

## Telemetry

- `screen.floor-editor.viewed` (persona, branch)
- `screen.floor-editor.action` (action id, duration_ms)
- `screen.floor-editor.error` (code)

## Open questions

- none
