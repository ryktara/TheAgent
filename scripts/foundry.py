#!/usr/bin/env python3
"""Foundry CLI. Python 3.11+ standard library only.

Subcommands:
  validate       lint skills, packs, schemas, index.csv  (implemented)
  scaffold-pack  create packs/<slug>/ from the pack schema (implemented)
  query          query data/*.csv                         (P5)
  metrics        summarise .foundry/metrics.jsonl          (P7)
  gate           run a phase gate                          (P7)
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
PACKS_DIR = ROOT / "packs"
SCHEMAS_DIR = ROOT / "schemas"
MAX_SKILL_LINES = 150
INDEX_HEADER = ["slug", "name", "aliases", "keywords", "confidence_threshold"]

# Description must start with one of these (verb or trigger noun), case-insensitive.
TRIGGER_WORDS = {
    # verbs
    "build", "implement", "resume", "write", "edit", "review", "match", "grill", "ask",
    "draft", "model", "design", "specify", "spec", "threat", "map", "split", "release",
    "hand", "handoff", "generate", "create", "validate", "audit", "plan", "run", "scaffold",
    "produce", "derive", "check", "convert", "extract", "compile", "verify", "record",
    "select", "route", "load", "fix", "test", "ship", "deploy", "measure", "score",
    # trigger nouns
    "brief", "pack", "prd", "domain", "architecture", "adr", "schema", "api", "openapi",
    "tokens", "screen", "screens", "ticket", "tickets", "wizard", "metrics", "gate",
    "compliance", "security", "ui", "code", "handoff", "eval", "evals", "glossary",
}


# --------------------------------------------------------------------------- errors
class FoundryError(Exception):
    def __init__(self, path: Path | str, line: int, msg: str):
        self.path, self.line, self.msg = str(path), line, msg
        super().__init__(f"{self.path}:{line}: {msg}")


# --------------------------------------------------------------------------- YAML subset
class YamlError(ValueError):
    def __init__(self, line: int, msg: str):
        self.line, self.msg = line, msg
        super().__init__(f"line {line}: {msg}")


def _scalar(tok: str) -> Any:
    tok = tok.strip()
    if tok == "" or tok in ("null", "~"):
        return None
    if len(tok) >= 2 and tok[0] == tok[-1] and tok[0] in "\"'":
        inner = tok[1:-1]
        return inner.replace('\\"', '"') if tok[0] == '"' else inner.replace("''", "'")
    if tok == "true":
        return True
    if tok == "false":
        return False
    if re.fullmatch(r"-?\d+", tok):
        return int(tok)
    if re.fullmatch(r"-?\d+\.\d+", tok):
        return float(tok)
    return tok


def _split_top(s: str, sep: str = ",") -> list[str]:
    """Split on sep at bracket depth 0, respecting quotes."""
    out, depth, cur, q = [], 0, [], None
    for ch in s:
        if q:
            cur.append(ch)
            if ch == q:
                q = None
            continue
        if ch in "\"'":
            q = ch
            cur.append(ch)
        elif ch in "[{":
            depth += 1
            cur.append(ch)
        elif ch in "]}":
            depth -= 1
            cur.append(ch)
        elif ch == sep and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if "".join(cur).strip() or out:
        out.append("".join(cur))
    return [x for x in out if x.strip() != ""]


def _split_kv(item: str) -> tuple[str, str]:
    q = None
    for i, ch in enumerate(item):
        if q:
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch == ":" and (i + 1 == len(item) or item[i + 1] in " \t"):
            return item[:i].strip(), item[i + 1:].strip()
    raise ValueError(f"expected 'key: value' in {item!r}")


def _flow(tok: str, line: int) -> Any:
    tok = tok.strip()
    if tok.startswith("[") and tok.endswith("]"):
        return [_flow(x, line) for x in _split_top(tok[1:-1])]
    if tok.startswith("{") and tok.endswith("}"):
        d: dict[str, Any] = {}
        for item in _split_top(tok[1:-1]):
            try:
                k, v = _split_kv(item)
            except ValueError as e:
                raise YamlError(line, str(e)) from None
            d[_scalar(k)] = _flow(v, line)
        return d
    if tok.startswith(("[", "{")):
        raise YamlError(line, "unterminated flow collection (multi-line flow is outside the subset)")
    return _scalar(tok)


def _strip_comment(raw: str) -> str:
    q = None
    for i, ch in enumerate(raw):
        if q:
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch == "#" and (i == 0 or raw[i - 1] in " \t"):
            return raw[:i]
    return raw


def parse_yaml(text: str) -> Any:
    """Parse the Foundry YAML subset (see packs/README.md). Raises YamlError."""
    lines: list[tuple[int, int, str]] = []  # (lineno, indent, content)
    for n, raw in enumerate(text.splitlines(), 1):
        if raw.strip().startswith("#"):
            continue
        content = _strip_comment(raw).rstrip()
        if not content.strip():
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise YamlError(n, "tabs in indentation")
        lines.append((n, len(content) - len(content.lstrip(" ")), content.strip()))
    if not lines:
        return {}
    val, idx = _parse_block(lines, 0, lines[0][1])
    if idx != len(lines):
        raise YamlError(lines[idx][0], "unexpected content")
    return val


def _parse_block(lines, idx, indent):
    n, ind, content = lines[idx]
    if content.startswith("- ") or content == "-":
        return _parse_list(lines, idx, indent)
    return _parse_map(lines, idx, indent)


def _parse_list(lines, idx, indent):
    out = []
    while idx < len(lines):
        n, ind, content = lines[idx]
        if ind < indent:
            break
        if ind > indent:
            raise YamlError(n, "unexpected indentation")
        if not (content.startswith("- ") or content == "-"):
            raise YamlError(n, "expected list item")
        rest = content[1:].strip()
        if rest == "":
            if idx + 1 < len(lines) and lines[idx + 1][1] > indent:
                val, idx = _parse_block(lines, idx + 1, lines[idx + 1][1])
                out.append(val)
                continue
            out.append(None)
            idx += 1
            continue
        if rest.startswith(("[", "{")):
            out.append(_flow(rest, n))
            idx += 1
            continue
        if ":" in rest and not rest.startswith(("\"", "'")):
            raise YamlError(n, "block mapping inside a list item is outside the subset; use {k: v}")
        out.append(_scalar(rest))
        idx += 1
    return out, idx


def _parse_map(lines, idx, indent):
    out: dict[str, Any] = {}
    while idx < len(lines):
        n, ind, content = lines[idx]
        if ind < indent:
            break
        if ind > indent:
            raise YamlError(n, "unexpected indentation")
        if content.startswith("- "):
            raise YamlError(n, "list item where mapping key expected")
        try:
            k, v = _split_kv(content)
        except ValueError:
            raise YamlError(n, "expected 'key: value'") from None
        key = _scalar(k)
        if key in out:
            raise YamlError(n, f"duplicate key {key!r}")
        if v == "":
            if idx + 1 < len(lines) and lines[idx + 1][1] > indent:
                val, idx = _parse_block(lines, idx + 1, lines[idx + 1][1])
                out[key] = val
                continue
            out[key] = None
            idx += 1
            continue
        if v in ("|", ">"):
            raise YamlError(n, "multi-line block scalars are outside the subset")
        out[key] = _flow(v, n)
        idx += 1
    return out, idx


def split_frontmatter(text: str) -> tuple[str, int, str]:
    """Return (frontmatter_text, body_start_line, body). Raises YamlError."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise YamlError(1, "missing frontmatter opener '---'")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), i + 2, "\n".join(lines[i + 1:])
    raise YamlError(len(lines), "missing frontmatter closer '---'")


# --------------------------------------------------------------------------- JSON Schema (subset)
_TYPES = {
    "object": dict, "array": list, "string": str, "boolean": bool,
    "integer": int, "number": (int, float), "null": type(None),
}


def _is_type(v: Any, t: str) -> bool:
    if t == "integer":
        return isinstance(v, int) and not isinstance(v, bool)
    if t == "number":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    if t == "boolean":
        return isinstance(v, bool)
    return isinstance(v, _TYPES[t])


def validate_schema(value: Any, schema: dict, path: str = "$") -> list[str]:
    """Minimal JSON Schema 2020-12 validator covering the keywords Foundry schemas use."""
    errs: list[str] = []
    if schema is True or schema == {}:
        return errs
    if schema is False:
        return [f"{path}: not allowed"]
    t = schema.get("type")
    if t is not None:
        types = t if isinstance(t, list) else [t]
        if not any(_is_type(value, x) for x in types):
            return [f"{path}: expected {'/'.join(types)}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{path}: {value!r} not in {schema['enum']}")
    if "const" in schema and value != schema["const"]:
        errs.append(f"{path}: must equal {schema['const']!r}")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errs.append(f"{path}: shorter than {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errs.append(f"{path}: longer than {schema['maxLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errs.append(f"{path}: {value!r} does not match /{schema['pattern']}/")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errs.append(f"{path}: below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errs.append(f"{path}: above maximum {schema['maximum']}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append(f"{path}: fewer than {schema['minItems']} items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errs.append(f"{path}: more than {schema['maxItems']} items")
        if "items" in schema:
            for i, item in enumerate(value):
                errs += validate_schema(item, schema["items"], f"{path}[{i}]")
    if isinstance(value, dict):
        for req in schema.get("required", []):
            if req not in value:
                errs.append(f"{path}: missing required '{req}'")
        props = schema.get("properties", {})
        for k, v in value.items():
            if k in props:
                errs += validate_schema(v, props[k], f"{path}.{k}")
            elif "additionalProperties" in schema:
                ap = schema["additionalProperties"]
                if ap is False:
                    errs.append(f"{path}: unexpected property '{k}'")
                elif isinstance(ap, dict):
                    errs += validate_schema(v, ap, f"{path}.{k}")
    return errs


def load_schema(name: str, schemas_dir: Path | None = None) -> dict:
    return json.loads(((schemas_dir or SCHEMAS_DIR) / name).read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- validate
def _first_word(desc: str) -> str:
    m = re.match(r"\s*([A-Za-z][A-Za-z-]*)", desc or "")
    return m.group(1).lower() if m else ""


def validate_skill(path: Path, schema: dict) -> list[FoundryError]:
    errs: list[FoundryError] = []
    text = path.read_text(encoding="utf-8")
    n_lines = len(text.splitlines())
    if n_lines > MAX_SKILL_LINES:
        errs.append(FoundryError(path, MAX_SKILL_LINES + 1, f"SKILL.md has {n_lines} lines; max {MAX_SKILL_LINES}"))
    try:
        fm_text, _, _ = split_frontmatter(text)
        fm = parse_yaml(fm_text)
    except YamlError as e:
        errs.append(FoundryError(path, e.line + 1 if e.line else 1, f"frontmatter: {e.msg}"))
        return errs
    if not isinstance(fm, dict):
        errs.append(FoundryError(path, 2, "frontmatter is not a mapping"))
        return errs
    for msg in validate_schema(fm, schema):
        errs.append(FoundryError(path, 2, f"frontmatter {msg}"))
    if fm.get("name") and fm["name"] != path.parent.name:
        errs.append(FoundryError(path, 2, f"name '{fm['name']}' != folder '{path.parent.name}'"))
    desc = fm.get("description")
    if isinstance(desc, str):
        fw = _first_word(desc)
        if fw not in TRIGGER_WORDS:
            errs.append(FoundryError(path, 3, f"description must start with a verb or trigger noun; got '{fw}'"))
        if re.match(r"\s*this skill", desc, re.I):
            errs.append(FoundryError(path, 3, "description restates identity ('This skill ...')"))
    return errs


def validate_pack(path: Path, schema: dict) -> list[FoundryError]:
    errs: list[FoundryError] = []
    try:
        data = parse_yaml(path.read_text(encoding="utf-8"))
    except YamlError as e:
        return [FoundryError(path, e.line, e.msg)]
    if not isinstance(data, dict):
        return [FoundryError(path, 1, "pack.yaml is not a mapping")]
    for msg in validate_schema(data, schema):
        errs.append(FoundryError(path, 1, msg))
    if data.get("slug") and data["slug"] != path.parent.name:
        errs.append(FoundryError(path, 1, f"slug '{data['slug']}' != folder '{path.parent.name}'"))
    for key, rel in (data.get("reference") or {}).items():
        if isinstance(rel, str) and not (path.parent / rel).exists():
            errs.append(FoundryError(path, 1, f"reference.{key} -> {rel} does not exist"))
    return errs


def validate_index(path: Path) -> list[FoundryError]:
    packs_dir = path.parent
    if not path.exists():
        return [FoundryError(path, 1, "packs/index.csv missing")]
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return [FoundryError(path, 1, "empty index.csv")]
        if header != INDEX_HEADER:
            return [FoundryError(path, 1, f"header {header} != {INDEX_HEADER}")]
        errs = []
        for n, row in enumerate(reader, 2):
            if len(row) != len(INDEX_HEADER):
                errs.append(FoundryError(path, n, f"expected {len(INDEX_HEADER)} columns, got {len(row)}"))
                continue
            if not (packs_dir / row[0] / "pack.yaml").exists():
                errs.append(FoundryError(path, n, f"pack '{row[0]}' has no pack.yaml"))
            try:
                t = float(row[4])
                if not 0 <= t <= 1:
                    raise ValueError
            except ValueError:
                errs.append(FoundryError(path, n, f"confidence_threshold '{row[4]}' not in [0,1]"))
    return errs


def run_validate(root: Path = ROOT, quiet: bool = False) -> int:
    skills_dir, packs_dir, schemas_dir = root / "skills", root / "packs", root / "schemas"
    errs: list[FoundryError] = []
    checked = 0
    try:
        skill_schema = load_schema("skill-frontmatter.schema.json", schemas_dir)
        pack_schema = load_schema("pack.schema.json", schemas_dir)
        for name in ("decisions.schema.json", "metrics.schema.json"):
            load_schema(name, schemas_dir)
    except (OSError, json.JSONDecodeError) as e:
        print(f"{schemas_dir}:1: cannot load schema: {e}")
        return 1
    for p in sorted(skills_dir.glob("*/SKILL.md")):
        checked += 1
        errs += validate_skill(p, skill_schema)
    for p in sorted(packs_dir.glob("*/pack.yaml")):
        checked += 1
        errs += validate_pack(p, pack_schema)
    errs += validate_index(packs_dir / "index.csv")
    for e in errs:
        print(f"{e.path}:{e.line}: {e.msg}")
    if not quiet:
        print(f"validate: {checked} files checked, {len(errs)} error(s)")
    return 1 if errs else 0


# --------------------------------------------------------------------------- scaffold-pack
PACK_TEMPLATE = """slug: {slug}
name: {title}
aliases: [{title_lower}]
confidence_keywords: [{first_word}]
personas: [owner, staff, customer]
jobs: [{{id: core-job, must: true, screens: [home]}}]
must_have: [core-job]
should_have: []
entities: {{Entity: {{states: [draft, active, closed]}}}}
invariants: ["Entity has exactly one state at a time"]
integrations: {{}}
regional: {{AE: {{tax: "VAT 5%"}}}}
compliance_must: []
nfr_defaults: {{offline: optional}}
stack_default: {{web: nextjs, api: hono, db: postgres}}
ui_profile: {{style: clean-operational, density: medium, touch: 44dp}}
questions: [{{id: region, ask: "Primary country?", default: AE, reversible: true}}]
reference: {{screens: reference/screens.md, workflows: reference/workflows.md, glossary: reference/glossary.csv, compliance: reference/compliance.md, ux_patterns: reference/ux-patterns.md}}
"""

REFERENCE_FILES = {
    "screens.md": "# Screens\n",
    "workflows.md": "# Workflows\n",
    "glossary.csv": "term,definition,aliases\n",
    "compliance.md": "# Compliance\n",
    "ux-patterns.md": "# UX patterns\n",
}


def run_scaffold_pack(slug: str, root: Path = ROOT, force: bool = False) -> int:
    if not re.fullmatch(r"[a-z][a-z0-9]*(-[a-z0-9]+)*", slug):
        print(f"scaffold-pack: slug '{slug}' must be kebab-case")
        return 1
    pack_dir = root / "packs" / slug
    if pack_dir.exists() and not force:
        print(f"scaffold-pack: {pack_dir} already exists (use --force to overwrite)")
        return 1
    (pack_dir / "reference").mkdir(parents=True, exist_ok=True)
    title = " ".join(w.upper() if w in ("pos", "crm", "erp", "hms") else w.capitalize() for w in slug.split("-"))
    (pack_dir / "pack.yaml").write_text(
        PACK_TEMPLATE.format(slug=slug, title=title, title_lower=title.lower(), first_word=slug.split("-")[0]),
        encoding="utf-8",
    )
    for name, body in REFERENCE_FILES.items():
        (pack_dir / "reference" / name).write_text(body, encoding="utf-8")
    print(f"scaffold-pack: created {pack_dir.relative_to(root)}/pack.yaml and reference/ ({len(REFERENCE_FILES)} files)")
    print(f"next: add a row to packs/index.csv -> {slug},{title},{title.lower()},{slug.split('-')[0]},0.7")
    return 0


# --------------------------------------------------------------------------- main
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="foundry", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate", help="lint skills, packs, schemas, index.csv")
    v.add_argument("--root", type=Path, default=ROOT)
    v.add_argument("--quiet", action="store_true")
    s = sub.add_parser("scaffold-pack", help="create packs/<slug>/ from the schema")
    s.add_argument("slug")
    s.add_argument("--root", type=Path, default=ROOT)
    s.add_argument("--force", action="store_true")
    for name in ("query", "metrics", "gate"):
        p = sub.add_parser(name, help="not implemented in P0")
        p.add_argument("args", nargs="*")
    a = ap.parse_args(argv)
    if a.cmd == "validate":
        return run_validate(a.root.resolve(), a.quiet)
    if a.cmd == "scaffold-pack":
        return run_scaffold_pack(a.slug, a.root.resolve(), a.force)
    print(f"foundry {a.cmd}: not implemented in P0")
    return 2


if __name__ == "__main__":
    sys.exit(main())
