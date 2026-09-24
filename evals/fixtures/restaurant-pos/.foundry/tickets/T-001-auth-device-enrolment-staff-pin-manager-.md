---
id: "T-001"
title: "Auth: device enrolment, staff PIN, manager override"
type: "feature"
blockedBy: ["T-000"]
jobs: []
screens: []
operations: ["staff_list", "staff_get", "role_list", "role_get"]
adrs: ["0002"]
controls: ["SEC-AUTH-05", "SEC-AUTH-06", "SEC-AUTH-11", "SEC-SESS-01", "SEC-SESS-07", "SEC-ACC-01"]
estimate: "L"
files_likely_touched: ["apps/api/src/people/auth.ts", "apps/api/src/people/devices.ts", "apps/web/app/(auth)/pin/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given an enrolled device token, When a request carries it, Then branch scope is set and unknown tokens get 401"
  - "Given a staff PIN, When 3 wrong entries occur, Then the PIN locks for 60 s and an audit event is written"
  - "Given a void over threshold, When a manager enters a PIN, Then the approver id is stored on the audit event"
  - "Given a PIN verified offline, When sync runs, Then the event is marked pending-audit"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-001 — Auth: device enrolment, staff PIN, manager override

## Slice

Device enrolment endpoint and token middleware; Argon2id PIN hashing with local hash cache; manager override modal wired to audit; sessions table.

## Acceptance tests

1. Given an enrolled device token, When a request carries it, Then branch scope is set and unknown tokens get 401
2. Given a staff PIN, When 3 wrong entries occur, Then the PIN locks for 60 s and an audit event is written
3. Given a void over threshold, When a manager enters a PIN, Then the approver id is stored on the audit event
4. Given a PIN verified offline, When sync runs, Then the event is marked pending-audit

## Definition of done

- typecheck
- unit
- integration
- e2e-smoke
- a11y-axe
- lint
- semgrep
- screenshot
- spec-review
- detect_changes_risk<=medium
