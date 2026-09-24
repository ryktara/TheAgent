# restaurant-pos reference app: cost

Measured from Claude Code transcripts (`foundry.py metrics ingest`) and priced with `data/model-prices.csv` (public list prices: sonnet for the builder/finisher/reviewers, haiku for ui-review, the parent's own turns priced at the opus tier). Tickets built before P8 have partial transcript coverage; their rows are lower bounds. Figures are what this build cost, not a quote.

## Every ticket

| ticket | type | title | output tok | cache_read | sonnet $ | haiku $ | parent $ | total $ | wall min | blocking fixed |
|---|---|---|---|---|---|---|---|---|---|---|
| T-000 | scaffold | Repo scaffold, toolchain, CI | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| T-001 | feature | Auth: device enrolment, staff PIN, manager o | 54,543 | 21,100,142 | 2.08 | 0.08 | 33.86 | 36.02 | 26 | 5 |
| T-002 | feature | Tenancy and branch scoping with RLS | 27,124 | 15,487,306 | 1.78 | 0.21 | 22.04 | 24.03 | 12 | 0 |
| T-003 | feature | Schema, migrations, seed data | 113,673 | 46,300,402 | 5.55 | 0.30 | 71.13 | 76.97 | 65 | 1 |
| T-004 | feature | Design tokens, shell layout, RTL switch, com | 18,820 | 10,632,387 | 0.91 | 0.13 | 15.49 | 16.53 | 13 | 0 |
| T-005 | feature | Offline store and sync outbox | 98,446 | 17,918,485 | 3.75 | 0.00 | 28.93 | 32.68 | 45 | 1 |
| T-006 | feature | Take order table + merge transfer tables + m | 75,914 | 15,868,636 | 2.87 | 0.00 | 24.07 | 26.94 | 23 | 5 |
| T-007 | feature | Take order counter (order-entry) | 11,871 | 11,172,361 | 1.98 | 0.00 | 13.05 | 15.03 | 8 | 2 |
| T-008 | feature | Send to kitchen (kds, order-entry) | 219,589 | 51,191,573 | 9.06 | 0.21 | 80.41 | 89.69 | 90 | 6 |
| T-009 | feature | Modify order (modifier-sheet, order-entry) | 16,328 | 12,593,986 | 1.93 | 0.00 | 16.17 | 18.09 | 9 | 4 |
| T-010 | feature | Kds bump (kds) | 16,654 | 13,258,668 | 1.94 | 0.00 | 16.57 | 18.51 | 12 | 2 |
| T-011 | feature | Take payment (tender) | 32,445 | 49,696,822 | 19.57 | 0.24 | 1.46 | 21.27 | 64 | 4 |
| T-012 | feature | Print receipt (receipt-preview) | 24,206 | 44,259,929 | 15.12 | 0.09 | 8.08 | 23.29 | 37 | 1 |
| T-013 | feature | Split bill (split-bill) | 21,055 | 36,599,472 | 14.06 | 0.43 | 1.48 | 15.97 | 52 | 0 |
| T-014 | feature | Apply discount (manager-pin, tender) | 59,604 | 110,060,516 | 37.63 | 0.75 | 13.78 | 52.16 | 55 | 7 |
| T-015 | feature | Tips service charge (tender) | 15,295 | 20,313,975 | 7.44 | 0.00 | 1.53 | 8.97 | 28 | 0 |
| T-016 | feature | Hold void comp (manager-pin, order-entry) | 29,151 | 67,107,769 | 23.60 | 0.36 | 1.55 | 25.51 | 53 | 12 |
| T-017 | feature | Manage menu (menu-management) | 32,298 | 51,452,816 | 19.34 | 0.23 | 1.55 | 21.12 | 76 | 0 |
| T-018 | feature | Open close shift (shift-close, shift-open) | 31,279 | 41,183,670 | 15.71 | 0.16 | 4.42 | 20.28 | 63 | 3 |
| T-019 | feature | End of day (end-of-day) | 28,364 | 37,495,903 | 13.79 | 0.27 | 4.43 | 18.49 | 67 | 3 |
| T-020 | feature | Refund (manager-pin, refund) | 59,594 | 91,312,472 | 34.36 | 0.45 | 30.40 | 65.20 | 198 | 10 |
| T-021 | feature | Staff roles (staff-roles) | 17,305 | 45,226,338 | 15.57 | 0.21 | 11.71 | 27.49 | 59 | 3 |
| T-022 | feature | Inventory basic (inventory, recipe-editor) | 21,163 | 36,794,326 | 15.95 | 0.24 | 4.47 | 20.66 | 80 | 2 |
| T-023 | feature | Offline sync (sync-status) | 31,778 | 48,406,222 | 18.70 | 0.29 | 9.02 | 28.01 | 89 | 0 |
| T-024 | feature | Reports (reports) | 18,748 | 49,506,011 | 16.41 | 0.49 | 1.59 | 18.48 | 50 | 3 |
| T-025 | feature | Take order qr (should-have) | 21,544 | 35,398,820 | 12.78 | 0.17 | 4.78 | 17.73 | 47 | 3 |
| T-026 | feature | Multi branch (should-have) | 20,098 | 30,308,868 | 10.53 | 0.28 | 4.16 | 14.98 | 39 | 0 |
| T-027 | feature | Delivery orders (should-have) | 24,546 | 27,333,291 | 12.43 | 0.00 | 3.41 | 15.85 | 36 | 4 |
| T-028 | feature | Loyalty (should-have) | 29,010 | 54,850,702 | 20.27 | 0.27 | 41.84 | 62.38 | 798 | 1 |
| T-029 | feature | Reservations waitlist (should-have) | 20,031 | 20,326,580 | 6.71 | 0.12 | 12.07 | 18.90 | 29 | 2 |
| T-030 | feature | Purchasing (should-have) | 24,032 | 27,491,140 | 7.87 | 0.23 | 18.25 | 26.36 | 29 | 2 |
| T-031 | integration | Integration: payments adapter (network-intl) | 7,316 | 11,299,979 | 5.69 | 0.08 | 1.04 | 6.82 | 24 | 0 |
| T-032 | integration | Integration: delivery adapter (talabat) | 10,033 | 7,271,108 | 4.25 | 0.00 | 0.00 | 4.25 | 18 | 0 |
| T-033 | integration | Integration: einvoicing adapter (ae-fta) | 13,307 | 8,799,454 | 4.14 | 0.07 | 1.00 | 5.21 | 18 | 0 |
| T-034 | compliance | Compliance: access controls (12) | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| T-035 | compliance | Compliance: agentic controls (12) | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| T-036 | compliance | Compliance: api controls (13) | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| T-037 | compliance | Compliance: auth controls (10) | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| T-038 | compliance | Compliance: business-logic controls (17) | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| T-039 | compliance | Compliance: compliance controls (12) | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| T-040 | compliance | Compliance: config controls (11) | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| T-041 | compliance | Compliance: crypto controls (8) | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| T-042 | compliance | Compliance: data controls (17) | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| T-043 | compliance | Compliance: error-log controls (11) | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| T-044 | compliance | Compliance: input controls (14) | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| T-045 | compliance | Compliance: payments controls (3) | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| T-046 | compliance | Compliance: session controls (10) | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| T-047 | compliance | Compliance: supply-chain controls (4) | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| T-900 | release | Release: deploy, observability, runbook | 0 | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| **total** | 49 tickets | | 1,245,164 | 1,168,020,129 | 383.78 | 6.35 | 503.73 | **893.86** | 2312 | 86 |

## Medians per ticket type

| type | tickets | output tok | cache_read | total $ | wall min |
|---|---|---|---|---|---|
| scaffold | 1 | 0 | 0 | 0.00 | 0 |
| feature | 30 | 25,835 | 36,696,899 | 21.20 | 48 |
| integration | 3 | 10,033 | 8,799,454 | 5.21 | 18 |
| compliance | 14 | 0 | 0 | 0.00 | 0 |
| release | 1 | 0 | 0 | 0.00 | 0 |

## Phases 0–10 (design pipeline, run in P2–P6 before transcript metrics existed)

| phase | note | self-reported tokens out | transcript cost $ |
|---|---|---|---|
| 0 | - | - | - |
| 1 | - | - | - |
| 2 | - | - | - |
| 3 | - | - | - |
| 4 | - | - | - |
| 5 | - | - | - |
| 6 | - | - | - |
| 7 | - | - | - |
| 8 | - | - | - |
| 9 | - | - | - |
| 10 | - | - | - |

Phases 0–10 for this app were run with the P2–P6 skills before per-phase transcript ingest existed; the retail-pos generalisation run (P10) measured the same pipeline at $4.29 for T-000 and phases 0–10 in one session at under 30 minutes wall.

