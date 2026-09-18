# Data files

Reference is data, not prose. Every CSV here is queried by `python scripts/foundry.py query <name>
--<col> <value> [--n 20] [--json]` (exact or substring match, at most 20 rows by default). No data
file enters an agent context whole. Sources and verification status: [SOURCES.md](SOURCES.md).

| File | Rows | Columns | Consumed by |
|------|-----:|---------|-------------|
| ux-rules.csv | 243 | id, priority, category, platform, rule, anti_pattern, why, source, applies_to, check | design-skeleton (do/avoid), screens-skeleton (a11y and RTL rule ids), gate screens |
| palettes.csv | 60 | id, name, mood, industry_tags, primary, primary_fg, secondary, accent, bg, surface, surface_alt, text, text_muted, border, success, warning, danger, info, dark_bg, dark_surface, dark_text | design-skeleton; `design-check` fails CI on any contrast pair below target |
| typography.csv | 32 | id, heading_font, body_font, mono_font, arabic_font, urdu_font, scale_ratio, base_px, weights, mood, use_case, google_fonts_url | design-skeleton |
| styles.csv | 26 | id, name, description, density, radius, shadow, border, motion_level, best_for, avoid_for, css_keywords | design-skeleton |
| product-types.csv | 64 | id, name, tags, default_style, default_palette_tag, default_typography_tag, density, nav_pattern, key_screens, anti_patterns | design-skeleton, screens-skeleton |
| charts.csv | 27 | id, chart, use_for, avoid_for, library_web, a11y_notes, mobile_fallback | screen-spec (reports), P7 implement |
| components.csv | 50 | id, component, shadcn_name, radix_primitive, states, a11y_role, keyboard, rtl_notes, min_target | design-skeleton inventory, screens-skeleton, gate screens |
| stacks.csv | 14 | stack_id, layer, package, scaffold_cmd, test_cmd, typecheck_cmd, lint_cmd, a11y_cmd, notes | architecture, data-model, P7 implement |

ux-rules priority order (1 = highest): accessibility and rtl-i18n, touch-interaction, performance,
style-consistency and operational-ui, layout-responsive and print, typography-color, motion,
forms-feedback, navigation, charts-data. Palette contrast targets: text/bg 4.5, text_muted/bg 4.5,
primary_fg/primary 4.5, border/bg 3, semantics/bg 3, dark_text/dark_bg 4.5.
