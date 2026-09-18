# Migrations

ORM: prisma. Schema: `prisma/schema.prisma`.

Validate: `npx prisma validate`

Migrate: Migrations via npx prisma migrate dev; schema at prisma/schema.prisma

Rule: one migration per ticket; never edit an applied migration; money columns keep Decimal(12,2).
