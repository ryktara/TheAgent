"""Foundry phases 7-8: design system and screen specs, plus the design validators.

Imported by foundry.py; Python 3.11+ stdlib only.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

import foundry as F

DATA = F.ROOT / "data"
REQUIRED_MASTER_SECTIONS = ["Intent", "Palette", "Typography", "Scales", "Components", "Do and avoid", "RTL", "Print"]
SCREEN_STATES = ["empty", "loading", "error", "offline", "locked", "success"]


# ----------------------------------------------------------------------------- contrast (WCAG 2.x)
def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _srgb_to_linear(r) + 0.7152 * _srgb_to_linear(g) + 0.0722 * _srgb_to_linear(b)


def contrast_ratio(a: str, b: str) -> float:
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


PALETTE_PAIRS = [("text", "bg", 4.5), ("text_muted", "bg", 4.5), ("primary_fg", "primary", 4.5), ("border", "bg", 3.0),
                 ("success", "bg", 3.0), ("warning", "bg", 3.0), ("danger", "bg", 3.0), ("info", "bg", 3.0),
                 ("text", "surface", 4.5), ("dark_text", "dark_bg", 4.5), ("dark_text", "dark_surface", 4.5),
                 ("dark_text_muted", "dark_bg", 4.5), ("dark_primary", "dark_bg", 3.0), ("dark_secondary", "dark_bg", 3.0), ("dark_accent", "dark_bg", 3.0),
                 ("dark_border", "dark_bg", 3.0), ("dark_success", "dark_bg", 3.0), ("dark_warning", "dark_bg", 3.0), ("dark_danger", "dark_bg", 3.0), ("dark_info", "dark_bg", 3.0)]
TEXT_ROLES = ["text", "text_muted", "primary_fg"]


def check_palette_row(row: dict) -> list[str]:
    errs = []
    for fg, bg, target in PALETTE_PAIRS:
        if fg not in row or bg not in row or not row[fg] or not row[bg]:
            continue
        r = contrast_ratio(row[fg], row[bg])
        if r < target:
            errs.append(f"{row.get('id')}: {fg}/{bg} {r:.2f} < {target}")
    return errs


def check_palettes(path: Path) -> tuple[int, list[str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    errs = []
    for r in rows:
        errs += check_palette_row(r)
    return len(rows), errs


# ----------------------------------------------------------------------------- tokens checks
def check_tokens(tokens: dict, touch_min: int = 44, operational: bool = False) -> list[str]:
    errs = []
    f = tokens.get("foundry") or {}
    scale = [v.get("$value") if isinstance(v, dict) else v for v in (tokens.get("font", {}).get("size") or {}).values()]
    sizes = [int(str(s).replace("px", "")) for s in scale if s is not None]
    if not sizes:
        errs.append("font.size scale missing")
    else:
        if min(sizes) < 16 and not operational:
            errs.append(f"font.size base {min(sizes)} < 16")
        if sizes[0] < 16:
            errs.append(f"font.size base {sizes[0]} < 16")
        if any(b <= a for a, b in zip(sizes, sizes[1:])):
            errs.append("font.size scale not monotonic")
        ratios = [b / a for a, b in zip(sizes, sizes[1:]) if a]
        if ratios and not all(1.10 <= r <= 1.34 for r in ratios):
            errs.append(f"font.size ratio outside 1.125-1.333: {[round(r, 3) for r in ratios]}")
    spacing = [int(str(v.get("$value") if isinstance(v, dict) else v).replace("px", "")) for v in (tokens.get("space") or {}).values()]
    if not spacing or any(s % 4 for s in spacing):
        errs.append("space scale must be non-empty multiples of 4")
    radius = tokens.get("radius") or {}
    if len(radius) > 5:
        errs.append(f"radius scale has {len(radius)} steps; max 5")
    z = tokens.get("z") or {}
    if len(z) > 7:
        errs.append(f"z-index scale has {len(z)} layers; max 7")
    motion = tokens.get("motion") or {}
    durs = [int(str(v.get("$value") if isinstance(v, dict) else v).replace("ms", "")) for k, v in (motion.get("duration") or {}).items()]
    if not durs or any(d < 100 or d > 400 for d in durs):
        errs.append(f"motion durations must be 100-400ms: {durs}")
    if "reduced" not in motion:
        errs.append("motion.reduced variant missing")
    tt = (tokens.get("touch") or {}).get("min")
    tt = tt.get("$value") if isinstance(tt, dict) else tt
    if tt is None or int(str(tt).replace("px", "").replace("dp", "")) < touch_min:
        errs.append(f"touch.min {tt} < {touch_min}")
    if operational and not (f.get("tabular_numerals") is True):
        errs.append("foundry.tabular_numerals must be true for operational or financial products")
    return errs


def run_design_check(root: Path, project: Path | None, palettes_only: bool = False) -> int:
    n, errs = check_palettes(root / "data" / "palettes.csv")
    print(f"design-check: palettes {n} rows, {len(errs)} failing pairs")
    for e in errs:
        print("  " + e)
    if not palettes_only and project is not None:
        tp = project / "design-system" / "tokens.json"
        if tp.exists():
            tokens = json.loads(tp.read_text(encoding="utf-8"))
            meta = tokens.get("foundry") or {}
            terrs = check_tokens(tokens, int(meta.get("touch_min", 44)), bool(meta.get("operational")))
            print(f"design-check: tokens.json {len(terrs)} issue(s)")
            for e in terrs:
                print("  " + e)
            errs += terrs
        else:
            print("design-check: no design-system/tokens.json in project (skipped)")
    return 1 if errs else 0


# ----------------------------------------------------------------------------- data access
def _rows(name: str) -> list[dict]:
    with (DATA / f"{name}.csv").open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _tags(s: str) -> set[str]:
    return {t.strip().lower() for t in re.split(r"[,;]", s or "") if t.strip()}


def _score(row_tags: set[str], wanted: set[str]) -> int:
    return len(row_tags & wanted)


def product_type_for(pack: dict) -> dict:
    rows = _rows("product-types")
    by_id = {r["id"]: r for r in rows}
    if pack["slug"] in by_id:
        return by_id[pack["slug"]]
    wanted = _tags(",".join(pack.get("aliases") or [])) | {pack["slug"].split("-")[0]}
    best = max(rows, key=lambda r: _score(_tags(r["tags"]), wanted))
    return best if _score(_tags(best["tags"]), wanted) else by_id.get("admin-dashboard", rows[0])


def pick_palette(ptype: dict, ui: dict, prefer_dark: bool) -> dict:
    rows = _rows("palettes")
    pinned = ui.get("palette") or (ui.get("themes") or {}).get("default")
    if pinned:
        for r in rows:
            if r["id"] == pinned:
                return r
    wanted = _tags(ptype["tags"]) | {ptype["default_palette_tag"], "operational" if ptype["density"] == "high" else "saas"}
    if prefer_dark:
        wanted.add("dark")
    ranked = sorted(rows, key=lambda r: (-_score(_tags(r["industry_tags"]), wanted), r["id"]))
    return ranked[0]


def pick_typography(ptype: dict, rtl: bool, ui: dict | None = None) -> dict:
    rows = _rows("typography")
    if ui and ui.get("typography"):
        for r in rows:
            if r["id"] == ui["typography"]:
                return r
    wanted = _tags(ptype["tags"]) | {ptype["default_typography_tag"]}
    def sc(r):
        s = _score(_tags(r["use_case"]) | _tags(r["mood"]), wanted)
        if rtl and r["arabic_font"] in ("IBM Plex Sans Arabic", "Cairo", "Tajawal", "Almarai", "Noto Naskh Arabic", "Readex Pro", "Vazirmatn", "Noto Sans Arabic"):
            s += 1
        return s
    return sorted(rows, key=lambda r: (-sc(r), r["id"]))[0]


def pick_style(ptype: dict, ui: dict) -> dict:
    rows = _rows("styles")
    by_id = {r["id"]: r for r in rows}
    if ui.get("style") in by_id:
        return by_id[ui["style"]]
    return by_id.get(ptype["default_style"], rows[0])


# ----------------------------------------------------------------------------- phase 7: design system
def _type_scale(base: int, ratio: float, steps: int = 7) -> dict[str, int]:
    names = ["base", "md", "lg", "xl", "2xl", "3xl", "4xl"]
    sizes = [round(base * ratio ** i) for i in range(steps)]
    out: dict[str, int] = {}
    last = 0
    for n, s in zip(names, sizes):
        s = max(s, last + 1)
        out[n] = s
        last = s
    return out


def design_tokens(pal: dict, typo: dict, style: dict, ui: dict, ptype: dict, region_rtl: bool) -> dict:
    base = int(typo["base_px"])
    if ui.get("font_min_px"):
        base = max(base, int(ui["font_min_px"]))
    ratio = float(typo["scale_ratio"])
    touch = int(str(ui.get("touch", "44dp")).replace("dp", "").replace("px", "")) if ui.get("touch") else 44
    operational = ptype["density"] == "high" or "fintech" in ptype["tags"] or "trading" in ptype["tags"]
    src = lambda s: {"foundry": {"source": s}}
    color: dict[str, Any] = {}
    for role in ("primary", "primary_fg", "secondary", "accent", "bg", "surface", "surface_alt", "text", "text_muted", "border", "success", "warning", "danger", "info"):
        color[role] = {"$type": "color", "$value": pal[role], "$extensions": src(f"palettes.csv:{pal['id']}")}
    dark = {"bg": pal["dark_bg"], "surface": pal["dark_surface"], "surface_alt": pal["dark_surface"], "text": pal["dark_text"], "text_muted": pal.get("dark_text_muted", pal["dark_text"]),
            "primary": pal.get("dark_primary", pal["primary"]), "primary_fg": pal["dark_bg"] if contrast_ratio(pal["dark_bg"], pal.get("dark_primary", pal["primary"])) >= 4.5 else "#ffffff",
            "secondary": pal.get("dark_secondary", pal["secondary"]), "accent": pal.get("dark_accent", pal["accent"]), "border": pal.get("dark_border", pal["border"]),
            "success": pal.get("dark_success", pal["success"]), "warning": pal.get("dark_warning", pal["warning"]), "danger": pal.get("dark_danger", pal["danger"]), "info": pal.get("dark_info", pal["info"])}
    non_text_only = [r for r in ("primary", "secondary", "accent", "border", "success", "warning", "danger", "info") if contrast_ratio(pal[r], pal["bg"]) < 4.5]
    radius_map = {"0px": [0], "2px": [0, 2], "4px": [0, 4, 8], "6px": [0, 6, 12], "8px": [0, 8, 16], "10px": [0, 10, 20], "12px": [0, 12, 24, 999], "14px": [0, 14, 28, 999], "16px": [0, 16, 32, 999]}
    radii = radius_map.get(style["radius"], [0, 8, 16])
    motion_level = style["motion_level"]
    durations = {"fast": 100, "base": 200 if motion_level != "none" else 100, "slow": 320 if motion_level in ("medium", "high") else 240}
    scale = _type_scale(base, ratio)
    return {
        "$schema": "https://design-tokens.github.io/community-group/format/",
        "foundry": {"palette": pal["id"], "typography": typo["id"], "style": style["id"], "product_type": ptype["id"], "touch_min": touch,
                    "operational": operational, "tabular_numerals": True, "rtl": region_rtl, "text_roles": TEXT_ROLES, "non_text_only": non_text_only,
                    "themes": ui.get("themes") or {}},
        "color": {"light": color, "dark": {k: {"$type": "color", "$value": v, "$extensions": src(f"palettes.csv:{pal['id']}")} for k, v in dark.items()}},
        "font": {"family": {"heading": {"$type": "fontFamily", "$value": typo["heading_font"], "$extensions": src(f"typography.csv:{typo['id']}")},
                            "body": {"$type": "fontFamily", "$value": typo["body_font"], "$extensions": src(f"typography.csv:{typo['id']}")},
                            "mono": {"$type": "fontFamily", "$value": typo["mono_font"], "$extensions": src(f"typography.csv:{typo['id']}")},
                            "arabic": {"$type": "fontFamily", "$value": typo["arabic_font"], "$extensions": src(f"typography.csv:{typo['id']}")},
                            "urdu": {"$type": "fontFamily", "$value": typo["urdu_font"], "$extensions": src(f"typography.csv:{typo['id']}")}},
                 "size": {k: {"$type": "dimension", "$value": f"{v}px", "$extensions": src(f"scale base {base} ratio {ratio}")} for k, v in scale.items()},
                 "features": {"numerals": {"$type": "string", "$value": "tabular-nums", "$extensions": src("ux-rules.csv:TYP-04")}}},
        "space": {str(i): {"$type": "dimension", "$value": f"{v}px", "$extensions": src("4px scale")} for i, v in enumerate([0, 4, 8, 12, 16, 24, 32, 48, 64])},
        "radius": {f"r{i}": {"$type": "dimension", "$value": f"{v}px", "$extensions": src(f"styles.csv:{style['id']}")} for i, v in enumerate(radii)},
        "shadow": {"none": {"$type": "shadow", "$value": "none"}, "sm": {"$type": "shadow", "$value": "0 1px 2px rgba(0,0,0,.08)"}, "md": {"$type": "shadow", "$value": "0 4px 12px rgba(0,0,0,.12)"}},
        "z": {"base": {"$value": 0}, "sticky": {"$value": 10}, "drawer": {"$value": 20}, "dialog": {"$value": 30}, "toast": {"$value": 40}, "tooltip": {"$value": 50}},
        "motion": {"duration": {k: {"$type": "duration", "$value": f"{v}ms", "$extensions": src(f"styles.csv:{style['id']} motion {motion_level}")} for k, v in durations.items()},
                   "easing": {"standard": {"$value": "cubic-bezier(.2,0,0,1)"}, "enter": {"$value": "cubic-bezier(0,0,0,1)"}, "exit": {"$value": "cubic-bezier(.3,0,1,1)"}},
                   "reduced": {"$value": "transition-duration: 1ms; animation: none", "$extensions": src("ux-rules.csv:MOT-03")}},
        "touch": {"min": {"$type": "dimension", "$value": f"{touch}px", "$extensions": src(f"ui_profile.touch {ui.get('touch', '44dp')}")}},
    }


def tokens_css(tokens: dict) -> str:
    out = [":root {"]
    for k, v in tokens["color"]["light"].items():
        out.append(f"  --color-{k.replace('_', '-')}: {v['$value']};")
    for k, v in tokens["font"]["size"].items():
        out.append(f"  --text-{k}: {v['$value']};")
    for k, v in tokens["font"]["family"].items():
        out.append(f"  --font-{k}: \"{v['$value']}\";")
    for k, v in tokens["space"].items():
        out.append(f"  --space-{k}: {v['$value']};")
    for k, v in tokens["radius"].items():
        out.append(f"  --radius-{k}: {v['$value']};")
    for k, v in tokens["motion"]["duration"].items():
        out.append(f"  --duration-{k}: {v['$value']};")
    out.append(f"  --touch-min: {tokens['touch']['min']['$value']};")
    out.append("  font-variant-numeric: tabular-nums;")
    out.append("}")
    out.append("@media (prefers-color-scheme: dark) { :root:not([data-theme=\"light\"]) {")
    for k, v in tokens["color"]["dark"].items():
        out.append(f"  --color-{k.replace('_', '-')}: {v['$value']};")
    out.append("} }")
    out.append("@media (prefers-reduced-motion: reduce) { * { transition-duration: 1ms !important; animation: none !important; } }")
    return "\n".join(out) + "\n"


def _rules_for(ptype: dict, categories: list[str] | None = None, max_priority: int = 5, limit: int = 15) -> list[dict]:
    rows = _rows("ux-rules")
    keys = _tags(ptype["key_screens"]) | _tags(ptype["tags"])
    picked = []
    for r in rows:
        if int(r["priority"]) > max_priority:
            continue
        if categories and r["category"] not in categories:
            continue
        applies = _tags(r["applies_to"])
        boost = 1 if (applies & keys or r["category"] in ("operational-ui", "rtl-i18n", "print") and ptype["density"] == "high") else 0
        picked.append((int(r["priority"]) - boost, r["id"], r))
    picked.sort(key=lambda x: (x[0], x[1]))
    return [r for _, _, r in picked[:limit]]


def components_for(ptype: dict, screens: list[str]) -> list[dict]:
    rows = _rows("components")
    keys = _tags(ptype["key_screens"]) | set(screens)
    base = {"button", "icon-button", "input", "select", "dialog", "toast", "empty-state", "skeleton", "data-table", "tabs", "badge", "search", "sidebar" if ptype["nav_pattern"] == "sidebar" else "bottom-tabs"}
    ops = {"numpad", "tender-keypad", "pin-pad", "quantity-stepper", "modifier-sheet", "kds-ticket", "order-card", "table-map-tile", "receipt-preview", "banner-offline", "split-bill", "floor-canvas", "customer-display", "virtual-list"}
    wanted = set(base)
    if ptype["density"] == "high" and ("pos" in ptype["tags"] or "kds" in ptype["tags"]):
        wanted |= ops
    if "trading" in ptype["tags"] or "analytics" in ptype["tags"] or "reports" in keys:
        wanted |= {"chart-card", "kpi-tile"}
    if "reservations" in keys or "booking" in ptype["tags"]:
        wanted |= {"date-picker"}
    return [r for r in rows if r["id"] in wanted]


def master_md(pack: dict, ledger: dict, pal: dict, typo: dict, style: dict, ptype: dict, tokens: dict, rtl: bool, print_scope: bool, brand: dict | None) -> str:
    ui = pack.get("ui_profile") or {}
    scale = tokens["font"]["size"]
    comps = components_for(ptype, [])
    rules = _rules_for(ptype)
    rtl_rules = [r for r in _rows("ux-rules") if r["category"] == "rtl-i18n"][:8]
    print_rules = [r for r in _rows("ux-rules") if r["category"] == "print"][:6]
    out = ["# Design system — MASTER", "", f"Pack {pack['slug']} · product type {ptype['id']} · style {style['id']} · palette {pal['id']} · typography {typo['id']}.",
           "Overrides: `pages/<screen-id>.md` replaces a section of this file by heading (see pages/README.md).", "",
           "## Intent", "", "<!-- model: write up to 5 sentences; leading words: deliberate, operational, calm, dense -->",
           f"Deliberate {style['name'].lower()} for {ptype['name'].lower()}: {style['description'].lower()}.",
           f"Mood {pal['mood']}; one accent ({pal['accent']}), neutrals for everything else, semantic colours only for meaning.",
           f"Density {ptype['density']}; navigation {ptype['nav_pattern']}; touch targets {tokens['touch']['min']['$value']}.", ""]
    if brand:
        out += [f"Brand input: {brand}", ""]
    out += ["## Palette", "", "| Role | Light | Dark | Contrast vs bg (light) | Use |", "|------|-------|------|------------------------|-----|"]
    for role in ("primary", "primary_fg", "secondary", "accent", "bg", "surface", "surface_alt", "text", "text_muted", "border", "success", "warning", "danger", "info"):
        dark = tokens["color"]["dark"].get(role, {}).get("$value", "-")
        ratio = contrast_ratio(pal[role], pal["bg"]) if role != "bg" else 1.0
        if role in ("bg", "surface", "surface_alt"):
            use = "surface"
        elif role == "primary_fg":
            use = "text on primary"
        elif ratio >= 4.5:
            use = "text-safe"
        elif ratio >= 3.0:
            use = "non-text-only (fills, borders, icons)"
        else:
            use = "decorative"
        out.append(f"| {role} | `{pal[role]}` | `{dark}` | {ratio:.2f}:1 | {use} |")
    if tokens["foundry"].get("themes"):
        out.append("")
        out.append("Themes: " + ", ".join(f"{k} → `{v}`" for k, v in tokens["foundry"]["themes"].items()) + ". Each theme is a palettes.csv row applied as a token swap.")
    out += ["", "## Typography", "", f"Heading {typo['heading_font']} · body {typo['body_font']} · mono {typo['mono_font']} · Arabic {typo['arabic_font']} · Urdu {typo['urdu_font']} · weights {typo['weights']} · tabular numerals on.", "",
            "| Step | Size | Use |", "|------|------|-----|"]
    uses = {"base": "body, inputs, table cells, captions at base weight", "md": "labels, list titles", "lg": "section titles", "xl": "page titles", "2xl": "amount due, KPI values", "3xl": "display, kiosk", "4xl": "hero, queue numbers"}
    for k, v in scale.items():
        out.append(f"| {k} | {v['$value']} | {uses.get(k, '')} |")
    out += ["", "## Scales", "", f"- Spacing: {', '.join(v['$value'] for v in tokens['space'].values())}",
            f"- Radius: {', '.join(v['$value'] for v in tokens['radius'].values())} ({style['radius']} base)",
            f"- Shadow: none, sm, md ({style['shadow']} default)", f"- Z-index: {', '.join(tokens['z'].keys())}",
            f"- Motion: {', '.join(f'{k} {v['$value']}' for k, v in tokens['motion']['duration'].items())}; reduced-motion variant removes movement",
            f"- Touch: minimum {tokens['touch']['min']['$value']}; numpad keys 64px", ""]
    out += ["## Components", "", f"Text-safe roles for any component label: {', '.join(TEXT_ROLES)}. Non-text-only roles: {', '.join(tokens['foundry']['non_text_only']) or 'none'} (fills, borders, icons only).", "",
            "| Id | Component | shadcn | States | Min target |", "|----|-----------|--------|--------|------------|"]
    for c in comps:
        out.append(f"| `{c['id']}` | {c['component']} | {c['shadcn_name']} | {c['states']} | {c['min_target']} |")
    out += ["", "## Do and avoid", "", "| Rule | Do | Avoid | Source |", "|------|----|-------|--------|"]
    for r in rules:
        out.append(f"| `{r['id']}` | {r['rule']} | {r['anti_pattern']} | {r['source']} |")
    out += ["", "## RTL", ""]
    if rtl:
        out += [f"- `{r['id']}` {r['rule']}" for r in rtl_rules]
    else:
        out += ["- Region is LTR; logical CSS properties still required so RTL can be enabled later (`RTL-03`)."]
    out += ["", "## Print", ""]
    if print_scope:
        out += [f"- `{r['id']}` {r['rule']}" for r in print_rules]
    else:
        out += ["- No receipts or printed reports in scope."]
    out.append("")
    return "\n".join(out)


def run_design_skeleton(project: Path, root: Path) -> int:
    sel = F.load_selection(project)
    pack = F.load_pack(root, sel["chosen"])
    ledger = F.load_ledger(project, sel["chosen"])
    ui = pack.get("ui_profile") or {}
    ptype = product_type_for(pack)
    region = next((str(d["value"]) for d in ledger.get("decisions", []) if d.get("maps_to") == "region.country" or d["id"] == "region"), "AE")
    reg = (pack.get("regional") or {}).get(region) or {}
    langs = reg.get("receipt_lang") or reg.get("languages") or ["en"]
    rtl = any(l in ("ar", "ur") for l in langs)
    brand = next((d for d in ledger.get("decisions", []) if d["id"] == "brand" and d["value"] is True), None)
    prefer_dark = str(ui.get("dark", "")).lower() in ("default", "always")
    pal = pick_palette(ptype, ui, prefer_dark)
    typo = pick_typography(ptype, rtl, ui)
    style = pick_style(ptype, ui)
    tokens = design_tokens(pal, typo, style, ui, ptype, rtl)
    print_scope = any("receipt" in f or "print" in f or "report" in f for f in (pack.get("must_have") or []))
    ds = project / "design-system"
    (ds / "pages").mkdir(parents=True, exist_ok=True)
    (ds / "MASTER.md").write_text(master_md(pack, ledger, pal, typo, style, ptype, tokens, rtl, print_scope, {"brand": "answered"} if brand else None), encoding="utf-8", newline="\n")
    (ds / "tokens.json").write_text(json.dumps(tokens, indent=2) + "\n", encoding="utf-8", newline="\n")
    (ds / "tailwind.tokens.css").write_text(tokens_css(tokens), encoding="utf-8", newline="\n")
    (ds / "pages" / "README.md").write_text("# Page overrides\n\nCreate `pages/<screen-id>.md` with any of the MASTER.md headings (`## Palette`, `## Typography`, `## Scales`, `## Components`, `## Do and avoid`, `## RTL`, `## Print`). A section present here replaces the same section of MASTER.md for that screen only; absent sections inherit. Keep overrides rare and cite the ux-rule id that justifies them.\n", encoding="utf-8", newline="\n")
    print(f"design-skeleton: palette {pal['id']}, typography {typo['id']}, style {style['id']}, product type {ptype['id']} -> design-system/MASTER.md, tokens.json, tailwind.tokens.css")
    return 0


def gate_design(project: Path, root: Path) -> list[str]:
    import foundry_phases as P
    errs = P.gate_api(project, root) if (project / "openapi.yaml").exists() else P.gate_data(project, root)
    if errs:
        return errs
    ds = project / "design-system"
    for name in ("MASTER.md", "tokens.json", "tailwind.tokens.css", "pages/README.md"):
        if not (ds / name).exists():
            errs.append(f"design-system/{name} missing")
    if errs:
        return errs
    n, perrs = check_palettes(root / "data" / "palettes.csv")
    errs += perrs
    tokens = json.loads((ds / "tokens.json").read_text(encoding="utf-8"))
    meta = tokens.get("foundry") or {}
    errs += check_tokens(tokens, int(meta.get("touch_min", 44)), bool(meta.get("operational")))
    master = (ds / "MASTER.md").read_text(encoding="utf-8")
    for sec in REQUIRED_MASTER_SECTIONS:
        if f"## {sec}" not in master:
            errs.append(f"MASTER.md missing section '## {sec}'")
    bad = set(meta.get("text_roles") or []) & set(meta.get("non_text_only") or [])
    if bad:
        errs.append(f"tokens.json: non-text-only role(s) used as text: {', '.join(sorted(bad))}")
    for role in meta.get("text_roles") or []:
        lv = ((tokens.get("color") or {}).get("light") or {}).get(role, {}).get("$value")
        bgv = ((tokens.get("color") or {}).get("light") or {}).get("primary" if role == "primary_fg" else "bg", {}).get("$value")
        if lv and bgv and contrast_ratio(lv, bgv) < 4.5:
            errs.append(f"tokens.json: text role {role} has contrast {contrast_ratio(lv, bgv):.2f} < 4.5")
    comp_ids = {r["id"] for r in _rows("components")}
    inv = master.split("## Components", 1)[1].split("\n## ", 1)[0] if "## Components" in master else ""
    for cid in re.findall(r"^\| `([a-z0-9-]+)` \|", inv, re.M):
        if cid not in comp_ids:
            errs.append(f"MASTER.md component `{cid}` not in components.csv")
    return errs


# ----------------------------------------------------------------------------- phase 8: screens
def _screen_section(root: Path, pack: dict, screen_id: str) -> str:
    p = root / "packs" / pack["slug"] / (pack.get("reference") or {}).get("screens", "reference/screens.md")
    if not p.exists():
        return ""
    text = p.read_text(encoding="utf-8")
    m = re.search(rf"^## {re.escape(screen_id)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def _section_field(section: str, label: str) -> str:
    m = re.search(rf"^\|\s*{re.escape(label)}\s*\|\s*(.*?)\s*\|\s*$", section, re.M)
    return m.group(1) if m else ""


def _ops_for_job(spec: dict, job_id: str) -> tuple[list[str], list[str]]:
    reads, writes = [], []
    for path, methods in (spec.get("paths") or {}).items():
        for m, op in (methods or {}).items():
            if m not in ("get", "post", "patch", "put", "delete"):
                continue
            xf = op.get("x-foundry") or {}
            if xf.get("job") == job_id:
                (reads if m == "get" else writes).append(op["operationId"])
    return reads, writes


def _entity_ops(spec: dict, entity: str) -> tuple[list[str], list[str]]:
    sn = re.sub(r"(?<!^)(?=[A-Z])", "_", entity).lower()
    reads, writes = [], []
    for path, methods in (spec.get("paths") or {}).items():
        for m, op in (methods or {}).items():
            if m not in ("get", "post", "patch", "put", "delete"):
                continue
            oid = op.get("operationId", "")
            if oid in (f"{sn}_list", f"{sn}_get"):
                reads.append(oid)
            elif oid in (f"{sn}_create", f"{sn}_update"):
                writes.append(oid)
    return reads, writes


def _comp_ids_for_screen(screen_id: str, section: str, ptype: dict) -> list[str]:
    all_ids = {r["id"] for r in _rows("components")}
    text = (section + " " + screen_id).lower()
    picked = {"button", "empty-state", "skeleton", "toast"}
    hints = {"numpad": "numpad", "keypad": "tender-keypad", "pin": "pin-pad", "qty": "quantity-stepper", "modifier": "modifier-sheet", "table": "data-table", "kds": "kds-ticket",
             "item grid": "order-card", "floor": "floor-canvas", "receipt": "receipt-preview", "offline": "banner-offline", "split": "split-bill", "chart": "chart-card", "kpi": "kpi-tile",
             "tabs": "tabs", "search": "search", "dialog": "dialog", "modal": "dialog", "sheet": "bottom-sheet", "select": "select", "date": "date-picker", "timeline": "data-table",
             "customer display": "customer-display", "chip": "chip", "badge": "badge", "drawer": "drawer", "list": "virtual-list", "input": "input", "form": "input", "switch": "switch"}
    for k, v in hints.items():
        if k in text:
            picked.add(v)
    if screen_id in ("table-map", "floor-editor"):
        picked |= {"table-map-tile", "floor-canvas"}
    if screen_id in ("order-entry",):
        picked |= {"order-card", "quantity-stepper", "modifier-sheet", "numpad", "banner-offline"}
    if screen_id == "tender":
        picked |= {"tender-keypad", "numpad", "banner-offline"}
    if screen_id in ("shift-open", "shift-close", "manager-pin", "refund"):
        picked.add("pin-pad" if screen_id != "shift-open" else "numpad")
    return sorted(c for c in picked if c in all_ids)


def _rules_for_components(comp_ids: list[str], rtl: bool) -> tuple[list[str], list[str]]:
    rows = _rows("ux-rules")
    a11y, rtl_rules = [], []
    cs = set(comp_ids)
    for r in rows:
        applies = _tags(r["applies_to"])
        if r["category"] in ("accessibility", "touch-interaction") and (applies & cs or "layout" in applies or "page" in applies):
            a11y.append(r["id"])
        if r["category"] == "rtl-i18n" and (applies & cs or "layout" in applies or "text" in applies):
            rtl_rules.append(r["id"])
    a11y = a11y[:8] if len(a11y) >= 3 else [r["id"] for r in rows if r["category"] == "accessibility"][:3]
    return a11y, (rtl_rules[:4] if rtl else [])


def _wireframe(screen_id: str, zones: str, phone: bool = False) -> list[str]:
    w = 34 if phone else 62
    parts = [z.strip() for z in re.split(r";|,", zones) if z.strip()][:4] or ["header", "content", "actions"]
    lines = ["+" + "-" * w + "+", "|" + f" {screen_id} ".ljust(w) + "|", "+" + "-" * w + "+"]
    if phone:
        for p in parts:
            lines += ["|" + f" {p[:w-2]} ".ljust(w) + "|", "|" + " " * w + "|"]
    else:
        half = w // 2
        if len(parts) >= 2:
            left, right = parts[0], parts[1]
            for _ in range(3):
                lines.append("|" + f" {left[:half-2]} ".ljust(half) + "|" + f" {right[:half-3]} ".ljust(w - half - 1) + "|")
            for p in parts[2:]:
                lines += ["+" + "-" * w + "+", "|" + f" {p[:w-2]} ".ljust(w) + "|"]
        else:
            lines += ["|" + f" {parts[0][:w-2]} ".ljust(w) + "|"] * 3
    lines.append("+" + "-" * w + "+")
    return lines[:20]


SCREEN_TYPES = {"order-entry": "order-entry", "tender": "tender", "kds": "kds", "delivery-inbox": "kds", "table-map": "table-map", "floor-editor": "table-map",
                "receipt-preview": "receipt", "reports": "reports", "split-bill": "tender", "refund": "tender", "manager-pin": "tender", "shift-open": "form", "shift-close": "form",
                "end-of-day": "form", "menu-management": "list", "inventory": "list", "purchasing": "list", "staff-roles": "list", "reservations": "list", "customer-lookup": "list",
                "sync-status": "generic", "branch-switcher": "generic", "recipe-editor": "form", "modifier-sheet": "form", "qr-self-order": "order-entry"}


def _copy_rows() -> dict[str, dict]:
    p = DATA / "copy.csv"
    if not p.exists():
        return {}
    with p.open(encoding="utf-8", newline="") as fh:
        return {r["id"]: r for r in csv.DictReader(fh)}


def copy_for(state: str, screen_id: str, langs: list[str]) -> tuple[str, str, str]:
    """(en, ar, ur) for a screen state; falls back to generic type rows."""
    rows = _copy_rows()
    stype = SCREEN_TYPES.get(screen_id, "generic")
    for key in (f"state.{state}.{screen_id}", f"state.{state}.{stype}", f"state.{state}.generic"):
        r = rows.get(key)
        if r:
            return r["en"], r["ar"] if "ar" in langs else "", r["ur"] if "ur" in langs else ""
    return "", "", ""


def screen_spec_md(screen_id: str, jobs: list[dict], pack: dict, section: str, spec: dict, ptype: dict, rtl: bool, route_prefix: str = "/", langs: list[str] | None = None) -> str:
    langs = langs or ["en"]
    personas = sorted({j.get("persona") or "staff" for j in jobs})
    reads, writes = [], []
    for j in jobs:
        r, w = _ops_for_job(spec, j["id"])
        reads += r; writes += w
        if j.get("entity") and j["entity"] != "none":
            er, ew = _entity_ops(spec, j["entity"])
            reads += er; writes += ew
    reads = sorted(set(reads)); writes = sorted(set(writes))
    comps = _comp_ids_for_screen(screen_id, section, ptype)
    a11y, rtl_rules = _rules_for_components(comps, rtl)
    purpose = _section_field(section, "Purpose") or f"{screen_id.replace('-', ' ')} for {', '.join(personas)}"
    actions = _section_field(section, "Primary actions") or "primary action; secondary action"
    zones = _section_field(section, "Layout zones") or "header; content; action bar"
    states_txt = _section_field(section, "States")
    role = _section_field(section, "Role") or personas[0]
    a11y_note = _section_field(section, "A11y")
    rtl_note = _section_field(section, "RTL")
    comps_note = _section_field(section, "Components")
    offline = "offline" in (section + " ".join(pack.get("must_have") or [])).lower() and ptype["density"] == "high"
    print_scope = screen_id in ("receipt-preview", "shift-close", "end-of-day", "reports", "refund") or "print" in section.lower()
    layout = f"{ptype['nav_pattern']} / {ptype['density']} density"
    fm = ["---", f"id: {F._yq(screen_id)}", f"jobs: {F._yq([j['id'] for j in jobs])}", f"personas: {F._yq(personas)}", f"route: {F._yq(route_prefix + screen_id)}",
          f"layout: {F._yq(layout)}", f"components: {F._yq(comps)}", "data:", f"  reads: {F._yq(reads)}", f"  writes: {F._yq(writes)}", "  events: []",
          f"offline: {'true' if offline else 'false'}", f"print: {'true' if print_scope else 'false'}", "---", ""]
    out = fm + [f"# {screen_id}", "", "## Purpose", "", purpose, "", f"Role access: {role}.", "", "## Layout zones", "", "Desktop / tablet:", "", "```"]
    out += _wireframe(screen_id, zones) + ["```", "", "Phone:", "", "```"] + _wireframe(screen_id, zones, phone=True) + ["```", ""]
    out += ["## Actions", "", "| Action | Kind | Component |", "|--------|------|-----------|"]
    for i, a in enumerate([x.strip() for x in re.split(r";", actions) if x.strip()][:8]):
        out.append(f"| {a} | {'primary' if i == 0 else 'secondary'} | `{'button' if 'button' in comps else comps[0]}` |")
    ur_col = "ur" in langs
    out += ["", "## States", "", "| State | Copy (en) | Copy (ar) |" + (" Copy (ur) |" if ur_col else "") + " Notes |", "|-------|-----------|-----------|" + ("-----------|" if ur_col else "") + "-------|"]
    default_copy = {"empty": f"Nothing here yet. Start with {actions.split(';')[0].strip().lower()}.", "loading": "Loading…", "error": "Something went wrong. Retry, or contact the manager.",
                    "offline": "Offline. Changes are saved on this device and sync when the connection returns." if offline else "Read-only while offline.",
                    "locked": "A manager PIN is needed for this action.", "success": "Done."}
    hints = {}
    for part in re.split(r";", states_txt):
        k, _, v = part.partition(":")
        if v.strip():
            hints[k.strip().lower()] = v.strip()
    for st in SCREEN_STATES:
        en, ar, ur = copy_for(st, screen_id, langs)
        hinted = next((v for k, v in hints.items() if st in k), None)
        copy = hinted or en or default_copy[st]
        ar_cell = ar if ar else "<!-- ar: translate -->"
        note = "from screens.md" if hinted else ("copy.csv" if en else "default")
        out.append(f"| {st} | {copy} | {ar_cell} |" + (f" {ur or '<!-- ur: translate -->'} |" if ur_col else "") + f" {note} |")
    out += ["", "## Validation and error copy", "", "- `FRM-02` Error copy says what happened and how to fix it in one sentence.", "- `FRM-01` Validate on blur; re-validate on change after the first error; summarise on submit.",
            "- `FRM-03` Submit stays enabled; errors listed on attempt.", "", "## Keyboard and shortcuts", "", "| Key | Action |", "|-----|--------|"]
    kb = {"kds": [("1–9", "bump ticket in slot"), ("R", "recall last bump"), ("S", "cycle station")], "order-entry": [("digits", "PLU search"), ("Enter", "add highlighted item"), ("Escape", "close sheet")],
          "tender": [("digits", "amount"), ("Enter", "complete"), ("Escape", "cancel card wait")], "table-map": [("Arrows", "move between tables"), ("Enter", "open order")]}
    for k, a in kb.get(screen_id, [("Tab / Shift+Tab", "move focus"), ("Enter", "activate"), ("Escape", "close dialog or sheet")]):
        out.append(f"| {k} | {a} |")
    out += ["", "## Accessibility checklist", ""] + [f"- `{r}`" for r in a11y]
    if a11y_note:
        out.append(f"- Screen note: {a11y_note}")
    out += ["", "## RTL notes", ""] + ([f"- `{r}`" for r in rtl_rules] if rtl_rules else ["- LTR region; logical properties still required."])
    if rtl_note:
        out.append(f"- Screen note: {rtl_note}")
    out += ["", "## Telemetry", "", f"- `screen.{screen_id}.viewed` (persona, branch)", f"- `screen.{screen_id}.action` (action id, duration_ms)", f"- `screen.{screen_id}.error` (code)", "",
            "## Open questions", "", "- none", ""]
    if comps_note:
        out.insert(out.index("## Actions"), f"Components from screens.md: {comps_note}\n")
    return "\n".join(out)


def run_screens_skeleton(project: Path, root: Path) -> int:
    import foundry_phases as P
    sel = F.load_selection(project)
    pack = F.load_pack(root, sel["chosen"])
    ledger = F.load_ledger(project, sel["chosen"])
    ptype = product_type_for(pack)
    jobs_in_scope, _ = P._in_scope_ids(project, pack)
    job_by_id = {j["id"]: j for j in pack.get("jobs") or []}
    spec = F.parse_yaml((project / "openapi.yaml").read_text(encoding="utf-8"))
    region = next((str(d["value"]) for d in ledger.get("decisions", []) if d.get("maps_to") == "region.country" or d["id"] == "region"), "AE")
    reg = (pack.get("regional") or {}).get(region) or {}
    rtl = any(l in ("ar", "ur") for l in (reg.get("receipt_lang") or reg.get("languages") or ["en"]))
    screens: dict[str, list[dict]] = {}
    for jid in jobs_in_scope:
        j = job_by_id.get(jid)
        if not j:
            continue
        for sc in j.get("screens") or []:
            screens.setdefault(sc, []).append(j)
    out_dir = project / ".foundry" / "screens"
    out_dir.mkdir(parents=True, exist_ok=True)
    langs = [str(l) for l in (reg.get("receipt_lang") or reg.get("languages") or ["en"])]
    for sc, jobs in screens.items():
        section = _screen_section(root, pack, sc)
        (out_dir / f"{sc}.md").write_text(screen_spec_md(sc, jobs, pack, section, spec, ptype, rtl, langs=langs), encoding="utf-8", newline="\n")
    print(f"screens-skeleton: {len(screens)} screens for {len(jobs_in_scope)} jobs -> .foundry/screens/")
    return 0


def gate_screens(project: Path, root: Path) -> list[str]:
    import foundry_phases as P
    errs = gate_design(project, root)
    if errs:
        return errs
    sel = F.load_selection(project)
    pack = F.load_pack(root, sel["chosen"])
    ledger = F.load_ledger(project, sel["chosen"])
    jobs_in_scope, _ = P._in_scope_ids(project, pack)
    sdir = project / ".foundry" / "screens"
    files = sorted(sdir.glob("*.md")) if sdir.exists() else []
    if not files:
        return [".foundry/screens/ has no screen files"]
    spec = F.parse_yaml((project / "openapi.yaml").read_text(encoding="utf-8"))
    op_ids = {op.get("operationId") for methods in (spec.get("paths") or {}).values() for m, op in (methods or {}).items() if m in ("get", "post", "patch", "put", "delete")}
    comp_ids = {r["id"] for r in _rows("components")}
    rule_ids = {r["id"] for r in _rows("ux-rules")}
    region = next((str(d["value"]) for d in ledger.get("decisions", []) if d.get("maps_to") == "region.country" or d["id"] == "region"), "AE")
    reg = (pack.get("regional") or {}).get(region) or {}
    rtl = any(l in ("ar", "ur") for l in (reg.get("receipt_lang") or reg.get("languages") or ["en"]))
    jobs_covered: set[str] = set()
    routes: dict[str, str] = {}
    for f in files:
        text = f.read_text(encoding="utf-8")
        try:
            fm_text, _, body = F.split_frontmatter(text)
            fm = F.parse_yaml(fm_text)
        except F.YamlError as e:
            errs.append(f"{f.name}: frontmatter {e}")
            continue
        jobs_covered |= set(fm.get("jobs") or [])
        route = fm.get("route")
        if route in routes:
            errs.append(f"{f.name}: route {route} duplicates {routes[route]}")
        routes[route] = f.name
        for c in fm.get("components") or []:
            if c not in comp_ids:
                errs.append(f"{f.name}: component `{c}` not in components.csv")
        data = fm.get("data") or {}
        for oid in list(data.get("reads") or []) + list(data.get("writes") or []):
            if oid not in op_ids:
                errs.append(f"{f.name}: operationId {oid} not in openapi.yaml")
        states_sec = body.split("## States", 1)[1].split("\n## ", 1)[0] if "## States" in body else ""
        for st in SCREEN_STATES:
            m = re.search(rf"^\| {st} \| (.*?) \|", states_sec, re.M)
            if not m or not m.group(1).strip():
                errs.append(f"{f.name}: state '{st}' missing or empty copy")
        a11y_sec = body.split("## Accessibility checklist", 1)[1].split("\n## ", 1)[0] if "## Accessibility checklist" in body else ""
        a11y_ids = re.findall(r"`([A-Z0-9]+-\d+)`", a11y_sec)
        if len(a11y_ids) < 3:
            errs.append(f"{f.name}: fewer than 3 a11y rule ids")
        for rid in re.findall(r"`([A-Z0-9]+-\d+)`", body):
            if rid not in rule_ids:
                errs.append(f"{f.name}: rule id {rid} not in ux-rules.csv")
        if rtl:
            rtl_sec = body.split("## RTL notes", 1)[1].split("\n## ", 1)[0] if "## RTL notes" in body else ""
            if not re.search(r"`RTL-\d+`", rtl_sec):
                errs.append(f"{f.name}: region is RTL but no RTL rule id cited")
    for jid in jobs_in_scope:
        if jid not in jobs_covered:
            errs.append(f"job {jid} has no screen")
    return errs


GATES = {"design": gate_design, "screens": gate_screens}
