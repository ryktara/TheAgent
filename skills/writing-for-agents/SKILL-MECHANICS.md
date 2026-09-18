# SKILL.md mechanics

Machine-checked by `scripts/foundry.py validate` against `schemas/skill-frontmatter.schema.json`.

## Frontmatter fields

| Field | Type | Rule |
|-------|------|------|
| `name` | string | kebab-case, equals the folder name |
| `description` | string | starts with a verb or trigger noun; one trigger per branch; no "This skill" |
| `invocation` | `user` \| `model` | `user` = only reachable by `/name`; `model` = reachable by agent or human |
| `model` | `haiku` \| `sonnet` \| `opus` | routing hint for the phase that runs this skill |
| `reads` | list of strings | `.foundry/` artifacts or repo paths consumed; `[]` when none |
| `writes` | list of strings | artifacts produced; `[]` when none |
| `gate` | string | shell command that must exit 0 before the skill reports done |

## Frontmatter syntax accepted

The validator ships a minimal YAML subset parser (no PyYAML). Use only:

```yaml
key: scalar
key: [a, b, c]            # flow list on one line
key:
  - item                  # block list
key: "quoted string"
```

Nested mappings, anchors, multi-line strings and block mappings inside lists are outside the
subset. Keep frontmatter flat.

## Body rules

- At most 150 lines for the whole file, frontmatter included.
- `## Steps` numbered; each step's final line begins with `Done when:`.
- `## Reference` holds tables and short lists every branch needs.
- Disclosed reference lives in sibling files named by one pointer line, e.g.
  `Deeper: SKILL-MECHANICS.md`.

## Invocation edges

```
user-invoked  ──may call──▶  model-invoked
model-invoked ──never──▶     user-invoked
```

The orchestrators are `/foundry`, `/foundry-build`, `/foundry-resume`. Everything else is
model-invoked.
