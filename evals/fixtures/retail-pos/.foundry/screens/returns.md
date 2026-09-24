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
| Policy: returns within 7 days with receipt             [!]   |
+-------------------------------+------------------------------+
| Original sale #10234          | Return basket                |
| Abaya Blk/M  ret. 1   [-1+]   | Abaya Blk/M      -250.00     |
| Thobe Wht/L  ret. 2   [-0+]   | Reason: [Wrong size v]       |
| Scarf Red    ret. 0    --     | Restock: [Yes v]             |
|                               | Refund to: [Original card v] |
|                               | Refund total     -287.50     |
+-------------------------------+------------------------------+
| [Exchange items]                        [  Confirm return  ] |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Policy: 7 days with receipt [!]  |
+----------------------------------+
| Abaya Blk/M  ret. 1     [-1+]    |
| Thobe Wht/L  ret. 2     [-0+]    |
+----------------------------------+
| Reason   [Wrong size v]          |
| Restock  [Yes v]                 |
| Refund   [Original card v]       |
| Total refund        -287.50      |
+----------------------------------+
| [Exchange]   [ Confirm return ]  |
+----------------------------------+
```

Components from screens.md: ReturnLineRow, ReasonSelect, RefundMethodSelect, PolicyBanner

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Set return quantity | primary | `quantity-stepper` |
| Choose reason, restock and refund method | primary | `select` |
| View original receipt | secondary | `receipt-preview` |
| Approve outside policy (manager PIN) | secondary | `pin-pad` |
| Exchange items | secondary | `button` |
| Confirm return | primary | `button` |
## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Find the original sale to start a return. | ابحث عن عملية البيع الأصلية لبدء الإرجاع. | reviewed |
| loading | Loading the sale… | جارٍ تحميل عملية البيع… | reviewed |
| error | Quantity is more than can be returned. Lower it. | الكمية أكبر من المسموح بإرجاعه. خفّضها. | reviewed |
| offline | Offline. The return is saved here and syncs later; card refunds wait for the connection. | لا يوجد اتصال. يُحفظ الإرجاع هنا ويُزامن لاحقًا، واسترداد البطاقة ينتظر الاتصال. | reviewed |
| locked | Outside the return window. A manager PIN is needed. | خارج مدة الإرجاع. يلزم رمز المدير. | reviewed |
| success | Return done. Refund {amount}; credit note issued. | تم الإرجاع. المبلغ المسترد {amount}، وصدر إشعار دائن. | reviewed |
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

- Return window length and whether no-receipt returns are allowed are not set; confirm with the store.
