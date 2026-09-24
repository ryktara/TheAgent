---
id: "customer-display"
jobs: ["customer-display"]
personas: ["customer"]
route: "/customer-display"
routes: [{path: "/customer-display"}]
layout: "action-bar / high density"
components: ["button", "empty-state", "skeleton", "toast", "virtual-list"]
data:
  reads: ["sale_get", "sale_list"]
  writes: ["sale_create", "sale_customer_display", "sale_update"]
  events: []
offline: true
print: false
---

# customer-display

## Purpose

Second screen facing the customer: lines as scanned, promotions, total, QR to pay, thank you

Role access: customer.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
|                     ABAYA CLASSIC 52 BLACK       SAR 450.00  |
+--------------------------------------------------------------+
| T-shirt M Navy            1 x 60.00                  60.00   |
| Abaya Classic 52 Black    1 x 450.00                450.00   |
| Promo: 2nd T-shirt 50%                              -30.00   |
+--------------------------------------------------------------+
| TOTAL incl. VAT 15%                             SAR 480.00   |
+--------------------------------------------------------------+
| Points earned +48                           [ QR to pay ]    |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| ABAYA 52 BLACK       SAR 450.00  |
+----------------------------------+
| T-shirt M Navy           60.00   |
| Promo 2nd T-shirt       -30.00   |
+----------------------------------+
| TOTAL incl. VAT     SAR 480.00   |
| Points +48         [ QR ]        |
+----------------------------------+
```

Components from screens.md: CustomerLineList, TotalBanner

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Show basket lines (read-only) | primary | `virtual-list` |
| Idle slideshow | secondary | `empty-state` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Welcome. Your items will appear here. | أهلًا بك. ستظهر مشترياتك هنا. | copy.csv |
| loading | Connecting to the till… | جارٍ الاتصال بنقطة البيع… | copy.csv |
| error | Display disconnected. Please check the total with the cashier. | انقطع اتصال الشاشة. يرجى التأكد من الإجمالي مع أمين الصندوق. | copy.csv |
| offline | Offline. Your total is still correct; the receipt syncs later. | لا يوجد اتصال. الإجمالي صحيح وستتم مزامنة الفاتورة لاحقًا. | copy.csv |
| locked | Till is closed. Please use another counter. | نقطة البيع مغلقة. يرجى التوجّه إلى صندوق آخر. | copy.csv |
| success | Thank you. You earned 48 points. | شكرًا لك. حصلت على 48 نقطة. | copy.csv |

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
- Screen note: High contrast, 24 px minimum

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Follows customer language

## Telemetry

- `screen.customer-display.viewed` (persona, branch)
- `screen.customer-display.action` (action id, duration_ms)
- `screen.customer-display.error` (code)

## Open questions

- Screen is read-only but frontmatter writes include sale_create and sale_update; confirm whether the display should hold any write binding.
