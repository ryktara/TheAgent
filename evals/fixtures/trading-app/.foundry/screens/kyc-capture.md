---
id: "kyc-capture"
jobs: ["open-account", "kyc-tier-upgrade"]
personas: ["retail-trader"]
route: "/kyc-capture"
routes: [{path: "/kyc-capture"}]
layout: "bottom-tabs / high density"
components: ["button", "empty-state", "skeleton", "toast", "virtual-list"]
data:
  reads: ["account_get", "account_list", "kyc_case_get", "kyc_case_list"]
  writes: ["account_create", "account_open_account", "account_update", "kyc_case_create", "kyc_case_kyc_tier_upgrade", "kyc_case_update"]
  events: []
offline: false
print: false
---

# kyc-capture

## Purpose

Collect identity for the requested KYC tier: national ID rail or document + selfie via vendor SDK

Role access: retail-trader.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| kyc-capture                                                  |
+--------------------------------------------------------------+
| Tier card at top (limits unlo | step list                    |
| Tier card at top (limits unlo | step list                    |
| Tier card at top (limits unlo | step list                    |
+--------------------------------------------------------------+
| vendor SDK frame                                             |
+--------------------------------------------------------------+
| save-and-resume                                              |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| kyc-capture                      |
+----------------------------------+
| Tier card at top (limits unlocke |
|                                  |
| step list                        |
|                                  |
| vendor SDK frame                 |
|                                  |
| save-and-resume                  |
|                                  |
+----------------------------------+
```

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Choose rail (UAE Pass, Nafath/Absher, NADRA Verisys, or document scan), selfie/liveness, address, source of funds, suitability questionnaire | primary | `button` |

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
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- `A11Y-18`
- Screen note: Camera steps have text alternative and manual upload path

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors; ID numbers LTR

## Telemetry

- `screen.kyc-capture.viewed` (persona, branch)
- `screen.kyc-capture.action` (action id, duration_ms)
- `screen.kyc-capture.error` (code)

## Open questions

- none
