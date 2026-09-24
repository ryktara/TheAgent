---
id: "T-024"
title: "Audit trail (audit-log)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006", "T-014"]
jobs: ["audit-trail"]
screens: ["audit-log"]
operations: ["audit_event_audit_trail"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/compliance/audit-trail.ts", "apps/api/src/compliance/audit-trail.test.ts", "apps/web/app/audit-log/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the audit-log screen, When audit trail completes, Then the AuditEvent state and totals match the domain invariants"
  - "Given a retail-trader role, When audit trail is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'When equity falls below the stop-out level of RiskLimit, positions close largest-loss firs' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'AuditEvent is append-only; each row carries prev_hash of the previous row so tampering bre' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-024 — Audit trail (audit-log)

## Slice

Vertical slice for job `audit-trail`: operations audit_event_audit_trail; screens audit-log; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the audit-log screen, When audit trail completes, Then the AuditEvent state and totals match the domain invariants
2. Given a retail-trader role, When audit trail is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'When equity falls below the stop-out level of RiskLimit, positions close largest-loss firs' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'AuditEvent is append-only; each row carries prev_hash of the previous row so tampering bre' is checked, Then it holds

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
