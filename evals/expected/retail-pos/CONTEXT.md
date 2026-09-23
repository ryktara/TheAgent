# Retail POS — CONTEXT

A point-of-sale and stock system for a single clothing shop in Riyadh [D:region] [D:branches], used by cashiers at the till and by the manager and stock-keeper in the back office.

Ubiquitous language for this project. Every noun in the PRD, the domain model and the code uses
the term in this file; aliases are accepted in conversation and normalised in artifacts.

## Entities

| Entity | Context | States |
|--------|---------|--------|
| Product | catalog | draft, active, discontinued |
| Variant | catalog | active, out-of-stock, discontinued |
| Barcode | catalog | active, retired |
| Sale | sales | open, parked, tendering, paid, partially-returned, returned, void |
| SaleLine | sales | active, voided, returned |
| Tender | sales | pending, authorised, captured, declined, refunded, voided |
| Return | sales | requested, approved, refunded, exchanged, rejected |
| Promotion | sales | draft, scheduled, active, expired |
| LoyaltyAccount | customers | active, frozen, closed |
| Customer | customers | guest, registered, blocked |
| GiftCard | customers | issued, active, redeemed, expired, void |
| Layaway | customers | open, paid, collected, cancelled, expired |
| PurchaseOrder | inventory | draft, sent, partially-received, received, closed, cancelled |
| GoodsReceipt | inventory | draft, posted |
| StockCount | inventory | planned, counting, review, posted |
| StockMovement | inventory | recorded |
| Transfer | inventory | draft, dispatched, in-transit, received, discrepancy |
| Supplier | inventory | active, blocked |
| CashDrawerSession | sales | open, closed, reconciled |
| Receipt | sales | issued, reprinted, voided, reported, report-failed |
| SyncEvent | sync | pending, sent, acked, conflict |
| TaxRule | sales | active, retired |
| Staff | people | active, suspended |
| Store | people | active, suspended |

## Glossary

| Term | Definition | Aliases |
|------|------------|---------|
| Sale | One customer transaction from first scan to paid; owns lines tenders and receipt | transaction;basket;ticket |
| SaleLine | One product variant with qty or weight and price on a Sale | line;basket line |
| Product | A sellable item grouping its variants | item;article |
| Variant | A specific size/colour/pack of a Product with its own SKU and stock | SKU variant;option |
| SKU | Stock keeping unit; the internal code for one Variant | item code;article number |
| PLU | Price look-up code typed for items without a barcode such as produce | PLU code |
| Barcode | A scannable code linked to a Variant | bar code |
| Restricted circulation number | GS1 prefix 02 or 20-29 code for in-store use such as weighed items | RCN;in-store code |
| Variable measure item | An item sold by weight or length whose price varies per unit | weighed item;random weight |
| Prefix-2 barcode | EAN-13 starting with 2 carrying an item code and embedded weight or price | scale barcode;weight barcode |
| Scale label | Label printed by a label-printing scale with price and prefix-2 barcode | scale ticket |
| Tender | A payment method used on a Sale | payment;tender type |
| Split tender | Paying one Sale with more than one tender | split payment |
| Cash drop | Removing excess cash from the drawer to the safe during a shift | safe drop;skim |
| Pickup | Manager collection of cash from a till | cash pickup |
| Paid-out | Cash paid from the drawer for an expense with reason | petty cash out |
| Blind count | Counting the drawer without seeing the expected amount | blind close |
| X report | Mid-day sales summary that does not reset totals | X read |
| Z report | End-of-day report that closes and locks the day | Z read;day end |
| Cash drawer session | Period a drawer is assigned to a cashier from float to count | till session;shift |
| Receipt | Printed or sent proof of sale with fiscal fields | bill;slip |
| Gift receipt | Receipt without prices for gifting and returns |  |
| Return | Customer bringing back items for refund | refund |
| Exchange | Return where the value is used for other items | swap |
| Store credit | Balance given instead of cash refund usable on future purchases | credit note;voucher |
| Gift card | Prepaid stored-value card or code | gift voucher |
| Layaway | Reserving goods against a deposit and paying in instalments before collecting | lay-by;layby |
| Price override | Changing a line price at the till with approval | price change;manual price |
| Promotion | A rule-based discount such as BOGO or tiered | promo;offer;deal |
| Mix and match | Promotion across a group of different items e.g. any 3 for 10 | M&M;any-of |
| Tiered promotion | Discount that grows with spend or qty thresholds | spend and save |
| Loyalty points | Points earned per spend and redeemed as tender | rewards;points |
| Loyalty tier | Customer level with better earn rate | membership level |
| Customer display | Screen facing the customer showing lines and total | pole display;second screen |
| Shrinkage | Stock lost to theft damage error or expiry | shrink;stock loss |
| Stock take | Full physical count of stock | inventory count;physical inventory |
| Cycle count | Counting a subset of stock on a rotating schedule | rolling count |
| Stock adjustment | Manual change of stock with a reason | write-off;adjustment |
| Stock movement | Ledger record of any stock change | inventory transaction |
| On hand | Current stock quantity in a store | SOH;stock on hand |
| Dead stock | Items with no sales for a long period | slow movers;non-moving |
| Stock valuation | Value of stock at cost | inventory value |
| Purchase order | Order sent to a supplier | PO |
| Goods receipt note | Record of goods received against a PO | GRN;receiving |
| Return to vendor | Sending goods back to the supplier | RTV;purchase return |
| Supplier | Vendor who supplies goods | vendor |
| Transfer | Moving stock between stores | stock transfer;inter-branch transfer |
| Shelf edge label | Price label on the shelf edge | SEL;shelf talker |
| MRP | Maximum retail price printed on pack (Pakistan India) | maximum retail price |
| Minimart | Small self-service grocery | convenience store |
| Khaata | Customer credit ledger kept by the shop (Pakistan) | khata;udhaar;credit book |
| Udhaar | Buying on credit to pay later | udhar;credit |
| TRN | UAE tax registration number printed on invoices | tax registration number |
| VAT-inclusive price | Price shown to the customer including VAT | gross price |
| Simplified tax invoice | ZATCA B2C invoice with QR | simplified invoice |
| TLV QR | Tag-length-value encoded QR required by ZATCA | ZATCA QR |
| FBR invoice number | Number returned by FBR for each POS sale in Pakistan | IRN;FBR number |
| E-receipt | Egypt ETA electronic B2C receipt | ETA receipt |
| Fawtara | Oman Tax Authority e-invoicing programme | Oman e-invoicing |
| Fiscal report | Submitting a sale to the tax authority | reporting;clearance |
| Unit price | Price per kg litre or 100 g shown on labels | price per unit |
| Label printer | Printer for barcodes and shelf labels | thermal label printer |
| Cost price | Price paid to the supplier | cost |
| Offline queue | Sales stored on device until sync | sync queue |
| Audit log | Append-only record of sensitive actions | audit trail |

## Feature vocabulary

| Id | Meaning |
|----|---------|
| `checkout` | checkout (PRD §4) |
| `barcode-scan` | barcode scan (PRD §4) |
| `plu-lookup` | plu lookup (PRD §4) |
| `weighed-items` | weighed items (PRD §4) |
| `variants` | variants (PRD §4) |
| `tender-cash-card-wallet` | tender cash card wallet (PRD §4) |
| `split-tender` | split tender (PRD §4) |
| `receipt-bilingual-qr` | receipt bilingual qr (PRD §4) |
| `returns-exchanges` | returns exchanges (PRD §4) |
| `price-override` | price override (PRD §4) |
| `promotions-engine` | promotions engine (PRD §4) |
| `catalog-management` | catalog management (PRD §4) |
| `goods-receipt` | goods receipt (PRD §4) |
| `stock-count` | stock count (PRD §4) |
| `stock-adjustments` | stock adjustments (PRD §4) |
| `label-printing` | label printing (PRD §4) |
| `cash-management` | cash management (PRD §4) |
| `z-report` | z report (PRD §4) |
| `e-invoice` | e invoice (PRD §4) |
| `reports-core` | reports core (PRD §4) |
| `shrinkage-report` | shrinkage report (PRD §4) |
| `staff-roles` | staff roles (PRD §4) |
| `offline-queue` | offline queue (PRD §4) |
| `audit-log` | audit log (PRD §4) |
| `loyalty` | loyalty (PRD §4) |
| `stock-transfers` | stock transfers (PRD §4) |

## Job vocabulary

| Id | Meaning |
|----|---------|
| `scan-and-sell` | scan and sell (PRD §3) |
| `sell-weighed-item` | sell weighed item (PRD §3) |
| `take-payment` | take payment (PRD §3) |
| `issue-receipt` | issue receipt (PRD §3) |
| `return-exchange` | return exchange (PRD §3) |
| `price-override` | price override (PRD §3) |
| `manage-promotions` | manage promotions (PRD §3) |
| `loyalty-points` | loyalty points (PRD §3) |
| `gift-card-store-credit` | gift card store credit (PRD §3) |
| `layaway` | layaway (PRD §3) |
| `manage-catalog` | manage catalog (PRD §3) |
| `purchase-orders` | purchase orders (PRD §3) |
| `receive-goods` | receive goods (PRD §3) |
| `stock-take` | stock take (PRD §3) |
| `stock-adjust` | stock adjust (PRD §3) |
| `stock-transfer` | stock transfer (PRD §3) |
| `manage-suppliers` | manage suppliers (PRD §3) |
| `e-invoicing` | e invoicing (PRD §3) |
| `customer-display` | customer display (PRD §3) |
| `cash-management` | cash management (PRD §3) |
| `reports-shrinkage` | reports shrinkage (PRD §3) |
| `print-labels` | print labels (PRD §3) |
| `staff-roles` | staff roles (PRD §3) |
| `multi-store` | multi store (PRD §3) |
| `offline-sync` | offline sync (PRD §3) |

## Decisions vocabulary

| Decision | Canonical word | Source |
|----------|----------------|--------|
| region | region country = SA | brief |
| branches | org branches = single | brief |
| variants | catalog variants = true | brief |
| einvoice | compliance einvoice = true | timeout-default |
| loyalty | features loyalty = true | brief |
| payments | payments provider = network-intl | timeout-default |
| weighed-items | catalog weighed items = false | timeout-default |
| offline | nfr offline = true | timeout-default |
| gift-cards | features gift cards = false | timeout-default |
| customer-credit | features customer credit = false | pack-default |
| stock-transfer | inventory transfers = true | pack-default |
| payment-provider-name | payments provider name = Network International | agent-fact |

## Project-specific terms

<!-- model: add up to 10 terms the pack glossary lacks, same table shape -->

| Term | Definition | Aliases |
|------|------------|---------|
