# Trading App — UX patterns

Dense, calm, honest. Money UI where a mis-tap costs real money. Every pattern names its id so
screen specs can cite it. Baseline: dark theme default (palette trading-dark-cb), touch 44 dp,
text 14 px minimum, contrast 4.5:1, tabular numerals everywhere a number appears, numbers LTR
inside RTL layouts.

## Colour-blind-safe direction

- **TRD-CB-01 Never colour alone.** Up = blue + ▲ + leading "+"; down = orange + ▼ + leading "−".
  The glyph and sign carry the meaning; colour only reinforces. Deuteranopia/protanopia safe.
- **TRD-CB-02 P&L cells.** Value, sign, arrow, and percent in brackets: "+1,240.50 ▲ (+2.1%)".
  Zero shows "0.00" in neutral text with "—" glyph.
- **TRD-CB-03 Candles.** Up candles hollow outline, down candles filled; colour follows
  TRD-CB-01. Greyscale screenshot still readable.
- **TRD-CB-04 Flash on tick.** Price cell background pulses 300 ms in direction colour; respects
  prefers-reduced-motion (no pulse, arrow only).
- **TRD-CB-05 User setting.** Option "Green up / red down" for users who expect it, still paired
  with arrows; region default may be set by founder.

## Order ticket

- **TRD-TKT-01 Side first.** Buy/Sell as a two-segment toggle with text labels, full-width submit
  button repeats the side and quantity: "Buy 100 ENGRO @ Limit 312.50".
- **TRD-TKT-02 Type tabs.** Market, Limit, Stop, Stop-limit, OCO, Bracket; only types the
  venue supports are shown; each tab has one-line help.
- **TRD-TKT-03 Steppers snap.** Price steps by tick size, quantity by lot size; typed values
  snap on blur with a note "rounded to tick 0.01".
- **TRD-TKT-04 Preview before submit.** Estimated cost, fees, margin required, buying power after,
  and for market orders a slippage note; bracket shows max loss and target profit.
- **TRD-TKT-05 Fat-finger guard.** Orders more than N% away from last price or above M× average
  size need a second confirm naming the deviation.
- **TRD-TKT-06 Idempotent submit.** Button disables on tap, shows spinner until ack; the
  client_order_id is reused on retry so a double tap never doubles the order.
- **TRD-TKT-07 Best-execution link.** Small "How we execute" link under submit to the policy.

## Depth ladder and chart

- **TRD-DEP-01 Centred spread.** Asks above, bids below, spread row centred and labelled; size
  bars are horizontal with numeric labels.
- **TRD-DEP-02 Own orders.** Working orders appear as a marker in the ladder row with qty;
  drag to amend (pro only), keyboard: arrow to row, Enter to prefill ticket.
- **TRD-DEP-03 One-click opt-in.** One-click trading is off by default, enabled per session
  with a warning; a persistent "ONE-CLICK ON" chip shows while enabled.
- **TRD-CHT-01 Chart defaults.** Candlestick, 1D for equities, 15m for FX/crypto; volume pane;
  crosshair with OHLC readout; data-table alternative for screen readers.
- **TRD-CHT-02 Order lines.** Working orders as dashed lines with label; fills as small markers.

## Risk and warnings

- **TRD-RSK-01 Risk warning interstitial.** Full-screen sheet before first leveraged/complex
  trade: headline loss statistic, 3–5 plain bullets, knowledge-check question, checkbox, Continue
  enabled after scroll to end; stored as versioned acknowledgement.
- **TRD-RSK-02 Persistent risk line.** Leveraged product screens show a one-line risk warning in
  the footer; never dismissible.
- **TRD-RSK-03 Margin gauge.** Margin level as a number (%) plus a segmented bar with labelled
  thresholds (maintenance, stop-out); never a colour-only dial.
- **TRD-RSK-04 Margin call banner.** Sticky top banner with deficit, deadline countdown and two
  actions: Deposit, Reduce positions.
- **TRD-RSK-05 Stale data.** Quote older than threshold greys the price, shows clock icon and
  "Delayed" label; ticket blocks market orders on stale quotes.
- **TRD-RSK-06 Paper watermark.** Paper mode shows diagonal "PAPER" watermark and hatched header on
  every trading screen; switching modes requires explicit confirmation.

## KYC and onboarding

- **TRD-KYC-01 Tier ladder.** Tiers shown as a vertical ladder with limits each unlocks (deposit
  cap, withdraw, leverage, crypto); current tier highlighted with label, not colour only.
- **TRD-KYC-02 National ID first.** Offer UAE Pass / Nafath / NADRA path first where available;
  document scan as fallback; explain why each item is needed in one sentence.
- **TRD-KYC-03 Save and resume.** Every step saves; returning users land on the next step.
- **TRD-KYC-04 Honest waiting.** In-review shows expected time and what happens next; no fake
  progress bars.

## Money movement

- **TRD-MNY-01 Withdrawable vs balance.** Show balance, reserved (open orders/margin) and
  withdrawable separately with a one-line explanation.
- **TRD-MNY-02 Cool-down clarity.** New beneficiary shows the exact local time it becomes usable.
- **TRD-MNY-03 Same-name rule.** Beneficiary form states "Accounts must be in your name" before
  the user types.
- **TRD-MNY-04 Crypto address safety.** Network selector first, address whitelist, first-8/last-8
  characters echoed for confirmation, travel-rule form when required.

## Statements and reports

- **TRD-STM-01 Statement list.** Grouped by kind (daily confirm, monthly, annual tax); each row
  has period, issued date, checksum tooltip, PDF and CSV.
- **TRD-STM-02 Corrections.** A superseded statement shows a banner linking the correction.
- **TRD-STM-03 Tax disclaimer.** Tax report states whether amounts were withheld at source or are
  report-only, per jurisdiction.

## Density and layout

- **TRD-DNS-01 Density modes.** Comfortable (mobile default) and compact (pro/web); row height
  32 px compact, 44 px comfortable.
- **TRD-DNS-02 Pro terminal.** Web layout of dockable panels: watchlist, chart, depth, ticket,
  positions, orders; layouts saved per user.
- **TRD-DNS-03 Numbers align.** Right-aligned decimals, fixed decimals per instrument, thousands
  separators per locale, currency code after amount.
- **TRD-DNS-04 RTL.** Chrome mirrors; price columns, charts, depth ladder and numeric inputs stay
  LTR; Urdu uses Noto Nastaliq only for prose, never in tables.

## Notifications

- **TRD-NTF-01 Fill notifications.** Push on fill with side, qty, price; tap opens the Order.
- **TRD-NTF-02 Alert once.** Price alert fires once per crossing and shows the crossing price.
- **TRD-NTF-03 Critical channel.** Margin calls and withdrawals use push + email + in-app; never
  marketing channels.

## Empty and error states

- **TRD-EMP-01 First run.** Empty watchlist offers curated lists for the region (KSE-100 names,
  TASI leaders, DFM/ADX blue chips, major FX pairs, top crypto).
- **TRD-ERR-01 Rejects explain.** Order rejects show reason in plain words and the fix
  ("Price outside daily limit 290.00–330.00").
- **TRD-ERR-02 Reconnect.** WebSocket drop shows banner, disables trading actions, auto-reconnects
  with backoff and resubscribes; never queues orders offline.

## Accessibility

- **TRD-A11Y-01 Live regions.** Price cells are not live regions (too chatty); fills, rejects and
  margin calls are announced via a polite/assertive live region respectively.
- **TRD-A11Y-02 Keyboard trading.** Pro terminal: B/S open ticket, Esc cancels, Enter submits only
  from the preview step; every shortcut is listed in a help overlay.
