---
name: bounded-grilling
description: Ask the founder the bounded question set for phase 2 and write the decision ledger. Run unattended when FOUNDRY_UNATTENDED=1 or the brief asked for no questions.
invocation: model
model: sonnet
reads: [.foundry/brief.md, .foundry/pack.yaml, packs/<slug>/pack.yaml]
writes: [.foundry/decisions.yaml]
gate: python scripts/foundry.py gate grill
---

# bounded-grilling — phase 2

Packs answer first, humans answer last. The question list is computed, never improvised.
Budget: 7 in round 1, 3 in round 2, 0 after. Every entry lands in the ledger through `decide`.

## Steps

1. **Seed the ledger from the brief.**

   ```
   python scripts/foundry.py decide --apply-prefilled
   ```

   Done when: `.foundry/decisions.yaml` exists with one `source: brief` entry per prefilled
   question.

2. **Unattended branch.** When `FOUNDRY_UNATTENDED=1`, `/foundry --unattended` was used, or
   `.foundry/pack.yaml` carries flag `no-questions-requested`:

   ```
   python scripts/foundry.py decide --auto-unattended
   ```

   then continue at step 7. Confirms keep the prefilled value; everything else takes the pack
   default; all such entries carry `source: timeout-default`.
   Done when: ledger `mode` is `unattended` and step 7 is next.

3. **Plan round 1.**

   ```
   python scripts/foundry.py grill-plan --round 1 --json
   ```

   Facts are the agent's job: for any planned question answerable from the brief, an attached
   repo, or an existing config, write the answer with `--source agent-fact --rationale "<where
   it was found>"` and drop it from the list.
   Done when: the remaining list holds only questions no artifact can answer.

4. **Ask round 1 in ONE message.** Design-tree format, one block per question, in plan order:

   ```
   ❓ Q<n> — <id>: <ask>
      choices: a | b | c            (choice questions only)
   ➡️ recommended: <default> — <one line: why the pack recommends it>
   ```

   Use the AskUserQuestion tool when available (one question per entry, default first and
   marked recommended); plain text otherwise. Then record every answer:

   ```
   python scripts/foundry.py decide --id <id> --value <v> --source human --round 1
   ```

   Silence or "use the default" on a question → same command with `--source timeout-default`.
   Done when: every round-1 question id has a ledger entry and `grill-plan --round 1` is empty.

5. **Rematch when generic.** When `.foundry/pack.yaml` `chosen` is `generic`, after round 1:

   ```
   python scripts/foundry.py match --brief .foundry/brief.md --rematch --write
   ```

   The product-summary answer is appended to the brief and rescored. When a domain pack now
   clears its threshold the selection carries flag `rematched`; the ledger restarts for the
   new pack (mode kept, round-1 count kept): run `decide --apply-prefilled` again, then
   `grill-plan --round 1` for the new pack's confirms and remaining budget.
   Done when: `chosen` is a domain pack or the rematch left `generic` in place.

6. **Round 2, once.** `grill-plan --round 2 --json`; when non-empty, repeat step 4 with
   `--round 2`. Round 2 is asked at most once.
   Done when: `grill-plan --round 2` is empty.

7. **Close the frontier.**

   ```
   python scripts/foundry.py decide --apply-defaults
   python scripts/foundry.py gate grill
   ```

   `apply-defaults` resolves `derive_from` questions from their parent answer with
   `source: agent-fact` and takes the pack default for the rest.
   Done when: rounds 1 and 2 both return no questions, `decisions.yaml` validates, the ledger
   has an entry for every question id in the pack, and the gate prints `pass`.

## Reference

| `why` in plan | Meaning | Ledger source when answered |
|---------------|---------|-----------------------------|
| confirm-prefill | brief implied an irreversible answer; founder confirms or overrides | human |
| pack-rank | next unanswered question by pack rank | human or timeout-default |
| followup | unlocked by a round-1 answer via `followups` | human or timeout-default |

Value syntax for `--value`: choice ids as written in the plan, `true`/`false` for bool, plain
numbers, free text in quotes. `decide` rejects a choice outside the list.
