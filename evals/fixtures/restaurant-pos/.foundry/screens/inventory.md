---
id: "inventory"
jobs: ["inventory-basic"]
personas: ["manager"]
route: "/inventory"
layout: "action-bar / high density"
components: ["badge", "button", "data-table", "empty-state", "input", "skeleton", "toast"]
data:
  reads: ["inventory_item_get", "inventory_item_list"]
  writes: ["inventory_item_create", "inventory_item_inventory_basic", "inventory_item_update"]
  events: []
offline: true
print: false
---

# inventory

## Purpose

Stock on hand, movements, wastage, low-stock alerts

Role access: manager.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| inventory                                                    |
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
| inventory                        |
+----------------------------------+
| header                           |
|                                  |
| content                          |
|                                  |
| action bar                       |
|                                  |
+----------------------------------+
```

Components from screens.md: StockTable, MovementLog, WastageForm

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Adjust, record wastage with reason, receive stock, set par level | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | "Add inventory items or import" | لا توجد سجلات بعد. أنشئ السجل الأول. <!-- unreviewed --> | from screens.md |
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
- `A11Y-10`
- `A11Y-11`
- `A11Y-12`
- `A11Y-13`
- Screen note: Table sortable with announced sort state

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.inventory.viewed` (persona, branch)
- `screen.inventory.action` (action id, duration_ms)
- `screen.inventory.error` (code)

## Open questions

- none
