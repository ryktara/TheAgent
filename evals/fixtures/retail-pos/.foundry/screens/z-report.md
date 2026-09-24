---
id: "z-report"
jobs: ["cash-management"]
personas: ["cashier"]
route: "/z-report"
routes: [{path: "/z-report"}]
layout: "action-bar / high density"
components: ["button", "data-table", "drawer", "empty-state", "receipt-preview", "skeleton", "toast"]
data:
  reads: ["cash_drawer_session_get", "cash_drawer_session_list"]
  writes: ["cash_drawer_session_cash_management"]
  events: []
offline: true
print: true
---

# z-report

## Purpose

End-of-day Z: sales, returns, tax, tenders, drawer variance; locks the day

Role access: store-manager.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| Z report - Date - Drawer                  [Print X] [Print Z] |
+--------------------------------------------------------------+
| Report preview (receipt-preview)                             |
|  Sales gross / net        | Returns                          |
|  VAT 15%                  | Tenders: cash, card, mada        |
|  Expected cash | Counted | Variance                          |
+--------------------------------------------------------------+
| Open sessions: 0                               [Export]      |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Z report          Date           |
+----------------------------------+
| Report preview                   |
|  Sales / Returns / VAT           |
|  Tenders                         |
|  Variance                        |
+----------------------------------+
| [Print X] [Print Z] [Export]     |
+----------------------------------+
```

Components from screens.md: ReportRender

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Print X (no reset) | secondary | `button` |
| Print Z (locks the day) | primary | `button` |
| Export | secondary | `button` |
| Review open sessions blocking Z | secondary | `drawer` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No sales recorded for this day yet. | لا توجد مبيعات مسجّلة لهذا اليوم بعد. | copy.csv |
| loading | Totalling the day's sales… | جارٍ احتساب مبيعات اليوم… | copy.csv |
| error | Z report could not be built. Retry, or check open drawer sessions. | تعذّر إعداد تقرير Z. أعد المحاولة أو راجع جلسات الدرج المفتوحة. | copy.csv |
| offline | Offline. X prints from this device; Z waits until all sales sync. | غير متصل. يمكن طباعة تقرير X من هذا الجهاز، وينتظر تقرير Z حتى تُزامن كل المبيعات. | copy.csv |
| locked | Close all open drawer sessions before printing Z, or enter a manager PIN. | أغلق جميع جلسات الدرج المفتوحة قبل طباعة تقرير Z، أو أدخل رمز المدير. | copy.csv |
| success | Z printed. The day is locked. | تمت طباعة تقرير Z وإقفال اليوم. | copy.csv |

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
- Screen note: Tables with headers

## RTL notes

- `RTL-01`
- `RTL-02`
- `RTL-03`
- `RTL-05`
- Screen note: Mirrors

## Telemetry

- `screen.z-report.viewed` (persona, branch)
- `screen.z-report.action` (action id, duration_ms)
- `screen.z-report.error` (code)

## Open questions

- none
