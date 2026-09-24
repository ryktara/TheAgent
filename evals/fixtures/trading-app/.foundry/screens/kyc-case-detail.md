---
id: "kyc-case-detail"
jobs: ["review-kyc-case"]
personas: ["compliance-officer"]
route: "/kyc-case-detail"
routes: [{path: "/kyc-case-detail"}]
layout: "bottom-tabs / high density"
components: ["button", "dialog", "empty-state", "skeleton", "toast"]
data:
  reads: ["kyc_case_get", "kyc_case_list"]
  writes: ["kyc_case_create", "kyc_case_review_kyc_case", "kyc_case_update"]
  events: []
offline: false
print: false
---

# kyc-case-detail

## Purpose

Decide one KycCase with evidence side by side

Role access: compliance-officer.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| kyc-case-detail                                              |
+--------------------------------------------------------------+
| Document images + liveness sc | vendor checks (PEP           |
| Document images + liveness sc | vendor checks (PEP           |
| Document images + liveness sc | vendor checks (PEP           |
+--------------------------------------------------------------+
| sanctions                                                    |
+--------------------------------------------------------------+
| adverse media)                                               |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| kyc-case-detail                  |
+----------------------------------+
| Document images + liveness score |
|                                  |
| vendor checks (PEP               |
|                                  |
| sanctions                        |
|                                  |
| adverse media)                   |
|                                  |
+----------------------------------+
```

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Approve tier, reject with reason code, request info, escalate to ComplianceCase | primary | `button` |

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
- `A11Y-04`
- `A11Y-08`
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- Screen note: Decision buttons have confirmation dialogs naming the tier

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`

## Telemetry

- `screen.kyc-case-detail.viewed` (persona, branch)
- `screen.kyc-case-detail.action` (action id, duration_ms)
- `screen.kyc-case-detail.error` (code)

## Open questions

- none
