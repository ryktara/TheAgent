---
name: screen-spec
description: Specify every in-scope screen for phase 8 as .foundry/screens/<id>.md with wireframes, states, copy, bindings and accessibility rules; fan out one subagent per screen when there are more than 8.
invocation: model
model: sonnet
reads: [.foundry/prd.md, .foundry/domain.yaml, openapi.yaml, design-system/MASTER.md, packs/<slug>/reference/screens.md, data/components.csv, data/ux-rules.csv]
writes: [.foundry/screens/*.md]
gate: python scripts/foundry.py gate screens
---

# screen-spec — phase 8

Every job has a screen; every screen has six states with copy, real data bindings and rule
ids. The skeleton reads only the `## <screen-id>` section of the pack's screens.md per screen;
the model refines wireframes and copy.

## Steps

1. **Generate.**

   ```
   python scripts/foundry.py screens-skeleton
   ```

   Done when: `.foundry/screens/` holds one file per screen named in PRD §3 jobs and the
   command printed the screen and job counts.

2. **Refine per screen.** For each file: redraw the two ASCII wireframes from the layout
   zones (≤20 lines each), write the six state copies in English and Arabic (replace the
   `<!-- ar -->` placeholders; keep numerals Western), tighten the actions table to the
   components the screen truly uses, and fill open questions only when a decision is missing.
   When more than 8 screens exist, dispatch one subagent per screen with this return contract:
   the finished file path plus a summary of at most 10 lines, nothing else.
   Done when: no file contains `<!--` and every screen's wireframes match its layout zones.

3. **Bindings.** Every operationId under `data.reads` and `data.writes` exists in
   openapi.yaml; add the job operations a refined screen needs (for example `order_split_bill`
   on tender) and remove ones it does not.
   Done when: `gate screens` reports no unknown operationId.

4. **Gate.**

   ```
   python scripts/foundry.py gate screens
   ```

   Done when: the gate prints `pass`: every PRD job has a screen; every screen has six states
   with copy; every component, operationId and rule id exists; at least 3 a11y rule ids and,
   in RTL regions, at least 1 RTL rule per screen; routes unique.

## Reference

| Frontmatter field | Source |
|-------------------|--------|
| jobs, personas | PRD §3 jobs that list this screen |
| route | `/<screen-id>` (rename in refinement when the app router differs) |
| layout | product type nav pattern and density |
| components | components.csv ids matched from the screens.md section and screen id |
| data.reads / writes | openapi operations whose x-foundry.job is one of the screen's jobs, plus CRUD of the job entity |
| offline, print | from the screens.md section and pack must-haves |

Subagent prompt shape: "Refine `.foundry/screens/<id>.md` per skills/screen-spec/SKILL.md step 2;
return the path and ≤10 lines." Parent context never receives the file body.
