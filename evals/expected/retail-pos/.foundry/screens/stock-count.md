---
id: "stock-count"
jobs: ["stock-take", "stock-adjust"]
personas: ["stock-keeper"]
route: "/stock-count"
routes: [{path: "/stock-count"}]
layout: "action-bar / high density"
components: ["button", "data-table", "empty-state", "numpad", "skeleton", "toast", "virtual-list"]
data:
  reads: ["stock_count_get", "stock_count_list"]
  writes: ["stock_count_create", "stock_count_stock_take", "stock_count_update", "stock_movement_stock_adjust"]
  events: []
offline: true
print: false
---

# stock-count

## Purpose

Full stock take or cycle count, plus manual adjustments (damage, theft, expiry)

Role access: stock-keeper (post: store-manager).

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| stock-count                                                  |
+--------------------------------------------------------------+
| Count list                    | variance review with value   |
| Count list                    | variance review with value   |
| Count list                    | variance review with value   |
+--------------------------------------------------------------+
| reason picker                                                |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| stock-count                      |
+----------------------------------+
| Count list                       |
|                                  |
| variance review with value       |
|                                  |
| reason picker                    |
|                                  |
+----------------------------------+
```

Components from screens.md: ScanField, CountRow, VarianceTable

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Start count (scope: all, category, bin), scan and count, review variance, post | primary | `button` |
| adjust with reason | secondary | `button` |

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
- Screen note: Counts entered with numpad

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Mirrors

## Telemetry

- `screen.stock-count.viewed` (persona, branch)
- `screen.stock-count.action` (action id, duration_ms)
- `screen.stock-count.error` (code)

## Open questions

- none
