---
id: "kyc-review-queue"
jobs: ["review-kyc-case"]
personas: ["compliance-officer"]
route: "/kyc-review-queue"
routes: [{path: "/kyc-review-queue"}]
layout: "bottom-tabs / high density"
components: ["button", "data-table", "empty-state", "skeleton", "toast", "virtual-list"]
data:
  reads: ["kyc_case_get", "kyc_case_list"]
  writes: ["kyc_case_create", "kyc_case_review_kyc_case", "kyc_case_update"]
  events: []
offline: false
print: false
---

# kyc-review-queue

## Purpose

Compliance officer queue of KycCase rows in submitted/in-review, sorted by risk and age

Role access: compliance-officer (support read-only).

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| kyc-review-queue                                             |
+--------------------------------------------------------------+
| Filters left                  | dense table (age             |
| Filters left                  | dense table (age             |
| Filters left                  | dense table (age             |
+--------------------------------------------------------------+
| tier                                                         |
+--------------------------------------------------------------+
| risk score                                                   |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| kyc-review-queue                 |
+----------------------------------+
| Filters left                     |
|                                  |
| dense table (age                 |
|                                  |
| tier                             |
|                                  |
| risk score                       |
|                                  |
+----------------------------------+
```

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Claim case, filter (PEP hit, sanctions hit, high risk country, tier), bulk-assign | primary | `button` |

## States

| State | Copy (en) | Copy (ur) | Notes |
|-------|-----------|-----------|-------|
| empty | "Queue clear" | ابھی یہاں کچھ نہیں ہے۔ <!-- unreviewed --> | from screens.md |
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

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`

## Telemetry

- `screen.kyc-review-queue.viewed` (persona, branch)
- `screen.kyc-review-queue.action` (action id, duration_ms)
- `screen.kyc-review-queue.error` (code)

## Open questions

- none
