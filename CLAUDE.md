# FOUNDRY — house style and repo conventions

Foundry is a Claude Code plugin: an autonomous app-engineering skill system. A founder types
`/foundry "I need a restaurant POS"` and receives a designed, architected, implemented, tested
app with at most 7 questions asked. Every file in this repo obeys the rules below.

## House style (adapted from mattpocock/skills "writing-for-agents")

1. **Two invocation classes.** `invocation: user` skills orchestrate; they are reachable only when
   a human types `/name`. `invocation: model` skills hold reusable discipline; agent or human may
   reach them. User-invoked may call model-invoked. Never the reverse.
2. **Description is a context pointer.** Front-load the trigger word. One trigger per distinct
   branch. No identity restatement ("This skill is..."). The description alone decides when the
   skill fires.
3. **Information hierarchy.** In-file steps, then in-file reference, then disclosed reference (a
   sibling file behind a pointer). Inline what every branch needs. Disclose what only some
   branches reach.
4. **Completion criteria.** Every step ends on a criterion that is checkable and exhaustive:
   "every entity has an invariant", never "understanding reached".
5. **Leading words over sentences.** Single pretrained concepts: tracer bullet, red/green,
   frontier, blast radius, single source of truth. Phrase positively. A prohibition appears only
   as a hard guardrail and always paired with the positive target.
6. **Single source of truth.** The environment is a source of truth: point at package.json, do not
   restate it. Prune no-ops: delete any sentence the model already obeys by default.
7. **Frontmatter is complete.** Every SKILL.md carries `name`, `description`, `invocation`,
   `model` (haiku|sonnet|opus hint), `reads` (.foundry/ artifacts consumed), `writes` (artifacts
   produced), `gate` (command that must pass before the skill reports done).
   Spec: skills/writing-for-agents/SKILL-MECHANICS.md.

## Repo conventions

- **SKILL.md is at most 150 lines.** Deeper material lives in sibling files reached by a pointer.
- **Windows-first.** Scripts are Python 3.11+ stdlib only. Every script has `foundry.ps1` and
  `foundry.sh` wrappers. Paths use `pathlib`; separators are never hard-coded.
- **Packs** are `packs/<slug>/pack.yaml` (restricted YAML subset, see packs/README.md) plus a
  `reference/` folder. `packs/index.csv` is the routing table.
- **Data** files are CSV under `data/`, queried by `scripts/foundry.py query` (P5+).
- **Schemas** are JSON Schema draft 2020-12 under `schemas/`; validate is the gate.
- **Artifacts** the pipeline produces live under `.foundry/` in the target app repo, never here.
- **Commits** are per deliverable group with imperative subject lines.
- **Code intelligence** comes from codebase-memory-mcp once code exists (graph before grep).
- **Subscription-only (hard rule, P10).** Foundry runs inside a logged-in Claude Code session and nowhere
  else: no API key is read, stored, checked by `doctor` or mentioned anywhere in this repo; no script
  invokes the CLI non-interactively; there is no headless mode. Model-needing evals are run by a human
  typing `/foundry-eval`; CI runs the deterministic stages only. A change that needs a key is rejected.

## Running validate

```
python scripts/foundry.py validate
python -m unittest scripts/test_foundry.py
```

Wrappers: `scripts/foundry.ps1 validate` and `scripts/foundry.sh validate`.

Validate checks: every skills/*/SKILL.md frontmatter against schemas/skill-frontmatter.schema.json,
line count at most 150, description starts with a verb or trigger noun, every packs/*/pack.yaml
against schemas/pack.schema.json, and the packs/index.csv header. Any failure prints
`file:line: message` and exits non-zero. CI runs the same command on every push.
