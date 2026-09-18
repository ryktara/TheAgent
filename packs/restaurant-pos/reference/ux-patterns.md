# Restaurant POS — UX patterns

Operational UI: fast, forgiving, glanceable from a metre away. Every pattern names its id so
screen specs can cite it. Baseline: touch 48 dp, text 16 px minimum, contrast 4.5:1 (7:1 on KDS
dark theme), tabular numerals everywhere an amount appears.

## Entry

- **POS-NUM-01 Numpad first.** Amount, qty and PIN entry use a fixed 3×4 numpad with 00 and
  backspace; keys 64 dp; typed value shown large above; never a native keyboard for numbers.
- **POS-NUM-02 Quantity chips.** 1–9 as chips beside the item; tapping an item again increments;
  long-press opens the numpad for 10+.
- **POS-NUM-03 Quick cash.** Exact, next round note (50, 100, 200 or local equivalents); change
  shown in 40 px as soon as tendered ≥ due.
- **POS-SRCH-01 PLU and search.** A single field accepts PLU digits or name; results update per
  keystroke; barcode scanner input lands here.
- **POS-MOD-01 Modifier sheet.** Bottom sheet, groups as sections, required groups first with a
  red "choose 1" until satisfied; Done shows the running line total; sheet opens automatically
  for items with required groups.
- **POS-MOD-02 Notes and allergens.** Free text plus allergen chips (nuts, dairy, gluten,
  shellfish, egg, soy); allergen lines render a warning icon on the KDS.

## Ticket and kitchen

- **POS-TKT-01 Ticket grouping.** Lines grouped by course, then seat; unsent lines highlighted;
  swipe left on a line for void/comp/note; long-press to move seat.
- **POS-KDS-01 Order age colour.** Green under 5 min, amber under 10, red at 10 or more; colour
  applies to the card header and the timer; also encoded with an icon for colour-blind users.
- **POS-KDS-02 Bump bar.** Keys 1–9 bump ticket in that slot, R recalls last bump, S cycles
  station, arrows scroll; on-screen legend visible; touch bump is the whole card header.
- **POS-KDS-03 Held and rush.** Held lines hatched grey; rush tickets pinned first with a flame
  icon and a distinct sound.
- **POS-KDS-04 Dark theme.** KDS uses dark background, 7:1 contrast, 20 px text minimum; no
  pure white.

## Money

- **POS-SPL-01 Split bill.** Mode tabs (seat, item, equal, custom); bill columns with totals;
  remaining bar at the bottom turns green at zero; each column has its own Pay.
- **POS-TND-01 Tender screen.** Amount due at 48 px top-left (top-right in RTL); tender rows list
  paid amounts; numpad right; Complete enabled only at remaining ≤ 0; overpayment shows change.
- **POS-TND-02 Card wait state.** Spinner with "Waiting for terminal", cancel after 5 s, timeout
  at 60 s with retry or other tender.
- **POS-TND-03 Service charge and tip.** Service charge appears as its own line with a remove
  control that asks for a PIN; tip chips 0/5/10/15% and custom.
- **POS-RCT-01 Receipt preview.** Facsimile at 80 mm width; language toggle; print, e-receipt
  (WhatsApp, SMS, email), no receipt; reprint stamps REPRINT.
- **POS-RFD-01 Refund.** Find by receipt number or scan; lines with checkboxes; reason chips;
  PIN modal; refund to original tender preselected.

## Guarded actions

- **POS-PIN-01 Manager PIN pattern.** Modal shows the action summary and reason chips first,
  PIN second; approver name appears after success; three failures lock for 60 s; offline PINs
  verify against the local hash and mark the event pending-audit.
- **POS-PIN-02 Policy thresholds.** Void under threshold and discount under 10% need a reason
  only; above needs PIN; thresholds live in Branch settings.

## Connectivity

- **POS-OFF-01 Offline banner.** Persistent top banner "Offline, orders saved on this device"
  with queue count; turns into "Syncing 12" then disappears; never blocks ordering.
- **POS-OFF-02 Sync status.** Header icon with three states (synced, queued n, conflict); tap
  opens sync-status.
- **POS-OFF-03 Degraded payments.** Card row shows "Terminal offline" and offers cash or manual
  approval code entry with a warning.

## Floor

- **POS-FLR-01 Table chip.** Number large, covers and minutes small, total on billed; colour by
  state with a state icon; long-press for merge, transfer, dirty.
- **POS-FLR-02 Merge and transfer.** Pick source, pick target, confirm sheet lists lines moved;
  undo available for 10 s.

## Language and RTL

- **POS-RTL-01 Mirroring rules.** Layout, navigation, tabs, lists and swipe directions mirror;
  numpads, prices, phone numbers, QR codes, floor canvas coordinates do not.
- **POS-RTL-02 Bilingual receipts.** Arabic block first for SA, English first for AE unless the
  customer toggles; both blocks carry the same totals.
- **POS-RTL-03 Fonts.** Arabic and Urdu use a system font with Naskh/Nastaliq fallback at 18 px
  minimum; numerals Western by default with Arabic-Indic option per branch.

## Error copy examples

| Situation | Copy |
|-----------|------|
| Sold-out item tapped | "Chicken Mandi is 86'd. Manager can reset it in Menu." |
| Void over limit | "Void of 145.00 needs a manager PIN." |
| Split remaining | "12.50 still unassigned. Move items or add a bill." |
| Terminal timeout | "No reply from the card terminal. Retry, or take another tender." |
| Shift close blocked | "3 open orders: T4, T9, Counter 21. Pay, void or transfer them first." |
| Fiscal report failing (SA) | "2 receipts not yet reported to ZATCA. Retrying automatically." |
| Offline PIN | "Approved offline by Sara. Will be audited on sync." |
| Duplicate PLU | "PLU 104 is already used by Karak Tea." |

## Anti-patterns to replace

| Replace | With |
|---------|------|
| Native number keyboard for amounts | POS-NUM-01 numpad |
| Modal confirmation for every void | Reason chip inline; PIN only over threshold |
| Spinner over the whole screen while offline | POS-OFF-01 banner, local write |
| Colour-only KDS age | Colour plus icon plus timer text |
| Tiny 32 dp buttons on tender | 64 dp numpad, 56 dp tender rows |

## Layout budgets

| Screen | Max taps to complete | Notes |
|--------|----------------------|-------|
| order-entry, add plain item | 1 | tap item |
| order-entry, item with required modifier | 3 | item, modifier, done |
| tender, exact cash | 2 | Exact, Complete |
| tender, card | 2 | Card, Complete after approval |
| split equal 2 ways | 3 | Split, Equal, 2 |
| void unfired line | 2 | swipe, reason |
| shift close, no variance | 4 | Close, count, confirm, print |

## Motion and feedback

- **POS-FBK-01** New KDS ticket: slide in from the right plus a short chime; respects reduced motion
  by cutting the slide and keeping the chime.
- **POS-FBK-02** Successful payment: full-width green bar for 1.5 s with change amount; drawer
  opens in the same frame for cash.
- **POS-FBK-03** Sync complete: header icon pulses once; no toast.
- **POS-FBK-04** Errors never block the ticket: inline under the offending control, red 16 px text
  with an icon.

## Hardware affordances

- **POS-HW-01** Barcode scanner input is treated as keyboard wedge into the PLU field regardless
  of focus.
- **POS-HW-02** Customer display mirrors the ticket lines and total; shows the tip prompt during
  tender when enabled.
- **POS-HW-03** Printer status chip in the header: ready, paper low, offline; printing queues
  when offline.
