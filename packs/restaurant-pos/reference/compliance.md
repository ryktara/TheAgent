# Restaurant POS — compliance

Control ids are referenced from `pack.yaml` `compliance_must` / `compliance_should` and from
`.foundry/compliance.yaml` in phase 9. Each control maps to features (must_have ids) and names
its verification. Facts marked UNVERIFIED in sources.md carry the same mark here.

## All regions

| Id | Control | Features | Verification |
|----|---------|----------|--------------|
| C-ALL-01 | Card data never touches POS code: hosted fields, hosted page, or terminal-only capture; PCI-DSS SAQ A scope for online, terminal SAQ for in-person | tender-cash-card-wallet, qr-self-order | code review: no PAN fields; provider integration doc |
| C-ALL-02 | Receipt numbering gapless and increasing per branch; reprints marked; voids retain number | receipt-bilingual-qr, offline-queue | unit test on number allocator incl. offline blocks |
| C-ALL-03 | Audit log for every order, payment, refund, void, comp, discount, shift and menu price event with actor and approver | audit-log, hold-void-comp, refunds | integration test: event per transition; append-only table grants |
| C-ALL-04 | Tax computed per TaxRule with inclusive/exclusive handling and one rounding per order; tax breakdown on receipt | tender-cash-card-wallet, receipt-bilingual-qr | unit tests with regional fixtures |
| C-ALL-05 | Financial records retained 5 years minimum (7 where required); exportable | reports-core, end-of-day | retention config; export e2e |
| C-ALL-06 | Staff PINs hashed; guarded actions require approver; lockout after 3 wrong PINs | staff-roles, hold-void-comp | unit test |
| C-ALL-07 | Personal data (customer phone, allergens, khaata) minimised, exportable and deletable on request (GDPR, UAE PDPL, KSA PDPL baseline) | loyalty, reports-core | workflow test |
| C-ALL-08 | Daily encrypted backups; restore drill quarterly | offline-queue | runbook |

## UAE (AE)

| Id | Control | Features | Verification |
|----|---------|----------|--------------|
| C-AE-01 | Prices displayed and charged tax-inclusive (VAT 5%); receipt shows TRN, VAT amount, total | menu-management, receipt-bilingual-qr | fixture receipt review |
| C-AE-02 | Tax invoice fields per FTA: supplier name, TRN, date, description, VAT rate, VAT amount, total; bilingual en/ar | receipt-bilingual-qr | fixture receipt review |
| C-AE-03 | Hotel F&B bills show municipality fee (Dubai 7%) and service charge (10%) as separate lines before VAT; Tourism Dirham never applied to F&B | tips-service-charge, tender-cash-card-wallet | unit test on hotel branch rule |
| C-AE-04 | E-invoicing readiness: B2B invoices exportable in the FTA data dictionary format for the 2027 mandate; B2C receipts out of scope until notified | e-invoicing | export job exists |

## Saudi Arabia (SA)

| Id | Control | Features | Verification |
|----|---------|----------|--------------|
| C-SA-01 | Simplified tax invoice for B2C with TLV QR (tags 1–5: seller name, VAT number, timestamp, total with VAT, VAT amount); VAT 15% inclusive display | receipt-bilingual-qr | QR decode test |
| C-SA-02 | Simplified invoices reported to ZATCA Fatoora in XML within 24 h; retry queue with alert at 20 h; cryptographic stamp per device (phase 2 integrated devices) | e-invoicing, offline-queue | integration test against sandbox |
| C-SA-03 | Arabic-first receipt with English secondary; Hijri date optional | receipt-bilingual-qr | fixture |

## Pakistan (PK)

| Id | Control | Features | Verification |
|----|---------|----------|--------------|
| C-PK-01 | FBR POS integration where notified: each sale sent in real time, FBR invoice number and QR printed; offline buffer with resend | e-invoicing, receipt-bilingual-qr, offline-queue | sandbox test |
| C-PK-02 | Provincial sales tax on restaurant services by payment mode: Punjab 16% cash / 8% card; Sindh 15% cash / 8% card, wallet or QR; rate table per province editable | tender-cash-card-wallet | unit tests per province and tender |
| C-PK-03 | KP and Balochistan rates configurable (UNVERIFIED current rates) | tender-cash-card-wallet | config review |

## Other GCC and Egypt (UNVERIFIED rates, configurable)

| Id | Control | Notes |
|----|---------|-------|
| C-QA-01 | No VAT in force; receipts without tax lines; service charge shown | UNVERIFIED |
| C-BH-01 | VAT 10% inclusive; 3 minor units; hotel/restaurant levy | UNVERIFIED |
| C-KW-01 | No VAT; 3 minor units | UNVERIFIED |
| C-OM-01 | VAT 5%; 3 minor units | UNVERIFIED |
| C-EG-01 | VAT 14%; ETA e-receipt for B2C | UNVERIFIED |

## PCI scope decisions

| Decision | Choice | Consequence |
|----------|--------|-------------|
| Online (QR self-order, pay links) | Provider hosted page or redirect | SAQ A: about 24 requirements; no card fields on merchant domain |
| Online with merchant-hosted page loading provider iframe/JS | Avoid | Would move to SAQ A-EP: about 140 requirements plus ASV scans |
| In-person | Provider terminal (semi-integrated: amount pushed, approval code returned) | Terminal vendor holds P2PE/PTS scope; POS stores only approval code, last 4, scheme |
| SoftPOS | Provider app on Android; POS receives result only | Same as terminal |
| Storage | Never store PAN, expiry, CVV; provider token only for refunds | Code review + secret scan |

## Data retention

| Data | Retention | Basis |
|------|-----------|-------|
| Orders, receipts, payments, refunds, shifts | 5 years (AE VAT record-keeping), 6 years KSA, 6 years PK (UNVERIFIED exact) | tax law |
| Audit log | Same as financial records | tax audit |
| Customer PII | Until deletion request or 2 years inactivity | PDPL baseline |
| KDS tickets | 90 days | operational |
| Sync queue | Until acked plus 30 days | operational |

## Audit log events

| Event | Fields beyond base (ts, actor, device, branch, object id) |
|-------|-------------------------------------------------------------|
| order.opened | table, covers, channel |
| order.line_added / line_voided / line_comped | line id, reason, approver |
| order.sent / fired | course, station |
| order.discount_applied | discount id, amount, approver |
| order.service_charge_removed | approver |
| order.merged / transferred | source and target tables |
| order.voided | reason, approver |
| payment.captured / declined / voided | tender, amount, provider ref, approval code |
| refund.requested / processed | amount, reason, approver |
| receipt.issued / reprinted | number, language, fiscal ref |
| shift.opened / closed | float, counted, variance, approver if over policy |
| day.locked | totals hash |
| menu.price_changed / item_86 | item, old, new, channel |
| staff.pin_changed / role_changed | target staff |
| sync.conflict_resolved | entity, rule applied |
| fiscal.reported / report_failed | regime, external id, error |

## Feature to control matrix

| Feature (must_have id) | Controls |
|------------------------|----------|
| order-entry | C-ALL-03 |
| table-map | C-ALL-03 |
| modifiers | C-ALL-04 (modifier prices taxed with the line) |
| course-firing | C-ALL-03 |
| send-to-kitchen | C-ALL-03 |
| kds | none (operational) |
| hold-void-comp | C-ALL-03, C-ALL-06 |
| split-bill | C-ALL-02, C-ALL-04 (one receipt per bill, rounding per bill) |
| merge-transfer | C-ALL-03 |
| discounts | C-ALL-03, C-ALL-06 |
| tips-service-charge | C-AE-03, C-ALL-04 |
| tender-cash-card-wallet | C-ALL-01, C-ALL-04, C-PK-02 |
| split-tender | C-ALL-01 |
| receipt-bilingual-qr | C-ALL-02, C-AE-01, C-AE-02, C-SA-01, C-SA-03, C-PK-01 |
| refunds | C-ALL-01, C-ALL-03, C-ALL-06 |
| shift-cash-count | C-ALL-03 |
| z-report | C-ALL-05 |
| end-of-day | C-ALL-05, C-ALL-08 |
| menu-management | C-AE-01 (inclusive prices), C-ALL-03 |
| floor-management | none |
| inventory-basic | none |
| reports-core | C-ALL-05, C-ALL-07 |
| staff-roles | C-ALL-06 |
| offline-queue | C-ALL-02, C-SA-02, C-PK-01, C-ALL-08 |
| audit-log | C-ALL-03 |

## Verification cadence

| Control group | When | Owner |
|---------------|------|-------|
| C-ALL-01 PCI scope | every release touching tender or qr-self-order | security-review |
| C-ALL-02 numbering | every release; nightly fixture run across two offline devices | code-review |
| C-ALL-03 audit | every release; monthly sample audit by owner | owner |
| C-ALL-04 tax | every release; when a TaxRule changes | accountant |
| C-AE, C-SA, C-PK fiscal | before go-live per region; after regulator changes | accountant |
| C-ALL-08 backups | quarterly restore drill | owner |
