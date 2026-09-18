# Generic pack — workflows

Each workflow names its persona, trigger, steps, terminal states and the AuditEvents it must
produce. Steps marked (S) run on the server without user interaction.

## 1. Tenant bootstrap (owner)

Trigger: first sign-up.
1. Owner creates account with email and password.
2. (S) Verification email sent; account stays `invited` until verified.
3. Owner verifies; Tenant is created in `trial`; owner gets role `owner`.
4. Owner completes organisation settings: name, locale, timezone, currency.
5. Dashboard shows the onboarding checklist: invite a user, create a record, run a report.
Terminal: Tenant `active` once the first record exists or a plan is chosen.
Audit: tenant.created, user.verified, settings.updated.

## 2. Invite and onboard a user (admin → staff)

1. Admin enters email and picks a role.
2. (S) Invite token issued, expires in 7 days; invite email sent.
3. Invitee opens the link, sets name and password, accepts.
4. User becomes `active`; admin is notified.
5. Expired invites can be resent; an accepted invite cannot be reused.
Audit: user.invited, user.accepted, user.role_changed.

## 3. Create and progress a record (staff)

1. Staff opens "New record", fills required fields; draft autosaves.
2. Save validates on client and server; Record enters `draft`.
3. Staff or a permitted role transitions `draft → active`.
4. Edits on an `active` record write a full before/after diff to AuditEvent.
5. When work is complete, the record is archived and becomes read-only.
Invariant checks on every transition; rejected transitions return the violated invariant.
Audit: record.created, record.updated, record.state_changed.

## 4. Search, filter and bulk action (staff)

1. Type a query; results update after 250 ms debounce; the URL holds the query state.
2. Add filter chips; save the view with a name for reuse.
3. Select rows; choose a bulk action (change state, assign, export, archive).
4. (S) Bulk actions run as a job; a progress toast reports counts; failures are listed per row.
Audit: one AuditEvent per affected record plus one job.summary event.

## 5. Run and schedule a report (manager)

1. Pick a report; set date range and grouping.
2. Reports over 5 000 rows run async; the user is notified on completion.
3. Export in CSV, XLSX or PDF; the file link expires after 24 h.
4. Optionally schedule: cadence, recipients, format.
Audit: report.ran, report.exported, report.scheduled.

## 6. Role and permission change (admin)

1. Admin opens Roles; edits the permission matrix or assigns a role.
2. (S) Changes apply on the next request; active sessions of affected users refresh claims.
3. Removing the last `owner` is refused.
Audit: role.updated, user.role_changed.

## 7. Password reset and account lockout (any user)

1. Five failed sign-ins in 15 minutes lock the account for 15 minutes.
2. "Forgot password" sends a single-use link valid for 30 minutes.
3. Reset invalidates every other session for that user.
Audit: auth.locked, auth.reset_requested, auth.reset_completed, session.revoked.

## 8. Data export and deletion request (owner)

1. Owner requests a full export; (S) a job builds a zip of CSVs and files.
2. Download link is emailed; it expires in 7 days.
3. Deletion request starts a 30-day grace period; the Tenant moves to `suspended`.
4. After the grace period, (S) personal data is erased; AuditEvents are retained pseudonymised.
Audit: data.export_requested, data.export_ready, tenant.deletion_requested, tenant.deleted.

## 9. Notification delivery (system)

1. A domain event creates a Notification in `pending`.
2. (S) Dispatcher respects user preferences per channel and quiet hours.
3. In-app delivery marks `sent`; opening marks `read`; email failures retry three times.
Audit: notification.sent, notification.failed.
