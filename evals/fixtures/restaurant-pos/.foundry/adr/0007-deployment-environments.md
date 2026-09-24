---
id: "0007"
title: "Deployment and environments"
status: accepted
decision_refs: ["D:branches"]
date: "2026-09-18"
---

# ADR 0007: Deployment and environments

## Context

Small team, one branch(es), no SRE. Local development must run on Windows without WSL [D:branches].

## Decision

Local: docker compose with postgres and the api; web via the framework dev server; the print bridge runs natively. Production default: one VPS or Fly.io app per organisation with managed Postgres, TLS at the edge, nightly backups. Environments: local, staging, production; secrets injected by the platform; preview environment per PR is added in P7 when CI exists.

## Alternatives

| Alternative | Rejected because |
|-------------|------------------|
| Kubernetes | operational cost far above a single-organisation deployment |
| Serverless functions | websocket fan-out and long-lived sync connections fit poorly |

## Consequences

- Same container image for staging and production
- Deploy is one command in the runbook
- Wizard covers DNS, secrets and provider onboarding

## Revisit when

More than 100 branches, multi-region residency, or a second organisation.
