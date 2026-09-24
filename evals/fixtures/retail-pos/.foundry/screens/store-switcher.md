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
| Header: [Store: Olaya v]                                     |
+--------------------------------------------------------------+
| Store cards                                                  |
|  +----------------+  +----------------+                      |
|  | Olaya          |  | Store 2        |                      |
|  | Active         |  | Suspended      |                      |
|  +----------------+  +----------------+                      |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| [Store: Olaya v]                 |
+----------------------------------+
| Store cards                      |
|  Olaya - active                  |
|  Store 2 - suspended             |
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
| empty | No stores set up yet. | لا توجد متاجر مُعدّة بعد. | copy.csv |
| loading | Loading stores… | جارٍ تحميل المتاجر… | copy.csv |
| error | Stores could not be loaded. Retry. | تعذّر تحميل المتاجر. أعد المحاولة. | copy.csv |
| offline | Offline. You can switch stores when the connection returns. | غير متصل. يمكنك تبديل المتجر عند عودة الاتصال. | copy.csv |
| locked | This store is suspended. Only the owner can open it. | هذا المتجر موقوف. فتحه متاح للمالك فقط. | copy.csv |
| success | Store switched. | تم تبديل المتجر. | copy.csv |

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

- Multi-store is out of PRD scope: keep this screen (job multi-store) or remove it and its route?
