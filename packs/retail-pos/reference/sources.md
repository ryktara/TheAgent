# Retail POS — sources

Accessed 2026-09-23 unless noted. VERIFIED = read on the linked page (or its search abstract)
during research. UNVERIFIED = stated from prior knowledge; confirm before it drives a control.

## UAE

| Fact | Status | Source |
|------|--------|--------|
| VAT 5%; displayed prices must be VAT-inclusive | VERIFIED | https://www.khaleejtimes.com/uae/businesses-in-uae-must-display-vat-inclusive-prices-to-avoid-penalties-fta |
| E-invoicing B2B/B2G mandate from 2027; B2C exempt until further notice | VERIFIED | https://www.cleartax.com/ae/e-invoicing-uae |
| Stores must display return and refund policy; Federal Law 15 of 2020, Cabinet Decision 66 of 2023; defective goods must be repaired, replaced or refunded | VERIFIED | https://u.ae/en/information-and-services/justice-safety-and-the-law/consumer-protection ; https://www.uaeexperthub.com/consumer-rights-uae-returns-refunds-counterfeit/ |
| Net quantity labelling in metric units per UAE.S GSO R87 / GSO ISO 1000; Arabic labelling mandatory; ESMA merged into MoIAT 2020 | VERIFIED | https://www.trade.gov/knowledge-product/united-arab-emirates-labelingmarking-requirements |
| Scale verification stickers required on retail scales | UNVERIFIED | — |

## Saudi Arabia

| Fact | Status | Source |
|------|--------|--------|
| ZATCA simplified tax invoice TLV QR tags 1–5; reporting within 24 h | VERIFIED | https://www.wafeq.com/en-sa/tax-and-reporting/qr-code-requirements-for-e-invoices-zatca-saudi-arabia ; https://zatca.gov.sa/en/E-Invoicing/Introduction/Guidelines/Documents/E-Invoicing_Detailed__Guideline.pdf |
| VAT 15% | VERIFIED | https://zatca.gov.sa |
| 7-day return/exchange for unused goods; stores cannot refuse; refund includes VAT | VERIFIED | https://www.arabnews.com/node/1696931/saudi-arabia ; https://giraffy.com/ksa/en/learn/Learn/spend-and-save/warranty-and-return |

## Pakistan

| Fact | Status | Source |
|------|--------|--------|
| Tier-1 retailers must integrate all POS with FBR; receipt carries FBR invoice number and verifiable QR | VERIFIED | https://download1.fbr.gov.pk/Docs/20201201313212651FAQs-POSIntegration.pdf ; https://www.brecorder.com/news/40345444 |
| Receipt shows NTN, STRN, item tax rates and amounts | VERIFIED | https://taxflow.com.pk/blog/fbr-pos-integration-retailers |
| Standard GST 18% on goods | UNVERIFIED | — |
| MRP printing and khaata practice | UNVERIFIED (market practice) | — |

## Other GCC and Egypt

| Fact | Status | Source |
|------|--------|--------|
| Bahrain VAT 10% from 1 Jan 2022; VAT-inclusive price display | VERIFIED | https://www.bahrain.bh/wps/portal/en/BNP/HomeNationalPortal ; https://www.avalara.com/us/en/vatlive/country-guides/africa-and-middle-east/bahrain/bahrain-vat-rates.html |
| Oman Fawtara: Peppol PINT OM, phase 1 Aug 2026 (100 large), phase 2 Feb 2027, phase 3 Aug 2027 | VERIFIED | https://www.vatupdate.com/2026/07/27/oman-launches-fawtara-e-invoicing-four-phase-rollout-begins-august-2026-e-invoicing-faqs/ ; https://www.cleartax.com/om/e-invoicing-oman |
| Egypt ETA e-receipt for B2C, rolled out in sub-phases; submission within 24 h | VERIFIED | https://sovos.com/regulatory-updates/global-vat/egypt-tax-authority-extends-e-receipt-obligations-for-b2c-transactions/ ; https://invoicedataextraction.com/blog/egypt-e-receipt-requirements |
| Qatar and Kuwait: no VAT in force | UNVERIFIED (carried from restaurant-pos orchestrator note) | — |
| Oman VAT 5%, Egypt VAT 14% | UNVERIFIED (carried from restaurant-pos) | — |
| BHD, KWD, OMR use 3 minor units | VERIFIED | https://www.iso.org/iso-4217-currency-codes.html |

## Barcodes, PCI

| Fact | Status | Source |
|------|--------|--------|
| GS1 prefixes 020–029 are restricted circulation numbers for retailer internal use, incl. variable-measure (weighed) items in EAN-13 | VERIFIED | https://www.gs1.org/docs/barcodes/SummaryOfGS1MOPrefixes20-29.pdf ; https://gs1.se/en/guides/how-to-guides/barcode-label-items-of-varying-weight/ |
| Layout of weight vs price digits in prefix-2 codes varies by GS1 member organisation and scale config | VERIFIED | https://www.gs1.org/docs/barcodes/SummaryOfGS1MOPrefixes20-29.pdf |
| SAQ A for fully outsourced card capture; SAQ A-EP when merchant page loads provider JS | VERIFIED | https://hyperproof.io/resource/pci-dss-4-0-update-new-saq-a-eligibility-criteria/ |
