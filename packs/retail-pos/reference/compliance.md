# Retail POS — compliance

Control ids are referenced from `pack.yaml` `compliance_must` / `compliance_should` and from
`.foundry/compliance.yaml` in phase 9. Each control maps to features (must_have or should_have
ids) and names its verification. Facts marked UNVERIFIED in sources.md carry the same mark here.

## All regions

| Id | Control | Features | Verification |
|----|---------|----------|--------------|
| C-ALL-01 | Card data never touches POS code: terminal-only or provider-hosted capture; PCI-DSS SAQ A scope for online pay links, terminal/P2PE scope for in-person | tender-cash-card-wallet, split-tender | code review: no PAN fields; provider integration doc |
| C-ALL-02 | Receipt numbering gapless and increasing per store; reprints marked; voids keep number | receipt-bilingual-qr, offline-queue | unit test on allocator incl. offline blocks |
| C-ALL-03 | Audit log for every sale, tender, return, price override, void, promotion change, stock adjustment, count post and drawer event with actor and approver | audit-log, price-override, stock-adjustments | integration test: event per transition; append-only grants |
| C-ALL-04 | Tax per TaxRule with inclusive/exclusive handling, one rounding per sale; tax breakdown on receipt | checkout, receipt-bilingual-qr | unit tests with regional fixtures |
| C-ALL-05 | Financial records (sales, receipts, returns, Z reports) retained 5 years minimum, 6 in SA/PK; exportable | reports-core, z-report | retention config; export e2e |
| C-ALL-06 | Price display: shelf labels and customer display show the price actually charged (tax-inclusive where the region requires); unit price per kg on weighed items | label-printing, catalog-management, weighed-items | label fixture review |
| C-ALL-07 | Returns policy displayed at the till and printed on the receipt; defective goods always returnable regardless of policy | returns-exchanges, receipt-bilingual-qr | receipt fixture; policy text config |
| C-ALL-08 | Consumer protection: no hidden charges, promotions honoured at the shelf price, gift card terms printed; staff PINs hashed with lockout after 3 wrong PINs | promotions-engine, staff-roles, gift-cards | unit test on promo price vs label; PIN lockout test |
| C-ALL-09 | Personal data (phone, khaata, loyalty) minimised, exportable and deletable (UAE PDPL, KSA PDPL baseline) | loyalty, khaata-credit | workflow test |
| C-ALL-10 | Daily encrypted backups; restore drill quarterly | offline-queue | runbook |

## UAE (AE)

| Id | Control | Features | Verification |
|----|---------|----------|--------------|
| C-AE-01 | Prices displayed and charged VAT-inclusive (5%); shelf labels and receipts consistent; receipt shows TRN, VAT amount, total | label-printing, receipt-bilingual-qr | fixture review |
| C-AE-02 | Tax invoice fields per FTA; bilingual en/ar | receipt-bilingual-qr | fixture review |
| C-AE-03 | Return and exchange policy clearly displayed in store (Federal Law 15 of 2020 and Cabinet Decision 66 of 2023); weights in metric units, net quantity labels per GSO/UAE.S; scales under MoIAT metrology | returns-exchanges, weighed-items, label-printing | policy config; label fixture |
| C-AE-04 | E-invoicing readiness: B2B invoices exportable for an accredited service provider for the 2027 mandate; B2C receipts out of scope until notified | e-invoice | export job exists |

## Saudi Arabia (SA)

| Id | Control | Features | Verification |
|----|---------|----------|--------------|
| C-SA-01 | Simplified tax invoice for B2C with TLV QR (tags 1–5 seller name, VAT number, timestamp, total with VAT, VAT amount; phase 2 tags for integrated devices); VAT 15% inclusive | receipt-bilingual-qr | QR decode test |
| C-SA-02 | Simplified invoices reported to ZATCA Fatoora within 24 h; retry queue alert at 20 h; cryptographic stamp per device | e-invoice, offline-queue | sandbox integration test |
| C-SA-03 | Return/exchange within 7 days for unused goods (exclusions per Ministry of Commerce); refund includes VAT; policy in clear Arabic | returns-exchanges | policy config + unit test on refund amount |
| C-SA-04 | Arabic-first receipt with English secondary; Hijri date optional | receipt-bilingual-qr | fixture |

## Pakistan (PK)

| Id | Control | Features | Verification |
|----|---------|----------|--------------|
| C-PK-01 | FBR POS integration for tier-1 retailers: each sale reported in real time; FBR invoice number and verifiable QR printed with NTN/STRN; offline buffer with resend | e-invoice, receipt-bilingual-qr, offline-queue | sandbox test |
| C-PK-02 | Sales tax rate table per product (GST, reduced/exempt items) editable; rate VERIFY-BEFORE-GO-LIVE | checkout | unit tests per tax class |
| C-PK-03 | Price never above printed MRP; khaata ledger statement printable for the customer | catalog-management, khaata-credit | unit test on MRP cap |

## Other GCC and Egypt

| Id | Control | Notes |
|----|---------|-------|
| C-QA-01 | No VAT in force; receipts without tax lines; returns policy displayed | confirmed |
| C-BH-01 | VAT 10% with VAT-inclusive price display; 3 minor units | VERIFIED |
| C-KW-01 | No VAT; 3 minor units | confirmed |
| C-OM-01 | VAT 5%; 3 minor units | confirmed |
| C-OM-02 | Fawtara e-invoicing (Peppol PINT OM, UBL 2.1) readiness by phase; B2C scope to be confirmed (UNVERIFIED) | phase dates VERIFIED |
| C-EG-01 | VAT 14%; ETA e-receipt for B2C submitted within 24 h of issue | VERIFIED |

## PCI scope decisions

| Decision | Choice | Consequence |
|----------|--------|-------------|
| In-person | Provider terminal, semi-integrated (amount pushed, approval returned) | POS stores approval code, last 4, scheme only |
| SoftPOS | Provider app; POS receives result only | Same as terminal |
| Online pay links / marketplaces | Provider-hosted page | SAQ A; no card fields on merchant domain |
| Gift cards | Code stored hashed; balance server-side | Not card data, but treated as bearer value |
| Storage | Never PAN, expiry, CVV | Code review + secret scan |

## Data retention

| Data | Retention | Basis |
|------|-----------|-------|
| Sales, receipts, tenders, returns, Z reports | 5 years AE, 6 years SA and PK | tax law |
| Stock movements, counts, GRNs | Same as financial records | inventory valuation audit |
| Audit log | Same as financial records | tax audit |
| Customer PII | Until deletion request or 2 years inactivity | PDPL baseline |
| Sync queue | Until acked plus 30 days | operational |

## Audit log events

| Event | Fields beyond base (ts, actor, device, store, object id) |
|-------|-----------------------------------------------------------|
| sale.opened / parked / recalled / voided | reason, approver |
| sale.line_added / line_voided | variant, qty, weight |
| sale.price_overridden | line, list price, new price, reason, approver |
| promotion.applied | promotion id, discount |
| tender.captured / declined / voided | kind, amount, provider ref |
| return.approved / refunded / exchanged | lines, method, approver |
| giftcard.issued / redeemed / voided | amount, balance after |
| stock.adjusted | variant, qty, reason, approver |
| stockcount.posted | variance value, approver |
| grn.posted / transfer.received | lines, discrepancies |
| drawer.opened / drop / pickup / closed | amount, variance, approver |
| day.z_printed | totals hash |
| fiscal.reported / report_failed | regime, external id, error |

## Feature to control matrix

| Feature | Controls |
|---------|----------|
| checkout | C-ALL-04, C-PK-02 |
| weighed-items | C-ALL-06, C-AE-03 |
| tender-cash-card-wallet | C-ALL-01 |
| receipt-bilingual-qr | C-ALL-02, C-ALL-07, C-AE-01, C-AE-02, C-SA-01, C-SA-04, C-PK-01 |
| returns-exchanges | C-ALL-07, C-AE-03, C-SA-03 |
| price-override | C-ALL-03 |
| promotions-engine | C-ALL-08 |
| label-printing | C-ALL-06, C-AE-01 |
| e-invoice | C-SA-02, C-PK-01, C-AE-04, C-OM-02, C-EG-01 |
| z-report | C-ALL-05 |
| offline-queue | C-ALL-02, C-SA-02, C-PK-01, C-ALL-10 |
| audit-log | C-ALL-03 |

## Verification cadence

| Control group | When | Owner |
|---------------|------|-------|
| C-ALL-01 PCI scope | every release touching tender | security-review |
| C-ALL-02 numbering | every release; nightly two-device offline fixture | code-review |
| C-ALL-04, C-ALL-06 tax and price display | every release; on TaxRule or label template change | accountant |
| C-AE, C-SA, C-PK, C-EG fiscal | before go-live per region; after regulator changes | accountant |
| C-ALL-10 backups | quarterly restore drill | owner |
