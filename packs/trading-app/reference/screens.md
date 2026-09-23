# Trading App — screens

Every screen has states: empty, loading, error, stale (quotes older than `nfr_defaults.stale_quote_ms`),
restricted (Account restricted or frozen), market-closed. There is no offline state: without a live
connection trading actions disable and a reconnect banner shows. Role access is the minimum role;
admin inherits read of everything but trades nothing. Numbers use tabular numerals; up/down is
always colour plus arrow or sign (see ux-patterns.md TRD-CB-01). RTL: layout mirrors for ar and ur;
prices, quantities, order-book columns and charts stay left-to-right.

## signup

| Aspect | Detail |
|--------|--------|
| Purpose | Create the Account shell before KYC: phone, email, password or passkey, jurisdiction |
| Primary actions | Enter phone → OTP, email, create passkey, pick country of residence, accept terms version |
| Layout zones | Stepper (3 steps); single column form; legal footer with regulator name and licence number |
| States | error: phone in use; blocked-jurisdiction: "We cannot serve residents of X"; pending-kyc on success |
| Data bindings | Account (state pending-kyc, jurisdiction), terms version, AuditEvent signup |
| Role | retail-trader (anonymous until OTP) |
| A11y | OTP field one input with autocomplete one-time-code; errors linked via aria-describedby |
| RTL | Mirrors; phone number and OTP stay LTR |

## kyc-capture

| Aspect | Detail |
|--------|--------|
| Purpose | Collect identity for the requested KYC tier: national ID rail or document + selfie via vendor SDK |
| Primary actions | Choose rail (UAE Pass, Nafath/Absher, NADRA Verisys, or document scan), selfie/liveness, address, source of funds, suitability questionnaire |
| Layout zones | Tier card at top (limits unlocked); step list; vendor SDK frame; save-and-resume |
| States | vendor-down: fall back to document upload; needs-info: highlighted fields from reviewer note |
| Data bindings | KycCase (tier_requested, vendor, vendor_ref), Account.kyc_tier |
| Role | retail-trader |
| A11y | Camera steps have text alternative and manual upload path |
| RTL | Mirrors; ID numbers LTR |

## kyc-status

| Aspect | Detail |
|--------|--------|
| Purpose | Show current tier, limits per tier, and progress of any open KycCase |
| Primary actions | Upgrade tier, respond to needs-info, view expiry of documents |
| Layout zones | Tier ladder (Tier 0 view-only, Tier 1 deposit/trade cap, Tier 2 full, Tier 3 leverage/pro) |
| States | in-review with SLA estimate; rejected with appeal link to support; expired → re-verify CTA |
| Data bindings | KycCase states, Account.kyc_tier, RiskLimit per tier |
| Role | retail-trader |

## kyc-review-queue

| Aspect | Detail |
|--------|--------|
| Purpose | Compliance officer queue of KycCase rows in submitted/in-review, sorted by risk and age |
| Primary actions | Claim case, filter (PEP hit, sanctions hit, high risk country, tier), bulk-assign |
| Layout zones | Filters left; dense table (age, tier, risk score, hits, vendor result); preview pane right |
| States | empty: "Queue clear"; SLA breach rows flagged with icon and label |
| Data bindings | KycCase list, Staff assignee |
| Role | compliance-officer (support read-only) |

## kyc-case-detail

| Aspect | Detail |
|--------|--------|
| Purpose | Decide one KycCase with evidence side by side |
| Primary actions | Approve tier, reject with reason code, request info, escalate to ComplianceCase |
| Layout zones | Document images + liveness score; vendor checks (PEP, sanctions, adverse media); history; decision bar |
| States | four-eyes: decisions on high-risk cases need a second Staff approver |
| Data bindings | KycCase, Account, AuditEvent trail for the case |
| Role | compliance-officer |
| A11y | Decision buttons have confirmation dialogs naming the tier |

## deposit

| Aspect | Detail |
|--------|--------|
| Purpose | Fund a Wallet through an allowed rail |
| Primary actions | Pick rail (bank transfer with virtual IBAN/reference, card via hosted fields, JazzCash/Easypaisa, open banking via Lean/Tarabut, crypto address), enter amount |
| Layout zones | Rail list with fees and ETA; amount with currency; instructions card; recent Transfer list |
| States | tier-cap: "Tier 1 allows up to X"; third-party funds rejected; pending/settled chips |
| Data bindings | Transfer (direction deposit), Wallet.available, LedgerEntry on settlement |
| Role | retail-trader |

## withdraw

| Aspect | Detail |
|--------|--------|
| Purpose | Withdraw to a verified same-name beneficiary |
| Primary actions | Pick beneficiary, amount, confirm with MFA |
| Layout zones | Withdrawable amount (available minus open-margin), beneficiary list, cool-down banner |
| States | cool-down: "New beneficiary usable from 14:05 tomorrow"; held: compliance review; travel-rule form for crypto |
| Data bindings | Transfer (requested → held/approved → sent), Wallet, KycCase tier, cooldown_until |
| Role | retail-trader (compliance-officer reads held/approved) |

## watchlist

| Aspect | Detail |
|--------|--------|
| Purpose | Home screen: user Watchlist rows with live Quote per Instrument |
| Primary actions | Add/remove symbol, reorder, switch list, tap row → instrument-detail, swipe → quick trade |
| Layout zones | List tabs; rows: symbol, name, last, change with arrow and sign, sparkline; search |
| States | empty: suggested lists; stale quotes greyed with clock icon; halted Instrument badge |
| Data bindings | Watchlist, Quote (WebSocket), Instrument state |
| Role | retail-trader |

## instrument-detail

| Aspect | Detail |
|--------|--------|
| Purpose | One Instrument: price, chart, depth, stats, news, position |
| Primary actions | Buy, Sell, set alert, add to watchlist, open full chart |
| Layout zones | Header (bid/ask/last/spread); mini chart; tabs Overview, Depth, News, Position |
| States | halted / close-only banners; market-closed with next session time |
| Data bindings | Instrument, Quote, Candle, Position, NewsItem |
| Role | retail-trader |

## depth-ladder

| Aspect | Detail |
|--------|--------|
| Purpose | Level 2 order book with click-to-trade for pro-trader |
| Primary actions | Click price to prefill ticket; one-click mode (pro only, explicit opt-in) |
| Layout zones | Bid size / price / ask size columns centred on spread; own working orders marked |
| States | depth-unavailable for venues without L2; stale dims ladder |
| Data bindings | Quote depth snapshot and deltas, open Order rows |
| Role | retail-trader (one-click: pro-trader) |

## chart

| Aspect | Detail |
|--------|--------|
| Purpose | Candlestick chart with intervals, indicators, drawings and order markers |
| Primary actions | Change interval, add indicator, drag order line to amend |
| Layout zones | Chart canvas; interval bar; indicator panel; volume sub-pane |
| States | loading history; gap markers for halts |
| Data bindings | Candle (derived), Fill markers, working Order lines |
| Role | retail-trader |
| A11y | Data-table alternative with last 50 candles; hollow vs filled bodies so up/down survives greyscale |

## order-ticket

| Aspect | Detail |
|--------|--------|
| Purpose | Build and submit an Order: market, limit, stop, stop-limit, OCO, bracket |
| Primary actions | Side, type, qty or notional, price(s), TIF, leverage (if enabled), preview, submit |
| Layout zones | Side toggle; type tabs; inputs; cost/margin/fee preview; best-execution note; submit bar |
| States | insufficient buying power; outside tick/lot; risk-warning required; paper mode watermark |
| Data bindings | Order (client_order_id), Wallet.available, RiskLimit, Instrument tick/lot, PaperAccount |
| Role | retail-trader |

## risk-warning

| Aspect | Detail |
|--------|--------|
| Purpose | Interstitial before first leveraged/complex product trade and after each warning version change |
| Primary actions | Read, answer knowledge check, acknowledge |
| Layout zones | Full-screen sheet; loss statistic; plain-language bullets; checkbox; Continue disabled until scrolled |
| Data bindings | Account.risk_ack_at, warning version, AuditEvent |
| Role | retail-trader |

## open-orders

| Aspect | Detail |
|--------|--------|
| Purpose | Working and recent Order rows with amend and cancel |
| Primary actions | Cancel, cancel all, amend price/qty, view Fill list |
| Layout zones | Tabs Working / Filled / Cancelled; OCO and bracket children grouped |
| States | pending-cancel spinner until venue ack; rejected with reason |
| Data bindings | Order, Fill |
| Role | retail-trader |

## positions

| Aspect | Detail |
|--------|--------|
| Purpose | Open Position rows with live P&L and close actions |
| Primary actions | Close, partial close, add stop/take-profit, reverse |
| Layout zones | Totals strip (equity, used margin, free margin, margin level %); position rows |
| States | margin-call banner; liquidating rows locked |
| Data bindings | Position (derived from Fill), Quote, MarginCall |
| Role | retail-trader |

## portfolio

| Aspect | Detail |
|--------|--------|
| Purpose | Account-level view: allocation, performance, cash per currency |
| Primary actions | Switch period, switch account (live/paper), export |
| Layout zones | Equity curve; allocation donut with labels; Wallet balances; realised/unrealised table |
| Data bindings | Account, Wallet, Position, LedgerEntry summaries |
| Role | retail-trader |

## risk-limits

| Aspect | Detail |
|--------|--------|
| Purpose | Maintain RiskLimit rows per jurisdiction, tier, instrument class and account |
| Primary actions | Edit limit (four-eyes), suspend, view accounts near limits |
| Layout zones | Matrix jurisdiction × asset class; detail drawer; change history |
| Data bindings | RiskLimit, AuditEvent |
| Role | compliance-officer |

## margin-call

| Aspect | Detail |
|--------|--------|
| Purpose | Tell the trader equity fell below maintenance and what to do before the deadline |
| Primary actions | Deposit, reduce positions, view stop-out level |
| Layout zones | Deficit amount, deadline countdown, margin level gauge with numeric label, positions sorted by loss |
| States | open → met; liquidating with executed closes list |
| Data bindings | MarginCall, Position, Wallet |
| Role | retail-trader (support read) |

## leverage-settings

| Aspect | Detail |
|--------|--------|
| Purpose | Choose leverage per asset class within the jurisdiction cap |
| Primary actions | Slider snapped to allowed steps, confirm with risk-warning |
| Data bindings | RiskLimit.max_leverage, Instrument.max_leverage, Account.leverage_enabled |
| States | locked: tier or appropriateness test not passed |
| Role | retail-trader |

## alerts

| Aspect | Detail |
|--------|--------|
| Purpose | Manage price and percent-move Alert rows |
| Primary actions | Create (above/below/cross), disarm, re-arm, choose channel |
| Data bindings | Alert, Quote |
| States | triggered list with time; limit of 50 active |
| Role | retail-trader |

## statements

| Aspect | Detail |
|--------|--------|
| Purpose | Daily confirmations, monthly statements, annual summaries |
| Primary actions | View PDF, download, email |
| Data bindings | Statement (issued, checksum) |
| States | generating; corrected statement badge linking to superseded one |
| Role | retail-trader |

## tax-report

| Aspect | Detail |
|--------|--------|
| Purpose | Realised gains, dividends and withholding per tax year per jurisdiction |
| Primary actions | Pick year, download CSV/PDF |
| Data bindings | Fill, LedgerEntry kinds dividend/withholding, Statement kind tax |
| States | report-only disclaimer where the app does not withhold |
| Role | retail-trader |

## news

| Aspect | Detail |
|--------|--------|
| Purpose | NewsItem feed filtered by watchlist and holdings |
| Primary actions | Open article, filter by symbol |
| Data bindings | NewsItem, Watchlist |
| States | retracted items hidden; source attribution always visible |
| Role | retail-trader |

## paper-mode

| Aspect | Detail |
|--------|--------|
| Purpose | Toggle into a PaperAccount with virtual funds for practice |
| Primary actions | Switch mode, reset balance, compare with live |
| Layout zones | Persistent "PAPER" watermark and amber-hatched header on every trading screen |
| Data bindings | PaperAccount, Order (paper) |
| Role | retail-trader |

## referrals

| Aspect | Detail |
|--------|--------|
| Purpose | Invite friends; show Referral status and rewards |
| Primary actions | Share code, view terms |
| Data bindings | Referral |
| States | reward pending until referee KYC and funding |
| Role | retail-trader |

## copy-leaders

| Aspect | Detail |
|--------|--------|
| Purpose | Browse lead traders with verified stats |
| Primary actions | View profile, follow |
| Layout zones | Cards: return, max drawdown, risk score, followers, track-record length |
| States | past-performance disclaimer on every card |
| Data bindings | Account (leader opt-in), Statement-derived stats |
| Role | pro-trader |

## copy-settings

| Aspect | Detail |
|--------|--------|
| Purpose | Configure a CopyLink: allocation, ratio, stop-loss |
| Primary actions | Start, pause, stop, close copied positions |
| Data bindings | CopyLink, RiskLimit |
| Role | pro-trader |

## surveillance-alerts

| Aspect | Detail |
|--------|--------|
| Purpose | Market-abuse and AML alerts (spoofing, wash trades, layering, structuring deposits) |
| Primary actions | Triage, merge into ComplianceCase, dismiss with reason |
| Layout zones | Alert table (rule, account, score, time); timeline preview |
| Data bindings | surveillance rule hits, Order, Fill, Transfer |
| Role | compliance-officer |

## compliance-case-detail

| Aspect | Detail |
|--------|--------|
| Purpose | Investigate one ComplianceCase and record outcome (incl. STR filing reference) |
| Primary actions | Add note, freeze Account, request docs, close, mark reported |
| Data bindings | ComplianceCase, Account, AuditEvent |
| States | four-eyes on freeze and close |
| Role | compliance-officer |

## support-inbox

| Aspect | Detail |
|--------|--------|
| Purpose | SupportTicket queue with complaint flag and SLA |
| Primary actions | Assign, reply, escalate, flag as complaint |
| Data bindings | SupportTicket, Account summary (read) |
| Role | support |

## ticket-detail

| Aspect | Detail |
|--------|--------|
| Purpose | One SupportTicket thread with account context |
| Primary actions | Reply, macro, escalate to compliance, resolve |
| Data bindings | SupportTicket, Order and Transfer read-only |
| Role | support |

## instrument-admin

| Aspect | Detail |
|--------|--------|
| Purpose | Create and maintain Instrument rows: symbol, venue, tick/lot, leverage cap, Shariah flag, state |
| Primary actions | Add, halt, set close-only, delist, bulk import |
| Data bindings | Instrument, RiskLimit, AuditEvent |
| Role | admin |

## staff-roles

| Aspect | Detail |
|--------|--------|
| Purpose | Staff accounts, roles, MFA status, four-eyes groups |
| Primary actions | Invite, suspend, change role (four-eyes) |
| Data bindings | Staff, AuditEvent |
| Role | admin |

## audit-log

| Aspect | Detail |
|--------|--------|
| Purpose | Search the hash-chained AuditEvent log; export for regulators |
| Primary actions | Filter by actor/entity/time, verify chain, export signed CSV |
| Data bindings | AuditEvent |
| States | chain-broken: red banner with first bad row id |
| Role | compliance-officer |
