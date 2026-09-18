# Data files

Reference is data, not prose. Every CSV here is queried by `scripts/foundry.py query` (P5),
which returns at most 20 rows. No data file enters an agent context whole.

## Planned CSVs and columns

| File | Columns |
|------|---------|
| ux-rules.csv | id, priority (1–10), category, rule, must_have, anti_pattern, source (HIG/M3/WCAG2.2), applies_to |
| palettes.csv | id, name, mood, primary, secondary, accent, bg, surface, text, contrast_ratio_min, product_types |
| typography.csv | id, heading_font, body_font, mono_font, scale_ratio, base_px, line_height, use_case, source_url |
| styles.csv | id, name, description, keywords, density, radius, shadow, motion, best_for, avoid_for |
| product-types.csv | id, name, keywords, default_style, default_palette, default_typography, density, touch_target, charts |
| charts.csv | id, chart_type, best_for, data_shape, min_points, max_series, a11y_notes, library_hint |
| security-controls.csv | id, framework (ASVS/OWASP-Agentic-Top10), level, category, control, verification, applies_to |
| stacks.csv | id, name, scaffold_cmd, typecheck_cmd, test_cmd, lint_cmd, a11y_cmd, sast_cmd, deploy_target |

Priority order for ux-rules (1 = highest): Accessibility, Touch, Performance, Style, Layout,
Typography/Color, Animation, Forms, Navigation, Charts.

## Query contract (P5)

```
python scripts/foundry.py query <file> --where col=value [--limit 20] [--columns a,b]
```

Output is a markdown table. Rows above the limit are counted, not printed.
