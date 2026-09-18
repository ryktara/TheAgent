---
name: api-contract
description: Produce openapi.yaml and .foundry/events.yaml for phase 6 from the domain model and jobs; add sync, webhook and job operations the integrations require.
invocation: model
model: sonnet
reads: [.foundry/domain.yaml, .foundry/architecture.md, .foundry/adr/0006-integrations-boundary.md, .foundry/decisions.yaml]
writes: [openapi.yaml, .foundry/events.yaml]
gate: python scripts/foundry.py gate api
---

# api-contract — phase 6b

Contract first. The skeleton emits CRUD per entity, one operation per job, sync push/pull,
inbound webhooks per chosen integration category, cursor pagination, ETag on mutable
resources and `x-foundry` metadata on every operation. The model tightens authz and payloads.

## Steps

1. **Generate.**

   ```
   python scripts/foundry.py api-skeleton
   ```

   Done when: `openapi.yaml` and `.foundry/events.yaml` exist and the command printed path,
   operation and event counts.

2. **Tighten authz.** For every operation, replace the generated `x-foundry.authz` sentence
   with the exact rule: role list, branch scope, and the manager-PIN condition when the job's
   workflow guards it (open only the matching section of
   `packs/<slug>/reference/workflows.md`).
   Done when: no `x-foundry.authz` still reads "manager PIN when the job guards it".

3. **Shape job payloads.** Each job operation's request body names the fields the workflow
   step needs (for example `send-to-kitchen`: course; `split-bill`: mode, seats or amounts).
   Done when: no job operation has an empty `type: object` request body.

4. **Integrations.** Keep only webhook paths for providers chosen in the ledger; add outbound
   adapter contracts as `components.schemas` when ADR 0006 names them.
   Done when: webhook enums list only chosen providers.

5. **Gate.**

   ```
   python scripts/foundry.py gate api
   ```

   Structural check: OpenAPI 3.1, unique operationIds, `x-foundry.authz` on every operation,
   2xx and 4xx responses, a path per entity, an operation per job, events.yaml validates;
   `npx @redocly/cli lint` runs when available.
   Done when: the gate prints `pass`.

## Reference

| x-foundry field | Meaning |
|-----------------|---------|
| job | job id or read/create/update/archive |
| personas | who calls it |
| authz | the rule the api enforces |
| idempotent | safe to retry with the same Idempotency-Key |
| offline_capable | device may queue it in the outbox |
| audit | writes an audit event |
