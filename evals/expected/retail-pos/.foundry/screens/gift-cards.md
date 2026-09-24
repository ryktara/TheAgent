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
| gift-cards                                                   |
+--------------------------------------------------------------+
| Card lookup                   | balance and history          |
| Card lookup                   | balance and history          |
| Card lookup                   | balance and history          |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| gift-cards                       |
+----------------------------------+
| Card lookup                      |
|                                  |
| balance and history              |
|                                  |
+----------------------------------+
```

Components from screens.md: CodeField, BalanceCard, HistoryList

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Scan/enter code, load amount, check balance, void (PIN) | primary | `button` |

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

- none
