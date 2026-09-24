---
id: "gift-cards"
jobs: ["gift-card-store-credit"]
personas: ["cashier"]
route: "/gift-cards"
routes: [{path: "/gift-cards"}]
layout: "action-bar / high density"
components: ["button", "empty-state", "pin-pad", "skeleton", "toast", "virtual-list"]
data:
  reads: ["gift_card_get", "gift_card_list"]
  writes: ["gift_card_create", "gift_card_gift_card_store_credit", "gift_card_update"]
  events: []
offline: true
print: false
---

# gift-cards

## Purpose

Issue, top up, check balance, void gift cards and store credit

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| Gift cards & store credit     [Code / scan ______] [Look up] |
+-----------------------------+--------------------------------+
| BalanceCard                 | HistoryList                    |
|  GC-4821-XXXX  Active       |  12/09  Issued     +SAR 200.00 |
|  Balance SAR 150.00         |  18/09  Redeemed   -SAR 50.00  |
|  Expires 31/12/2027         |                                |
+-----------------------------+--------------------------------+
| Amount [SAR ______]                                          |
+--------------------------------------------------------------+
| [Void (PIN)]           [Check balance]    [Issue / top up]   |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Gift cards                       |
+----------------------------------+
| [Code / scan ______] [Look up]   |
+----------------------------------+
| GC-4821-XXXX   Active            |
| Balance SAR 150.00  exp 12/2027  |
+----------------------------------+
| 12/09 Issued      +SAR 200.00    |
| 18/09 Redeemed    -SAR 50.00     |
+----------------------------------+
| Amount [SAR ____]                |
| [Void]           [Issue/top up]  |
+----------------------------------+
```

Components from screens.md: CodeField, BalanceCard, HistoryList

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Issue or top up | primary | `button` |
| Check balance | secondary | `button` |
| Browse history | secondary | `virtual-list` |
| Void (manager PIN) | destructive | `pin-pad` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Scan or enter a gift card code. | امسح رمز بطاقة الهدية أو أدخله. | reviewed |
| loading | Checking balance… | جارٍ التحقق من الرصيد… | reviewed |
| error | Card expired, void, or balance too low. | البطاقة منتهية أو ملغاة أو رصيدها غير كافٍ. | reviewed |
| offline | Offline. Balance checks and top-ups wait for connection. | غير متصل. التحقق من الرصيد والشحن بانتظار الاتصال. | reviewed |
| locked | Voiding a card needs a manager PIN. | إلغاء البطاقة يتطلب رمز المدير. | reviewed |
| success | Balance SAR {balance}. | الرصيد {balance} ريال. | reviewed |

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
- Screen note: Balance announced

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.gift-cards.viewed` (persona, branch)
- `screen.gift-cards.action` (action id, duration_ms)
- `screen.gift-cards.error` (code)

## Open questions

- Out of PRD scope: gift cards are not enabled (decision D:gift-cards = false, later phase); screen kept for reference only.
- If enabled later: ZATCA treatment of gift card sale (non-taxable voucher vs taxable supply) needs a decision.
