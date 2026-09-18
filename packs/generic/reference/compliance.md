# Generic pack — compliance baseline

Applies to every app built from this pack. Domain packs add controls; they never remove these.
Each control has an id, a requirement, and how it is verified. Sources: GDPR, UAE Federal
Decree-Law 45/2021 (PDPL), KSA PDPL (Royal Decree M/19), NIST SP 800-63B, OWASP ASVS 4.0.

## Privacy (GDPR / UAE PDPL / KSA PDPL common baseline)

| Id | Requirement | Verification |
|----|-------------|--------------|
| PRV-01 | Lawful basis recorded per personal-data category in `compliance.yaml` | file review |
| PRV-02 | Privacy notice shown at sign-up and linked in the footer | e2e test opens the notice |
| PRV-03 | Consent captured for optional processing (marketing, analytics) with timestamp | AuditEvent consent.given exists |
| PRV-04 | Data subject export within 30 days: implemented as self-service export | workflow 8 e2e |
| PRV-05 | Data subject deletion with 30-day grace, then erasure; audit retained pseudonymised | workflow 8 e2e |
| PRV-06 | Data residency: AE and SA tenants stored in-region or with documented transfer basis | ADR data-store names region |
| PRV-07 | Breach notification runbook: 72 h to regulator (GDPR, KSA), "as soon as practicable" (UAE) | runbook file exists |
| PRV-08 | Processor list (email, storage, payments) documented with DPAs | compliance.yaml processors |
| PRV-09 | Data minimisation: every personal field maps to a stated purpose | schema review |
| PRV-10 | Retention per data class with automatic purge job | job exists and is scheduled |

## Authentication and passwords (NIST 800-63B)

| Id | Requirement | Verification |
|----|-------------|--------------|
| AUT-01 | Minimum 8 characters, maximum at least 64, all printable Unicode allowed | unit test |
| AUT-02 | Check against a breached-password list; reject matches | unit test with known-bad value |
| AUT-03 | No composition rules (forced symbols) and no periodic forced rotation | policy review |
| AUT-04 | Rate limit: 5 failures per 15 min per account and per IP, then lockout 15 min | integration test |
| AUT-05 | Passwords hashed with Argon2id or bcrypt cost 12+ | code review |
| AUT-06 | Session tokens: httpOnly, secure, sameSite=lax; idle timeout 24 h; absolute 30 d | integration test |
| AUT-07 | Password reset links single-use, 30 min validity; reset revokes other sessions | integration test |
| AUT-08 | MFA available for owner and admin roles; enforced when payments enabled | e2e |
| AUT-09 | SSO tokens validated for issuer, audience, expiry, nonce | unit test |

## Authorisation

| Id | Requirement | Verification |
|----|-------------|--------------|
| AZ-01 | Every API endpoint declares its required permission; none default to open | api-contract gate |
| AZ-02 | Multi-tenant: RLS policies on every tenant-scoped table | schema gate |
| AZ-03 | Object-level checks on detail, edit, delete (no IDOR) | security-review |
| AZ-04 | Last owner cannot be removed or demoted | unit test |

## Audit log

| Id | Requirement | Verification |
|----|-------------|--------------|
| AUD-01 | Every create, update, delete, state change and permission change writes an AuditEvent | integration test |
| AUD-02 | AuditEvent fields: ts, actor, tenant, action, object type, object id, before, after, ip, user agent | schema |
| AUD-03 | Append-only: no update or delete permission on the audit table | db grant review |
| AUD-04 | Retained 1 year minimum; 5 years when financial records exist | retention config |
| AUD-05 | Exportable by owner; filterable by actor, object, date | e2e |

## Transport, secrets, dependencies

| Id | Requirement | Verification |
|----|-------------|--------------|
| SEC-01 | TLS 1.2+ everywhere; HSTS on | deploy config |
| SEC-02 | Secrets in the platform vault; none in source or logs | semgrep + secret scan |
| SEC-03 | Dependency audit in CI; high severity blocks merge | CI config |
| SEC-04 | Security headers: CSP, X-Content-Type-Options, Referrer-Policy, frame-ancestors | header test |
| SEC-05 | Uploads: type allow-list, size cap, virus scan when public | integration test |
| SEC-06 | Backups daily, encrypted, restore tested quarterly | runbook |
