---
name: ui-review
description: Review a ticket's screens as a subagent from screenshots, screen specs and axe results, returning a fixed JSON verdict to .foundry/reviews/T-xxx.ui.json.
invocation: model
model: haiku
reads: [.foundry/reviews/T-xxx.pack.md, .foundry/reviews/T-xxx.diff, .foundry/screenshots/T-xxx/, .foundry/tickets/T-xxx.status.yaml]
writes: [.foundry/reviews/T-xxx.ui.json]
gate: python -c "import json,sys;d=json.load(open(sys.argv[1]));sys.exit(0 if d.get('verdict') in ('pass','fail') else 1)" .foundry/reviews/T-xxx.ui.json
---

# ui-review — phase 12 (subagent)

Screens judged against their spec and the design system, with the screenshots as evidence.

## Steps

1. **States.** For each screen in the ticket, confirm the six states (empty, loading, error,
   offline, locked, success) exist in the implementation and match the spec copy ids.
   Done when: each state per screen has a finding or "ok".

2. **Tokens and components.** Grep the diff for raw hex or px values where a token exists
   (`--color-*`, `--space-*`, `--radius-*`, `--touch-min`); confirm components use the
   inventory names from MASTER.md and shadcn names from components.csv.
   Done when: no raw hex remains where a token exists, or each case is a finding.

3. **Screenshots.** Open `.foundry/screenshots/T-xxx/<screen>-{light,dark}-{ltr,rtl}.png`:
   RTL mirrors layout while numerals, prices and numpads stay LTR; dark theme uses dark tokens;
   touch targets look ≥ 48 px; amounts right-aligned.
   Done when: each of the four shots per screen has a finding or "ok".

4. **Axe.** Read the a11y-axe step tail in `T-xxx.status.yaml`; serious or critical
   violations are blocking.
   Done when: the axe result is reflected in the verdict.

5. **Return.** Write `.foundry/reviews/T-xxx.ui.json` and reply with that JSON only:
   `{"ticket", "verdict": "pass|fail", "blocking": [{file, line, issue, fix}], "nonblocking": [...]}`, at most 400 tokens.
   Done when: the file exists and the reply is the JSON.

## Reference

Blocking: missing state, raw hex where a token exists, RTL not mirrored, serious axe violation,
touch target under 48 px on an operational screen. Non-blocking: spacing rhythm, copy tone,
icon choice.

## Inputs (P10)

The subagent receives three things: this skill's SKILL.md path, the project root and the review pack
(`.foundry/reviews/T-xxx.pack.md`, a header of at most 600 tokens: acceptance tests, operations with authz,
controls, changed files; `.foundry/reviews/T-xxx.diff`: the diff plus new files). Read those two files
first; open another file only to verify a finding, at most three. Reply with the findings JSON only.
On a re-review the pack header says `re-review: hunks since <sha>` and lists your previous blocking items:
judge only those hunks and that list; areas that passed stay passed. Every blocking item carries `file`,
`line` and a concrete `fix` so the finisher applies it without re-reading the codebase.
