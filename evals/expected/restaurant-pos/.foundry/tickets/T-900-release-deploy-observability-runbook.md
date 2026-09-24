---
id: "T-900"
title: "Release: deploy, observability, runbook"
type: "release"
blockedBy: ["T-028", "T-029", "T-030", "T-031", "T-032", "T-033", "T-000"]
jobs: []
screens: []
operations: []
adrs: ["0007", "0008"]
controls: ["SEC-CFG-01", "SEC-CFG-02", "SEC-CFG-04", "SEC-LOG-01", "SEC-DATA-06"]
estimate: "L"
files_likely_touched: ["Dockerfile", "fly.toml", "docs/runbook.md", "CHANGELOG.md"]
acceptance_tests:
  - "Given the container image, When deployed to staging, Then /health is ok and the smoke e2e passes on the deployed URL"
  - "Given structured logs, When a request fails, Then the request id links web, api and provider logs"
  - "Given the runbook, When a new operator follows it, Then deploy, rollback and backup restore complete without help"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-900 — Release: deploy, observability, runbook

## Slice

Container build, staging and production environments per ADR 0007, error tracking and metrics per ADR 0008, runbook, changelog.

## Acceptance tests

1. Given the container image, When deployed to staging, Then /health is ok and the smoke e2e passes on the deployed URL
2. Given structured logs, When a request fails, Then the request id links web, api and provider logs
3. Given the runbook, When a new operator follows it, Then deploy, rollback and backup restore complete without help

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
