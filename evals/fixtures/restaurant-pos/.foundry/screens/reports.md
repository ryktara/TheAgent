---
id: "reports"
jobs: ["reports"]
personas: ["owner"]
route: "/reports"
layout: "action-bar / high density"
components: ["button", "chart-card", "data-table", "date-picker", "empty-state", "skeleton", "toast"]
data:
  reads: []
  writes: ["job_reports"]
  events: []
offline: true
print: true
---

# reports

## Purpose

Sales by hour, item, category, server, channel; tax; discounts; voids; payment mix

Role access: owner (manager for daily).

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| reports                                                      |
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
| reports                          |
+----------------------------------+
| header                           |
|                                  |
| content                          |
|                                  |
| action bar                       |
|                                  |
+----------------------------------+
```

Components from screens.md: ReportPicker, FilterBar, DataTable, Chart (one per report)

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Pick report, date range, branch, export CSV/PDF, schedule email | primary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No sales in this range. | لا توجد مبيعات في هذه الفترة. <!-- unreviewed --> | copy.csv |
| loading | Building report… | جارٍ إعداد التقرير… <!-- unreviewed --> | copy.csv |
| error | Report failed. Narrow the range and retry. | فشل التقرير. ضيّق الفترة وأعد المحاولة. <!-- unreviewed --> | copy.csv |
| offline | Reports need a connection. | التقارير تتطلب اتصالًا. <!-- unreviewed --> | copy.csv |
| locked | Owner access needed for this report. | هذا التقرير يتطلب صلاحية المالك. <!-- unreviewed --> | copy.csv |
| success | Report ready. | التقرير جاهز. <!-- unreviewed --> | copy.csv |

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
- Screen note: Charts carry a data table alternative

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.reports.viewed` (persona, branch)
- `screen.reports.action` (action id, duration_ms)
- `screen.reports.error` (code)

## Open questions

- none
