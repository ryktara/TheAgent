# Trading App — workflows

Notation: (S) server step; → state transition; ✗ failure path. Every transition on Account,
KycCase, Transfer, Order, MarginCall, RiskLimit, Instrument and ComplianceCase writes one
AuditEvent (see compliance.md C-ALL-05). Money moves only as balanced LedgerEntry sets.

## 1. Onboarding with KYC tiers (retail-trader, compliance-officer)

| Step | Actor | Action | Transition | Failure |
|-----:|-------|--------|------------|---------|
| 1 | retail-trader | Sign up: phone OTP, email, passkey, residence | Account → pending-kyc | blocked jurisdiction ✗ stop with notice |
| 2 | retail-trader | Tier 1: national ID rail (UAE Pass / Nafath / NADRA Verisys) or document + liveness | KycCase draft → submitted | vendor down ✗ document upload fallback |
| 3 | (S) | Vendor callback: identity, PEP, sanctions, adverse media | KycCase → in-review (hit) or approved (clean, low risk) | callback timeout ✗ poll then manual |
| 4 | compliance-officer | Review hits, decide | KycCase → approved / rejected / needs-info | high risk ✗ needs second approver |
| 5 | (S) | Set Account.kyc_tier; Account → active | RiskLimit for tier applies | |
| 6 | retail-trader | Suitability / appropriateness questionnaire for leverage or complex products | Account.leverage_enabled | fail ✗ leverage stays off; cool-off before retry |
| 7 | retail-trader | Tier 2/3 upgrade: proof of address, source of funds/wealth | new KycCase | expiry ✗ Account → restricted until re-verified |

PK specifics: broker submits UIN request to NCCPL and opens a CDC sub-account (or links a CDC
investor account) before first trade; SA: Nafath/Absher identity then broker account at the
Tadawul member; AE: UAE Pass for Emirates ID holders, document route for others.

## 2. Funding (deposit)

1. retail-trader picks rail; (S) creates Transfer requested with unique reference.
2. Rail confirms (bank webhook, card capture, wallet callback, open-banking payment status).
3. (S) name-match payer to Account owner ✗ third-party funds → Transfer held → compliance-officer.
4. Transfer → settled; LedgerEntry pair: debit client-money bank, credit client Wallet.
5. Tier cap check: cumulative deposits above tier limit → held pending tier upgrade.

## 3. Withdrawal with cool-down

| Step | Actor | Action | Transition | Failure |
|-----:|-------|--------|------------|---------|
| 1 | retail-trader | Add beneficiary (same-name bank account or whitelisted wallet address) | cooldown_until = now + 24h (configurable) | name mismatch ✗ reject |
| 2 | retail-trader | Request withdrawal with MFA | Transfer requested; Wallet.reserved += amount | amount > withdrawable ✗ |
| 3 | (S) | Checks: KYC tier, cool-down elapsed, no open MarginCall, velocity, AML rules | → approved or held | held ✗ compliance-officer queue |
| 4 | compliance-officer | Clear or refuse held Transfer | held → approved / cancelled | refuse releases reservation |
| 5 | (S) | Crypto only: travel-rule payload to beneficiary VASP above threshold | travel_rule_ref set | counterparty unknown ✗ held |
| 6 | (S) | Send via rail / custody (Fireblocks policy) | → sent → settled | fail ✗ → failed, reversal LedgerEntry |

## 4. Place an order (market, limit, stop, OCO, bracket)

| Step | Actor | Action | Transition | Failure |
|-----:|-------|--------|------------|---------|
| 1 | retail-trader | Build ticket; client generates client_order_id | Order new (local) | tick/lot invalid ✗ inline |
| 2 | retail-trader | Leveraged/complex product and no current ack | risk-warning shown | decline ✗ no Order |
| 3 | (S) | Idempotency: existing client_order_id → return it | | |
| 4 | (S) | Pre-trade: Instrument tradable, RiskLimit, buying power/margin, fat-finger band, restricted list | Wallet.reserved += cost | fail → rejected with reason |
| 5 | (S) | Route to venue (FIX NewOrderSingle or REST) | Order → accepted on venue ack | venue reject → rejected; timeout → status query |
| 6 | (S) | Execution reports | Fill booked; Order → partially-filled / filled; Position recomputed | fill after cancel ✗ alert + reconciliation |
| 7 | (S) | OCO: one leg fills → cancel sibling; bracket: parent fill arms stop and take-profit children | children accepted | |
| 8 | (S) | Trade confirmation Statement issued end of day | | |

Cancel/amend: cancel request → pending-cancel on client; venue ack → cancelled; a fill racing the
cancel is booked and the cancel applies to remaining qty only.

## 5. Margin call and stop-out

| Step | Actor | Action | Transition | Failure |
|-----:|-------|--------|------------|---------|
| 1 | (S) | Mark-to-market on each Quote tick batch; equity < maintenance | MarginCall open; push + email + in-app banner | |
| 2 | retail-trader | Deposit or reduce positions | equity ≥ maintenance → MarginCall met | |
| 3 | (S) | Deadline passes or equity < stop-out | MarginCall → liquidating; close largest-loss position first, re-check after each close | venue closed ✗ queue at open, block new risk |
| 4 | (S) | Equity back above maintenance or no positions left | MarginCall closed | negative balance ✗ negative-balance protection write-off where offered |
| 5 | support | Answer trader questions using read-only margin-call view | | |

## 6. Compliance case review (compliance-officer)

1. Surveillance rules raise alerts: spoofing/layering, wash trades, marking the close, insider
   pre-news trading, deposit structuring, rapid in-out funding, copy-trading abuse.
2. Officer triages in surveillance-alerts; merges related alerts into a ComplianceCase open.
3. investigating: pulls Order/Fill/Transfer timelines, requests documents via support.
4. Outcome: closed-no-action (reason), escalated (MLRO), or reported (STR ref from goAML or
   national FIU portal); freeze Account needs second Staff approval.
5. Evidence pack exported from audit-log with chain verification.

## 7. Support ticket and complaint

1. support receives ticket (in-app, email); tags category; flags complaint when the client
   expresses dissatisfaction with a service outcome.
2. Complaint → acknowledgement sent immediately with due date; escalation at SLA 80%.
3. Resolution recorded with root cause; final response letter includes regulator escalation route.

## 8. Admin: instrument lifecycle

draft → tradable (after tick/lot/leverage/Shariah flag set and four-eyes approval) → halted
(venue halt, auto from feed) → tradable, or → close-only (corporate action, delisting notice) →
delisted. Changing max_leverage re-evaluates open positions' margin at next tick.

## 9. Paper trading

Switch to PaperAccount; orders fill against live Quote with simulated slippage; no LedgerEntry to
real Wallet; reset restores virtual balance; every screen shows the PAPER watermark.

## 10. Copy trading (pro-trader)

Leader opts in (Tier 3, track record ≥ 90 days); follower creates CopyLink with allocation; each
leader Fill generates a proportional follower Order that passes the follower's own risk checks;
stop-loss on the link pauses copying and optionally closes copied positions.

## 11. Statements and tax

Daily confirmations after close; monthly statements by 5th business day; annual tax pack per
jurisdiction (PK: CGT and dividend WHT as reported by NCCPL/CDC; SA: dividend WHT for
non-residents; AE: report-only). Statements are immutable; corrections supersede.

## 12. Price alerts

1. retail-trader creates Alert armed with condition (above, below, percent move) and threshold.
2. (S) evaluates on each Quote; on crossing → triggered; notification sent once; last_side stored.
3. Re-arm happens only when the Quote returns across the threshold (hysteresis band optional).
4. Disarmed alerts are kept 30 days for history.

## 13. Risk limit change (compliance-officer, four-eyes)

1. Officer drafts a RiskLimit change (e.g. max_leverage for crypto in AE from 5 to 2).
2. Second officer approves; (S) applies at next tick; AuditEvent with before/after hashes.
3. Positions over the new cap: no forced close; new risk blocked; client notified.

## 14. Referral qualification

invited → signed-up (code captured at signup) → qualified (referee KycCase approved and first
deposit settled) → rewarded (LedgerEntry marketing expense → referrer Wallet); abuse rules void
self-referrals and shared devices.
