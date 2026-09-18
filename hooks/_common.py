"""Shared helpers for Foundry hooks. Fail-open: every hook catches everything and exits 0."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def read_payload() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def project_dir(payload: dict) -> Path:
    return Path(payload.get("cwd") or ".").resolve()


def parse_yaml_subset(text: str) -> dict:
    """Tiny reader for .foundry/build.yaml (flat keys, flow lists)."""
    out: dict = {}
    for line in text.splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            out[k.strip()] = [x.strip().strip('"') for x in v[1:-1].split(",") if x.strip()]
        elif v in ("null", ""):
            out[k.strip()] = None
        else:
            out[k.strip()] = v.strip('"')
    return out


def build_state(project: Path) -> dict:
    p = project / ".foundry" / "build.yaml"
    try:
        return parse_yaml_subset(p.read_text(encoding="utf-8"))
    except OSError:
        return {}


def active_ticket_frontmatter(project: Path) -> dict:
    state = build_state(project)
    tid = state.get("active_ticket")
    if not tid:
        return {}
    for p in (project / ".foundry" / "tickets").glob(f"{tid}-*.md"):
        text = p.read_text(encoding="utf-8")
        if text.startswith("---"):
            fm = text.split("---", 2)[1]
            return parse_yaml_subset(fm) | {"_file": p.name, "_text": text}
    return {}


def emit(obj: dict) -> None:
    sys.stdout.write(json.dumps(obj))
    sys.stdout.flush()


def safe_main(fn) -> None:
    try:
        fn()
    except Exception as e:  # fail open
        try:
            sys.stderr.write(f"foundry hook error (ignored): {e}\n")
        except Exception:
            pass
    sys.exit(0)
