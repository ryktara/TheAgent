---
id: "menu-management"
jobs: ["manage-menu", "multi-branch"]
personas: ["manager", "owner"]
route: "/menu-management"
layout: "action-bar / high density"
components: ["button", "data-table", "empty-state", "modifier-sheet", "skeleton", "toast"]
data:
  reads: ["branch_get", "branch_list", "menu_item_get", "menu_item_list"]
  writes: ["branch_multi_branch", "menu_item_create", "menu_item_manage_menu", "menu_item_update"]
  events: []
offline: true
print: false
---

# menu-management

## Purpose

Categories, items, variants, modifier groups, availability, channel pricing

Role access: manager.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| menu-management                                              |
+--------------------------------------------------------------+
| Category tree left            | item table centre            |
| Category tree left            | item table centre            |
| Category tree left            | item table centre            |
+--------------------------------------------------------------+
| item editor right                                            |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| menu-management                  |
+----------------------------------+
| Category tree left               |
|                                  |
| item table centre                |
|                                  |
| item editor right                |
|                                  |
+----------------------------------+
```

Components from screens.md: CategoryTree, ItemTable, ItemEditor, ChannelPriceGrid, ModifierGroupEditor

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Add/edit item (bilingual names), set PLU, price by channel, tax rule, station, 86 toggle, schedule | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | import from CSV | لا توجد سجلات بعد. أنشئ السجل الأول. <!-- unreviewed --> | from screens.md |
| loading | Loading list… | جارٍ تحميل القائمة… <!-- unreviewed --> | copy.csv |
| error | duplicate PLU | تعذّر تحميل القائمة. أعد المحاولة. <!-- unreviewed --> | from screens.md |
| offline | Showing the last saved list. Edits are queued. | عرض آخر قائمة محفوظة. التعديلات في قائمة الانتظار. <!-- unreviewed --> | copy.csv |
| locked | price change needs manager | رمز المدير مطلوب لتعديل هذه القائمة. <!-- unreviewed --> | from screens.md |
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
- Screen note: Tree is a treeview with arrow navigation

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Editor fields mirror; name_ar field is RTL regardless of UI language

## Telemetry

- `screen.menu-management.viewed` (persona, branch)
- `screen.menu-management.action` (action id, duration_ms)
- `screen.menu-management.error` (code)

## Open questions

- none
