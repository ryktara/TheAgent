---
id: "T-000"
title: "Repo scaffold, toolchain, CI"
type: "scaffold"
blockedBy: []
jobs: []
screens: []
operations: []
adrs: ["0001"]
controls: ["SEC-SC-01", "SEC-SC-06", "SEC-CFG-05"]
estimate: "M"
files_likely_touched: ["package.json", "apps/web/", "apps/api/", "packages/db/", ".github/workflows/ci.yml", "docker-compose.yml", ".env.example"]
acceptance_tests:
  - "Given a clean clone, When `npm ci && npm run build` runs, Then it exits 0 on Windows and Linux"
  - "Given the scaffold, When `npx tsc -p mobile --noEmit` and `npx vitest run --dir api` run, Then both exit 0 with zero tests failing"
  - "Given CI, When a PR opens, Then typecheck, lint, unit, a11y and semgrep jobs run and are required"
  - "Given docker compose up, When the api starts, Then /health returns ok and the db accepts connections"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-000 — Repo scaffold, toolchain, CI

## Slice

Monorepo from stacks.csv: web `npx create-expo-app@latest mobile --template blank-typescript`; api `npm create hono@latest api -- --template nodejs`; prisma init; lint, typecheck, vitest, playwright+axe wired; docker compose with postgres; .env.example listing every variable; CI workflow. No CODEOWNERS.

## Acceptance tests

1. Given a clean clone, When `npm ci && npm run build` runs, Then it exits 0 on Windows and Linux
2. Given the scaffold, When `npx tsc -p mobile --noEmit` and `npx vitest run --dir api` run, Then both exit 0 with zero tests failing
3. Given CI, When a PR opens, Then typecheck, lint, unit, a11y and semgrep jobs run and are required
4. Given docker compose up, When the api starts, Then /health returns ok and the db accepts connections

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
