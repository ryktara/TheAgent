---
name: writing-for-agents
description: Write or edit a SKILL.md, CLAUDE.md, or agent instruction file so it loads cheaply and fires at the right moment. Review an existing skill for pruning.
invocation: model
model: sonnet
reads: []
writes: []
gate: python scripts/foundry.py validate
---

# Writing for agents

House style for every instruction file in this repo. Frontmatter spec: SKILL-MECHANICS.md.

## Steps

1. **Classify invocation.** Orchestrator that a human triggers → `invocation: user`.
   Reusable discipline any agent may reach → `invocation: model`. User-invoked skills call
   model-invoked ones; the reverse edge never exists.
   Done when: frontmatter `invocation` is set and every skill this one calls is `model`.

2. **Write the description as a context pointer.** First word is the trigger (a verb or the
   noun the user will say). One trigger per distinct branch the skill handles. Zero identity
   restatement.
   Done when: the description begins with a verb or trigger noun and names each branch once.

3. **Lay out the information hierarchy.** In-file steps first. In-file reference next (tables,
   short lists every branch needs). Disclosed reference last: a sibling file, reached by one
   pointer line, for material only some branches reach.
   Done when: SKILL.md is at most 150 lines and every sibling file is named by a pointer.

4. **End every step on a completion criterion.** Checkable and exhaustive: a count, a
   file, a passing command, a "for every X, Y" clause.
   Done when: each step's last line begins with "Done when:" and could be verified by a script.

5. **Prefer leading words.** Replace explanatory sentences with single pretrained concepts:
   tracer bullet, red/green, frontier, blast radius, single source of truth, idempotent.
   Phrase positively. Keep a prohibition only as a hard guardrail, paired with the positive
   target ("keep secrets in the vault; never in source").
   Done when: no sentence explains a concept the model already holds.

6. **Prune.** Delete every sentence the model obeys by default. Delete restatements of
   package.json, tsconfig, or any other file the environment already exposes.
   Done when: removing any remaining line would change agent behaviour.

7. **Complete the frontmatter.** name, description, invocation, model, reads, writes, gate.
   Done when: `python scripts/foundry.py validate` passes.

## Reference

| Leading word | Concept it replaces |
|--------------|---------------------|
| tracer bullet | thin vertical slice touching every layer end to end |
| red/green | failing test first, then minimal code to pass |
| frontier | set of questions whose prerequisites are all answered |
| blast radius | files and callers affected by a change |
| source of truth | the one place a fact is stored; everything else points at it |

Model hint guidance: `haiku` for lookups and validation, `sonnet` for implementation and
authoring, `opus` for architecture, security and judgement calls.
