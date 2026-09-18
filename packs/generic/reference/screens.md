# Generic pack — screens

Every screen carries four states: empty, loading, error, populated. Every list screen has
search, filter, sort, pagination and bulk select. Every form has inline validation, a dirty
guard and a keyboard-submittable primary action.

## auth

| Sub-screen | Purpose | Key elements | States |
|------------|---------|--------------|--------|
| sign-in | Enter the app | email, password, "forgot password", SSO buttons when enabled | error: wrong credentials, locked, unverified |
| sign-up / accept-invite | Join a tenant | name, email, password strength meter, invite token | error: expired invite |
| forgot / reset | Recover access | email; then new password twice | success: redirect to sign-in |
| verify-email | Confirm ownership | 6-digit code or link | resend with 60s cooldown |
| mfa (optional) | Second factor | TOTP code, recovery codes | error: wrong code, rate-limited |

Data bindings: User, Session. Analytics: sign_in_success, sign_in_failure(reason).

## dashboard

- Header: tenant switcher (multi-tenant only), global search, notifications bell, avatar menu.
- KPI row: four stat tiles derived from Record counts by state and time window.
- Activity feed: last 20 AuditEvents with actor, verb, object, relative time.
- Quick actions: "New record", "Run report", role-gated.
- Empty state on first login explains the three things to do first.

## list

- Table with sticky header, column chooser, saved views, row density toggle.
- Toolbar: search (debounced 250 ms), filter chips, sort, export CSV, bulk actions.
- Row click opens detail; checkbox enables bulk; keyboard: j/k move, enter open.
- Pagination: cursor-based, 25 rows default, page size selector.
- Empty: illustration plus "Create your first record" and "Import CSV".

## detail

- Header: title, state badge, primary action (state transition), overflow menu.
- Tabs: Overview, Activity (AuditEvents for this record), Files, Related.
- Side panel: metadata (created by, updated by, owner, tags).
- Danger zone at the bottom: archive, delete (role-gated, confirm by typing the name).

## edit

- Sections with sticky section nav on wide screens.
- Field types: text, long text, number, money, date, select, multi-select, toggle, file.
- Validation: inline on blur, summary on submit, server errors mapped to fields.
- Autosave draft every 10 s for long forms; explicit Save publishes.
- Unsaved-changes guard on navigation.

## settings

| Tab | Contents |
|-----|----------|
| Profile | name, email, avatar, password change, sessions list with revoke |
| Organisation | name, logo, locale, timezone, currency, tax id |
| Users & roles | invite, role assignment, disable, resend invite |
| Roles | matrix of permissions per role; custom roles when enabled |
| Billing (when payments) | plan, invoices, payment method via hosted fields |
| Integrations | connect, disconnect, status, last sync |
| Data | export all, request deletion, retention settings |
| Audit log | filterable AuditEvent table, export |

## reports

- Report picker: predefined reports plus saved custom reports.
- Parameters panel: date range presets, group by, filters.
- Output: table and one chart; export CSV, XLSX, PDF.
- Scheduling: email a report daily/weekly to chosen users.
- Long-running reports run async with a progress indicator and notification on completion.

## notifications

- Bell dropdown with unread count, mark all read, link to full page.
- Preferences per channel (in-app, email) per event type.

## users-roles

- Users table: name, email, role, status, last active; invite button; row actions resend, disable.
- Roles tab: permission matrix (rows permissions, columns roles); custom roles when enabled.
- Guard: the last owner cannot be demoted or disabled.
- States: empty (invite your first teammate), loading skeleton, error retry.

## audit-log

- AuditEvent table: time, actor, action, object, before/after diff on expand.
- Filters: actor, object type, action, date range; export CSV.
- Append-only; no edit or delete actions exist on this screen.
- States: empty (no activity yet), loading, error.
