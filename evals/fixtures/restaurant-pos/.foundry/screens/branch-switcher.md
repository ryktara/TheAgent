---
id: "branch-switcher"
jobs: ["multi-branch"]
personas: ["owner"]
route: "/branch-switcher"
layout: "action-bar / high density"
components: ["button", "date-picker", "empty-state", "pin-pad", "select", "skeleton", "switch", "toast"]
data:
  reads: ["branch_get", "branch_list"]
  writes: ["branch_multi_branch"]
  events: []
offline: true
print: false
---

# branch-switcher

## Purpose

Owner moves between branches; device is pinned to one

Role access: owner.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| branch-switcher                                              |
+--------------------------------------------------------------+
| header                        | content                      |
| header                        | content                      |
| header                        | content                      |
+--------------------------------------------------------------+
| action bar                                                   |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| branch-switcher                  |
+----------------------------------+
| header                           |
|                                  |
| content                          |
|                                  |
| action bar                       |
|                                  |
+----------------------------------+
```

Components from screens.md: BranchMenu

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Select branch | primary | `button` |
| view consolidated | secondary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | Nothing here yet. | لا يوجد شيء هنا بعد. <!-- unreviewed --> | copy.csv |
| loading | Loading… | جارٍ التحميل… <!-- unreviewed --> | copy.csv |
| error | Something went wrong. Retry, or contact the manager. | حدث خطأ ما. أعد المحاولة أو تواصل مع المدير. <!-- unreviewed --> | copy.csv |
| offline | Offline. Changes are saved on this device and sync when the connection returns. | غير متصل. تُحفظ التغييرات على هذا الجهاز وتُزامن عند عودة الاتصال. <!-- unreviewed --> | copy.csv |
| locked | A manager PIN is needed for this action. | هذا الإجراء يتطلب رمز المدير. <!-- unreviewed --> | copy.csv |
| success | Done. | تم. <!-- unreviewed --> | copy.csv |

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
- `A11Y-06`
- `A11Y-08`
- `A11Y-10`
- `A11Y-12`
- `A11Y-14`
- Screen note: Menu button with current branch label

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.branch-switcher.viewed` (persona, branch)
- `screen.branch-switcher.action` (action id, duration_ms)
- `screen.branch-switcher.error` (code)

## Open questions

- none
