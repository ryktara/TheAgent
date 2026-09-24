"""`foundry.py setup [--apply]` — the /foundry-setup skill's checks and self-test (P11).

Steps: doctor --build, pnpm + Playwright browsers present, codebase-memory-mcp registered (prints the JSON;
--apply writes it to ~/.claude.json), validate, then a self-test: match on the golden briefs and design-check.
Prints "ready" or the exact missing item. Stdlib only; never reads an API key (subscription-only).
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import foundry as F
import foundry_phases as P

ROOT = Path(__file__).resolve().parents[1]


def _run(cmd: list[str], timeout: int = 120) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace", shell=(sys.platform == "win32"))
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except (OSError, subprocess.SubprocessError) as e:
        return 1, str(e)


def _playwright_browsers_present() -> bool:
    home = Path.home()
    candidates = [home / "AppData" / "Local" / "ms-playwright", home / "Library" / "Caches" / "ms-playwright", home / ".cache" / "ms-playwright"]
    return any(d.exists() and any(d.iterdir()) for d in candidates if d.exists())


def register_cbm(apply: bool) -> str:
    cfg = Path.home() / ".claude.json"
    if P.cbm_registered():
        return "ok"
    if not apply:
        return f"missing: add to {cfg} (or run `foundry.py setup --apply`): {P.CBM_MCP_JSON}"
    try:
        d = json.loads(cfg.read_text(encoding="utf-8")) if cfg.exists() else {}
    except json.JSONDecodeError:
        return f"cannot parse {cfg}; add by hand: {P.CBM_MCP_JSON}"
    d.setdefault("mcpServers", {})["codebase-memory"] = {"command": "codebase-memory-mcp", "args": []}
    cfg.write_text(json.dumps(d, indent=2), encoding="utf-8")
    return f"registered in {cfg} (restart Claude Code)"


def selftest(root: Path) -> list[str]:
    """30-second self-test: every golden brief matches its expected pack; palette contrast passes."""
    import foundry_design as D
    errs: list[str] = []
    briefs = sorted((root / "evals" / "briefs").glob("*.md"))
    for b in briefs:
        exp_p = root / "evals" / "expected" / f"{b.stem}.yaml"
        if not exp_p.exists():
            continue
        exp = F.parse_yaml(exp_p.read_text(encoding="utf-8"))
        body = "\n".join(l for l in b.read_text(encoding="utf-8").splitlines() if not l.startswith("#")).strip()
        res = F.match_brief(body, root)
        if res["chosen"] != exp.get("expected_pack") or res["confidence"] < float(exp.get("min_confidence", 0)):
            errs.append(f"match {b.stem}: chose {res['chosen']} {res['confidence']:.2f}, expected {exp.get('expected_pack')}")
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = D.run_design_check(root, None, True)
    if rc != 0:
        errs.append("design-check: palette contrast failures (see `foundry.py design-check --palettes-only`)")
    return errs


def run_setup(root: Path, apply: bool) -> int:
    t0 = time.time()
    missing: list[str] = []
    print("== doctor --build")
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = P.run_doctor(require_cbm=True)
    print(buf.getvalue().strip())
    if rc != 0:
        missing.append("doctor: a hard requirement is missing (see the table above)")
    print("== pnpm")
    if shutil.which("pnpm"):
        print("pnpm ok")
    elif apply and shutil.which("corepack"):
        code, out = _run(["corepack", "enable"]); code2, out2 = _run(["corepack", "prepare", "pnpm@latest", "--activate"], 300)
        print("pnpm installed via corepack" if shutil.which("pnpm") else "pnpm: corepack ran but pnpm is still not on PATH; open a new terminal")
        if not shutil.which("pnpm"):
            missing.append("pnpm: run `corepack enable && corepack prepare pnpm@latest --activate` in a new terminal")
    else:
        missing.append("pnpm: run `corepack enable && corepack prepare pnpm@latest --activate` (or `foundry.py setup --apply`)")
    print("== playwright browsers")
    if _playwright_browsers_present():
        print("playwright browsers ok")
    elif apply and shutil.which("npx"):
        code, out = _run(["npx", "--yes", "playwright", "install", "chromium"], 900)
        print("playwright chromium installed" if code == 0 else "playwright install failed: " + out[-300:])
        if code != 0:
            missing.append("playwright: run `npx playwright install chromium`")
    else:
        missing.append("playwright browsers: run `npx playwright install chromium` (or `foundry.py setup --apply`)")
    print("== codebase-memory-mcp registration")
    msg = register_cbm(apply)
    print(msg)
    if msg.startswith(("missing", "cannot")):
        missing.append("codebase-memory-mcp: " + msg)
    print("== validate")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        vrc = F.run_validate(root, quiet=True) if hasattr(F, "run_validate") else 0
    print(buf.getvalue().strip() or f"validate rc {vrc}")
    if vrc != 0:
        missing.append("validate: errors above")
    print("== self-test (match on golden briefs + design-check)")
    for e in selftest(root):
        print("  " + e); missing.append("self-test: " + e)
    print(f"\nsetup: {'ready' if not missing else 'NOT READY'} ({time.time() - t0:.0f}s)")
    for m in missing:
        print("  - " + m)
    return 0 if not missing else 1
