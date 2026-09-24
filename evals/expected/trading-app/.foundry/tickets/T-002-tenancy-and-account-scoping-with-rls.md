---
id: "T-002"
title: "Tenancy and account scoping with RLS"
type: "feature"
blockedBy: ["T-001"]
jobs: []
screens: []
operations: []
adrs: ["0003"]
controls: ["SEC-ACC-02", "SEC-ACC-05", "SEC-ACC-08"]
estimate: "M"
files_likely_touched: ["packages/db/prisma/migrations/", "apps/api/src/people/branch.ts", "apps/api/src/middleware/scope.ts"]
acceptance_tests:
  - "Given two branches, When a device of branch A lists orders, Then only branch A rows return"
  - "Given an owner session, When the branch switcher selects B, Then reads and writes target B"
  - "Given the app db role, When it attempts to bypass RLS, Then Postgres denies"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-002 — Tenancy and account scoping with RLS

## Slice

branch_id on every operational table; RLS policies; scope middleware; owner branch switcher.

## Acceptance tests

1. Given two branches, When a device of branch A lists orders, Then only branch A rows return
2. Given an owner session, When the branch switcher selects B, Then reads and writes target B
3. Given the app db role, When it attempts to bypass RLS, Then Postgres denies

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
