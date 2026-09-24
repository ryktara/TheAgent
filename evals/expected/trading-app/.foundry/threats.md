---
pack: "trading-app"
decisions_hash: "97bd6752b826"
boundaries: ["internet<->edge", "edge<->api", "api<->db", "api<->payment-provider", "terminal<->local-print-bridge", "device<->offline-store"]
---

# Threat model — Trading App

STRIDE per trust boundary from data/threat-patterns.csv, controls from data/security-controls.csv
filtered by this project's decisions. Operation authz matrix from openapi.yaml `x-foundry`.

## Boundary: internet<->edge

| Id | STRIDE | Threat | Controls | Severity |
|----|--------|--------|----------|----------|
| TP-IE-01 | S | Attacker impersonates the web app via phishing domain to capture staff credentials | `SEC-AUTH-08`, `SEC-CRY-01`, `SEC-AUTH-13` | medium |
| TP-IE-02 | T | Request tampering in transit (downgrade, MITM on hotel wifi) | `SEC-CRY-01` | high |
| TP-IE-03 | R | Client denies sending a request; no request ids | `SEC-LOG-01` | low |
| TP-IE-04 | I | Verbose errors or debug endpoints leak stack traces and versions | `SEC-LOG-04`, `SEC-CFG-02`, `SEC-CFG-06` | medium |
| TP-IE-05 | D | Volumetric or credential-stuffing traffic exhausts the api | `SEC-AUTH-04`, `SEC-API-02` | medium |
| TP-IE-06 | E | Missing security headers enable clickjacking or script injection on back-office pages | `SEC-API-08`, `SEC-IN-03` | medium |

## Boundary: edge<->api

| Id | STRIDE | Threat | Controls | Severity |
|----|--------|--------|----------|----------|
| TP-EA-01 | S | Stolen device token reused from another network | `SEC-AUTH-06`, `SEC-SESS-08`, `SEC-API-11` | high |
| TP-EA-02 | T | Client sets server-owned fields (total, state, branch_id) in request bodies | `SEC-ACC-04`, `SEC-BL-01` | high |
| TP-EA-03 | R | Money-moving action without actor identity | `SEC-LOG-02`, `SEC-AUTH-11` | high |
| TP-EA-04 | I | List endpoints leak other branches' orders (BOLA) | `SEC-ACC-02`, `SEC-API-03` | high |
| TP-EA-05 | D | Unbounded pagination or bulk operations exhaust the api | `SEC-IN-10`, `SEC-API-02` | medium |
| TP-EA-06 | E | Operator calls admin routes or refund operation directly | `SEC-ACC-01`, `SEC-ACC-03`, `SEC-SESS-07` | high |
| TP-EA-07 | T | Replay of a payment POST creates a duplicate charge | `SEC-API-01` | high |

## Boundary: api<->db

| Id | STRIDE | Threat | Controls | Severity |
|----|--------|--------|----------|----------|
| TP-AD-01 | S | App role used to bypass RLS with BYPASSRLS | `SEC-ACC-05` | medium |
| TP-AD-02 | T | SQL injection through string-built queries | `SEC-IN-04` | high |
| TP-AD-03 | R | Audit rows updated or deleted after the fact | `SEC-DATA-07`, `SEC-LOG-02` | high |
| TP-AD-04 | I | Backups unencrypted or exposed | `SEC-DATA-06`, `SEC-CRY-03` | medium |
| TP-AD-05 | D | Long-running report queries lock operational tables | `SEC-API-03` | low |
| TP-AD-06 | E | Migration run with superuser in production | `SEC-CFG-01`, `SEC-ACC-05` | medium |

## Boundary: api<->payment-provider

| Id | STRIDE | Threat | Controls | Severity |
|----|--------|--------|----------|----------|
| TP-AT-01 | S | Fake provider endpoint via DNS or SSRF | `SEC-API-06`, `SEC-CRY-01` | medium |
| TP-AT-02 | T | Provider response tampered or malformed leads to wrong Payment state | `SEC-API-12`, `SEC-PAY-05` | medium |
| TP-AT-03 | R | Payment captured at provider but not recorded locally | `SEC-PAY-05`, `SEC-API-05` | high |
| TP-AT-04 | I | Provider secrets leaked through logs or devices | `SEC-PAY-03`, `SEC-CRY-03`, `SEC-DATA-08` | high |
| TP-AT-05 | D | Provider outage blocks all tenders | `SEC-API-05`, `SEC-CFG-08` | medium |
| TP-AT-06 | E | Sandbox keys swapped for live keys without a human step | `SEC-CFG-08`, `SEC-AGT-12` | medium |

## Boundary: terminal<->local-print-bridge

| Id | STRIDE | Threat | Controls | Severity |
|----|--------|--------|----------|----------|
| TP-PB-01 | S | Rogue LAN device sends print jobs or opens the drawer | `SEC-CFG-07` | high |
| TP-PB-02 | T | Control bytes injected through item names into ESC/POS | `SEC-IN-07` | medium |
| TP-PB-03 | R | Drawer opened without a tender recorded | `SEC-LOG-02`, `SEC-BL-07` | medium |
| TP-PB-04 | I | Receipt data sniffed on the LAN | `SEC-CFG-07`, `SEC-CRY-01` | low |
| TP-PB-05 | D | Printer offline blocks tender completion | `SEC-API-05` | low |

## Boundary: device<->offline-store

| Id | STRIDE | Threat | Controls | Severity |
|----|--------|--------|----------|----------|
| TP-DO-01 | T | Duplicate or replayed outbox events create double orders | `SEC-BL-11`, `SEC-API-11` | high |
| TP-DO-02 | R | Receipt numbers reused across devices | `SEC-BL-08`, `SEC-OFF-04` | high |
| TP-DO-03 | I | PII persisted beyond the shift on the device | `SEC-OFF-02`, `SEC-DATA-03` | medium |
| TP-DO-04 | D | Sync storm after reconnect starves ordering | `SEC-OFF-05` | medium |
| TP-DO-05 | T | Conflicting edits resolved non-deterministically | `SEC-OFF-03` | medium |

## Boundary: admin

| Id | STRIDE | Threat | Controls | Severity |
|----|--------|--------|----------|----------|
| TP-AM-01 | S | Owner account taken over via password reuse | `SEC-AUTH-02`, `SEC-AUTH-08` | high |
| TP-AM-02 | T | Role matrix edited to grant refund rights to operators | `SEC-ACC-07`, `SEC-LOG-02` | high |
| TP-AM-03 | R | Settings changed without audit | `SEC-LOG-02` | medium |
| TP-AM-04 | I | Export of all customers by a non-owner | `SEC-ACC-03`, `SEC-ACC-09` | medium |
| TP-AM-05 | E | Last owner demoted, locking out the organisation | `SEC-ACC-06` | medium |

## Operation authz matrix

| operationId | Job | Personas | Authz | Audit | Idempotent | Money | Controls |
|-------------|-----|----------|-------|-------|------------|-------|----------|
| `account_list` | read | retail-trader, admin | role in [retail-trader, admin] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `account_create` | create | retail-trader, admin | role in [retail-trader, admin] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `account_get` | read | retail-trader, admin | role in [retail-trader, admin] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `account_update` | update | retail-trader, admin | role in [retail-trader, admin] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `account_archive` | archive | retail-trader, admin | role == admin | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `instrument_list` | read | retail-trader, admin | role in [retail-trader, admin] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `instrument_create` | create | retail-trader, admin | role in [retail-trader, admin] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `instrument_get` | read | retail-trader, admin | role in [retail-trader, admin] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `instrument_update` | update | retail-trader, admin | role in [retail-trader, admin] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `instrument_archive` | archive | retail-trader, admin | role == admin | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_list` | read | retail-trader, admin, compliance-officer, support | role in [retail-trader, admin] and branch scope; or role == compliance-officer (read only); or role == support (read only) | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_create` | create | retail-trader, admin | role in [retail-trader, admin] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_get` | read | retail-trader, admin, compliance-officer, support | role in [retail-trader, admin] and same branch; or role == compliance-officer (read only); or role == support (read only) | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_update` | update | retail-trader, admin | role in [retail-trader, admin] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_archive` | archive | retail-trader, admin | role == admin | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `ledger_entry_list` | read | retail-trader, admin | role == admin | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `ledger_entry_get` | read | retail-trader, admin | role == admin | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `transfer_list` | read | retail-trader, admin, compliance-officer | role in [retail-trader, admin] and branch scope; or role == compliance-officer (read only, states requested, held, approved) | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `transfer_create` | create | retail-trader, admin | role in [retail-trader, admin] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `transfer_get` | read | retail-trader, admin, compliance-officer | role in [retail-trader, admin] and same branch; or role == compliance-officer (read only, states requested, held, approved) | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `transfer_update` | update | retail-trader, admin | role in [retail-trader, admin] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `transfer_archive` | archive | retail-trader, admin | role == admin | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `risk_limit_list` | read | retail-trader, admin | role == admin | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `risk_limit_get` | read | retail-trader, admin | role == admin | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `margin_call_list` | read | retail-trader, admin, support | role in [retail-trader, admin] and branch scope; or role == support (read only) | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `margin_call_create` | create | retail-trader, admin | role in [retail-trader, admin] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `margin_call_get` | read | retail-trader, admin, support | role in [retail-trader, admin] and same branch; or role == support (read only) | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `margin_call_update` | update | retail-trader, admin | role in [retail-trader, admin] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `margin_call_archive` | archive | retail-trader, admin | role == admin | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `kyc_case_list` | read | retail-trader, admin, support | role in [retail-trader, admin] and branch scope; or role == support (read only) | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `kyc_case_create` | create | retail-trader, admin | role in [retail-trader, admin] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `kyc_case_get` | read | retail-trader, admin, support | role in [retail-trader, admin] and same branch; or role == support (read only) | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `kyc_case_update` | update | retail-trader, admin | role in [retail-trader, admin] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `kyc_case_archive` | archive | retail-trader, admin | role == admin | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `compliance_case_list` | read | compliance-officer, admin | role == admin | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `compliance_case_get` | read | compliance-officer, admin | role == admin | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `alert_list` | read | retail-trader, admin | role in [retail-trader, admin] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `alert_create` | create | retail-trader, admin | role in [retail-trader, admin] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `alert_get` | read | retail-trader, admin | role in [retail-trader, admin] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `alert_update` | update | retail-trader, admin | role in [retail-trader, admin] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `alert_archive` | archive | retail-trader, admin | role == admin | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `statement_list` | read | retail-trader, admin | role in [retail-trader, admin] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `statement_create` | create | retail-trader, admin | role in [retail-trader, admin] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `statement_get` | read | retail-trader, admin | role in [retail-trader, admin] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `statement_update` | update | retail-trader, admin | role in [retail-trader, admin] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `statement_archive` | archive | retail-trader, admin | role == admin | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `watchlist_list` | read | retail-trader, admin | role in [retail-trader, admin] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `watchlist_create` | create | retail-trader, admin | role in [retail-trader, admin] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `watchlist_get` | read | retail-trader, admin | role in [retail-trader, admin] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `watchlist_update` | update | retail-trader, admin | role in [retail-trader, admin] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `watchlist_archive` | archive | retail-trader, admin | role == admin | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `news_item_list` | read | retail-trader, admin | role == admin | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `news_item_get` | read | retail-trader, admin | role == admin | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `paper_account_list` | read | retail-trader, admin | role in [retail-trader, admin] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `paper_account_create` | create | retail-trader, admin | role in [retail-trader, admin] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `paper_account_get` | read | retail-trader, admin | role in [retail-trader, admin] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `paper_account_update` | update | retail-trader, admin | role in [retail-trader, admin] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `paper_account_archive` | archive | retail-trader, admin | role == admin | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `referral_list` | read | retail-trader, admin | role in [retail-trader, admin] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `referral_create` | create | retail-trader, admin | role in [retail-trader, admin] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `referral_get` | read | retail-trader, admin | role in [retail-trader, admin] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `referral_update` | update | retail-trader, admin | role in [retail-trader, admin] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `referral_archive` | archive | retail-trader, admin | role == admin | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `copy_link_list` | read | pro-trader, admin | role in [pro-trader, admin] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `copy_link_create` | create | pro-trader, admin | role in [pro-trader, admin] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `copy_link_get` | read | pro-trader, admin | role in [pro-trader, admin] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `copy_link_update` | update | pro-trader, admin | role in [pro-trader, admin] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `copy_link_archive` | archive | pro-trader, admin | role == admin | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `support_ticket_list` | read | retail-trader, admin | role in [retail-trader, admin] and branch scope | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `support_ticket_create` | create | retail-trader, admin | role in [retail-trader, admin] and branch scope | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `support_ticket_get` | read | retail-trader, admin | role in [retail-trader, admin] and same branch | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `support_ticket_update` | update | retail-trader, admin | role in [retail-trader, admin] and same branch; state guards per domain.yaml | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `support_ticket_archive` | archive | retail-trader, admin | role == admin | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `audit_event_list` | read | compliance-officer, admin | role == admin | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `audit_event_get` | read | compliance-officer, admin | role == admin | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `staff_list` | read | admin | role == admin | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `staff_get` | read | admin | role == admin | no | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `account_open_account` | open-account | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `kyc_case_kyc_tier_upgrade` | kyc-tier-upgrade | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `kyc_case_review_kyc_case` | review-kyc-case | compliance-officer | role == compliance-officer or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `transfer_deposit_funds` | deposit-funds | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `transfer_withdraw_funds` | withdraw-funds | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `watchlist_manage_watchlist` | manage-watchlist | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `instrument_view_market_data` | view-market-data | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `order_place_order` | place-order | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `order_amend_cancel_order` | amend-cancel-order | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `position_view_positions` | view-positions | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `account_view_portfolio` | view-portfolio | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `risk_limit_manage_risk_limits` | manage-risk-limits | compliance-officer | role == compliance-officer or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `margin_call_handle_margin_call` | handle-margin-call | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `risk_limit_set_leverage` | set-leverage | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `alert_price_alerts` | price-alerts | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `statement_statements_tax` | statements-tax | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `news_item_read_news` | read-news | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `paper_account_paper_trade` | paper-trade | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `referral_refer_friend` | refer-friend | retail-trader | role == retail-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `copy_link_copy_trade` | copy-trade | pro-trader | role == pro-trader or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06` |
| `compliance_case_compliance_case_review` | compliance-case-review | compliance-officer | role == compliance-officer or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `support_ticket_support_tickets` | support-tickets | support | role == support or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `instrument_manage_instruments` | manage-instruments | admin | role == admin or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `staff_staff_roles` | staff-roles | admin | role == admin or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `audit_event_audit_trail` | audit-trail | compliance-officer | role == compliance-officer or role == admin; branch scope; step-up re-authentication when the job guards it | yes | yes | no | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01` |
| `webhook_payments` | payments-webhook | system | provider signature verified; idempotent on (provider, event_id) | yes | yes | yes | `SEC-ACC-01`, `SEC-ACC-02`, `SEC-IN-01`, `SEC-LOG-01`, `SEC-ACC-04`, `SEC-LOG-02`, `SEC-BL-01`, `SEC-BL-03`, `SEC-BL-04`, `SEC-BL-05`, `SEC-BL-06`, `SEC-API-04`, `SEC-CRY-06` |

## Top 10 risks

| Rank | Score | Boundary | Threat | Controls |
|-----:|------:|----------|--------|----------|
| 1 | 9 | edge<->api | Stolen device token reused from another network (TP-EA-01) | `SEC-AUTH-06`, `SEC-SESS-08`, `SEC-API-11` |
| 2 | 9 | edge<->api | Client sets server-owned fields (total, state, branch_id) in request bodies (TP-EA-02) | `SEC-ACC-04`, `SEC-BL-01` |
| 3 | 9 | edge<->api | Money-moving action without actor identity (TP-EA-03) | `SEC-LOG-02`, `SEC-AUTH-11` |
| 4 | 9 | edge<->api | List endpoints leak other branches' orders (BOLA) (TP-EA-04) | `SEC-ACC-02`, `SEC-API-03` |
| 5 | 9 | edge<->api | Operator calls admin routes or refund operation directly (TP-EA-06) | `SEC-ACC-01`, `SEC-ACC-03`, `SEC-SESS-07` |
| 6 | 9 | edge<->api | Replay of a payment POST creates a duplicate charge (TP-EA-07) | `SEC-API-01` |
| 7 | 9 | internet<->edge | Request tampering in transit (downgrade, MITM on hotel wifi) (TP-IE-02) | `SEC-CRY-01` |
| 8 | 6 | admin | Owner account taken over via password reuse (TP-AM-01) | `SEC-AUTH-02`, `SEC-AUTH-08` |
| 9 | 6 | admin | Role matrix edited to grant refund rights to operators (TP-AM-02) | `SEC-ACC-07`, `SEC-LOG-02` |
| 10 | 6 | api<->payment-provider | Payment captured at provider but not recorded locally (TP-AT-03) | `SEC-PAY-05`, `SEC-API-05` |

## Abuse cases

<!-- model: write one table per risky workflow (payment, refund, offline sync): actor, goal, path, control that stops it, residual risk -->

| Workflow | Actor | Goal | Path | Stopped by | Residual |
|----------|-------|------|------|------------|----------|
| payment | retail-trader | pocket cash by marking card paid | mark tender card without terminal approval | `SEC-PAY-02` approval code required; `SEC-PAY-05` nightly reconciliation | manual approval-code entry offline, audited |
| refund | manager | refund to own card | refund to a tender not on the order | `SEC-PAY-04` refund via provider token of the original payment; `SEC-BL-04` cap | cash refund fallback needs owner PIN |
| offline sync | device | replay events to duplicate orders | resend outbox with reused seq | `SEC-API-11` monotonic seq; `SEC-BL-11` client UUID dedupe | none beyond audit |

## Blocking findings

- none
