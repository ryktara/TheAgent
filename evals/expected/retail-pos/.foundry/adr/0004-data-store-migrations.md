---
id: "0004"
title: "Data store and migrations"
status: accepted
decision_refs: ["D:region"]
date: "2026-09-24"
---

# ADR 0004: Data store and migrations

## Context

Money in SAR with 2 minor units; nearest halala, once per sale [D:region]. Receipts, returns and stock movements are append-only.

## Decision

Postgres 16 as the system of record. ORM prisma with migrations committed under prisma/ and applied by the command in stacks.csv. Money columns Decimal(12,2); ids uuid v7; created_at/updated_at on every table; soft delete only where an invariant demands history; audit_events and receipts append-only via grants. Backups daily, restore drill quarterly.

## Alternatives

| Alternative | Rejected because |
|-------------|------------------|
| SQLite on the server | single-writer; multi-terminal branches and reporting need concurrency |
| MongoDB | invariants are relational; RLS and constraints are the gate |

## Consequences

- Schema skeleton generated from domain.yaml
- Every entity state is a Postgres enum
- Indexes on (branch_id, created_at) by default

## Revisit when

Write volume exceeds one Postgres primary, or a regulator demands a certified fiscal store.
