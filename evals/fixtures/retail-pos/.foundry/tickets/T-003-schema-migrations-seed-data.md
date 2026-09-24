---
id: "T-003"
title: "Schema, migrations, seed data"
type: "feature"
blockedBy: ["T-002"]
jobs: []
screens: []
operations: []
adrs: ["0004"]
controls: ["SEC-DATA-07", "SEC-IN-04"]
estimate: "M"
files_likely_touched: ["packages/db/prisma/schema.prisma", "packages/db/prisma/migrations/", "packages/db/seed.ts"]
acceptance_tests:
  - "Given prisma/schema.prisma, When `npx prisma validate` and `migrate dev` run, Then both succeed on an empty database"
  - "Given the audit table, When an UPDATE is attempted with the app role, Then it is denied"
  - "Given the seed, When it runs twice, Then it is idempotent and creates one store, roles, a clothing catalog with size/colour variants and SA VAT 15% inclusive tax rules"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-003 — Schema, migrations, seed data

## Slice

Migrations from the generated schema with check constraints from invariants; seed for the decided region; append-only grants on audit and receipts.

## Acceptance tests

1. Given prisma/schema.prisma, When `npx prisma validate` and `migrate dev` run, Then both succeed on an empty database
2. Given the audit table, When an UPDATE is attempted with the app role, Then it is denied
3. Given the seed, When it runs twice, Then it is idempotent and creates one store, roles, a clothing catalog with size/colour variants and SA VAT 15% inclusive tax rules

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
