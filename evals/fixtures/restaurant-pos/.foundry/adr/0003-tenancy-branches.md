---
id: "0003"
title: "Tenancy and branches"
status: accepted
decision_refs: ["D:branches", "D:central-menu-sync"]
date: "2026-09-18"
---

# ADR 0003: Tenancy and branches

## Context

Branches decision: single branch [D:branches] [D:central-menu-sync]. Every financial record is scoped to a branch; receipts, floats and tax rules are per branch.

## Decision

Single organisation (tenant) per deployment with branch_id on every operational table; Postgres row-level security keyed by branch for device roles, organisation-wide for owner roles. Schema is multi-branch ready; a second branch is a data row, not a migration. No cross-organisation tenancy in this release.

## Alternatives

| Alternative | Rejected because |
|-------------|------------------|
| Multi-tenant SaaS from day one | adds RLS complexity and billing before the first customer runs |
| Database per branch | reporting across branches becomes ETL; sync harder |

## Consequences

- Branch switcher only for owner roles
- Consolidated reports are simple SQL
- Adding organisations later means adding tenant_id above branch_id

## Revisit when

A second organisation must share the deployment, or a branch must run on its own server.
