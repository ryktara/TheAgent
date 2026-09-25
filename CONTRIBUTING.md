# Contributing to Foundry

Foundry is source-available (see LICENSE and the README licence note). Contributions are welcome
as issues and pull requests; by sending one you agree the owner may use it under the LICENSE terms.

## Where to start

- **A new domain pack** (the most useful contribution): docs/PACK-AUTHORING.md walks through
  `packs/<slug>/pack.yaml` (schema 2.0, `vocabulary:` block), the `reference/` folder, the routing
  row in `packs/index.csv`, the eval brief and expected outcome, and the de-domain grep gate.
- **Running the pipeline as an orchestrator** (how steps are planned, gated and reported):
  docs/ORCHESTRATOR.md.
- **House style for skills and scripts:** CLAUDE.md. SKILL.md is at most 150 lines; scripts are
  Python 3.11+ stdlib only and Windows-first; subscription-only, no API key anywhere.

## Before you open a pull request

```
python scripts/foundry.py validate
python -m unittest scripts/test_foundry.py
python hooks/test_hooks.py
python evals/run.py
```

All four must pass (CI runs them on windows-latest and ubuntu-latest). A `fix:` commit carries a
one-line reason in CHANGELOG.md. Model-needing evals (`/foundry-eval`) are run by a human in a
Claude Code session; paste the `evals/results/` summary line in the PR.
