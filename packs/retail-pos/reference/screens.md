# Retail POS — screens

Every screen has states: empty, loading, error, offline, locked (PIN required). Role access is
the minimum role; owner inherits everything. Touch targets 48 dp, body text 16 px minimum,
tabular numerals for every amount. RTL: whole layout mirrors when the UI language is ar or ur,
except numerals, prices, barcodes and the numpad grid which stay left-to-right. Scanner input
is captured globally on checkout, returns, goods-receipt, stock-count and labels (see ux-patterns
RET-SCAN-01).

## checkout

| Aspect | Detail |
|--------|--------|
| Purpose | Scan-first selling: barcode, PLU, weighed items, variants, promotions, customer, park and tender |
| Primary actions | Scan, type PLU/name, change qty (numpad), void line, price override (PIN), attach customer, park, recall, Pay |
| Layout zones | Top: big search field with scan indicator; left 60%: basket lines (newest on top); right 40%: totals, promotions applied, numpad, action bar |
| Basket line | qty or weight, name + variant (size/colour), unit price, strike-through list price when overridden or promoted, line total, promo badge |
| States | empty: "Scan an item to start"; unknown barcode: red toast + "Add product" for managers; out-of-stock: amber warning (blocked if Store.allow_negative_stock false); offline: banner, selling continues |
| Data bindings | Sale (open), SaleLine[], Promotion (evaluated), Customer, LoyaltyAccount points, TaxRule for totals |
| Role | cashier |
| Components | ScanField, BasketList, TotalsPanel, Numpad, PromoBadge, ActionBar, ParkedSalesDrawer |
| A11y | Each added line is announced "Added Milk 1 L, 6.50"; errors announced assertively |
| RTL | Basket and totals swap sides; amounts right-aligned in both directions |

## product-search

| Aspect | Detail |
|--------|--------|
| Purpose | Find a product without a barcode: name, SKU, PLU, brand, category, in Arabic or English |
| Primary actions | Type, filter by category, pick variant from size/colour matrix, add to basket |
| Layout zones | Full-height overlay: search field, category chips, results grid with image, price, stock at this store |
| States | no results: "No match. Try SKU or scan"; many results: first 50 + "refine" |
| Data bindings | Product, Variant, Barcode, on-hand from StockMovement projection |
| Role | cashier |
| Components | SearchField (debounced 80 ms, local index), CategoryChips, ResultCard, VariantMatrix |
| A11y | Results are a listbox; arrow keys and Enter add |
| RTL | Grid flows from the right; SKU and prices stay LTR |

## weighed-item

| Aspect | Detail |
|--------|--------|
| Purpose | Sell items priced per kg: live scale read or scale-printed EAN-13 prefix 2 label |
| Primary actions | Pick PLU (fruit grid), read weight, tare, accept; or scan scale label (weight/price decoded) |
| Layout zones | Modal: PLU picture grid left, live weight readout (3 decimals kg) right, tare chips, price per kg, computed price |
| States | scale unstable: readout flashes, Accept disabled; scale offline: manual weight entry needs manager PIN; zero weight: blocked |
| Data bindings | Product (sold_by weight), Variant price per kg, SaleLine weight_g, Barcode embedded |
| Role | cashier |
| Components | PluGrid, ScaleReadout, TareChips, Numpad |
| A11y | Weight announced on stable; large 48 px readout |
| RTL | Grid mirrors; readout stays LTR |

## tender

| Aspect | Detail |
|--------|--------|
| Purpose | Take payment: cash, card terminal, wallet, SoftPOS, gift card, store credit, loyalty points, khaata; split tender |
| Primary actions | Pick tender, enter amount (numpad), quick cash notes, redeem points, scan gift card, complete |
| Layout zones | Amount due 48 px top; tender tiles; tendered list; remaining bar; change due 40 px |
| States | card pending: spinner with terminal status; declined: red with retry; remaining > 0: Complete disabled; offline: card only if terminal standalone, else cash/gift card |
| Data bindings | Sale total, Tender[], GiftCard balance, LoyaltyAccount points, Customer khaata_balance and credit_limit |
| Role | cashier |
| Components | TenderTile, Numpad, QuickCash, RemainingBar, TerminalStatus |
| A11y | Change due announced; tender tiles labelled with kind and limit |
| RTL | Amount due top-right; numpad unchanged |

## receipt-preview

| Aspect | Detail |
|--------|--------|
| Purpose | Show and print/send the receipt with fiscal fields (TRN, QR, FBR number) |
| Primary actions | Print, email, WhatsApp, gift receipt (no prices), reprint (marked) |
| Layout zones | 80 mm receipt mock left; delivery options right |
| States | fiscal pending: "FBR number pending, will print on resend"; reported; report-failed with retry |
| Data bindings | Receipt, Sale, SaleLine, Tender, Store, TaxRule breakdown |
| Role | cashier |
| Components | ReceiptRender (bilingual), QrBlock, SendOptions |
| A11y | Receipt text selectable; send buttons labelled |
| RTL | Arabic-first layout for SA; bilingual columns elsewhere |

## returns

| Aspect | Detail |
|--------|--------|
| Purpose | Return or exchange items from a found Sale, or no-receipt return under policy |
| Primary actions | Pick lines and qty, choose reason, restock yes/no, refund method, exchange items (goes to checkout with credit) |
| Layout zones | Left: original sale lines with returnable qty; right: return basket, refund method, policy text |
| States | outside policy window: needs manager PIN; qty exceeds returnable: blocked; gift receipt: store credit only |
| Data bindings | Return, Sale, SaleLine returnable qty, Tender original kinds, GiftCard for store credit |
| Role | cashier (approval: store-manager) |
| Components | ReturnLineRow, ReasonSelect, RefundMethodSelect, PolicyBanner |
| A11y | Returnable qty in each row label |
| RTL | Columns mirror |

## receipt-lookup

| Aspect | Detail |
|--------|--------|
| Purpose | Find the original Sale: scan receipt barcode/QR, receipt number, date + amount, customer phone, card last 4 |
| Primary actions | Scan, type, filter date range, open sale |
| Layout zones | Search bar with mode chips; results list |
| States | not found: "Try date and amount"; other store: shown with store badge (multi-store) |
| Data bindings | Receipt, Sale, Customer, Tender |
| Role | cashier |
| Components | LookupModes, SaleResultRow |
| A11y | Results announce number, date, total |
| RTL | Mirrors |

## manager-pin

| Aspect | Detail |
|--------|--------|
| Purpose | Approve guarded actions: price override, return outside policy, void, drawer variance, stock adjustment |
| Primary actions | Enter PIN or tap badge, choose reason, approve/deny |
| Layout zones | Modal: action summary (old price → new price), reason chips, numpad |
| States | wrong PIN (3 tries then lockout 5 min); approver lacks limit: "Needs owner" |
| Data bindings | Staff (approver, override_limit_pct), SaleLine, Return, StockMovement |
| Role | store-manager |
| Components | Numpad, ReasonChips, ApprovalSummary |
| A11y | PIN digits masked; count announced |
| RTL | Summary mirrors; numpad unchanged |

## promotions

| Aspect | Detail |
|--------|--------|
| Purpose | Create and schedule BOGO, mix-and-match, tiered, percent/amount off, bundle price |
| Primary actions | New promotion, pick kind, pick products/categories, set rules, schedule, preview on sample basket |
| Layout zones | List with status; editor with rule builder and live basket preview |
| States | conflict: overlapping non-stackable promos warned; expired greyed |
| Data bindings | Promotion, Product, Variant, Store |
| Role | store-manager |
| Components | PromoList, RuleBuilder, BasketPreview |
| A11y | Rule builder fields labelled in words ("Buy 2 get 1") |
| RTL | Mirrors |

## customer-lookup

| Aspect | Detail |
|--------|--------|
| Purpose | Attach a customer by phone or loyalty card; show points, tier, khaata balance |
| Primary actions | Search phone, scan card, quick-create (name + phone), attach |
| Layout zones | Sheet: search, result card with points and balance |
| States | new: consent checkbox for marketing; blocked customer: warning |
| Data bindings | Customer, LoyaltyAccount |
| Role | cashier |
| Components | PhoneField, CustomerCard |
| A11y | Points and balance read out |
| RTL | Mirrors; phone stays LTR |

## gift-cards

| Aspect | Detail |
|--------|--------|
| Purpose | Issue, top up, check balance, void gift cards and store credit |
| Primary actions | Scan/enter code, load amount, check balance, void (PIN) |
| Layout zones | Card lookup; balance and history |
| States | expired; void; insufficient balance |
| Data bindings | GiftCard, Tender (redemptions) |
| Role | cashier |
| Components | CodeField, BalanceCard, HistoryList |
| A11y | Balance announced |
| RTL | Mirrors |

## layaway

| Aspect | Detail |
|--------|--------|
| Purpose | Reserve items for a customer against a deposit, take instalments, release on full payment |
| Primary actions | Create from basket, take payment, collect, cancel (refund per policy) |
| Layout zones | List by due date; detail with items, deposit, balance, schedule |
| States | overdue: amber; expired: stock released |
| Data bindings | Layaway, Sale, Customer, StockMovement reserve |
| Role | cashier |
| Components | LayawayList, PaymentSchedule |
| A11y | Due dates spoken in full |
| RTL | Mirrors |

## product-catalog

| Aspect | Detail |
|--------|--------|
| Purpose | Maintain products, variants (size/colour matrix), barcodes, prices, tax, cost, MRP |
| Primary actions | Create product, generate variant matrix, add barcodes, bulk import CSV, bulk price change |
| Layout zones | Table with filters; editor with tabs (details, variants, barcodes, stock, pricing) |
| States | duplicate barcode: blocked; missing Arabic name: warning in AE/SA |
| Data bindings | Product, Variant, Barcode, TaxRule |
| Role | store-manager |
| Components | ProductTable, VariantMatrix, BarcodeList, CsvImport |
| A11y | Matrix cells labelled "Size M, colour red" |
| RTL | Mirrors |

## purchase-orders

| Aspect | Detail |
|--------|--------|
| Purpose | Raise purchase orders from reorder suggestions, send to supplier |
| Primary actions | Suggest from reorder points, edit lines, send (PDF/email), cancel |
| Layout zones | PO list by status; editor with lines, costs, expected date |
| States | partially-received; overdue |
| Data bindings | PurchaseOrder, Supplier, Variant reorder_point |
| Role | stock-keeper |
| Components | PoList, PoEditor |
| A11y | Status as text, not colour only |
| RTL | Mirrors |

## goods-receipt

| Aspect | Detail |
|--------|--------|
| Purpose | Receive stock (GRN) against a PO or blind; scan to count; record supplier invoice |
| Primary actions | Pick PO, scan items, enter qty, flag damaged, post |
| Layout zones | Ordered vs received columns; scan field; variance highlight |
| States | over tolerance: blocked; unknown barcode: add or skip |
| Data bindings | GoodsReceipt, PurchaseOrder, Supplier, StockMovement |
| Role | stock-keeper |
| Components | ScanField, ReceiveTable, VarianceChip |
| A11y | Variance announced |
| RTL | Mirrors |

## stock-count

| Aspect | Detail |
|--------|--------|
| Purpose | Full stock take or cycle count, plus manual adjustments (damage, theft, expiry) |
| Primary actions | Start count (scope: all, category, bin), scan and count, review variance, post; adjust with reason |
| Layout zones | Count list; variance review with value; reason picker |
| States | counting (selling continues, movements after snapshot reconciled); review; posted |
| Data bindings | StockCount, StockMovement, Variant |
| Role | stock-keeper (post: store-manager) |
| Components | ScanField, CountRow, VarianceTable |
| A11y | Counts entered with numpad |
| RTL | Mirrors |

## transfers

| Aspect | Detail |
|--------|--------|
| Purpose | Move stock between stores or warehouse |
| Primary actions | Create, dispatch, receive by scanning, report discrepancy |
| Layout zones | List by status; detail with sent vs received |
| States | in-transit; discrepancy |
| Data bindings | Transfer, Store, StockMovement |
| Role | stock-keeper |
| Components | TransferList, ScanField |
| A11y | Status text |
| RTL | Mirrors |

## suppliers

| Aspect | Detail |
|--------|--------|
| Purpose | Supplier master: contact, TRN, terms, lead time, return-to-vendor rules |
| Primary actions | Create, edit, block, view POs and RTVs |
| Layout zones | List; detail with tabs |
| States | blocked |
| Data bindings | Supplier, PurchaseOrder |
| Role | store-manager |
| Components | SupplierTable, SupplierForm |
| A11y | Form labels |
| RTL | Mirrors |

## einvoice-status

| Aspect | Detail |
|--------|--------|
| Purpose | Monitor fiscal reporting: ZATCA, FBR, ETA; retry failures |
| Primary actions | Filter by status, retry, view payload and response |
| Layout zones | Counters (reported, pending, failed); table of Receipts |
| States | pending older than 20 h: red alert (ZATCA/ETA 24 h window) |
| Data bindings | Receipt fiscal_ref, SyncEvent |
| Role | accountant |
| Components | StatusCounters, ReceiptTable |
| A11y | Status text |
| RTL | Mirrors |

## customer-display

| Aspect | Detail |
|--------|--------|
| Purpose | Second screen facing the customer: lines as scanned, promotions, total, QR to pay, thank you |
| Primary actions | none (read-only); idle slideshow |
| Layout zones | Last line large; basket list; total 64 px; loyalty points earned |
| States | idle; in-sale; paid |
| Data bindings | Sale, SaleLine |
| Role | customer |
| Components | CustomerLineList, TotalBanner |
| A11y | High contrast, 24 px minimum |
| RTL | Follows customer language |

## cash-management

| Aspect | Detail |
|--------|--------|
| Purpose | Open drawer with float, cash drops, pickups, paid-outs, close with blind count |
| Primary actions | Open with float, drop, pickup, count by denomination, close |
| Layout zones | Session summary; denomination grid; event list |
| States | drawer over limit: prompt drop; variance above policy: manager PIN |
| Data bindings | CashDrawerSession, Tender cash |
| Role | cashier |
| Components | DenominationGrid, Numpad |
| A11y | Totals announced |
| RTL | Mirrors |

## z-report

| Aspect | Detail |
|--------|--------|
| Purpose | End-of-day Z: sales, returns, tax, tenders, drawer variance; locks the day |
| Primary actions | Print X (no reset), print Z (locks), export |
| Layout zones | Report preview |
| States | open sessions block Z |
| Data bindings | CashDrawerSession, Sale, Return, Tender, Receipt |
| Role | store-manager |
| Components | ReportRender |
| A11y | Tables with headers |
| RTL | Mirrors |

## reports

| Aspect | Detail |
|--------|--------|
| Purpose | Sales by item/category/staff/hour, margin, stock valuation, dead stock, shrinkage, promotion lift |
| Primary actions | Pick report, date range, store, export CSV |
| Layout zones | Report list; chart + table |
| States | empty range |
| Data bindings | Sale, SaleLine, StockMovement, StockCount, Promotion |
| Role | owner |
| Components | ReportPicker, Chart, DataTable |
| A11y | Tables accompany charts |
| RTL | Mirrors; charts keep time left to right |

## labels

| Aspect | Detail |
|--------|--------|
| Purpose | Print shelf-edge and product labels: price (VAT-inclusive), barcode, unit price per kg/100 g, Arabic name |
| Primary actions | Pick products (scan, from GRN, from price change), template, qty, print |
| Layout zones | Queue; template preview |
| States | printer offline; template missing field |
| Data bindings | Barcode, Variant, Product |
| Role | stock-keeper |
| Components | LabelQueue, TemplatePreview |
| A11y | Preview alt text |
| RTL | Arabic text right-aligned on label |

## staff-roles

| Aspect | Detail |
|--------|--------|
| Purpose | Staff, PINs, roles, override limits, store access |
| Primary actions | Add staff, set PIN, set role and override limit, suspend |
| Layout zones | List; editor |
| States | suspended |
| Data bindings | Staff, Store |
| Role | owner |
| Components | StaffTable, RoleSelect |
| A11y | Labels |
| RTL | Mirrors |

## store-switcher

| Aspect | Detail |
|--------|--------|
| Purpose | Switch store context; compare stores |
| Primary actions | Pick store |
| Layout zones | Dropdown in header; store cards |
| States | suspended store |
| Data bindings | Store |
| Role | owner |
| Components | StoreMenu |
| A11y | Menu |
| RTL | Mirrors |

## sync-status

| Aspect | Detail |
|--------|--------|
| Purpose | Offline queue, last sync, conflicts |
| Primary actions | Retry, view conflicts |
| Layout zones | Status; queue list |
| States | offline; conflict |
| Data bindings | SyncEvent |
| Role | cashier |
| Components | SyncBadge, QueueList |
| A11y | Status text |
| RTL | Mirrors |
