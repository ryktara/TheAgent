---
id: "T-010"
title: "Deposit funds (deposit)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006", "T-008"]
jobs: ["deposit-funds"]
screens: ["deposit"]
operations: ["transfer_deposit_funds"]
adrs: ["0002"]
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01", "SEC-SESS-07", "SEC-API-01", "SEC-BL-05"]
estimate: "L"
files_likely_touched: ["apps/api/src/accounts/deposit-funds.ts", "apps/api/src/accounts/deposit-funds.test.ts", "apps/web/app/deposit/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the deposit screen, When deposit funds completes, Then the Transfer state and totals match the domain invariants"
  - "Given a retail-trader role, When deposit funds is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A Transfer of direction withdrawal requires KycCase approved at the tier covering the amou' is checked, Then it holds"
  - "Given any sequence of actions, When the invariant 'A withdrawal Transfer is paid only to a beneficiary in the name of the Account owner' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-010 — Deposit funds (deposit)

## Slice

Vertical slice for job `deposit-funds`: operations transfer_deposit_funds; screens deposit; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the deposit screen, When deposit funds completes, Then the Transfer state and totals match the domain invariants
2. Given a retail-trader role, When deposit funds is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'A Transfer of direction withdrawal requires KycCase approved at the tier covering the amou' is checked, Then it holds
5. Given any sequence of actions, When the invariant 'A withdrawal Transfer is paid only to a beneficiary in the name of the Account owner' is checked, Then it holds

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
