---
id: "0008"
title: "Observability"
status: accepted
decision_refs: ["D:offline"]
date: "2026-09-18"
---

# ADR 0008: Observability

## Context

Operational app with offline devices: failures surface late unless every request and sync event is traceable [D:offline].

## Decision

Structured JSON logs with request id, device id, staff id and branch id on every line; error tracking with source maps for web, api and bridge; metrics for sync queue depth, ticket age and payment latency; health endpoint per container; alerts on fiscal reporting backlog (SA 20 h) and sync lag over 5 min.

## Alternatives

| Alternative | Rejected because |
|-------------|------------------|
| Console logs only | no correlation across device, api and provider |
| Full tracing platform on day one | cost and setup exceed the first release; add when p95 targets are missed |

## Consequences

- Request id propagates from device to provider calls
- Sync-status screen reads the same metrics
- Log retention 30 days, audit table forever

## Revisit when

p95 targets are missed and logs cannot explain why.
