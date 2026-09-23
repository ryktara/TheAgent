---
name: foundry
description: Build an app from a one-line brief. Run phases 0–10 (intake through threat model, compliance and tickets) with at most 7 questions; use --unattended for zero questions; continue with /foundry-continue; resume with /foundry-resume.
invocation: user
model: opus
reads: [brief]
writes: [.foundry/brief.md, .foundry/pack.yaml, .foundry/decisions.yaml, .foundry/prd.md, .foundry/domain.yaml, CONTEXT.md, .foundry/architecture.md, .foundry/adr/*.md, prisma/schema.prisma, openapi.yaml, .foundry/events.yaml, design-system/MASTER.md, design-system/tokens.json, .foundry/screens/*.md, .foundry/threats.md, .foundry/compliance.yaml, .foundry/tickets/*.md, .foundry/metrics.jsonl]
gate: python scripts/foundry.py gate tickets
---

# /foundry — orchestrator, phases 0–10

Argument: the brief in quotes, optionally followed by `--unattended`. Run every command from
the project root (the folder that will hold the app); `scripts/foundry.py` resolves to the
plugin. Implementation (phases 11–15) runs under /foundry-build.

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

1. **Pack match.** `metrics --phase 1 --start`; invoke pack-match; `gate 1`;
   `metrics --phase 1 --note "<slug> <confidence> <chosen_by>"`.
   Done when: gate 1 prints `pass`.

2. **Bounded grill.** `metrics --phase 2 --start`; invoke bounded-grilling; `gate 2`;
   `metrics --phase 2 --note "asked <n>/7 + <m>/3, mode <mode>"`.
   Done when: gate 2 prints `pass`.

3. **PRD.** `metrics --phase 3 --start`; invoke prd; `gate 3`;
   `metrics --phase 3 --note "prd <n> assumptions"`.
   Done when: gate 3 prints `pass`.

4. **Doctor, then domain model.** `python scripts/foundry.py doctor` (stop on FAIL and print
   the table). `metrics --phase 4 --start`; invoke domain-model; `gate 4`;
   `metrics --phase 4 --note "<entities> entities, <transitions> transitions"`.
   Done when: doctor is ok and gate 4 prints `pass`.

5. **Architecture.** `metrics --phase 5 --start`; invoke architecture; `gate 5`;
   `metrics --phase 5 --note "9 ADRs; CBM <present|absent>"`.
   Done when: gate 5 prints `pass`.

6. **Data and API.** `metrics --phase 6 --start`; invoke data-model, then api-contract;
   `gate 6`; `metrics --phase 6 --note "<models> models, <operations> operations"`.
   Done when: gate 6 prints `pass`.

7. **Design system.** `metrics --phase 7 --start`; invoke design-system; `gate 7`;
   `metrics --phase 7 --note "palette <id>, design-check ok"`.
   Done when: gate 7 prints `pass`.

8. **Screen specs.** `metrics --phase 8 --start`; invoke screen-spec; `gate 8`;
   `metrics --phase 8 --note "<n> screens"`.
   Done when: gate 8 prints `pass`.

9. **Threat model and compliance.** `metrics --phase 9 --start`; invoke threat-model, then
   compliance; `gate 9`; `metrics --phase 9 --note "pci <scope>, <n> controls, top risk <id>"`.
   Done when: gate 9 prints `pass`.

10. **Tickets.** `metrics --phase 10 --start`; invoke to-tickets; `gate 10`;
    `metrics --phase 10 --note "<n> tickets"`. A `regulated: true` pack also gets the
    regulator-licence wizard here (`wizard status` lists it; release stays blocked until a human confirms).
    Done when: gate 10 prints `pass`.

11. **Retry rule.** A failing gate re-runs that phase's skill once with the gate output as the
   fix list. A second failure stops the run; print the gate output verbatim.
   Done when: every phase passed, or the run stopped with the failing gate printed.

12. **Report.** Final message to the human, ten lines at most:

   ```
   Pack: <slug> (confidence <c>, chosen by <chosen_by>)
   Questions: <round1_used>/7 + <round2_used>/3, mode <mode>
   Assumptions: <count of pack-default + timeout-default entries> (prd.md §10)
   Model: <entities> entities, 9 ADRs, <operations> API operations
   Design: palette <id>, design-check <ok|n issues>, <screens> screens
   Security: pci_scope <scope>; top risks <id1>, <id2>, <id3>
   Tickets: <n> (next: T-000)
   Artifacts: .foundry/prd.md, domain.yaml, architecture.md, openapi.yaml, design-system/MASTER.md, .foundry/screens/, threats.md, compliance.yaml, tickets/
   Run /foundry-build to implement.
   ```

   Done when: the message is sent and nothing else follows it.

## Reference

| Phase | Skill | Gate | Artifact |
|------:|-------|------|----------|
| 0 | (inline) | `gate 0` | .foundry/brief.md |
| 1 | pack-match | `gate 1` | .foundry/pack.yaml |
| 2 | bounded-grilling | `gate 2` | .foundry/decisions.yaml |
| 3 | prd | `gate 3` | .foundry/prd.md |
| 4 | domain-model | `gate 4` | .foundry/domain.yaml, CONTEXT.md |
| 5 | architecture | `gate 5` | .foundry/architecture.md, .foundry/adr/ |
| 6 | data-model, api-contract | `gate 6` | prisma/schema.prisma, openapi.yaml, .foundry/events.yaml |
| 7 | design-system | `gate 7` | design-system/MASTER.md, tokens.json |
| 8 | screen-spec | `gate 8` | .foundry/screens/*.md |
| 9 | threat-model, compliance | `gate 9` | .foundry/threats.md, compliance.yaml |
| 10 | to-tickets | `gate 10` | .foundry/tickets/*.md |

Counts for the report: ledger `budget` and `source` values; entity count from domain.yaml;
operations = methods under `paths` in openapi.yaml; screens = files under .foundry/screens/; top risks from threats.md "Top 10 risks"; tickets = files under .foundry/tickets/.
