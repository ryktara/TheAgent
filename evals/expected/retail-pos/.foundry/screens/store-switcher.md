---
id: "store-switcher"
jobs: ["multi-store"]
personas: ["owner"]
route: "/store-switcher"
routes: [{path: "/store-switcher"}]
layout: "action-bar / high density"
components: ["button", "empty-state", "skeleton", "switch", "toast"]
data:
  reads: ["store_get", "store_list"]
  writes: ["store_multi_store"]
  events: []
offline: true
print: false
---

# store-switcher

## Purpose

Switch store context; compare stores

Role access: owner.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| store-switcher                                               |
+--------------------------------------------------------------+
| Dropdown in header            | store cards                  |
| Dropdown in header            | store cards                  |
| Dropdown in header            | store cards                  |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| store-switcher                   |
+----------------------------------+
| Dropdown in header               |
|                                  |
| store cards                      |
|                                  |
+----------------------------------+
```

Components from screens.md: StoreMenu

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Pick store | primary | `button` |

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
- `A11Y-08`
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- `A11Y-18`
- Screen note: Menu

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.store-switcher.viewed` (persona, branch)
- `screen.store-switcher.action` (action id, duration_ms)
- `screen.store-switcher.error` (code)

## Open questions

- none
