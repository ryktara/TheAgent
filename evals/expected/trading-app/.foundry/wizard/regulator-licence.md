---
slug: "regulator-licence"
ticket: "T-000"
why: "Trading App is a regulated activity: SECP must license or register the operator before real users trade, deposit or withdraw. Foundry cannot obtain a licence; it ships every regulated flow behind FEATURE_REGULATED_LIVE=false until a human confirms."
vars:
  - {name: "REGULATOR_NAME", desc: "Regulator that issued the licence or registration", regex: "^.{2,80}$"}
  - {name: "LICENCE_REF", desc: "Licence or registration reference", regex: "^.{3,64}$"}
  - {name: "LICENCE_EXPIRY", desc: "Licence expiry (YYYY-MM-DD)", regex: "^/d{4}-/d{2}-/d{2}$"}
  - {name: "COMPLIANCE_OFFICER_EMAIL", desc: "Compliance officer contact", regex: "^[^@/s]+@[^@/s]+$"}
validate: "python scripts/foundry.py wizard status"
created: "2026-09-24T09:52:06+00:00"
---

# Wizard: regulator-licence

**Why:** Trading App is a regulated activity: SECP must license or register the operator before real users trade, deposit or withdraw. Foundry cannot obtain a licence; it ships every regulated flow behind FEATURE_REGULATED_LIVE=false until a human confirms. The code ships behind a feature flag with a stub adapter until these values exist.

## Steps

1. Confirm with SECP which licence category covers the decided asset classes and custody model (see .foundry/compliance.yaml).
2. Obtain the licence or registration, or a written no-objection for a sandbox pilot.
3. Appoint a compliance officer and record the contact below.
4. Paste each value when the script prompts; then run `python scripts/foundry.py release confirm --by <your name>`.

## What to paste back

- `REGULATOR_NAME` — Regulator that issued the licence or registration (format `^.{2,80}$`)
- `LICENCE_REF` — Licence or registration reference (format `^.{3,64}$`)
- `LICENCE_EXPIRY` — Licence expiry (YYYY-MM-DD) (format `^\d{4}-\d{2}-\d{2}$`)
- `COMPLIANCE_OFFICER_EMAIL` — Compliance officer contact (format `^[^@\s]+@[^@\s]+$`)

## Run

```
pwsh .foundry/wizard/regulator-licence.ps1     # Windows
sh   .foundry/wizard/regulator-licence.sh      # macOS/Linux
```

The script validates each value, appends them to `.env.local` (git-ignored, never committed) and runs: `python scripts/foundry.py wizard status`.

Check: `python scripts/foundry.py wizard status` shows `regulator-licence` as done.
