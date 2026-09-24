# Design system — MASTER

Pack trading-app · product type trading-app · style fintech-dark · palette trading-dark-cb · typography inter-system.
Overrides: `pages/<screen-id>.md` replaces a section of this file by heading (see pages/README.md).

## Intent

<!-- model: write up to 5 sentences; leading words: deliberate, operational, calm, dense -->
Deliberate fintech dark for trading app: dark surfaces, dense tables, tabular numerals, restrained accent.
Mood dense, financial, blue/orange P&L; one accent (#ecbd51), neutrals for everything else, semantic colours only for meaning.
Density high; navigation bottom-tabs; touch targets 44px.

## Palette

| Role | Light | Dark | Contrast vs bg (light) | Use |
|------|-------|------|------------------------|-----|
| primary | `#527ce0` | `#5680e1` | 4.50:1 | non-text-only (fills, borders, icons) |
| primary_fg | `#0b0b0b` | `#14161a` | 1.11:1 | text on primary |
| secondary | `#7a66cc` | `#7a66cc` | 3.89:1 | non-text-only (fills, borders, icons) |
| accent | `#ecbd51` | `#ecbd51` | 10.12:1 | text-safe |
| bg | `#16181d` | `#14161a` | 1.00:1 | surface |
| surface | `#1f2228` | `#1d2025` | 1.11:1 | surface |
| surface_alt | `#282c33` | `#1d2025` | 1.27:1 | surface |
| text | `#e9eaed` | `#e9eaec` | 14.76:1 | text-safe |
| text_muted | `#acb0b9` | `#acb0b9` | 8.17:1 | text-safe |
| border | `#606776` | `#5e6473` | 3.13:1 | non-text-only (fills, borders, icons) |
| success | `#6494d8` | `#6494d8` | 5.72:1 | text-safe |
| warning | `#f0ac4c` | `#f0ac4c` | 9.06:1 | text-safe |
| danger | `#e79255` | `#e79255` | 7.31:1 | text-safe |
| info | `#5ab5e2` | `#5ab5e2` | 7.73:1 | text-safe |

Themes: default → `trading-dark-cb`, light → `indigo-calm`. Each theme is a palettes.csv row applied as a token swap.

## Typography

Heading Inter · body Inter · mono JetBrains Mono · Arabic IBM Plex Sans Arabic · Urdu Noto Nastaliq Urdu · weights 400,500,600,700 · tabular numerals on.

| Step | Size | Use |
|------|------|-----|
| base | 16px | body, inputs, table cells, captions at base weight |
| md | 19px | labels, list titles |
| lg | 23px | section titles |
| xl | 28px | page titles |
| 2xl | 33px | amount due, KPI values |
| 3xl | 40px | display, kiosk |
| 4xl | 48px | hero, queue numbers |

## Scales

- Spacing: 0px, 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px
- Radius: 0px, 6px, 12px (6px base)
- Shadow: none, sm, md (none default)
- Z-index: base, sticky, drawer, dialog, toast, tooltip
- Motion: fast 100ms, base 200ms, slow 240ms; reduced-motion variant removes movement
- Touch: minimum 44px; numpad keys 64px

## Components

Text-safe roles for any component label: text, text_muted, primary_fg. Non-text-only roles: primary, secondary, border (fills, borders, icons only).

| Id | Component | shadcn | States | Min target |
|----|-----------|--------|--------|------------|
| `button` | Button | button | default,hover,focus,active,disabled,loading,error | 44 |
| `icon-button` | Icon button | button | default,hover,focus,active,disabled,loading,error | 44 |
| `data-table` | Data table | table | default,hover,focus,active,disabled,loading,error | 36 |
| `toast` | Toast | sonner | default,loading,error | 0 |
| `dialog` | Dialog | dialog | default,hover,focus,active,disabled,loading,error | 44 |
| `tabs` | Tabs | tabs | default,hover,focus,active,disabled,loading,error | 44 |
| `select` | Select | select | default,hover,focus,active,disabled,loading,error | 44 |
| `chart-card` | Chart card | card | default,loading,error | 0 |
| `kpi-tile` | KPI tile | card | default,loading,error | 0 |
| `empty-state` | Empty state | - | default | 44 |
| `skeleton` | Skeleton | skeleton | loading | 0 |
| `input` | Text input | input | default,hover,focus,active,disabled,loading,error | 44 |
| `badge` | Badge | badge | default | 0 |
| `bottom-tabs` | Bottom tab bar | - | default,active | 48 |
| `search` | Search field | input | default,hover,focus,active,disabled,loading,error | 44 |

## Do and avoid

| Rule | Do | Avoid | Source |
|------|----|-------|--------|
| `RTL-01` | Layout, navigation, tabs, lists and swipe directions mirror in RTL | LTR layout with Arabic text | foundry |
| `RTL-02` | Numerals, prices, phone numbers, QR codes and numpads stay LTR in RTL | Mirrored numpad | foundry |
| `RTL-03` | Use logical CSS properties (margin-inline-start) everywhere | margin-left hard-coded | foundry |
| `RTL-04` | Arabic fonts with Naskh or Kufi fallback at 18 px minimum; Urdu Nastaliq at 20 px | Latin fallback boxes | foundry |
| `RTL-05` | Bidi isolation for mixed runs (unicode-bidi: isolate) in names and addresses | Scrambled mixed text | foundry |
| `RTL-06` | Icons with direction (arrows, back) mirror; icons without (clock, search) do not | Mirrored search icon | M3 |
| `RTL-07` | Dates and numbers formatted per locale with Western numerals by default, Arabic-Indic as a branch option | Hard-coded formats | foundry |
| `RTL-08` | Language switch persists per user and per receipt | Resets each session | foundry |
| `RTL-09` | Text expansion allowance of 30% for Arabic and Urdu in buttons and tables | Clipped Arabic labels | foundry |
| `RTL-10` | Pseudo-localisation test in CI for length and RTL | Untested RTL | foundry |
| `RTL-11` | Right-aligned amounts in both directions | Amounts flip alignment | foundry |
| `RTL-12` | Bilingual receipts carry identical totals in both blocks | Different rounding per language | foundry |
| `RTL-13` | Floor canvas and seat numbers never mirror; labels do | Mirrored floor plan | foundry |
| `RTL-14` | Receipt currency symbol position per locale (AED before, د.إ after) | Wrong symbol side | foundry |
| `RTL-15` | Item names entered in both languages; fallback shows the other language, never blank | Blank Arabic names | foundry |

## RTL

- `RTL-01` Layout, navigation, tabs, lists and swipe directions mirror in RTL
- `RTL-02` Numerals, prices, phone numbers, QR codes and numpads stay LTR in RTL
- `RTL-03` Use logical CSS properties (margin-inline-start) everywhere
- `RTL-04` Arabic fonts with Naskh or Kufi fallback at 18 px minimum; Urdu Nastaliq at 20 px
- `RTL-05` Bidi isolation for mixed runs (unicode-bidi: isolate) in names and addresses
- `RTL-06` Icons with direction (arrows, back) mirror; icons without (clock, search) do not
- `RTL-07` Dates and numbers formatted per locale with Western numerals by default, Arabic-Indic as a branch option
- `RTL-08` Language switch persists per user and per receipt

## Print

- `PRT-01` 80 mm receipt: 72 mm printable width, 42 columns at font A, 56 at font B
- `PRT-02` Thermal contrast: no greys, no thin lines under 2 px, bold for totals
- `PRT-03` QR code at least 25 mm square with quiet zone; one per receipt
- `PRT-04` Header: branch name, address, tax number; footer: receipt number, date, device
- `PRT-05` Bilingual receipt: Arabic block first for SA, English first for AE unless toggled
- `PRT-07` Reprint stamped REPRINT; voided receipts print VOID
