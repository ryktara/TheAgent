---
name: compliance
description: Map compliance for phase 9: every PRD §8 control and every applicable security control gets a status, an evidence method and, later, an owning ticket in .foundry/compliance.yaml.
invocation: model
model: haiku
reads: [.foundry/prd.md, .foundry/compliance.yaml, .foundry/threats.md, packs/<slug>/reference/compliance.md, data/security-controls.csv]
writes: [.foundry/compliance.yaml, .foundry/compliance-evidence-plan.md]
gate: python scripts/foundry.py gate security
---

# compliance — phase 9b

Every control has a status and an evidence method; owners arrive in phase 10. Runs after
threat-model on the same skeleton output.

## Steps

1. **Map pack controls to features.** For each `C-*` id in PRD §8, open only that row of
   `packs/<slug>/reference/compliance.md` and append `features: [<must_have ids>]` and
   `verification: <text>` to its entry in `.foundry/compliance.yaml`.
   Done when: every `C-*` entry carries features and verification.

2. **Set statuses.** `planned` for anything the tickets will build; `na` with a one-line reason
   for controls whose `applies_when` no longer holds (for example cash-only payments); `done`
   only with evidence attached.
   Done when: no entry lacks a status and every `na` has a reason.

3. **Evidence plan.** In `.foundry/compliance-evidence-plan.md`, each control names the test
   file, scan or review that will evidence it (verify column from security-controls.csv,
   made concrete: `apps/api/src/payments/refund.test.ts`, `semgrep ruleset`, `owner review`).
   Done when: every control row names a concrete artefact.

4. **Gate.**

   ```
   python scripts/foundry.py gate security
   ```

   Done when: the gate prints `pass` and `pci_scope` is set with its reason.

## Reference

| pci_scope | When |
|-----------|------|
| SAQ-A | hosted page or redirect online, semi-integrated terminal in person (default) |
| SAQ-A-EP | merchant page loads provider iframe or JS (avoid; requires ASV scans) |
| SAQ-D | direct card entry (forbidden by SEC-PAY-01) |
| na | no card payments |
