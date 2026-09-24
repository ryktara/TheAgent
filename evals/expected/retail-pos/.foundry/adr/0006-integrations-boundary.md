---
id: "0006"
title: "Integrations boundary"
status: accepted
decision_refs: ["D:payments"]
date: "2026-09-24"
---

# ADR 0006: Integrations boundary

## Context

Payments via network-intl; delivery platforms off; printing through a local bridge [D:payments]. Card data never enters the till.

## Decision

One adapter interface per integration category (PaymentAdapter, DeliveryAdapter, PrinterAdapter, AccountingAdapter, FiscalAdapter) behind the api; providers are modules selected by branch settings. Inbound webhooks are idempotent on (provider, event_id) with a stored receipt; outbound calls carry an idempotency key derived from the order or payment id. Terminal payments are semi-integrated: the api pushes the amount, the terminal returns approval code and last four; the POS stores only those.

## Alternatives

| Alternative | Rejected because |
|-------------|------------------|
| Direct provider SDK calls from the POS UI | spreads secrets and PCI scope to devices |
| Middleware aggregator for delivery | adds a vendor and a failure point; direct partner APIs exist |

## Consequences

- Provider secrets live only in the api environment
- Every adapter ships a sandbox test
- Tablet-fallback mode covers a platform outage

## Revisit when

A provider only offers a device-side SDK, or a fourth delivery platform is added.
