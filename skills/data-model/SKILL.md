---
name: data-model
description: Produce the database schema for phase 6 from .foundry/domain.yaml; refine only where an invariant demands a constraint or index.
invocation: model
model: sonnet
reads: [.foundry/domain.yaml, .foundry/architecture.md, .foundry/adr/0004-data-store-migrations.md, data/stacks.csv]
writes: [prisma/schema.prisma, migrations/README.md]
gate: python scripts/foundry.py gate data
---

# data-model — phase 6a

Schema follows the domain model; the skeleton emits one model per entity, an enum per state
list, relations from `*_id` fields, money as Decimal in the region's minor units, and a
(branch_id, created_at) index. The model adds what invariants require.

## Steps

1. **Generate.**

   ```
   python scripts/foundry.py schema-skeleton --orm prisma
   ```

   (`--orm drizzle` when ADR 0004 chose drizzle.)
   Done when: `prisma/schema.prisma` (or `db/schema.ts`) and `migrations/README.md` exist.

2. **Apply invariants.** For each invariant in `domain.yaml`:
   - uniqueness ("gapless per Branch", "one open Order per Table") → `@@unique` or a partial
     unique index noted in a `///` comment for the migration;
   - numeric rules ("never exceeds", "sums to") → `///` check-constraint comment naming the SQL;
   - append-only entities (audit, receipts, sync events) → no `updated_at` mutation path, note
     the grant in migrations/README.md.
   Done when: every invariant that can be a database rule has a constraint, index or a `///`
   comment naming the migration SQL.

3. **Relations and cascades.** Every `*_id` field references a model; deletes are soft
   (`deleted_at`) on ordering, payments and people; restrict on the rest.
   Done when: no dangling `*_id` and every relation has an explicit onDelete.

4. **Gate.**

   ```
   python scripts/foundry.py gate data
   ```

   Runs `npx prisma validate` when node and prisma are available, otherwise a structural check
   (model per entity, enum per state list, balanced braces).
   Done when: the gate prints `pass`.

## Reference

| Field rule | Type |
|------------|------|
| `id` | String uuid primary key |
| `*_id` naming an entity | uuid + relation |
| `*_at` | DateTime? |
| price, total, amount, delta, balance, cost, rate, pct | Decimal(12, minor units) |
| qty, count, seq, covers, number, seats | Int |
| `is_*`, opens_drawer, required, inclusive | Boolean |
| states | enum `<Entity>State` |
