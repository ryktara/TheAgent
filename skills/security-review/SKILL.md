---
name: security-review
description: Review a ticket's diff against its security controls as a subagent (authz, idempotency, audit, validation, secrets, semgrep), returning a fixed JSON verdict to .foundry/reviews/T-xxx.sec.json.
invocation: model
model: sonnet
reads: [.foundry/tickets/T-xxx.md, .foundry/reviews/T-xxx.changes.json, .foundry/threats.md, .foundry/compliance.yaml, data/security-controls.csv, .foundry/tickets/T-xxx.status.yaml]
writes: [.foundry/reviews/T-xxx.sec.json]
gate: python -c "import json,sys;d=json.load(open(sys.argv[1]));sys.exit(0 if d.get('verdict') in ('pass','fail') else 1)" .foundry/reviews/T-xxx.sec.json
---

# security-review — phase 12 (subagent)

Controls first. Every control id on the ticket is checked against the diff; the threat model's
authz matrix row for each operation is the expectation.

## Steps

1. **Controls.** For each id in the ticket's `controls`, run
   `python scripts/foundry.py query security-controls --id <id>` and verify the diff meets the
   control per its `verify` column (test present, review evidence, or scan clean).
   Done when: every control has a finding or "ok".

2. **Operations.** For each operationId: authz rule from threats.md enforced server-side;
   Idempotency-Key required on money and create POSTs; audit event written with actor and
   approver where the matrix says audit yes; request body validated with a schema that rejects
   unknown fields; no server-owned field accepted from the client.
   Done when: every operation has a finding or "ok".

3. **Secrets and scans.** No secrets, provider keys or card data patterns in the diff; the
   semgrep step tail in `T-xxx.status.yaml` shows no findings (or the step was skipped, noted
   as non-blocking).
   Done when: secrets and semgrep each have a finding or "ok".

4. **Return.** Write `.foundry/reviews/T-xxx.sec.json` and reply with that JSON only:
   `{"ticket", "verdict": "pass|fail", "blocking": [{file, line, issue, fix}], "nonblocking": [...]}`, at most 400 tokens.
   Done when: the file exists and the reply is the JSON.

## Reference

Blocking: authz missing or weaker than the matrix, no idempotency on money POST, audit missing,
unknown fields accepted, secret in diff, card data pattern, semgrep error-level finding.
Non-blocking: semgrep skipped, missing rate limit on a non-money route, log verbosity.
