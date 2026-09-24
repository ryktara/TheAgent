---
id: "layaway"
jobs: ["layaway"]
personas: ["cashier"]
route: "/layaway"
routes: [{path: "/layaway"}]
layout: "action-bar / high density"
components: ["button", "date-picker", "empty-state", "skeleton", "toast", "virtual-list"]
data:
  reads: ["layaway_get", "layaway_list"]
  writes: ["layaway_create", "layaway_layaway", "layaway_update"]
  events: []
offline: true
print: false
---

# layaway

## Purpose

Reserve items for a customer against a deposit, take instalments, release on full payment

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| Layaway                    [Filter: due v]  [+ From basket]  |
+-------------------------+------------------------------------+
| LayawayList (by due)    | Detail: LY-0042  Sara M.           |
| LY-0042 Sara  due 30/09 | 2 x Abaya S/Black    SAR 700.00    |
| LY-0039 Huda  overdue ! | Deposit SAR 200  Balance SAR 500   |
| LY-0031 Reem  expired   | PaymentSchedule                    |
|                         |  15/10  SAR 250   [date]           |
|                         |  30/10  SAR 250                    |
+-------------------------+------------------------------------+
| [Cancel & refund]         [Take payment]         [Collect]   |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Layaway            [+ Basket]    |
+----------------------------------+
| LY-0042 Sara      due 30/09      |
| LY-0039 Huda      overdue !      |
+----------------------------------+
| LY-0042  2 x Abaya S/Black       |
| Deposit 200  Balance SAR 500     |
| 15/10 SAR 250 | 30/10 SAR 250    |
+----------------------------------+
| [Cancel]  [Pay]      [Collect]   |
+----------------------------------+
```

Components from screens.md: LayawayList, PaymentSchedule

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Create from basket | primary | `button` |
| Take payment | primary | `button` |
| Collect items | secondary | `button` |
| Cancel and refund per policy | destructive | `button` |
| Set schedule date | secondary | `date-picker` |
| Open layaway from list | secondary | `virtual-list` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No layaways. Create one from a basket. | لا توجد حجوزات. أنشئ حجزًا من السلة. | reviewed |
| loading | Loading layaways… | جارٍ تحميل الحجوزات… | reviewed |
| error | Layaways could not be loaded. Retry. | تعذّر تحميل الحجوزات. أعد المحاولة. | reviewed |
| offline | Offline. Payments are queued and sync later. | غير متصل. الدفعات في قائمة الانتظار وتُزامن لاحقًا. | reviewed |
| locked | Cancelling needs a manager PIN. | الإلغاء يتطلب رمز المدير. | reviewed |
| success | Payment taken. Balance SAR {balance}. | تم استلام الدفعة. المتبقي {balance} ريال. | reviewed |

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
- Screen note: Due dates spoken in full

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.layaway.viewed` (persona, branch)
- `screen.layaway.action` (action id, duration_ms)
- `screen.layaway.error` (code)

## Open questions

- Out of PRD scope: layaway is not enabled by any decision (later phase); screen kept for reference only.
- If enabled later: ZATCA invoice timing (deposit as advance payment invoice vs one invoice on collection).
