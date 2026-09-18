# Restaurant POS — sources

Accessed 2026-09-18 unless noted. VERIFIED = read on the linked page during P3 research.
UNVERIFIED = stated from prior knowledge; the founder or a later step must confirm before the
value drives a compliance control.

## UAE

| Fact | Status | Source |
|------|--------|--------|
| E-invoicing pilot 1 July 2026; mandatory for revenue ≥ AED 50m from 1 Jan 2027, others 1 Jul 2027; B2C exempt until further notice | VERIFIED | https://www.vatupdate.com/2026/07/18/uae-two-ministerial-decisions-set-e-invoicing-scope-and-timeline/ ; https://www.cleartax.com/ae/e-invoicing-uae |
| VAT 5%; displayed prices must be tax-inclusive; penalty AED 5,000 (reduced from 15,000 by Cabinet Decision 49/2021) | VERIFIED | https://www.khaleejtimes.com/uae/businesses-in-uae-must-display-vat-inclusive-prices-to-avoid-penalties-fta ; https://www.mondaq.com/tax-authorities/1663664/vat-inclusive-displayed-prices-rule-exceptions-and-implications |
| Hotel bills: municipality fee 7% (Dubai), service charge 10%, Tourism Dirham AED 7–20 per room-night; fee not levied on Tourism Dirham; standalone restaurants charge VAT only | VERIFIED (7% figure; one source states 10%, treat exact rate as configurable) | https://mazeed.com/blog/hotel-tax-in-dubai/ ; https://www.dubaitravelplanner.com/dubai-tourist-tax/ |
| Tax invoice mandatory fields (TRN, VAT amount, etc.) | VERIFIED | https://invoicedataextraction.com/blog/uae-vat-invoice-requirements |
| Payment gateways with UAE onboarding: Network International N-Genius (hosted checkout, APIs), Telr, PayTabs, Tap, Checkout.com, Stripe UAE | VERIFIED (online) | https://www.skimbox.co/en/resources/blogs/uae-payment-gateway-comparison-telr-stripe-checkout ; https://www.carrilagency.com/blog/best-payment-gateways-in-uae-a-comprehensive-guide |
| Magnati in-person and online availability | UNVERIFIED (no result in search) | — |
| In-person semi-integrated terminal support per provider (NI, Magnati, Tap) | UNVERIFIED | — |
| SoftPOS / Tap to Phone available in UAE | VERIFIED | https://www.payselect.ae/newsroom/tap-to-pay-apps-mobile-payment-guide-for-uae-firms-2026 |
| Talabat, Deliveroo, Careem, Noon Food offer partner APIs used by POS vendors; Talabat publishes integration docs | VERIFIED | https://integration.talabat.com/en/documentation/ ; https://onlineemenu.com/talabat-integration.html ; https://grubtech.com/en/integrations |

## Saudi Arabia

| Fact | Status | Source |
|------|--------|--------|
| ZATCA phase 2: simplified tax invoice (B2C) needs QR with TLV tags 1–5 (seller name, VAT number, timestamp, total with VAT, VAT amount); tags 6–9 added in phase 2 for integrated devices; reporting within 24 h via API | VERIFIED | https://www.wafeq.com/en-sa/tax-and-reporting/qr-code-requirements-for-e-invoices-zatca-saudi-arabia ; https://www.cleartax.com/sa/ksa-einvoicing ; https://zatca.gov.sa/en/E-Invoicing/Introduction/Guidelines/Documents/E-Invoicing_Detailed__Guideline.pdf |
| VAT 15% | UNVERIFIED in this pass (widely known; confirm on zatca.gov.sa) | — |
| SoftPOS available (NearPay Visa certified; bank offerings) | VERIFIED | https://nearpay.io/news/near-pay-soft-pos-visa-tap-to-phone-certification ; https://www.stc.com.sa/content/stc/sa/en/business/integrate/digital-and-iot/financial-and-retail-solutions/soft-pos.html |

## Pakistan

| Fact | Status | Source |
|------|--------|--------|
| FBR POS integration: real-time invoice reporting, FBR invoice number and QR printed; mandatory for tier-1 retailers, expanding to restaurants and notified sectors; verification via Tax Asaan or SMS 9966 | VERIFIED | https://www.fbr.gov.pk/pos-invoice-verification/163085/163142 ; https://timelinedigi.com/blog/fbr-pos-integration-digital-invoicing-pakistan-retailers |
| Punjab (PRA) restaurant services: 16% cash, 8% card from 1 July 2026 (was 5%) | VERIFIED | https://propakistani.pk/2026/07/03/punjab-increases-restaurant-card-payment-tax/ ; https://www.geo.tv/latest/673313-true-punjab-has-increased-sales-tax-on-restaurant-bills-paid-by-card-to-8 |
| Sindh (SRB) restaurant services: 15% cash, 8% card/wallet/QR | VERIFIED | https://www.srb.gos.pk/srb/other-services/ |
| KP (KPRA) restaurant rate 16%; Balochistan rate | UNVERIFIED | https://zaffreaxon.com/blog/sales-tax-services-rates-by-province-2026-27 (general) |
| SoftPOS availability in Pakistan | UNVERIFIED | — |
| Record retention 6 years | UNVERIFIED | — |

## PCI DSS

| Fact | Status | Source |
|------|--------|--------|
| SAQ A: fully outsourced card capture (redirect or provider-hosted page), about 24 requirements; SAQ A-EP: merchant page loads provider iframe/JS, about 140 requirements plus ASV scans | VERIFIED | https://hyperproof.io/resource/pci-dss-4-0-update-new-saq-a-eligibility-criteria/ ; https://www.barradvisory.com/resource/understanding-saq-a-eligibility/ ; https://listings.pcisecuritystandards.org/documents/PCI-DSS-v4-0-SAQ-A-EP.pdf |

## Other GCC and Egypt

| Fact | Status |
|------|--------|
| Qatar: no VAT in force; Kuwait: no VAT | UNVERIFIED |
| Bahrain VAT 10%; Oman VAT 5%; Egypt VAT 14% and ETA e-receipt | UNVERIFIED |
| Minor units: BHD, KWD, OMR 3 decimals | UNVERIFIED (ISO 4217, stable) |
| Egypt service charge 12% common | UNVERIFIED |
