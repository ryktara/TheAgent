---
id: "T-020"
title: "Statements tax (statements, tax-report)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006", "T-014"]
jobs: ["statements-tax"]
screens: ["statements", "tax-report"]
operations: ["statement_statements_tax"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/compliance/statements-tax.ts", "apps/api/src/compliance/statements-tax.test.ts", "apps/web/app/statements/page.tsx", "apps/web/app/tax-report/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the statements screen, When statements tax completes, Then the Statement state and totals match the domain invariants"
  - "Given a cashier role, When statements tax is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A Statement is immutable once issued; corrections issue a new Statement referencing the ol' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-020 — Statements tax (statements, tax-report)

## Slice

Vertical slice for job `statements-tax`: operations statement_statements_tax; screens statements, tax-report; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the statements screen, When statements tax completes, Then the Statement state and totals match the domain invariants
2. Given a cashier role, When statements tax is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'A Statement is immutable once issued; corrections issue a new Statement referencing the ol' is checked, Then it holds

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
