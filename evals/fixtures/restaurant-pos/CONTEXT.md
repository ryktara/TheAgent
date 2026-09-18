# Restaurant POS — CONTEXT

A tablet point of sale for a dine-in restaurant in Sharjah [D:region] [D:service-model].

Ubiquitous language for this project. Every noun in the PRD, the domain model and the code uses
the term in this file; aliases are accepted in conversation and normalised in artifacts.

## Entities

| Entity | Context | States |
|--------|---------|--------|
| Order | ordering | draft, sent, in-progress, ready, served, billed, paid, closed, void, refunded |
| OrderLine | ordering | pending, held, fired, ready, served, voided, comped |
| Modifier | menu | active, hidden |
| ModifierGroup | menu | active, hidden |
| Table | ordering | free, seated, ordered, billed, dirty, blocked |
| Shift | ordering | open, closed, reconciled |
| Payment | payments | pending, authorised, captured, declined, refunded, voided |
| Tender | payments | active, disabled |
| Refund | payments | requested, approved, processed, failed |
| Receipt | payments | issued, reprinted, voided |
| MenuItem | menu | active, sold-out, hidden, seasonal |
| Variant | menu | active, hidden |
| Course | ordering | scheduled, fired, served |
| KitchenTicket | kitchen | new, in-progress, ready, bumped, recalled |
| Reservation | ordering | requested, confirmed, seated, no-show, cancelled |
| Customer | people | guest, registered, blocked |
| Discount | payments | active, expired |
| TaxRule | payments | active, retired |
| Branch | people | active, suspended |
| Staff | people | active, suspended |
| Role | people | active |
| InventoryItem | inventory | active, discontinued |
| Recipe | inventory | active, retired |
| StockMovement | inventory | recorded |
| SyncEvent | sync | pending, sent, acked, conflict |

## Glossary

| Term | Definition | Aliases |
|------|------------|---------|
| Order | One guest transaction from first line to close; owns lines payments and receipt | ticket;check;chit |
| OrderLine | One menu item with qty variant modifiers seat and course on an Order | line;item line |
| Cover | One guest seated at a table; used for per-head reporting | pax;head;guest count |
| Table | A physical seating unit on the floor plan with a state | seat;tbl |
| KOT | Kitchen Order Ticket: the fired lines sent to a kitchen station | kitchen ticket;KitchenTicket;chit |
| Fire | Send a course or line to the kitchen now | send;push |
| Hold | Keep a line on the order without firing it | park |
| Course | A timed group of lines such as starters mains desserts | seating course |
| Bump | Mark a kitchen ticket or line done on the KDS | clear;done |
| KDS | Kitchen display system: screen showing tickets per station | kitchen screen |
| PLU | Price look-up code typed to add an item quickly | item code;short code |
| Modifier | An option that changes an item such as size or extra cheese | option;add-on;extra |
| ModifierGroup | A set of modifiers with min and max selection rules | option group |
| Variant | A size or version of an item with its own price and SKU | size;portion |
| Split bill | Dividing one order into several bills by seat item equal or custom | split check;separate bills |
| Split tender | Paying one bill with more than one tender | mixed payment |
| Tender | A payment method such as cash card wallet room charge | payment type;MOP |
| Tab | An open order kept running across visits or the evening | open check;running bill |
| Bill | The printed request for payment before tender | check;pre-receipt |
| Receipt | The fiscal document issued after payment | invoice;tax invoice |
| Simplified tax invoice | KSA B2C receipt format required by ZATCA with TLV QR | فاتورة مبسطة |
| TLV QR | Tag-length-value base64 QR carrying seller VAT number time total and VAT | ZATCA QR |
| Tax-inclusive | Displayed price already contains tax; tax is extracted not added | inclusive pricing |
| Tax-exclusive | Tax added on top of the displayed price at the bill | exclusive pricing |
| Service charge | Percentage added to the bill by house policy shown separately | SC;service |
| Discount | A reduction applied to a line or the order with a reason | promo;offer |
| Comp | Give a line free with reason and approval; cost still deducted | complimentary;on the house |
| Void | Cancel a line or order with reason; fired voids need approval | cancel |
| Refund | Return money for a paid order fully or partly | return;reversal |
| Shift | A cashier session on one device with float and cash count | session;till session |
| Float | Opening cash in the drawer at shift start | opening balance;cash float |
| Cash count | Denomination count at shift close | cash up;cashing up |
| X-report | Shift summary printed without closing | mid-shift report |
| Z-report | Shift close summary that resets the shift totals | end of shift;Z |
| End of day | Business day close across devices with posting to accounting | EOD;day close |
| Customer display | Second screen facing the guest showing lines and total | CFD;customer-facing display |
| Channel | Where the order came from: dine-in counter qr delivery platform | source;order type |
| Parcel | Takeaway order (South Asian usage) | takeaway;take-out;to go |
| Quick service | Order and pay at the counter then collect | QSR;fast casual;counter service |
| Cloud kitchen | Delivery-only kitchen with no dining room possibly several brands | dark kitchen;ghost kitchen;virtual brand |
| Room charge | Hotel guest posts the bill to their room folio | post to room;charge to room |
| Aggregator | Delivery platform sending orders such as Talabat Deliveroo Careem Noon Food | delivery platform;marketplace |
| Reservation | A booked table for a time and party size | booking |
| Waitlist | Walk-in queue for tables with notify on ready | queue |
| Menu | All categories items variants and modifiers offered | catalogue |
| Availability schedule | Times when an item or category can be ordered | day-part;happy hour |
| Recipe | Bill of materials that maps an item to inventory quantities | BOM;recipe card |
| Yield | Portions one recipe batch produces | portion count |
| Stock deduction | Automatic inventory movement when an item is served | depletion |
| Purchase order | Request to a supplier for stock | PO |
| Goods receipt | Recording delivered stock against a PO | GRN;receiving |
| Offline queue | Local store of writes waiting to sync | sync queue;outbox |
| SyncEvent | One queued write with device id and sequence | event;outbox entry |
| Conflict | Two devices changed the same field while offline | merge conflict |
| Receipt block | Range of receipt numbers reserved to a device for offline use | number range |
| Branch | One physical location with its own receipts tax and float | outlet;location;store |
| Central menu | Menu published from head office to all branches | master menu |
| Per-branch price | Override of a central price at one branch | local price |
| Staff | Person with a PIN and role on the POS | employee;user |
| Role | Named permission set such as cashier waiter manager owner | permission set |
| Audit event | Immutable record of who did what to which object when | audit log entry |
| Loyalty points | Points earned per spend redeemable as discount | rewards |
| Order age | Minutes since a ticket was fired; drives KDS colours | ticket timer |
| Quick cash | Buttons for exact and round cash amounts at tender | fast cash |
| Hosted fields | Provider-hosted card inputs that keep card data off the POS | hosted payment page;iframe fields |
| SoftPOS | Accepting contactless cards on a phone without a terminal | tap to phone |
| Terminal | Card reader device that captures card payments | PDQ;card machine;EDC |

## Feature vocabulary

| Id | Meaning |
|----|---------|
| `order-entry` | order entry (PRD §4) |
| `table-map` | table map (PRD §4) |
| `modifiers` | modifiers (PRD §4) |
| `course-firing` | course firing (PRD §4) |
| `send-to-kitchen` | send to kitchen (PRD §4) |
| `hold-void-comp` | hold void comp (PRD §4) |
| `split-bill` | split bill (PRD §4) |
| `merge-transfer` | merge transfer (PRD §4) |
| `discounts` | discounts (PRD §4) |
| `tips-service-charge` | tips service charge (PRD §4) |
| `tender-cash-card-wallet` | tender cash card wallet (PRD §4) |
| `split-tender` | split tender (PRD §4) |
| `receipt-bilingual-qr` | receipt bilingual qr (PRD §4) |
| `refunds` | refunds (PRD §4) |
| `shift-cash-count` | shift cash count (PRD §4) |
| `end-of-day` | end of day (PRD §4) |
| `menu-management` | menu management (PRD §4) |
| `floor-management` | floor management (PRD §4) |
| `inventory-basic` | inventory basic (PRD §4) |
| `reports-core` | reports core (PRD §4) |
| `staff-roles` | staff roles (PRD §4) |
| `offline-queue` | offline queue (PRD §4) |
| `audit-log` | audit log (PRD §4) |

## Job vocabulary

| Id | Meaning |
|----|---------|
| `take-order-table` | take order table (PRD §3) |
| `take-order-counter` | take order counter (PRD §3) |
| `take-order-qr` | take order qr (PRD §3) |
| `modify-order` | modify order (PRD §3) |
| `send-to-kitchen` | send to kitchen (PRD §3) |
| `kds-bump` | kds bump (PRD §3) |
| `hold-void-comp` | hold void comp (PRD §3) |
| `split-bill` | split bill (PRD §3) |
| `merge-transfer-tables` | merge transfer tables (PRD §3) |
| `apply-discount` | apply discount (PRD §3) |
| `tips-service-charge` | tips service charge (PRD §3) |
| `take-payment` | take payment (PRD §3) |
| `print-receipt` | print receipt (PRD §3) |
| `refund` | refund (PRD §3) |
| `open-close-shift` | open close shift (PRD §3) |
| `end-of-day` | end of day (PRD §3) |
| `manage-menu` | manage menu (PRD §3) |
| `manage-floor` | manage floor (PRD §3) |
| `reservations-waitlist` | reservations waitlist (PRD §3) |
| `inventory-basic` | inventory basic (PRD §3) |
| `purchasing` | purchasing (PRD §3) |
| `delivery-orders` | delivery orders (PRD §3) |
| `reports` | reports (PRD §3) |
| `staff-roles` | staff roles (PRD §3) |
| `multi-branch` | multi branch (PRD §3) |
| `loyalty` | loyalty (PRD §3) |
| `offline-sync` | offline sync (PRD §3) |

## Decisions vocabulary

| Decision | Canonical word | Source |
|----------|----------------|--------|
| service-model | service model = dine-in | timeout-default |
| region | region country = AE | brief |
| payments | payments provider = network-intl | brief |
| branches | org branches = single | timeout-default |
| kds | kitchen output = both | timeout-default |
| delivery | integrations delivery = false | timeout-default |
| offline | nfr offline = true | timeout-default |
| reservations | features reservations = false | timeout-default |
| qr-self-order | features qr self order = false | pack-default |
| delivery-platforms | integrations delivery platforms = talabat | pack-default |
| central-menu-sync | org menu sync = central | pack-default |
| payment-provider-name | payments provider name = Network International | agent-fact |

## Project-specific terms

<!-- model: add up to 10 terms the pack glossary lacks, same table shape -->

| Term | Definition | Aliases |
|------|------------|---------|
