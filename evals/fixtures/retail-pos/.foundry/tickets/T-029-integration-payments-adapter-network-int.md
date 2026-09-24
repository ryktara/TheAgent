---
id: "T-029"
title: "Integration: payments adapter (network-intl)"
type: "integration"
blockedBy: ["T-005", "T-009"]
jobs: []
screens: []
operations: ["webhook_payments"]
adrs: ["0006"]
controls: ["SEC-API-04", "SEC-API-05", "SEC-CRY-06", "SEC-API-06", "SEC-PAY-01", "SEC-PAY-02", "SEC-PAY-03"]
estimate: "L"
files_likely_touched: ["apps/api/src/integrations/payments/network-intl.ts", "apps/api/src/integrations/payments/adapter.ts", "apps/api/src/webhooks/payments.ts"]
acceptance_tests:
  - "Given a sandbox network-intl account, When the adapter runs its contract test, Then every method returns the expected shape"
  - "Given a signed payments webhook, When it arrives twice, Then it is applied once and the second returns the stored receipt"
  - "Given an unsigned or tampered payments webhook, When it arrives, Then it is rejected with 401 and logged"
  - "Given the provider times out, When the adapter is called, Then the circuit opens after 3 failures and the UI offers a fallback"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-029 — Integration: payments adapter (network-intl)

## Slice

payments adapter interface plus network-intl module, webhook endpoint with idempotency on (provider, event_id), sandbox contract test, wizard note for live keys.

## Acceptance tests

1. Given a sandbox network-intl account, When the adapter runs its contract test, Then every method returns the expected shape
2. Given a signed payments webhook, When it arrives twice, Then it is applied once and the second returns the stored receipt
3. Given an unsigned or tampered payments webhook, When it arrives, Then it is rejected with 401 and logged
4. Given the provider times out, When the adapter is called, Then the circuit opens after 3 failures and the UI offers a fallback

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
