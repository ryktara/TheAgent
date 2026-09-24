---
id: "T-030"
title: "Integration: kyc adapter (sumsub)"
type: "integration"
blockedBy: ["T-004"]
jobs: []
screens: []
operations: []
adrs: ["0006"]
controls: ["SEC-API-04", "SEC-API-05", "SEC-CRY-06", "SEC-API-06"]
estimate: "L"
files_likely_touched: ["apps/api/src/integrations/kyc/sumsub.ts", "apps/api/src/integrations/kyc/adapter.ts", "apps/api/src/webhooks/kyc.ts"]
acceptance_tests:
  - "Given a sandbox sumsub account, When the adapter runs its contract test, Then every method returns the expected shape"
  - "Given a signed kyc webhook, When it arrives twice, Then it is applied once and the second returns the stored receipt"
  - "Given an unsigned or tampered kyc webhook, When it arrives, Then it is rejected with 401 and logged"
  - "Given the provider times out, When the adapter is called, Then the circuit opens after 3 failures and the UI offers a fallback"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-030 — Integration: kyc adapter (sumsub)

## Slice

kyc adapter interface plus sumsub module, webhook endpoint with idempotency on (provider, event_id), sandbox contract test, wizard note for live keys.

## Acceptance tests

1. Given a sandbox sumsub account, When the adapter runs its contract test, Then every method returns the expected shape
2. Given a signed kyc webhook, When it arrives twice, Then it is applied once and the second returns the stored receipt
3. Given an unsigned or tampered kyc webhook, When it arrives, Then it is rejected with 401 and logged
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
