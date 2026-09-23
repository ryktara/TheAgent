---
name: foundry-eval
description: Run the model-needing evals inside this Claude Code session (no API key, no headless mode): --stage triggers scores which skill fires for 40 prompts; --stage e2e runs /foundry unattended, gates 0–10, /foundry-build --n 2 and the release smoke in a temp dir against evals/thresholds.yaml.
invocation: user
model: sonnet
reads: [evals/triggers.csv, evals/thresholds.yaml, evals/briefs/restaurant-pos.md]
writes: [evals/results/triggers-<date>.json, evals/results/e2e-<date>.json]
gate: python evals/run.py --stage results
---

# /foundry-eval — model stages, run by a human in a session

Argument: `--stage triggers` or `--stage e2e` (default: both). Everything deterministic lives
in `python evals/run.py`; this skill supplies the model judgement and hands the result to the
script for scoring. Foundry has no API-key path and no headless runner by design: CI runs the
deterministic stages only, and the two stages below are run by a person typing `/foundry-eval`.

## Steps

1. **Triggers.** Print the prompts only (never the expected column):

   ```
   python -c "import csv;[print(repr(r['prompt'])) for r in csv.DictReader(open('evals/triggers.csv',encoding='utf-8'))]"
   ```

   For each prompt decide, from the skill descriptions in `skills/*/SKILL.md` frontmatter alone,
   which `invocation: user` skill you would invoke, or `none`. Write `evals/results/answers.json`
   as `{"<prompt>": "<skill|none>"}` with every prompt, then score:

   ```
   python evals/run.py --score-triggers evals/results/answers.json --model <your model id>
   ```

   Done when: `evals/results/triggers-<date>.json` exists and the score line printed pass
   (≥ `trigger_accuracy_min`); on FAIL list the misses verbatim in the report.

2. **E2E.** In a fresh temp directory (`git init`), run `/foundry --unattended` on
   `evals/briefs/restaurant-pos.md` exactly as the foundry skill says (phases 0–10, zero
   questions), note the wall seconds; then `/foundry-build --n 2` (scaffold + first feature
   through ticket-builder and ticket-finisher), note its wall seconds; then `release-skeleton`
   and `gate release`. Assert and record:

   ```
   python evals/run.py --assert-e2e <temp dir> --phases-wall <s> --build-wall <s> --pack restaurant-pos
   ```

   Done when: `evals/results/e2e-<date>.json` exists; every gate 0–10 passed, questions asked
   0, ticket count inside the band, T-000 and T-001 DoD green, per-ticket ceilings held, or each
   failing line is listed in the report.

3. **Thresholds.** When both stages pass and the medians moved, refresh the ceilings:

   ```
   python evals/run.py --update-thresholds --project <temp dir>
   ```

   Done when: `evals/thresholds.yaml` `as_of` is today, or the ceilings were left as they were
   with the reason stated.

4. **Report** (≤10 lines): trigger score with misses, e2e verdict with the failing lines,
   thresholds touched or not, the two results file names.
   Done when: the report is sent and `python evals/run.py --stage results` prints pass.

## Reference

| File | Holds |
|------|-------|
| evals/triggers.csv | 40 prompts with the expected skill (read by the scorer, not by you) |
| evals/thresholds.yaml | skeleton wall budgets and e2e ceilings (+25% over the last measured medians) |
| evals/results/ | dated JSON written by the scorer; `--stage results` reads the newest pair |
