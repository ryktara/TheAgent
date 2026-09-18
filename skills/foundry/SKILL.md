---
name: foundry
description: Build an app from a one-line brief. Run phases 0–3 (intake, pack match, bounded grill, PRD) with at most 7 questions; use --unattended for zero questions; continue with /foundry-continue; resume with /foundry-resume.
invocation: user
model: opus
reads: [brief]
writes: [.foundry/brief.md, .foundry/pack.yaml, .foundry/decisions.yaml, .foundry/prd.md, .foundry/metrics.jsonl]
gate: python scripts/foundry.py gate prd
---

# /foundry — orchestrator, phases 0–3

Argument: the brief in quotes, optionally followed by `--unattended`. Run every command from
the project root (the folder that will hold the app); `scripts/foundry.py` resolves to the
plugin. Phases 4–10 are P4+ pointers: docs/pipeline.md.

## Steps

0. **Intake.** Create `.foundry/`, write the brief verbatim to `.foundry/brief.md` under a
   `# Brief` heading, create an empty `.foundry/metrics.jsonl`. With `--unattended`, export
   `FOUNDRY_UNATTENDED=1` for every later command.

   ```
   python scripts/foundry.py metrics --phase 0 --start
   python scripts/foundry.py gate 0
   python scripts/foundry.py metrics --phase 0 --note "brief captured"
   ```

   Done when: gate 0 prints `pass`.

1. **Pack match.** `metrics --phase 1 --start`; invoke the pack-match skill; then
   `gate 1`; `metrics --phase 1 --note "<slug> <confidence> <chosen_by>"`.
   Done when: gate 1 prints `pass`.

2. **Bounded grill.** `metrics --phase 2 --start`; invoke the bounded-grilling skill; then
   `gate 2`; `metrics --phase 2 --note "asked <n>/7 + <m>/3, mode <attended|unattended>"`.
   Done when: gate 2 prints `pass`.

3. **PRD.** `metrics --phase 3 --start`; invoke the prd skill; then `gate 3`;
   `metrics --phase 3 --note "prd <n> assumptions"`.
   Done when: gate 3 prints `pass`.

4. **Retry rule.** A failing gate re-runs that phase's skill once with the gate output as the
   fix list. A second failure stops the run; print the gate output verbatim.
   Done when: every phase passed, or the run stopped with the failing gate printed.

5. **Report.** Final message to the human, six lines at most:

   ```
   Pack: <slug> (confidence <c>, chosen by <chosen_by>)
   Questions: <round1_used>/7 + <round2_used>/3, mode <mode>
   Assumptions: <count of pack-default + timeout-default entries> (see prd.md section 10)
   PRD: .foundry/prd.md
   Next: /foundry-continue
   ```

   Done when: the message is sent and nothing else follows it.

## Reference

| Phase | Skill | Gate | Artifact |
|------:|-------|------|----------|
| 0 | (inline) | `gate 0` | .foundry/brief.md |
| 1 | pack-match | `gate 1` | .foundry/pack.yaml |
| 2 | bounded-grilling | `gate 2` | .foundry/decisions.yaml |
| 3 | prd | `gate 3` | .foundry/prd.md |
| 4–10 | P4+ | docs/pipeline.md | |

Ledger counts for the report come from `.foundry/decisions.yaml` (`budget`, `mode`, and
`source` values). Assumption count = entries whose source is `pack-default` or
`timeout-default`.
