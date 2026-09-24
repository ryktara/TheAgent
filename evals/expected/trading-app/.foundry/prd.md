---
pack: trading-app
version: 1
decisions_hash: 97bd6752b826
generated_by: prd-skeleton
---

# PRD — Trading App

## 1. Product

A mobile trading app for retail investors in Pakistan [D:region] that trades listed equities [D:asset-class] on PSX first [D:market], routed through a licensed partner broker [D:custody-model], running on iOS and Android phones [D:platform]. Users open an account with KYC via Sumsub [D:kyc-vendor], deposit by bank transfer [D:funding-rails], see live PSX quotes, place market and limit orders, and track portfolio and P&L, with leveraged trading capped at 2:1 [D:leverage] [D:leverage-max]. The one thing it must never fail at: every leveraged order is preceded by a risk warning and the regulatory disclosures, and no order is ever double-submitted or lost.

## 2. Personas

| Persona | Role in the product | Kept because |
|---------|---------------------|--------------|
| retail-trader | pack persona | pack |
| pro-trader | pack persona | pack |
| compliance-officer | pack persona | pack |
| support | pack persona | pack |
| admin | pack persona | pack |

## 3. Jobs to be done

| Id | Persona | Job | must/should | Screens |
|----|---------|-----|-------------|---------|
| `open-account` | retail-trader | open account | must | signup, kyc-capture |
| `kyc-tier-upgrade` | retail-trader | kyc tier upgrade | must | kyc-capture, kyc-status |
| `review-kyc-case` | compliance-officer | review kyc case | must | kyc-review-queue, kyc-case-detail |
| `deposit-funds` | retail-trader | deposit funds | must | deposit |
| `withdraw-funds` | retail-trader | withdraw funds | must | withdraw |
| `manage-watchlist` | retail-trader | manage watchlist | must | watchlist |
| `view-market-data` | retail-trader | view market data | must | instrument-detail, depth-ladder, chart |
| `place-order` | retail-trader | place order | must | order-ticket, risk-warning |
| `amend-cancel-order` | retail-trader | amend cancel order | must | open-orders, order-ticket |
| `view-positions` | retail-trader | view positions | must | positions |
| `view-portfolio` | retail-trader | view portfolio | must | portfolio |
| `manage-risk-limits` | compliance-officer | manage risk limits | must | risk-limits |
| `handle-margin-call` | retail-trader | handle margin call | must | margin-call, positions |
| `set-leverage` | retail-trader | set leverage | should | leverage-settings, risk-warning |
| `price-alerts` | retail-trader | price alerts | must | alerts |
| `statements-tax` | retail-trader | statements tax | must | statements, tax-report |
| `read-news` | retail-trader | read news | should | news |
| `paper-trade` | retail-trader | paper trade | should | paper-mode, order-ticket |
| `refer-friend` | retail-trader | refer friend | should | referrals |
| `copy-trade` | pro-trader | copy trade | should | copy-leaders, copy-settings |
| `compliance-case-review` | compliance-officer | compliance case review | must | surveillance-alerts, compliance-case-detail |
| `support-tickets` | support | support tickets | must | support-inbox, ticket-detail |
| `manage-instruments` | admin | manage instruments | must | instrument-admin |
| `staff-roles` | admin | staff roles | must | staff-roles |
| `audit-trail` | compliance-officer | audit trail | must | audit-log |

## 4. Scope IN

- `kyc-tiers` — pack must-have
- `account-open` — pack must-have
- `deposit` — pack must-have
- `withdrawal-cooldown` — pack must-have
- `watchlists` — pack must-have
- `live-quotes` — pack must-have
- `depth-ladder` — pack must-have
- `candlestick-charts` — pack must-have
- `order-ticket` — pack must-have
- `market-limit-stop-orders` — pack must-have
- `oco-bracket-orders` — pack must-have
- `positions-pnl` — pack must-have
- `portfolio` — pack must-have
- `risk-limits` — pack must-have
- `margin-calls` — pack must-have
- `risk-warnings` — pack must-have
- `best-execution-disclosure` — pack must-have
- `price-alerts` — pack must-have
- `statements` — pack must-have
- `tax-reports` — pack must-have
- `compliance-cases` — pack must-have
- `market-abuse-surveillance` — pack must-have
- `support-tickets` — pack must-have
- `instrument-admin` — pack must-have
- `staff-roles` — pack must-have
- `audit-trail` — pack must-have
- `double-entry-ledger` — pack must-have
- `leverage` — enabled by leverage = true [D:leverage]

## 5. Scope OUT

- `swap-free-accounts` — not enabled by any decision; later phase
- `crypto-trading` — not enabled by any decision; later phase
- `travel-rule` — not enabled by any decision; later phase
- `paper-trading` — not enabled by any decision; later phase
- `copy-trading` — not enabled by any decision; later phase
- `referrals` — not enabled by any decision; later phase
- `news-feed` — not enabled by any decision; later phase
- `pro-terminal` — not enabled by any decision; later phase
- `two-factor-hardware-key` — not enabled by any decision; later phase
- `open-banking-funding` — not enabled by any decision; later phase

## 6. Non-functional requirements

- Offline: forbidden
- Latency: quote latency p95 150 ms; order ack p95 250 ms; p99 order ack p95 800 ms; stale quote p95 3000 ms
- Devices: per platform decision [D:platform]
- Languages: en [D:region]
- Other: websocket required; idempotent_order_submission required; audit_immutability hash-chained-append-only; uptime 99.95% market hours; rpo_s 0; rto_min 15; rtl required; font_min_px 14; touch_min_dp 44; session_timeout_min 15; mfa required

## 7. Integrations

| Category | Chosen | Source |
|----------|--------|--------|
| market-data | exchange-direct | pack default |
| brokers | fix-4.4-gateway | pack default |
| crypto-exchanges | ccxt-adapter | pack default |
| kyc | sumsub | [D:kyc-vendor] |
| payments | bank-transfer | pack default |
| custody | fireblocks | pack default |
| notifications | push-fcm-apns | pack default |
| surveillance | rules-engine | pack default |

## 8. Regional and compliance

- Region: PK [D:region]
- currency: PKR
- minor units: 2
- regulator: SECP
- exchanges: PSX
- clearing: NCCPL, CDC
- settlement: T+1
- kyc: nadra-verisys, cnic
- ids: UIN, CDC sub-account
- tax: dividends 15% filer / 30% non-filer final; CGT by holding period and filer status, collected via NCCPL
- islamic: shariah-screened-list
- lang: en, ur
- Must controls: `C-ALL-01`, `C-ALL-02`, `C-ALL-03`, `C-ALL-04`, `C-ALL-05`, `C-ALL-06`, `C-ALL-07`, `C-ALL-08`, `C-ALL-09`, `C-PK-01`, `C-PK-02`, `C-PK-03`, `C-PK-04`
- Should controls: `C-ALL-10`, `C-ALL-11`, `C-ALL-12`, `C-PK-05`

## 9. Success metrics

1. 90% of new retail-trader signups complete open-account and KYC tier 1 within 24 hours of starting, measured weekly.
2. 99.9% of place-order submissions acknowledged within 250 ms p95 during PSX market hours, measured daily.
3. 100% of leveraged orders show the risk warning and disclosures before submit, measured per release audit (monthly).
4. 95% of deposit-funds bank transfers credited to the ledger within 30 minutes of bank confirmation, measured weekly.
5. Live quote staleness under 3000 ms for 99.5% of view-market-data sessions, measured daily.

## 10. Open assumptions

Confirmed decisions (human, brief, derived):

- `platform` = "mobile" — brief: brief matched 'mobile trading app' [D:platform]
- `crypto` = false — agent-fact: derived from asset-class=equities [D:crypto]

Assumptions taken from pack defaults; each can be changed by editing `.foundry/decisions.yaml`:

- `asset-class` = "equities" — timeout-default; changeable [D:asset-class]
- `region` = "PK" — timeout-default; changeable [D:region]
- `leverage` = true — timeout-default; changeable [D:leverage]
- `market` = "PSX" — timeout-default; changeable [D:market]
- `custody-model` = "partner-broker" — timeout-default; changeable [D:custody-model]
- `islamic-accounts` = false — timeout-default; changeable [D:islamic-accounts]
- `kyc-vendor` = "sumsub" — timeout-default; changeable [D:kyc-vendor]
- `leverage-max` = 2 — timeout-default; changeable [D:leverage-max]
- `funding-rails` = "bank-transfer" — pack-default; changeable [D:funding-rails]
- `copy-trading` = false — pack-default; changeable [D:copy-trading]
