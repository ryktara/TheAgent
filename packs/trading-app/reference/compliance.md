# Trading App — compliance

Control ids are referenced from `pack.yaml` `compliance_must` / `compliance_should` and from
`.foundry/compliance.yaml` in phase 9. Each control maps to features (must_have / should_have ids)
and names its verification. Facts marked UNVERIFIED in sources.md carry the same mark here.
The pack is `regulated: true`: the release gate stays blocked until a human confirms the licence
(own or partner broker) covers every activity the app performs.

## All regions

| Id | Control | Features | Verification |
|----|---------|----------|--------------|
| C-ALL-01 | KYC/AML: identity verified before funding; tiered limits; PEP, sanctions and adverse-media screening at onboarding and on list updates; periodic re-KYC by risk | kyc-tiers, account-open, deposit | integration test with stub-kyc; sanctions rescreen job |
| C-ALL-02 | Risk warning and appropriateness check before the first leveraged or complex-product Order and after each warning version change; acknowledgement stored | risk-warnings, leverage | e2e: leveraged Order blocked without ack |
| C-ALL-03 | Best-execution: order-execution policy disclosed before first trade; per-order venue, time and price recorded; periodic execution-quality review | best-execution-disclosure, order-ticket | policy page exists; Fill carries venue and timestamps |
| C-ALL-04 | Segregation of client money: client Wallet balances held in designated client accounts, never netted with house funds; daily reconciliation ledger vs bank/custodian | double-entry-ledger, deposit | reconciliation job; invariant test |
| C-ALL-05 | Immutable audit trail: append-only, hash-chained AuditEvent for orders, transfers, KYC decisions, limit changes, staff actions; clock-synchronised timestamps | audit-trail | DB grants (no UPDATE/DELETE); chain verify test |
| C-ALL-06 | Records and statements retained at least 5 years (7 where regulator requires; configurable per jurisdiction); exportable | statements, tax-reports | retention config test |
| C-ALL-07 | Complaints handling: logged, acknowledged, answered within SLA, escalation route to regulator/ombudsman shown | support-tickets | workflow test |
| C-ALL-08 | Market-abuse monitoring: surveillance rules for spoofing, layering, wash trades, insider patterns; alerts reviewed and cases recorded | market-abuse-surveillance, compliance-cases | rules unit tests with fixtures |
| C-ALL-09 | Withdrawal controls: same-name beneficiary, cool-down on new beneficiaries, MFA, velocity limits; suspicious transaction reporting to national FIU | withdrawal-cooldown | e2e: withdrawal blocked during cool-down |
| C-ALL-10 | Crypto travel rule: originator/beneficiary data exchanged for virtual-asset transfers above the local threshold (FATF Rec. 16) | travel-rule, crypto-trading | test: transfer held without payload |
| C-ALL-11 | Negative-balance protection and stop-out for retail leveraged accounts | leverage, margin-calls | margin engine tests |
| C-ALL-12 | Personal data minimised, encrypted at rest, data-subject requests honoured within legal retention limits (UAE PDPL, KSA PDPL, PK draft law) | account-open | DPIA; field-level encryption review |

## UAE (AE)

| Id | Control | Features | Verification |
|----|---------|----------|--------------|
| C-AE-01 | Onshore securities / derivatives dealing only under a licence from the Capital Market Authority (formerly SCA, renamed 1 Jan 2026) or via a licensed partner; licence number displayed | account-open | human confirm at release gate |
| C-AE-02 | Virtual-asset activity in Dubai (outside DIFC) requires a VARA licence for the specific activity (exchange, broker-dealer, custody…); VARA travel rule above AED 3,500 | crypto-trading, travel-rule | human confirm; transfer test at AED 3,501 |
| C-AE-03 | If the entity sits in DIFC (DFSA) or ADGM (FSRA): retail leverage caps 30:1 majors / 20:1 minors, gold, major indices / 10:1 other commodities; 5:1 shares; 2:1 crypto (DFSA/FSRA figures from secondary source, UNVERIFIED against rulebook) | leverage, risk-limits | RiskLimit fixture per free zone |
| C-AE-04 | KYC with Emirates ID; UAE Pass as preferred digital identity rail where the licence permits (UNVERIFIED integration terms) | kyc-tiers | stub test |
| C-AE-05 | Islamic swap-free account option: no overnight interest; any admin fee disclosed and flat (UNVERIFIED Shariah board requirement) | swap-free-accounts | ledger test: no swap entries |
| C-AE-06 | Arabic disclosures and risk warnings alongside English | risk-warnings | copy review |

## Saudi Arabia (SA)

| Id | Control | Features | Verification |
|----|---------|----------|--------------|
| C-SA-01 | Securities business only by a CMA-authorised person (or its partner); Tadawul member routing | account-open | human confirm |
| C-SA-02 | T+2 settlement for Tadawul-listed securities; buying power reflects unsettled proceeds | positions-pnl, order-ticket | settlement date tests |
| C-SA-03 | Identity through Nafath/Absher national identity; Iqama for residents (UNVERIFIED broker integration terms) | kyc-tiers | stub test |
| C-SA-04 | Sharia-compliant product flag and screened-instrument list; Arabic-first UI | swap-free-accounts | instrument flag test |

## Pakistan (PK)

| Id | Control | Features | Verification |
|----|---------|----------|--------------|
| C-PK-01 | Brokerage only by a SECP-licensed securities broker (Securities Act 2015, Securities Brokers (Licensing and Operations) Regulations 2016) or via a licensed partner | account-open | human confirm |
| C-PK-02 | UIN issued via NCCPL and CDC sub-account (or linked CDC investor account) before the first trade | kyc-tiers | onboarding test |
| C-PK-03 | T+1 settlement at PSX from 9 Feb 2026; buying power and statements follow it | order-ticket, statements | settlement date tests |
| C-PK-04 | Identity verification via NADRA Verisys against CNIC | kyc-tiers | stub test |
| C-PK-05 | Tax pack shows dividend tax (15% filer / 30% non-filer) and CGT as collected by NCCPL; rates configurable, VERIFY-BEFORE-GO-LIVE | tax-reports | fixture test |

## Generic

| Id | Control | Features | Verification |
|----|---------|----------|--------------|
| C-GEN-01 | Local regulator and licence confirmed by a human before release; all C-ALL controls apply with local thresholds | account-open | release gate |

## Control to screen map

| Id | Screens |
|----|---------|
| C-ALL-01 | signup, kyc-capture, kyc-status, kyc-review-queue, kyc-case-detail |
| C-ALL-02 | risk-warning, leverage-settings, order-ticket |
| C-ALL-03 | order-ticket, open-orders, statements |
| C-ALL-04 | deposit, withdraw, portfolio |
| C-ALL-05 | audit-log, staff-roles, risk-limits, instrument-admin |
| C-ALL-06 | statements, tax-report |
| C-ALL-07 | support-inbox, ticket-detail |
| C-ALL-08 | surveillance-alerts, compliance-case-detail |
| C-ALL-09 | withdraw, kyc-case-detail |
| C-ALL-10 | withdraw, deposit |
| C-ALL-11 | margin-call, positions |
| C-ALL-12 | signup, kyc-capture |

## Region selection rules

- Only the decided region's `compliance_must` / `compliance_should` reach the PRD; C-ALL controls
  always apply.
- AE has three regimes: onshore federal (CMA, formerly SCA), Dubai virtual assets (VARA), and the
  financial free zones (DIFC → DFSA, ADGM → FSRA). The licence question in phase 10 records which
  regime the entity holds; controls for the other regimes are dropped.
- A crypto product in AE onshore outside Dubai needs a separate determination (CMA virtual-asset
  rules); treated as UNVERIFIED and escalated to the founder.
- SA crypto trading for retail is not assumed to be permitted; the pack disables crypto for SA
  unless the founder supplies a licence reference (UNVERIFIED).
- PK: crypto trading is not assumed to be permitted for retail; disabled unless a licence
  reference is supplied (UNVERIFIED).

## Release gate evidence (regulated pack)

| Evidence | Owner | Blocks release |
|----------|-------|----------------|
| Licence number and regulator name, or partner broker agreement | founder | yes |
| Order-execution policy published | compliance-officer | yes |
| Risk-warning copy approved per jurisdiction and language | compliance-officer | yes |
| Client-money bank / custodian designation letter | founder | yes |
| KYC vendor DPA and data residency | founder | yes |
| Surveillance rule set reviewed | compliance-officer | yes |
| Complaints procedure and regulator escalation text | support lead | yes |
| Penetration test report | engineering | yes |
| Retention periods per jurisdiction confirmed | compliance-officer | yes |
| Every UNVERIFIED row in sources.md resolved or accepted in writing | founder | yes |

## Verification notes

- Ledger invariants (debits = credits, Wallet = sum of entries) run as property tests and as a
  nightly reconciliation job that raises a ComplianceCase on any break.
- Audit chain verification runs nightly and on export; a break pages on-call and freezes staff
  write actions until reviewed.
- Leverage caps are data (RiskLimit rows), never constants in code; tests load per-jurisdiction
  fixtures.
- Travel-rule threshold is configuration keyed by jurisdiction (AE-VARA AED 3,500 verified).
- Tax rates are configuration with `as_of` and `note: VERIFY-BEFORE-GO-LIVE`.
- Statements carry a SHA-256 checksum stored in Statement.checksum and in the AuditEvent.
- Complaint SLA timers are business-day aware per jurisdiction calendar.
- Market-hours calendars (PSX, Tadawul, DFM/ADX) come from venue data, never hard-coded.
