---
id: "labels"
jobs: ["print-labels"]
personas: ["stock-keeper"]
route: "/labels"
routes: [{path: "/labels"}]
layout: "action-bar / high density"
components: ["banner-offline", "button", "empty-state", "quantity-stepper", "skeleton", "toast"]
data:
  reads: []
  writes: ["barcode_print_labels"]
  events: []
offline: true
print: true
---

# labels

## Purpose

Print shelf-edge and product labels: price (VAT-inclusive), barcode, unit price per kg/100 g, Arabic name

Role access: stock-keeper.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| labels                                                       |
+--------------------------------------------------------------+
| Queue                         | template preview             |
| Queue                         | template preview             |
| Queue                         | template preview             |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| labels                           |
+----------------------------------+
| Queue                            |
|                                  |
| template preview                 |
|                                  |
+----------------------------------+
```

Components from screens.md: LabelQueue, TemplatePreview

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Pick products (scan, from GRN, from price change), template, qty, print | primary | `button` |

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
- Screen note: Preview alt text

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Arabic text right-aligned on label

## Telemetry

- `screen.labels.viewed` (persona, branch)
- `screen.labels.action` (action id, duration_ms)
- `screen.labels.error` (code)

## Open questions

- none
