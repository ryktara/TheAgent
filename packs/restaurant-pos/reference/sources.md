# Restaurant POS — sources

Accessed 2026-09-18 unless noted. VERIFIED = read on the linked page during P3 research.
UNVERIFIED = stated from prior knowledge; the founder or a later step must confirm before the
value drives a compliance control.

## UAE

| Fact | Status | Source |
|------|--------|--------|
| E-invoicing pilot 1 July 2026; mandatory for revenue ≥ AED 50m from 1 Jan 2027, others 1 Jul 2027; B2C exempt until further notice | VERIFIED | https://www.vatupdate.com/2026/07/18/uae-two-ministerial-decisions-set-e-invoicing-scope-and-timeline/ ; https://www.cleartax.com/ae/e-invoicing-uae |
| VAT 5%; displayed prices must be tax-inclusive; penalty AED 5,000 (reduced from 15,000 by Cabinet Decision 49/2021) | VERIFIED | https://www.khaleejtimes.com/uae/businesses-in-uae-must-display-vat-inclusive-prices-to-avoid-penalties-fta ; https://www.mondaq.com/tax-authorities/1663664/vat-inclusive-displayed-prices-rule-exceptions-and-implications |
| Hotel bills: municipality fee 7% (Dubai), service charge 10%, Tourism Dirham AED 7–20 per room-night; fee not levied on Tourism Dirham; standalone restaurants charge VAT only | VERIFIED (7% confirmed by orchestrator 2026-09-18) | https://mazeed.com/blog/hotel-tax-in-dubai/ ; https://www.dubaitravelplanner.com/dubai-tourist-tax/ |
| Tax invoice mandatory fields (TRN, VAT amount, etc.) | VERIFIED | https://invoicedataextraction.com/blog/uae-vat-invoice-requirements |
| Payment gateways with UAE onboarding: Network International N-Genius (hosted checkout, APIs), Telr, PayTabs, Tap, Checkout.com, Stripe UAE | VERIFIED (online) | https://www.skimbox.co/en/resources/blogs/uae-payment-gateway-comparison-telr-stripe-checkout ; https://www.carrilagency.com/blog/best-payment-gateways-in-uae-a-comprehensive-guide |
| Magnati in-person and online availability | VERIFIED by orchestrator 2026-09-18 | orchestrator confirmation |
| In-person semi-integrated terminal support per provider (NI, Magnati, Tap) | BRANCH SETTING (varies by provider contract; configured per branch) | orchestrator decision |
| SoftPOS / Tap to Phone available in UAE | VERIFIED | https://www.payselect.ae/newsroom/tap-to-pay-apps-mobile-payment-guide-for-uae-firms-2026 |
| Talabat, Deliveroo, Careem, Noon Food offer partner APIs used by POS vendors; Talabat publishes integration docs | VERIFIED | https://integration.talabat.com/en/documentation/ ; https://onlineemenu.com/talabat-integration.html ; https://grubtech.com/en/integrations |

## Saudi Arabia

| Fact | Status | Source |
|------|--------|--------|
| ZATCA phase 2: simplified tax invoice (B2C) needs QR with TLV tags 1–5 (seller name, VAT number, timestamp, total with VAT, VAT amount); tags 6–9 added in phase 2 for integrated devices; reporting within 24 h via API | VERIFIED | https://www.wafeq.com/en-sa/tax-and-reporting/qr-code-requirements-for-e-invoices-zatca-saudi-arabia ; https://www.cleartax.com/sa/ksa-einvoicing ; https://zatca.gov.sa/en/E-Invoicing/Introduction/Guidelines/Documents/E-Invoicing_Detailed__Guideline.pdf |
| VAT 15% | VERIFIED by orchestrator 2026-09-18 | https://zatca.gov.sa |
| SoftPOS available (NearPay Visa certified; bank offerings) | VERIFIED | https://nearpay.io/news/near-pay-soft-pos-visa-tap-to-phone-certification ; https://www.stc.com.sa/content/stc/sa/en/business/integrate/digital-and-iot/financial-and-retail-solutions/soft-pos.html |

## Pakistan

| Fact | Status | Source |
|------|--------|--------|
| FBR POS integration: real-time invoice reporting, FBR invoice number and QR printed; mandatory for tier-1 retailers, expanding to restaurants and notified sectors; verification via Tax Asaan or SMS 9966 | VERIFIED | https://www.fbr.gov.pk/pos-invoice-verification/163085/163142 ; https://timelinedigi.com/blog/fbr-pos-integration-digital-invoicing-pakistan-retailers |
| Punjab (PRA) restaurant services: 16% cash, 8% card from 1 July 2026 (was 5%) | VERIFIED | https://propakistani.pk/2026/07/03/punjab-increases-restaurant-card-payment-tax/ ; https://www.geo.tv/latest/673313-true-punjab-has-increased-sales-tax-on-restaurant-bills-paid-by-card-to-8 |
| Sindh (SRB) restaurant services: 15% cash, 8% card/wallet/QR | VERIFIED | https://www.srb.gos.pk/srb/other-services/ |
| Provincial table (Punjab 16%/5% PRA, Sindh 15% SRB, KP 8% KPRA, Balochistan 15% BRA), as of 2026-09 | VERIFY-BEFORE-GO-LIVE (orchestrator-supplied values) | https://zaffreaxon.com/blog/sales-tax-services-rates-by-province-2026-27 (general) |
| SoftPOS availability in Pakistan | AVAILABLE, LIMITED (orchestrator note; provider coverage varies) | orchestrator confirmation |
| Record retention 6 years (KSA, PK) | VERIFIED by orchestrator 2026-09-18 | orchestrator confirmation |

## PCI DSS

| Fact | Status | Source |
|------|--------|--------|
| SAQ A: fully outsourced card capture (redirect or provider-hosted page), about 24 requirements; SAQ A-EP: merchant page loads provider iframe/JS, about 140 requirements plus ASV scans | VERIFIED | https://hyperproof.io/resource/pci-dss-4-0-update-new-saq-a-eligibility-criteria/ ; https://www.barradvisory.com/resource/understanding-saq-a-eligibility/ ; https://listings.pcisecuritystandards.org/documents/PCI-DSS-v4-0-SAQ-A-EP.pdf |

## Other GCC and Egypt

| Fact | Status | Source |
|------|--------|--------|
| Qatar: no VAT in force; Kuwait: no VAT | VERIFIED by orchestrator 2026-09-18 | orchestrator confirmation |
| Bahrain VAT 10%; Oman VAT 5%; Egypt VAT 14% and ETA e-receipt | VERIFIED by orchestrator 2026-09-18 | orchestrator confirmation |
| Minor units: BHD, KWD, OMR 3 decimals | VERIFIED by orchestrator 2026-09-18 (ISO 4217) | https://www.iso.org/iso-4217-currency-codes.html |
| Egypt service charge 12% common | UNVERIFIED | — |
