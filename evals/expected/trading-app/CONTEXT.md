# Trading App — CONTEXT

A mobile trading app for retail investors in Pakistan [D:region] that trades listed equities [D:asset-class] on PSX first [D:market], routed through a licensed partner broker [D:custody-model], running on iOS and Android phones [D:platform].

Ubiquitous language for this project. Every noun in the PRD, the domain model and the code uses
the term in this file; aliases are accepted in conversation and normalised in artifacts.

## Entities

| Entity | Context | States |
|--------|---------|--------|
| Account | accounts | pending-kyc, active, restricted, frozen, closed |
| Wallet | accounts | active, frozen |
| Instrument | markets | draft, tradable, halted, close-only, delisted |
| Order | trading | new, accepted, partially-filled, filled, cancelled, rejected |
| Fill | trading | booked, busted |
| Position | trading | open, closed |
| LedgerEntry | accounts | posted |
| Transfer | accounts | requested, held, approved, sent, settled, failed, cancelled |
| RiskLimit | trading | active, suspended |
| MarginCall | trading | open, met, liquidating, closed |
| KycCase | accounts | draft, submitted, in-review, approved, rejected, needs-info, expired |
| ComplianceCase | compliance | open, investigating, escalated, closed-no-action, reported |
| Alert | trading | armed, triggered, disarmed |
| Statement | compliance | generating, issued |
| Watchlist | markets | active |
| Quote | markets | live, stale |
| Candle | markets | open, closed |
| NewsItem | markets | published, retracted |
| PaperAccount | trading | active, reset |
| Referral | growth | invited, signed-up, qualified, rewarded, void |
| CopyLink | growth | active, paused, stopped |
| SupportTicket | growth | open, pending-customer, escalated, resolved, closed |
| AuditEvent | compliance | recorded |
| Staff | people | active, suspended |

## Glossary

| Term | Definition | Aliases |
|------|------------|---------|
| Account | A client trading account owned by one verified person with a KYC tier and jurisdiction | trading account;brokerage account |
| Wallet | Per-currency balance of an Account derived from ledger entries | cash balance;sub-wallet |
| Instrument | A tradable symbol on a venue with tick size lot size and leverage cap | symbol;security;ticker;contract |
| Order | A client instruction to buy or sell an Instrument | trade order;ticket |
| Fill | One execution against an Order at a price and quantity | execution;trade;exec report |
| Position | Net holding of an Instrument derived from fills | holding |
| LedgerEntry | One debit or credit line of a balanced double-entry transaction | journal line;posting |
| Transfer | A deposit or withdrawal of money or crypto | funding;payout;movement |
| RiskLimit | Configured cap on leverage order value or exposure by scope | limit;risk parameter |
| MarginCall | Notice that equity fell below maintenance margin | margin notice |
| KycCase | A verification case for one KYC tier | kyc application;verification case |
| ComplianceCase | An investigation opened from surveillance or AML alerts | case;investigation |
| AuditEvent | Append-only hash-chained record of an action | audit log entry |
| Bid | Highest price a buyer is willing to pay | bid price |
| Ask | Lowest price a seller is willing to accept | offer;ask price |
| Last | Price of the most recent trade | last price;ltp |
| Slippage | Difference between expected and executed price | execution slippage |
| Market order | Order that executes immediately at the best available price | mkt |
| Limit order | Order that executes only at the limit price or better | lmt |
| Stop order | Order that becomes a market order when the stop price is touched | stop-loss;stop market |
| Stop-limit order | Order that becomes a limit order when the stop price is touched | stop limit |
| OCO | One-cancels-other: two linked orders where a fill of one cancels the other | one cancels other |
| Bracket order | Entry order with attached take-profit and stop-loss children | bracket;attached orders |
| IOC | Immediate or cancel: fill what you can now and cancel the rest | immediate or cancel |
| FOK | Fill or kill: fill fully now or cancel | fill or kill |
| Partially filled | Order state where some but not all quantity has executed | partial fill |
| Order book | List of resting buy and sell orders by price | book;market depth |
| Depth ladder | Vertical price ladder showing sizes at each level with click-to-trade | dom;price ladder |
| Level 2 | Market data with multiple price levels of the book | l2;depth data |
| Candlestick | Chart bar showing open high low close for an interval | candle;ohlc bar |
| Tick size | Smallest allowed price increment | price step |
| Lot size | Smallest allowed quantity increment | board lot;market lot |
| Leverage | Ratio of exposure to margin posted | gearing |
| Margin | Collateral required to hold a leveraged position | initial margin |
| Initial margin | Margin required to open a position | im |
| Maintenance margin | Minimum equity to keep positions open before a margin call | mm;maintenance requirement |
| Margin level | Equity divided by used margin as a percent | margin ratio |
| Stop-out | Level at which positions are closed automatically | liquidation level |
| Equity | Balance plus unrealised P&L | account equity;net liquidation value |
| Mark-to-market | Revaluing positions at current prices | mtm |
| Swap-free account | Islamic account with no overnight interest | islamic account;sharia account |
| Best execution | Duty to obtain the best possible result for client orders | best ex |
| Execution venue | Exchange or market maker where an order executes | venue;market centre |
| KYC | Know your customer identity verification | customer due diligence;cdd |
| Sanctions screening | Checking clients against sanctions lists | watchlist screening |
| Market abuse | Insider dealing and market manipulation | market manipulation |
| Wash trade | Trade where buyer and seller are the same beneficial owner | self-trade |
| Paper trading | Simulated trading with virtual money | demo account;virtual trading |
| Copy trading | Automatically mirroring another trader's orders | social trading;mirror trading |
| Referral | Invite of a new client with a reward on qualification | invite |
| Watchlist | User list of instruments with live quotes | favourites |
| Quote | Live bid ask last snapshot for an Instrument | price;tick |
| NewsItem | A news headline linked to instruments | news;headline |
| Statement | Immutable periodic account document | account statement;contract note |
| Contract note | Trade confirmation issued after execution | trade confirmation |
| Withholding tax | Tax deducted at source on dividends or gains | wht |
| Capital gains tax | Tax on profits from selling securities | cgt |
| CDC sub-account | Account under a broker's CDC participant holding a client's shares | sub account |
| CDC investor account | Account held directly with CDC giving the client control of share movements | ias |
| Nomu | Saudi parallel market for smaller listings | parallel market |
| CMA | Capital Market Authority of Saudi Arabia; also the new name of the UAE federal regulator | capital market authority |
| DFM | Dubai Financial Market | dubai financial market |
| Open banking | Regulated API access to bank accounts for payments and data | account-to-account |

## Feature vocabulary

| Id | Meaning |
|----|---------|
| `kyc-tiers` | kyc tiers (PRD §4) |
| `account-open` | account open (PRD §4) |
| `deposit` | deposit (PRD §4) |
| `withdrawal-cooldown` | withdrawal cooldown (PRD §4) |
| `watchlists` | watchlists (PRD §4) |
| `live-quotes` | live quotes (PRD §4) |
| `depth-ladder` | depth ladder (PRD §4) |
| `candlestick-charts` | candlestick charts (PRD §4) |
| `order-ticket` | order ticket (PRD §4) |
| `market-limit-stop-orders` | market limit stop orders (PRD §4) |
| `oco-bracket-orders` | oco bracket orders (PRD §4) |
| `positions-pnl` | positions pnl (PRD §4) |
| `portfolio` | portfolio (PRD §4) |
| `risk-limits` | risk limits (PRD §4) |
| `margin-calls` | margin calls (PRD §4) |
| `risk-warnings` | risk warnings (PRD §4) |
| `best-execution-disclosure` | best execution disclosure (PRD §4) |
| `price-alerts` | price alerts (PRD §4) |
| `statements` | statements (PRD §4) |
| `tax-reports` | tax reports (PRD §4) |
| `compliance-cases` | compliance cases (PRD §4) |
| `market-abuse-surveillance` | market abuse surveillance (PRD §4) |
| `support-tickets` | support tickets (PRD §4) |
| `instrument-admin` | instrument admin (PRD §4) |
| `staff-roles` | staff roles (PRD §4) |
| `audit-trail` | audit trail (PRD §4) |
| `double-entry-ledger` | double entry ledger (PRD §4) |

## Job vocabulary

| Id | Meaning |
|----|---------|
| `open-account` | open account (PRD §3) |
| `kyc-tier-upgrade` | kyc tier upgrade (PRD §3) |
| `review-kyc-case` | review kyc case (PRD §3) |
| `deposit-funds` | deposit funds (PRD §3) |
| `withdraw-funds` | withdraw funds (PRD §3) |
| `manage-watchlist` | manage watchlist (PRD §3) |
| `view-market-data` | view market data (PRD §3) |
| `place-order` | place order (PRD §3) |
| `amend-cancel-order` | amend cancel order (PRD §3) |
| `view-positions` | view positions (PRD §3) |
| `view-portfolio` | view portfolio (PRD §3) |
| `manage-risk-limits` | manage risk limits (PRD §3) |
| `handle-margin-call` | handle margin call (PRD §3) |
| `set-leverage` | set leverage (PRD §3) |
| `price-alerts` | price alerts (PRD §3) |
| `statements-tax` | statements tax (PRD §3) |
| `read-news` | read news (PRD §3) |
| `paper-trade` | paper trade (PRD §3) |
| `refer-friend` | refer friend (PRD §3) |
| `copy-trade` | copy trade (PRD §3) |
| `compliance-case-review` | compliance case review (PRD §3) |
| `support-tickets` | support tickets (PRD §3) |
| `manage-instruments` | manage instruments (PRD §3) |
| `staff-roles` | staff roles (PRD §3) |
| `audit-trail` | audit trail (PRD §3) |

## Decisions vocabulary

| Decision | Canonical word | Source |
|----------|----------------|--------|
| asset-class | market asset class = equities | timeout-default |
| region | region country = PK | timeout-default |
| leverage | features leverage = true | timeout-default |
| platform | platform targets = mobile | brief |
| market | market primary = PSX | timeout-default |
| custody-model | broker model = partner-broker | timeout-default |
| islamic-accounts | features islamic accounts = false | timeout-default |
| kyc-vendor | kyc provider = sumsub | timeout-default |
| leverage-max | features leverage max = 2 | timeout-default |
| crypto | features crypto = false | agent-fact |
| funding-rails | funding methods = bank-transfer | pack-default |
| copy-trading | features copy trading = false | pack-default |

## Project-specific terms

<!-- model: add up to 10 terms the pack glossary lacks, same table shape -->

| Term | Definition | Aliases |
|------|------------|---------|
