# SYNC-RULES — offline/REST parity checklist (cite rule ids in findings)

Every transition an offline device can produce arrives as a sync event and is applied server-side
(`apps/api/src/sync/*`). The REST operation for the same transition exists for online callers.
Both paths obey the same rules; a finding cites the rule id and the path that breaks it.

| Id | Rule | Check |
|----|------|-------|
| SYNC-01 | Same role guard | the sync branch reads the role from the staff session on the push (`actor.role`), never from the payload; the allowed set equals the REST `requireRole` set (owner implied) |
| SYNC-02 | Server-owned fields stripped | `SERVER_OWNED` keys (money, branch_id, device_seq, receipt_number) are removed from `fields` before merge and reported as conflicts |
| SYNC-03 | Money recomputed | any event that changes lines reprices from the catalogue/tax rule (`priceLines`), never trusts client totals; discounts and service charges only through their own guarded transition |
| SYNC-04 | Idempotency | `(device_id, seq)` unique; a replay returns the stored ack; the batch Idempotency-Key replays the whole response |
| SYNC-05 | Audit event | every applied transition writes `audit_events` with `actor_id`, `device_id`, `entity`, `entity_id` and `offline: true` in the same transaction |
| SYNC-06 | State guard | the transition is applied only from the states the domain allows (DRAFT→SENT, SENT→VOID by merge, BUMPED→RECALLED within the window); other states produce a conflict, not a silent no-op |
| SYNC-07 | Derived data never client-supplied | work-queue ticket lines, receipt numbers, board state come from server data; client copies are ignored |
| SYNC-08 | Approver on the push | manager-gated actions (transfer, void/comp, recall after the window, discount over limit) require a manager/owner session on the push or an approver id resolved server-side; a client-sent role or flag is never an approval |
| SYNC-09 | Unhandled means refused | an action the sync store does not implement returns a conflict naming the REST operation to use; it is never merged as generic fields |
| SYNC-10 | Test parity | the integration suite has one assertion per offline transition: the refused case and the applied case with its audit row |

Blocking when SYNC-01, 02, 03, 07 or 08 fail; nonblocking for 04–06, 09, 10 unless money or roles are involved.
