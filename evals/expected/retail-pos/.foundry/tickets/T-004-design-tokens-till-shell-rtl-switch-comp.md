---
id: "T-004"
title: "Design tokens, till shell, RTL switch, component base"
type: "feature"
blockedBy: ["T-000"]
jobs: []
screens: []
operations: []
adrs: ["0009"]
controls: ["SEC-API-08"]
estimate: "M"
files_likely_touched: ["apps/web/app/layout.tsx", "apps/web/styles/tokens.css", "packages/ui/", "design-system/"]
acceptance_tests:
  - "Given tailwind.tokens.css, When the shell renders, Then computed styles use the token variables and tabular numerals"
  - "Given the language switch, When ar is selected, Then dir=rtl is set, layout mirrors and the numpad stays LTR"
  - "Given the axe scan, When the shell renders in both directions, Then zero serious violations"
dod: ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]
---

# T-004 — Design tokens, till shell, RTL switch, component base

## Slice

Tokens applied; app shell with nav pattern from MASTER.md; RTL switch; base components (button, input, dialog, toast, numpad, banner-offline) from components.csv.

## Acceptance tests

1. Given tailwind.tokens.css, When the shell renders, Then computed styles use the token variables and tabular numerals
2. Given the language switch, When ar is selected, Then dir=rtl is set, layout mirrors and the numpad stays LTR
3. Given the axe scan, When the shell renders in both directions, Then zero serious violations

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
