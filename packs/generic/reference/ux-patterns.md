# Generic pack — UX patterns

Patterns every business app inherits. Domain packs override by naming the pattern id.

## Navigation

- **NAV-01 Sidebar shell.** Collapsible left sidebar with sections; top bar holds search,
  notifications, avatar. Under 1024 px the sidebar becomes a drawer.
- **NAV-02 Breadcrumbs** on every detail and edit screen; last crumb is the current title.
- **NAV-03 Global search (ctrl/cmd+K)** searches records, users, settings; results grouped.
- **NAV-04 Tenant switcher** appears only when the user belongs to more than one tenant.

## Lists

- **LST-01 Data table** with sticky header, resizable columns, column chooser, density toggle.
- **LST-02 Filter chips** are additive, removable, and serialise to the URL.
- **LST-03 Saved views** per user; a default view per role.
- **LST-04 Empty state** has one illustration, one sentence, one primary action, one secondary.
- **LST-05 Skeleton loading** matches the final layout; no spinners over tables.
- **LST-06 Bulk bar** appears on selection with count and actions; escape clears selection.

## Forms

- **FRM-01 Single column** up to 640 px; two columns only for short related fields.
- **FRM-02 Labels above inputs**; helper text below; errors replace helper text in red with icon.
- **FRM-03 Validate on blur**, re-validate on change after first error, summarise on submit.
- **FRM-04 Primary action right-aligned** in a sticky footer on long forms; secondary to its left.
- **FRM-05 Dirty guard** confirms before leaving unsaved changes.
- **FRM-06 Autosave drafts** with "Saved 5 s ago" status text.
- **FRM-07 Money fields** show the currency symbol, tabular numerals, and two decimals.
- **FRM-08 Dates** use a locale-aware picker; typing is allowed; timezone shown when relevant.

## Feedback

- **FBK-01 Toasts** for success (4 s) and recoverable errors (persistent with action).
- **FBK-02 Inline confirmation** for destructive actions; typed confirmation for delete.
- **FBK-03 Progress** for jobs over 2 s: determinate when count is known, else indeterminate.
- **FBK-04 Optimistic updates** for state toggles with rollback on failure.

## Detail screens

- **DET-01 Header** with title, state badge, primary transition button, overflow menu.
- **DET-02 Tabs** for Overview, Activity, Files, Related; the URL holds the active tab.
- **DET-03 Activity tab** renders AuditEvents as a timeline with before/after diff on expand.

## Accessibility (WCAG 2.2 AA)

- **A11Y-01** Contrast 4.5:1 text, 3:1 UI components; verified by the design-system validator.
- **A11Y-02** Every interactive element reachable by keyboard with a visible focus ring.
- **A11Y-03** Touch targets 44 px minimum (48 dp on Android).
- **A11Y-04** Form fields have programmatic labels; errors are announced.
- **A11Y-05** Motion respects prefers-reduced-motion.
- **A11Y-06** RTL mirror for Arabic and Urdu; logical CSS properties throughout.

## Anti-patterns to replace

| Replace | With |
|---------|------|
| Modal-in-modal | Side panel or full page |
| Infinite scroll on data tables | Cursor pagination with page size |
| Disabled submit until valid | Enabled submit with summary of errors |
| Icon-only buttons without label | Icon plus label, or tooltip plus aria-label |
| Hover-only affordances | Always-visible or focus-visible affordances |
