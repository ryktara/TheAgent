---
id: "recipe-editor"
jobs: ["inventory-basic"]
personas: ["manager"]
route: "/recipe-editor"
routes: [{path: "/recipe-editor"}]
layout: "action-bar / high density"
components: ["button", "empty-state", "input", "quantity-stepper", "skeleton", "toast", "virtual-list"]
data:
  reads: ["inventory_item_get", "inventory_item_list"]
  writes: ["inventory_item_create", "inventory_item_inventory_basic", "inventory_item_update"]
  events: []
offline: true
print: false
---

# recipe-editor

## Purpose

Bill of materials per menu item so sales deduct stock

Role access: manager.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| recipe-editor                                                |
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
| recipe-editor                    |
+----------------------------------+
| header                           |
|                                  |
| content                          |
|                                  |
| action bar                       |
|                                  |
+----------------------------------+
```

Components from screens.md: ComponentList, CostPreview

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Add component, qty, unit, yield | primary | `button` |
| cost preview | secondary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Fill in the fields to continue. | املأ الحقول للمتابعة. <!-- unreviewed --> | copy.csv |
| loading | Saving… | جارٍ الحفظ… <!-- unreviewed --> | copy.csv |
| error | unit mismatch | بعض الحقول تحتاج مراجعة. صحّحها واحفظ مرة أخرى. <!-- unreviewed --> | from screens.md |
| offline | Saved on this device. It will sync when online. | تم الحفظ على هذا الجهاز وسيُزامن عند الاتصال. <!-- unreviewed --> | copy.csv |
| locked | Manager PIN needed to change this. | رمز المدير مطلوب لتغيير هذا. <!-- unreviewed --> | copy.csv |
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
- Screen note: Qty inputs labelled with unit

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.recipe-editor.viewed` (persona, branch)
- `screen.recipe-editor.action` (action id, duration_ms)
- `screen.recipe-editor.error` (code)

## Open questions

- none
