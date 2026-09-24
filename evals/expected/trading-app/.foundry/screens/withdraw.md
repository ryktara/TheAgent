---
id: "withdraw"
jobs: ["withdraw-funds"]
personas: ["retail-trader"]
route: "/withdraw"
routes: [{path: "/withdraw"}]
layout: "bottom-tabs / high density"
components: ["button", "empty-state", "input", "skeleton", "toast", "virtual-list"]
data:
  reads: ["transfer_get", "transfer_list"]
  writes: ["transfer_create", "transfer_update", "transfer_withdraw_funds"]
  events: []
offline: false
print: false
---

# withdraw

## Purpose

Withdraw to a verified same-name beneficiary

Role access: retail-trader (compliance-officer reads held/approved).

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| withdraw                                                     |
+--------------------------------------------------------------+
| Withdrawable amount (availabl | beneficiary list             |
| Withdrawable amount (availabl | beneficiary list             |
| Withdrawable amount (availabl | beneficiary list             |
+--------------------------------------------------------------+
| cool-down banner                                             |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| withdraw                         |
+----------------------------------+
| Withdrawable amount (available m |
|                                  |
| beneficiary list                 |
|                                  |
| cool-down banner                 |
|                                  |
+----------------------------------+
```

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Pick beneficiary, amount, confirm with MFA | primary | `button` |

## States

| State | Copy (en) | Copy (ur) | Notes |
|-------|-----------|-----------|-------|
| empty | Nothing here yet. | ابھی یہاں کچھ نہیں ہے۔ <!-- unreviewed --> | copy.csv |
| loading | Loading… | لوڈ ہو رہا ہے… <!-- unreviewed --> | copy.csv |
| error | Something went wrong. Retry, or contact the manager. | کچھ غلط ہو گیا۔ دوبارہ کوشش کریں یا منیجر سے رابطہ کریں۔ <!-- unreviewed --> | copy.csv |
| offline | Offline. Changes are saved on this device and sync when the connection returns. | آف لائن۔ تبدیلیاں اس ڈیوائس پر محفوظ ہیں اور کنکشن واپس آنے پر سنک ہوں گی۔ <!-- unreviewed --> | copy.csv |
| locked | A manager PIN is needed for this action. | اس عمل کے لیے منیجر پن درکار ہے۔ <!-- unreviewed --> | copy.csv |
| success | Done. | ہو گیا۔ <!-- unreviewed --> | copy.csv |

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
- `A11Y-10`
- `A11Y-11`
- `A11Y-12`
- `A11Y-14`

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`

## Telemetry

- `screen.withdraw.viewed` (persona, branch)
- `screen.withdraw.action` (action id, duration_ms)
- `screen.withdraw.error` (code)

## Open questions

- none
