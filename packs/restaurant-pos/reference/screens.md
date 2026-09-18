# Restaurant POS — screens

Every screen has states: empty, loading, error, offline, locked (PIN required). Role access is
the minimum role; owner inherits everything. Touch targets 48 dp, body text 16 px minimum,
tabular numerals for every amount. RTL: whole layout mirrors when the UI language is ar or ur,
except numerals, prices and the numpad grid which stay left-to-right.

## table-map

| Aspect | Detail |
|--------|--------|
| Purpose | Seat guests, see table state at a glance, open or resume an order |
| Primary actions | Tap free table → new order; tap seated table → resume; long-press → merge, transfer, mark dirty |
| Layout zones | Zone tabs (Indoor, Terrace, Shisha); floor canvas; legend; header with shift, sync, search |
| Table colour | free grey, seated blue, ordered amber, billed green, dirty striped, blocked hatched |
| States | empty: "No floor plan yet, open Floor editor"; offline: banner, all actions allowed; locked: PIN for transfer |
| Role | waiter |
| Components | FloorCanvas, TableChip (number, covers, age, total), ZoneTabs, LegendBar |
| A11y | Tables are buttons with label "Table 12, seated, 4 covers, 18 minutes"; zone tabs arrow-key navigable |
| RTL | Canvas coordinates unchanged; header and tabs mirror |

## order-entry

| Aspect | Detail |
|--------|--------|
| Purpose | Build the order fast: categories, items, variants, modifiers, seats, courses |
| Primary actions | Add item, set qty (chips 1–9, numpad), open modifier sheet, assign seat, fire course, hold, send, bill |
| Layout zones | Left 60%: category rail + item grid; right 40%: ticket (lines grouped by course/seat), totals, action bar |
| Ticket line | qty, name, modifiers indented, seat tag, course tag, line total, swipe for void/comp/notes |
| States | empty ticket: "Tap an item to start"; sold-out items greyed with "86"; offline: send queues locally; locked: void over limit |
| Role | waiter (counter mode: cashier) |
| Components | CategoryRail, ItemGrid (PLU search), TicketPanel, QtyChips, Numpad, ActionBar |
| A11y | Item cards announce name, price, allergens; qty chips are a radiogroup |
| RTL | Item grid and ticket swap sides; ticket amounts right-aligned in both directions |

## modifier-sheet

| Aspect | Detail |
|--------|--------|
| Purpose | Required and optional modifiers, notes, allergens, course, seat for one line |
| Primary actions | Select modifiers (min/max enforced), type note, tag allergen, set course, set seat, Done |
| Layout zones | Bottom sheet 70% height: groups as sections, sticky Done with running line total |
| States | error: "Choose at least one size"; locked: none |
| Role | waiter |
| Components | ModifierGroup (chips or steppers), NoteField, AllergenChips, CourseSelect, SeatSelect |
| A11y | Each group is a fieldset with legend and min/max in description |
| RTL | Sheet mirrors; chips wrap from the right |

## qr-self-order

| Aspect | Detail |
|--------|--------|
| Purpose | Guest orders from a phone after scanning the table QR |
| Primary actions | Browse menu, add items, pay now or pay at table, call waiter |
| Layout zones | Sticky header (table, language toggle), category chips, item list, cart drawer |
| States | table closed: "Ask staff to open a table"; kitchen closed: "Ordering paused"; payment failed |
| Role | customer (no login) |
| Components | LanguageToggle en/ar, ItemList, CartDrawer, HostedPaymentRedirect |
| A11y | WCAG AA, works without JS-heavy interactions, 200% zoom safe |
| RTL | Full mirror; Arabic names from MenuItem.name_ar |

## kds

| Aspect | Detail |
|--------|--------|
| Purpose | Kitchen sees fired tickets per station and bumps them |
| Primary actions | Bump line, bump ticket, recall, mark item 86, filter by station |
| Layout zones | Ticket rail (newest right, oldest left, 4–6 visible), station tabs, footer with counts |
| Ticket colour | age under 5 min green, under 10 amber, 10+ red; held lines hatched; rush icon |
| States | empty: "No open tickets"; offline: tickets from local queue, banner; error: printer fallback |
| Role | kitchen |
| Components | TicketCard, BumpBar (keyboard: 1–9 bump ticket n, R recall, S station), AgeTimer |
| A11y | Dark theme 7:1 contrast; ticket cards announce age; bump bar keys documented on screen |
| RTL | Ticket rail order stays chronological left→right; text mirrors |

## manager-pin

| Aspect | Detail |
|--------|--------|
| Purpose | Approve a guarded action: void over limit, comp, discount over policy, refund, price override |
| Primary actions | Enter 4–6 digit PIN or tap NFC card; reason picker; confirm |
| Layout zones | Modal: action summary, reason chips, numpad, approver name after PIN |
| States | error: wrong PIN (3 tries then 60 s lock); offline: allowed, logged as pending-audit |
| Role | manager |
| Components | ReasonChips, Numpad, ApproverBadge |
| A11y | PIN field masked, announces digits entered count only |
| RTL | Numpad stays LTR |

## split-bill

| Aspect | Detail |
|--------|--------|
| Purpose | Split one order into bills by seat, by item, equally, or by custom amount |
| Primary actions | Choose mode, drag items to bill columns, set n ways, edit amount, pay each bill |
| Layout zones | Mode tabs; columns per bill with totals; remaining balance bar; Pay button per column |
| States | error: "Remaining 12.50 not assigned"; offline: allowed; locked: none |
| Role | cashier |
| Components | ModeTabs, BillColumn, ItemDraggable, RemainingBar |
| A11y | Drag has keyboard alternative: select item then "Move to bill 2" |
| RTL | Columns mirror; amounts right-aligned |

## tender

| Aspect | Detail |
|--------|--------|
| Purpose | Take payment with one or more tenders, apply discount, tip, service charge, loyalty |
| Primary actions | Cash (numpad, quick amounts), card (terminal push), wallet QR, room charge, khaata, split tender, discount, tip |
| Layout zones | Left: amount due, tender list with paid amounts; right: numpad and quick chips; footer: Complete |
| States | card pending (spinner, cancel); declined (retry, other tender); offline card: "Terminal offline, take cash or queue"; locked: discount over policy |
| Role | cashier |
| Components | AmountDue, TenderRow, Numpad, QuickCash (exact, 50, 100, 200), TipSelector, DiscountPicker |
| A11y | Amount due is a live region; tender rows are buttons with paid state |
| RTL | Numpad LTR; tender list mirrors |

## receipt-preview

| Aspect | Detail |
|--------|--------|
| Purpose | Preview, print, email, WhatsApp the receipt in the chosen language |
| Primary actions | Language toggle, print, reprint (marked), send e-receipt, no receipt |
| Layout zones | Receipt facsimile (80 mm), actions row |
| Receipt content | Branch name, TRN/VAT no, receipt number, date, lines, discounts, service charge, tax breakdown, total, tenders, fiscal QR |
| States | printer offline: queue print, offer e-receipt; error: fiscal QR unavailable (SA: retry within 24 h) |
| Role | cashier |
| Components | ReceiptRenderer (ESC/POS and HTML), LanguageToggle, SendSheet |
| A11y | Facsimile has a text alternative listing lines |
| RTL | Arabic receipt right-aligned, numerals Western by default with Arabic-Indic option |

## refund

| Aspect | Detail |
|--------|--------|
| Purpose | Refund a paid order fully or partly to the original tender |
| Primary actions | Find order (receipt number, scan QR), select lines or amount, reason, PIN, process |
| Layout zones | Search bar, order summary, line selector, refund summary, PIN modal |
| States | error: exceeds captured; provider failed (retry, cash fallback with approval); offline: cash only |
| Role | manager |
| Components | OrderSearch, LineSelector, RefundSummary |
| A11y | Line checkboxes with amounts announced |
| RTL | Mirrors |

## shift-open

| Aspect | Detail |
|--------|--------|
| Purpose | Start a shift on a device with an opening float |
| Primary actions | Enter float (numpad), confirm; resumes an unclosed shift if present |
| States | error: unclosed shift on another device (offer takeover with PIN) |
| Role | cashier |
| Components | Numpad, ShiftSummary |
| A11y | Float field labelled with currency |
| RTL | Numpad LTR |

## shift-close

| Aspect | Detail |
|--------|--------|
| Purpose | Count cash, reconcile tenders, close the shift, print X/Z |
| Primary actions | Count by denomination, compare with expected, note variance, close, print Z |
| Layout zones | Denomination grid, expected vs counted, variance, open orders warning |
| States | blocked: open orders listed with jump links; offline: close allowed, Z queued |
| Role | cashier (variance over policy needs manager PIN) |
| Components | DenominationGrid, ReconcileTable, VarianceBadge |
| A11y | Denomination inputs labelled with value |
| RTL | Grid mirrors |

## end-of-day

| Aspect | Detail |
|--------|--------|
| Purpose | Close the business day across devices, post to accounting, archive |
| Primary actions | Review shift Zs, resolve open orders, post to accounting, lock day |
| States | blocked: unsynced devices; error: accounting sync failed (retry, skip) |
| Role | manager |
| Components | ShiftList, DayTotals, SyncChecklist |
| A11y | Checklist items are checkboxes with status text |
| RTL | Mirrors |

## menu-management

| Aspect | Detail |
|--------|--------|
| Purpose | Categories, items, variants, modifier groups, availability, channel pricing |
| Primary actions | Add/edit item (bilingual names), set PLU, price by channel, tax rule, station, 86 toggle, schedule |
| Layout zones | Category tree left, item table centre, item editor right |
| States | empty: import from CSV; error: duplicate PLU; locked: price change needs manager |
| Role | manager |
| Components | CategoryTree, ItemTable, ItemEditor, ChannelPriceGrid, ModifierGroupEditor |
| A11y | Tree is a treeview with arrow navigation |
| RTL | Editor fields mirror; name_ar field is RTL regardless of UI language |

## floor-editor

| Aspect | Detail |
|--------|--------|
| Purpose | Draw zones and tables |
| Primary actions | Add zone, drag table, set number and seats, shape, save |
| States | error: duplicate table number |
| Role | manager |
| Components | FloorCanvas (edit mode), TableInspector |
| A11y | Keyboard nudge for table position |
| RTL | Canvas unchanged |

## reservations

| Aspect | Detail |
|--------|--------|
| Purpose | Bookings and walk-in waitlist |
| Primary actions | Add booking, assign table, seat, no-show, notify by WhatsApp |
| Layout zones | Timeline by table, waitlist column, booking form |
| States | empty; offline: read-only |
| Role | waiter |
| Components | Timeline, WaitlistColumn, BookingForm |
| A11y | Timeline slots are buttons with time and table |
| RTL | Timeline mirrors |

## inventory

| Aspect | Detail |
|--------|--------|
| Purpose | Stock on hand, movements, wastage, low-stock alerts |
| Primary actions | Adjust, record wastage with reason, receive stock, set par level |
| States | empty: "Add inventory items or import"; low-stock badges |
| Role | manager |
| Components | StockTable, MovementLog, WastageForm |
| A11y | Table sortable with announced sort state |
| RTL | Mirrors |

## recipe-editor

| Aspect | Detail |
|--------|--------|
| Purpose | Bill of materials per menu item so sales deduct stock |
| Primary actions | Add component, qty, unit, yield; cost preview |
| States | error: unit mismatch |
| Role | manager |
| Components | ComponentList, CostPreview |
| A11y | Qty inputs labelled with unit |
| RTL | Mirrors |

## purchasing

| Aspect | Detail |
|--------|--------|
| Purpose | Purchase orders to suppliers and goods receipt |
| Primary actions | Create PO from low stock, send, receive, post to inventory |
| States | empty; offline: draft only |
| Role | manager |
| Components | POList, POEditor, ReceiveForm |
| A11y | Standard forms |
| RTL | Mirrors |

## delivery-inbox

| Aspect | Detail |
|--------|--------|
| Purpose | Aggregator orders land here, get accepted, and fire to KDS |
| Primary actions | Accept (prep time), reject with reason, mark ready, hand over to rider |
| Layout zones | Platform tabs, order cards with timer, detail pane |
| States | platform disconnected banner with tablet-fallback note; auto-accept on |
| Role | kitchen |
| Components | PlatformTabs, DeliveryOrderCard, RiderHandover |
| A11y | New order sound plus visual flash; cards announce platform and ETA |
| RTL | Mirrors |

## reports

| Aspect | Detail |
|--------|--------|
| Purpose | Sales by hour, item, category, server, channel; tax; discounts; voids; payment mix |
| Primary actions | Pick report, date range, branch, export CSV/PDF, schedule email |
| States | empty range; loading skeleton; error retry |
| Role | owner (manager for daily) |
| Components | ReportPicker, FilterBar, DataTable, Chart (one per report) |
| A11y | Charts carry a data table alternative |
| RTL | Mirrors |

## staff-roles

| Aspect | Detail |
|--------|--------|
| Purpose | Staff, PINs, roles, permissions, branch assignment |
| Primary actions | Add staff, set PIN, assign role, suspend |
| States | error: duplicate PIN within branch |
| Role | owner |
| Components | StaffTable, RoleMatrix |
| A11y | Matrix cells are checkboxes with row and column headers |
| RTL | Mirrors |

## branch-switcher

| Aspect | Detail |
|--------|--------|
| Purpose | Owner moves between branches; device is pinned to one |
| Primary actions | Select branch; view consolidated |
| States | single branch: hidden |
| Role | owner |
| Components | BranchMenu |
| A11y | Menu button with current branch label |
| RTL | Mirrors |

## customer-lookup

| Aspect | Detail |
|--------|--------|
| Purpose | Find or create a customer for loyalty, khaata, allergens |
| Primary actions | Search by phone, create, attach to order, redeem points |
| States | not found: create inline |
| Role | cashier |
| Components | PhoneSearch, CustomerCard |
| A11y | Search results as a listbox |
| RTL | Mirrors |

## sync-status

| Aspect | Detail |
|--------|--------|
| Purpose | Show queue depth, last sync, conflicts, and let staff retry |
| Primary actions | Retry now, view conflicts, export queue |
| States | online idle; offline with queue count; conflicts needing manager |
| Role | cashier |
| Components | QueueBadge, ConflictList |
| A11y | Status as live region |
| RTL | Mirrors |
