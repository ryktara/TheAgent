# Design system — MASTER

Pack restaurant-pos · product type restaurant-pos · style high-contrast-operational · palette ember-kitchen · typography inter-system.
Overrides: `pages/<screen-id>.md` replaces a section of this file by heading (see pages/README.md).

## Intent

<!-- model: write up to 5 sentences; leading words: deliberate, operational, calm, dense -->
Deliberate high-contrast operational for restaurant pos: large type, 7:1 text, thick focus rings, colour+icon semantics.
Mood warm, energetic; one accent (#0b92cb), neutrals for everything else, semantic colours only for meaning.
Density high; navigation action-bar; touch targets 48px.

## Palette

| Role | Light | Dark | Contrast vs bg (light) |
|------|-------|------|------------------------|
| primary | `#ca4c16` | `#ca4c16` | 4.61:1 |
| primary_fg | `#ffffff` | `-` | 1.00:1 |
| secondary | `#ab922b` | `-` | 3.05:1 |
| accent | `#0b92cb` | `-` | 3.51:1 |
| bg | `#ffffff` | `#1a1614` | 1.00:1 |
| surface | `#fbf9f9` | `#25201d` | 1.05:1 |
| surface_alt | `#f4f1f0` | `-` | 1.12:1 |
| text | `#261c17` | `#eceae9` | 16.65:1 |
| text_muted | `#72615a` | `-` | 5.88:1 |
| border | `#a48d84` | `-` | 3.12:1 |
| success | `#279b57` | `-` | 3.55:1 |
| warning | `#b36f0f` | `-` | 4.04:1 |
| danger | `#aa1818` | `-` | 7.36:1 |
| info | `#1d78a5` | `-` | 4.90:1 |

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
- Touch: minimum 48px; numpad keys 64px

## Components

| Id | Component | shadcn | States | Min target |
|----|-----------|--------|--------|------------|
| `button` | Button | button | default,hover,focus,active,disabled,loading,error | 44 |
| `icon-button` | Icon button | button | default,hover,focus,active,disabled,loading,error | 44 |
| `numpad` | Numpad | - | default,hover,focus,active,disabled,loading,error | 64 |
| `tender-keypad` | Tender keypad | - | default,hover,focus,active,disabled,loading,error | 64 |
| `pin-pad` | PIN pad | - | default,hover,focus,active,disabled,loading,error | 64 |
| `quantity-stepper` | Quantity stepper | - | default,hover,focus,active,disabled,loading,error | 44 |
| `modifier-sheet` | Modifier sheet | sheet | default,hover,focus,active,disabled,loading,error | 48 |
| `data-table` | Data table | table | default,hover,focus,active,disabled,loading,error | 36 |
| `virtual-list` | Virtual list | - | default,hover,focus,active,disabled,loading,error | 44 |
| `toast` | Toast | sonner | default,loading,error | 0 |
| `banner-offline` | Offline banner | alert | default,loading,error | 0 |
| `dialog` | Dialog | dialog | default,hover,focus,active,disabled,loading,error | 44 |
| `tabs` | Tabs | tabs | default,hover,focus,active,disabled,loading,error | 44 |
| `select` | Select | select | default,hover,focus,active,disabled,loading,error | 44 |
| `kds-ticket` | KDS ticket | - | default,focus,active,error | 56 |
| `order-card` | Order card / item tile | card | default,hover,focus,active,disabled,loading,error | 72 |
| `table-map-tile` | Table map tile | - | default,hover,focus,active,disabled,loading,error | 56 |
| `receipt-preview` | Receipt preview | - | default,loading,error | 0 |
| `chart-card` | Chart card | card | default,loading,error | 0 |
| `kpi-tile` | KPI tile | card | default,loading,error | 0 |
| `empty-state` | Empty state | - | default | 44 |
| `skeleton` | Skeleton | skeleton | loading | 0 |
| `input` | Text input | input | default,hover,focus,active,disabled,loading,error | 44 |
| `badge` | Badge | badge | default | 0 |
| `bottom-tabs` | Bottom tab bar | - | default,active | 48 |
| `search` | Search field | input | default,hover,focus,active,disabled,loading,error | 44 |
| `customer-display` | Customer display | - | default,loading | 0 |
| `split-bill` | Split bill board | - | default,hover,focus,active,disabled,loading,error | 48 |
| `floor-canvas` | Floor canvas | - | default,focus,active | 56 |

## Do and avoid

| Rule | Do | Avoid | Source |
|------|----|-------|--------|
| `A11Y-07` | Drag operations have a single-pointer alternative (select then move) | Drag-only split-bill assignment | WCAG2.2 2.5.7 |
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
- `PRT-06` Kitchen tickets: item names 2x size, modifiers indented, seat and course tags
