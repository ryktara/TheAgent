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
| Labels   [Scan] [From GRN] [From price change]     [Print]   |
+--------------------------------------------------------------+
| Queue                         | Template preview             |
|  Item / size / colour  [-2+]  |  Arabic name                 |
|  Item / size / colour  [-1+]  |  Price incl. VAT  SAR 199.00 |
|                               |  ||| barcode |||             |
+--------------------------------------------------------------+
| Template: [Swing tag v]                  Labels: 3           |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Labels            [Scan]         |
+----------------------------------+
| Queue                            |
|  Item / size / colour   [-1+]    |
+----------------------------------+
| Template preview                 |
+----------------------------------+
| [Print 3 labels]                 |
+----------------------------------+
```

Components from screens.md: LabelQueue, TemplatePreview

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Add products (scan, from GRN, from price change) | secondary | `button` |
| Set quantity per label | secondary | `quantity-stepper` |
| Pick template | secondary | `button` |
| Print | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No labels queued. Scan an item or load a GRN. | لا توجد ملصقات في القائمة. امسح صنفًا أو حمّل إشعار استلام. | copy.csv |
| loading | Loading label queue… | جارٍ تحميل قائمة الملصقات… | copy.csv |
| error | Template is missing a field. Pick another template, then retry. | القالب ينقصه حقل. اختر قالبًا آخر ثم أعد المحاولة. | copy.csv |
| offline | Printer or network offline. The queue is kept on this device. | الطابعة أو الشبكة غير متصلة. القائمة محفوظة على هذا الجهاز. | copy.csv |
| locked | Stock-keeper access is needed to print labels. | طباعة الملصقات تتطلب صلاحية أمين المخزن. | copy.csv |
| success | Labels sent to the printer. | أُرسلت الملصقات إلى الطابعة. | copy.csv |

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

- Purpose names unit price per kg/100 g; drop it for clothing swing tags and show size and colour instead?
