---
id: "promotions"
jobs: ["manage-promotions"]
personas: ["store-manager"]
route: "/promotions"
routes: [{path: "/promotions"}]
layout: "action-bar / high density"
components: ["button", "empty-state", "pin-pad", "skeleton", "toast", "virtual-list"]
data:
  reads: ["promotion_get", "promotion_list"]
  writes: ["promotion_manage_promotions"]
  events: []
offline: true
print: false
---

# promotions

## Purpose

Create and schedule BOGO, mix-and-match, tiered, percent/amount off, bundle price

Role access: store-manager.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| Promotions                     [Search]   [+ New promotion]  |
+------------------------+-------------------------------------+
| PromoList              | RuleBuilder                         |
| Summer 3-for-2  Active | Kind: [BOGO v]                      |
| Abaya 20% off   Sched. | Buy [2] get [1] free                |
| Eid bundle      Expired| Applies to: Tops, Scarves           |
|  (expired greyed)      | Schedule: 01/10 - 15/10  Stack: No  |
|                        +-------------------------------------+
|                        | BasketPreview (sample basket)       |
|                        | 3 x T-shirt  SAR 150 -> SAR 100     |
|                        | ! Overlaps "Summer 3-for-2"         |
+------------------------+-------------------------------------+
| [Cancel]                                  [Save & schedule]  |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Promotions           [+ New]     |
+----------------------------------+
| Summer 3-for-2          Active   |
| Abaya 20% off           Sched.   |
| Eid bundle              Expired  |
+----------------------------------+
| Editor (full screen on tap)      |
| Kind [BOGO v]  Buy 2 get 1       |
| Applies to: Tops, Scarves        |
| 01/10 - 15/10   Stack: No        |
| Preview: SAR 150 -> SAR 100      |
+----------------------------------+
| [Cancel]      [Save & schedule]  |
+----------------------------------+
```

Components from screens.md: PromoList, RuleBuilder, BasketPreview

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| New promotion / save and schedule | primary | `button` |
| Open promotion from list | secondary | `virtual-list` |
| Confirm save of non-stackable overlap | secondary | `pin-pad` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No promotions yet. Create the first one. | لا توجد عروض بعد. أنشئ أول عرض. | reviewed |
| loading | Loading promotions… | جارٍ تحميل العروض… | reviewed |
| error | Promotions could not be loaded. Retry. | تعذّر تحميل العروض. أعد المحاولة. | reviewed |
| offline | Offline. Edits are saved here and go live after sync. | غير متصل. تُحفظ التعديلات هنا وتُفعَّل بعد المزامنة. | reviewed |
| locked | Overlaps a non-stackable promotion. Manager PIN needed. | يتداخل مع عرض غير قابل للجمع. يلزم رمز المدير. | reviewed |
| success | Promotion scheduled. | تمت جدولة العرض. | reviewed |

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
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- Screen note: Rule builder fields labelled in words ("Buy 2 get 1")

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.promotions.viewed` (persona, branch)
- `screen.promotions.action` (action id, duration_ms)
- `screen.promotions.error` (code)

## Open questions

- Priority rule when two non-stackable promotions match the same basket (best for customer, or newest).
