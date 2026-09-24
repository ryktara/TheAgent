---
id: "purchasing"
jobs: ["purchasing"]
personas: ["manager"]
route: "/purchasing"
layout: "action-bar / high density"
components: ["banner-offline", "button", "empty-state", "input", "receipt-preview", "skeleton", "toast", "virtual-list"]
data:
  reads: ["inventory_item_get", "inventory_item_list"]
  writes: ["inventory_item_create", "inventory_item_purchasing", "inventory_item_update"]
  events: []
offline: true
print: false
---

# purchasing

## Purpose

Purchase orders to suppliers and goods receipt

Role access: manager.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| purchasing                                                   |
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
| purchasing                       |
+----------------------------------+
| header                           |
|                                  |
| content                          |
|                                  |
| action bar                       |
|                                  |
+----------------------------------+
```

Components from screens.md: POList, POEditor, ReceiveForm

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Create PO from low stock, send, receive, post to inventory | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No records yet. Create the first one. | لا توجد سجلات بعد. أنشئ السجل الأول. <!-- unreviewed --> | copy.csv |
| loading | Loading list… | جارٍ تحميل القائمة… <!-- unreviewed --> | copy.csv |
| error | The list could not be loaded. Retry. | تعذّر تحميل القائمة. أعد المحاولة. <!-- unreviewed --> | copy.csv |
| offline | draft only | عرض آخر قائمة محفوظة. التعديلات في قائمة الانتظار. <!-- unreviewed --> | from screens.md |
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
- Screen note: Standard forms

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Mirrors

## Telemetry

- `screen.purchasing.viewed` (persona, branch)
- `screen.purchasing.action` (action id, duration_ms)
- `screen.purchasing.error` (code)

## Open questions

- none
