---
name: wizard
description: Wizard for a human-only prerequisite (secret, third-party account, DNS, store listing, paid service): write .foundry/wizard/<slug>.md with exact steps and generate .ps1/.sh scripts that prompt, validate, write .env.local and verify; the ticket continues behind a feature flag.
invocation: model
model: sonnet
reads: [.foundry/tickets/T-xxx.md, .foundry/adr/0006-integrations-boundary.md, .env.example]
writes: [.foundry/wizard/<slug>.md, .foundry/wizard/<slug>.ps1, .foundry/wizard/<slug>.sh, .env.example]
gate: python scripts/foundry.py wizard status
---

# wizard — phase 13 (human-only steps)

Triggered by implement-ticket when a ticket cannot finish without something only a human can
obtain. The wizard is a contract: why, exact steps, what to paste back, how it is validated.
Secrets never enter the repo: `.env.local` is git-ignored and `bash_guard` refuses writes to it.

## Steps

1. **Name the prerequisite.** One slug per provider or account (`payments-network-intl`,
   `dns-production`, `apple-store-listing`). List every variable the code will read, its
   format as a regex, and the validation command that proves the values work (a sandbox call,
   a DNS lookup, a signed test webhook).
   Done when: slug, `--var NAME:description:regex` list and `--validate` command are fixed.

2. **Scaffold.**

   ```
   python scripts/foundry.py wizard scaffold --slug <slug> --ticket T-xxx --why "<one sentence>" \
     --var API_KEY:"Sandbox API key":"^[A-Za-z0-9_-]{20,}$" --var WEBHOOK_SECRET:"Webhook signing secret":"^.{16,}$" \
     --validate "node scripts/verify-<slug>.mjs" --step "Sign in at …" --step "Create sandbox keys under …"
   ```

   Done when: `.foundry/wizard/<slug>.md`, `.ps1` and `.sh` exist.

3. **Make the steps exact.** Edit the md: where to click (screen names, not screenshots), which
   plan or sandbox mode, what each value looks like, and the validation command's expected
   output. Add every variable to `.env.example` with a placeholder and a comment.
   Done when: a person with the provider account can finish in one sitting without asking.

4. **Write the validation script** named in `--validate`: it reads the variables from the
   environment, makes one harmless call (sandbox balance, DNS TXT lookup, signature check) and
   exits non-zero with a one-line reason on failure.
   Done when: the script exists and fails cleanly when the variables are missing.

5. **Stub behind a flag.** The adapter interface ships with a stub implementation selected when
   the variables are absent (`FEATURE_<SLUG>=off` default); the real module is wired but idle.
   Tests run against the stub; a contract test tagged `@live` runs only when the values exist.
   Done when: the ticket's DoD passes with the stub and `wizard status` lists the slug as pending.

6. **Report** (≤6 lines): slug, variables, validation command, what stays stubbed, the command
   the human runs.
   Done when: the report is sent.

## Reference

| Trigger | Typical variables | Validation |
|---------|-------------------|------------|
| payment provider | API key, webhook secret, merchant id | sandbox `GET /balance` + signed test webhook |
| e-invoicing / fiscal | certificate, client id, secret | sign a sample invoice in the sandbox |
| DNS / TLS | domain, DNS API token | `nslookup` TXT record, ACME dry run |
| store listing | developer account id, team id | CLI `whoami` against the store API |
| paid service (maps, SMS) | API key | one metered call with a known answer |

`wizard status` is `done` when every variable is present in `.env.local`; the release gate
lists pending wizards in the runbook.
