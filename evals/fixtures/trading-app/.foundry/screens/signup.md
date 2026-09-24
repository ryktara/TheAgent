---
id: "signup"
jobs: ["open-account"]
personas: ["retail-trader"]
route: "/signup"
routes: [{path: "/signup"}]
layout: "bottom-tabs / high density"
components: ["button", "empty-state", "input", "skeleton", "toast"]
data:
  reads: ["account_get", "account_list"]
  writes: ["account_create", "account_open_account", "account_update"]
  events: []
offline: false
print: false
---

# signup

## Purpose

Create the Account shell before KYC: phone, email, password or passkey, jurisdiction

Role access: retail-trader (anonymous until OTP).

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| signup                                                       |
+--------------------------------------------------------------+
| Stepper (3 steps)             | single column form           |
| Stepper (3 steps)             | single column form           |
| Stepper (3 steps)             | single column form           |
+--------------------------------------------------------------+
| legal footer with regulator name and licence number          |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| signup                           |
+----------------------------------+
| Stepper (3 steps)                |
|                                  |
| single column form               |
|                                  |
| legal footer with regulator name |
|                                  |
+----------------------------------+
```

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Enter phone → OTP, email, create passkey, pick country of residence, accept terms version | primary | `button` |

## States

| State | Copy (en) | Copy (ur) | Notes |
|-------|-----------|-----------|-------|
| empty | Nothing here yet. | ابھی یہاں کچھ نہیں ہے۔ <!-- unreviewed --> | copy.csv |
| loading | Loading… | لوڈ ہو رہا ہے… <!-- unreviewed --> | copy.csv |
| error | phone in use | کچھ غلط ہو گیا۔ دوبارہ کوشش کریں یا منیجر سے رابطہ کریں۔ <!-- unreviewed --> | from screens.md |
| offline | Offline. Changes are saved on this device and sync when the connection returns. | آف لائن۔ تبدیلیاں اس ڈیوائس پر محفوظ ہیں اور کنکشن واپس آنے پر سنک ہوں گی۔ <!-- unreviewed --> | copy.csv |
| locked | "We cannot serve residents of X" | اس عمل کے لیے منیجر پن درکار ہے۔ <!-- unreviewed --> | from screens.md |
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
- Screen note: OTP field one input with autocomplete one-time-code; errors linked via aria-describedby

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors; phone number and OTP stay LTR

## Telemetry

- `screen.signup.viewed` (persona, branch)
- `screen.signup.action` (action id, duration_ms)
- `screen.signup.error` (code)

## Open questions

- none
