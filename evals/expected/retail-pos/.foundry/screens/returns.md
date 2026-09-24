---
id: "returns"
jobs: ["return-exchange"]
personas: ["cashier"]
route: "/returns"
routes: [{path: "/returns"}]
layout: "action-bar / high density"
components: ["button", "empty-state", "pin-pad", "quantity-stepper", "receipt-preview", "select", "skeleton", "toast"]
data:
  reads: ["return_get", "return_list"]
  writes: ["return_create", "return_return_exchange", "return_update"]
  events: []
offline: true
print: false
---

# returns

## Purpose

Return or exchange items from a found Sale, or no-receipt return under policy

Role access: cashier (approval: store-manager).

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| returns                                                      |
+--------------------------------------------------------------+
| Left: original sale lines wit | right: return basket         |
| Left: original sale lines wit | right: return basket         |
| Left: original sale lines wit | right: return basket         |
+--------------------------------------------------------------+
| refund method                                                |
+--------------------------------------------------------------+
| policy text                                                  |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| returns                          |
+----------------------------------+
| Left: original sale lines with r |
|                                  |
| right: return basket             |
|                                  |
| refund method                    |
|                                  |
| policy text                      |
|                                  |
+----------------------------------+
```

Components from screens.md: ReturnLineRow, ReasonSelect, RefundMethodSelect, PolicyBanner

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Pick lines and qty, choose reason, restock yes/no, refund method, exchange items (goes to checkout with credit) | primary | `button` |

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
- `A11Y-06`
- `A11Y-08`
- `A11Y-10`
- `A11Y-12`
- `A11Y-14`
- Screen note: Returnable qty in each row label

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Columns mirror

## Telemetry

- `screen.returns.viewed` (persona, branch)
- `screen.returns.action` (action id, duration_ms)
- `screen.returns.error` (code)

## Open questions

- none
