---
name: foundry-continue
description: Continue a Foundry run from any passed gate through phase 10; alias of /foundry-resume kept for older runs.
invocation: user
model: opus
reads: [.foundry/prd.md, .foundry/decisions.yaml, .foundry/pack.yaml]
writes: []
gate: python scripts/foundry.py gate prd
---

# /foundry-continue — alias

/foundry-resume owns phases 0–10; this command delegates to it.

## Steps

1. **Delegate.** Run the /foundry-resume steps unchanged.
   Done when: /foundry-resume's report is printed.
