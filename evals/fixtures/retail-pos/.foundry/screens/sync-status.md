---
id: "sync-status"
jobs: ["offline-sync"]
personas: ["cashier"]
route: "/sync-status"
routes: [{path: "/sync-status"}]
layout: "action-bar / high density"
components: ["badge", "banner-offline", "button", "empty-state", "skeleton", "toast", "virtual-list"]
data:
  reads: ["sync_event_get", "sync_event_list", "sync_pull"]
  writes: ["sync_event_offline_sync", "sync_push"]
  events: []
offline: true
print: false
---

# sync-status

## Purpose

Offline queue, last sync, conflicts

Role access: cashier.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| Sync status   [badge: Offline / Synced]   Last sync 10:42    |
+--------------------------------------------------------------+
| Status                        | Queue list (virtual-list)    |
|  Pending: 12                  |  Sale #1042   pending        |
|  Conflicts: 1                 |  Return #88   conflict       |
|  [Retry]  [View conflicts]    |  Stock move   sent           |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Sync  [badge]  Last 10:42        |
+----------------------------------+
| Status: 12 pending, 1 conflict   |
+----------------------------------+
| Queue list                       |
+----------------------------------+
| [Retry] [View conflicts]         |
+----------------------------------+
```

Components from screens.md: SyncBadge, QueueList

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Retry sync | primary | `button` |
| View conflicts | secondary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Everything is synced. Nothing waiting. | تمت مزامنة كل شيء. لا يوجد ما ينتظر. | copy.csv |
| loading | Checking sync queue… | جارٍ فحص قائمة المزامنة… | copy.csv |
| error | Sync failed. Retry, or tell the manager if it keeps failing. | تعذّرت المزامنة. أعد المحاولة أو أبلغ المدير إذا تكرر ذلك. | copy.csv |
| offline | Offline. Sales are saved on this device and sync when the connection returns. | غير متصل. تُحفظ المبيعات على هذا الجهاز وتُزامن عند عودة الاتصال. | copy.csv |
| locked | A manager PIN is needed to resolve conflicts. | حلّ التعارضات يتطلب رمز المدير. | copy.csv |
| success | Sync complete. | اكتملت المزامنة. | copy.csv |

## Validation and error copy

- `FRM-02` Error copy says what happened and how to fix it in one sentence.
- `FRM-01` Validate on blur; re-validate on change after the first error; summarise on submit.
- `FRM-03` Submit stays enabled; errors listed on attempt.

## Keyboard and shortcuts

| Key | Action |
|-----|--------|
| Tab / Shift+Tab | move focus |
| Enter | activate |
| Escape | close dialog or sheet |

## Accessibility checklist

- `A11Y-01`
- `A11Y-02`
- `A11Y-03`
- `A11Y-08`
- `A11Y-12`
- `A11Y-13`
- `A11Y-14`
- `A11Y-16`
- Screen note: Status text

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.sync-status.viewed` (persona, branch)
- `screen.sync-status.action` (action id, duration_ms)
- `screen.sync-status.error` (code)

## Open questions

- none
