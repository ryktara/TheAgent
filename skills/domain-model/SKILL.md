---
name: domain-model
description: Model the domain for phase 4: write .foundry/domain.yaml and CONTEXT.md from the pack, the PRD and the workflows, then close every gap the gate names.
invocation: model
model: sonnet
reads: [.foundry/prd.md, .foundry/decisions.yaml, .foundry/pack.yaml, packs/<slug>/pack.yaml, packs/<slug>/reference/workflows.md]
writes: [.foundry/domain.yaml, CONTEXT.md]
gate: python scripts/foundry.py gate domain
---

# domain-model — phase 4

Ubiquitous language first. The skeleton carries every entity, state, invariant and default
transition; the model adds guards, missing transitions and project terms. Only the workflow
sections whose headings match in-scope jobs are opened.

## Steps

1. **Generate.**

   ```
   python scripts/foundry.py domain-skeleton
   ```

   Done when: `.foundry/domain.yaml` and `CONTEXT.md` exist and the command printed entity,
   transition and event counts.

2. **Walk each in-scope job.** For every job id in PRD §3, find the workflow in
   `packs/<slug>/reference/workflows.md` whose heading names that job (open only those
   sections). For every step with a transition or failure path, ensure `domain.yaml` has the
   transition with `by` = the persona in the step and `guard` = the condition in the step.
   Add invariants the workflow states that the skeleton lacks.
   Done when: every transition or failure path in the opened sections maps to a transition or
   invariant in `domain.yaml`.

3. **Name actors.** Every `by` is a pack persona or `system`.
   Done when: no transition has an empty or unknown actor.

4. **Add project terms.** Up to 10 rows under "Project-specific terms" in CONTEXT.md for words
   the brief or founder used that the pack glossary lacks (same table shape). Remove the
   `<!-- model: -->` comment.
   Done when: the section has 0–10 rows and no comment.

5. **Gate.**

   ```
   python scripts/foundry.py gate domain
   ```

   Done when: the gate prints `pass`: every PRD job and feature id resolves to a glossary term
   or entity in CONTEXT.md; every entity has an invariant and a transition; every transition
   names a persona; every event has a consumer or is marked external.

## Reference

| Skeleton rule | Detail |
|---------------|--------|
| Contexts | ordering, kitchen, payments, menu, inventory, people, reporting, sync |
| Default transitions | consecutive states form a chain; branch states (void, refunded, cancelled…) hang off the second state with guard "reason recorded" |
| Actor | persona of the first in-scope job whose id or screens share a word with the entity |
| Events | one per transition, named `<Entity><State>`; reporting consumes all; kitchen consumes sent/fired; sync consumes ordering and payments |
| Glossary filter | pack glossary rows whose term or alias shares a stem with in-scope jobs, features or entities |
