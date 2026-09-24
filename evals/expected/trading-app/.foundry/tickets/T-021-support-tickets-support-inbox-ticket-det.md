---
id: "T-021"
title: "Support tickets (support-inbox, ticket-detail)"
type: "feature"
blockedBy: ["T-003", "T-004", "T-006", "T-014"]
jobs: ["support-tickets"]
screens: ["support-inbox", "ticket-detail"]
operations: ["support_ticket_support_tickets"]
adrs: []
controls: ["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"]
estimate: "M"
files_likely_touched: ["apps/api/src/growth/support-tickets.ts", "apps/api/src/growth/support-tickets.test.ts", "apps/web/app/support-inbox/page.tsx", "apps/web/app/ticket-detail/page.tsx", "packages/db/prisma/schema.prisma"]
acceptance_tests:
  - "Given the support-inbox screen, When support tickets completes, Then the SupportTicket state and totals match the domain invariants"
  - "Given a retail-trader role, When support tickets is attempted without permission, Then the api returns 403 and logs authz.denied"
  - "Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"
  - "Given any sequence of actions, When the invariant 'A SupportTicket flagged as complaint gets an acknowledgement and a due date on creation' is checked, Then it holds"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-021 — Support tickets (support-inbox, ticket-detail)

## Slice

Vertical slice for job `support-tickets`: operations support_ticket_support_tickets; screens support-inbox, ticket-detail; copy from copy.csv; a11y scan; screenshot.

## Acceptance tests

1. Given the support-inbox screen, When support tickets completes, Then the SupportTicket state and totals match the domain invariants
2. Given a retail-trader role, When support tickets is attempted without permission, Then the api returns 403 and logs authz.denied
3. Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations
4. Given any sequence of actions, When the invariant 'A SupportTicket flagged as complaint gets an acknowledgement and a due date on creation' is checked, Then it holds

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
