"""Foundry phases 11-12 machinery: build state, DoD runner, scaffold (T-000).

Imported by foundry.py; Python 3.11+ stdlib only. Windows-first: commands run through the shell
as a single string so pnpm/npx shims resolve.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import foundry as F

DOD_STEPS = ["typecheck", "lint", "unit", "integration", "e2e-smoke", "a11y-axe", "screenshot", "semgrep", "detect_changes_risk", "spec-review"]
SCRIPT_FOR = {"typecheck": "typecheck", "lint": "lint", "unit": "test:unit", "integration": "test:integration", "e2e-smoke": "e2e:smoke", "a11y-axe": "a11y", "screenshot": "screenshot"}


# ----------------------------------------------------------------------------- build state
def build_state_path(project: Path) -> Path:
    return project / ".foundry" / "build.yaml"


def load_build(project: Path) -> dict:
    p = build_state_path(project)
    if p.exists():
        d = F.parse_yaml(p.read_text(encoding="utf-8"))
        d.setdefault("done", [])
        return d
    return {"cbm_project": None, "indexed_at": None, "generation": 0, "active_ticket": None, "done": [], "blockers": []}


def save_build(project: Path, state: dict) -> None:
    p = build_state_path(project)
    p.parent.mkdir(parents=True, exist_ok=True)
    order = ["cbm_project", "indexed_at", "generation", "active_ticket", "done", "blockers"]
    p.write_text(F.dump_yaml({k: state.get(k) for k in order}), encoding="utf-8", newline="\n")


def find_ticket(project: Path, tid: str) -> Path | None:
    return next(iter((project / ".foundry" / "tickets").glob(f"{tid}-*.md")), None)


def ticket_summary(project: Path, tid: str, max_lines: int = 80) -> str:
    p = find_ticket(project, tid)
    if p is None:
        return f"ticket {tid} not found"
    fm, body = F.split_frontmatter(p.read_text(encoding="utf-8"))[0], F.split_frontmatter(p.read_text(encoding="utf-8"))[2]
    t = F.parse_yaml(fm)
    lines = [f"{t['id']} — {t['title']} [{t['type']}, {t['estimate']}]", f"blockedBy: {', '.join(t.get('blockedBy') or []) or '-'}",
             f"jobs: {', '.join(t.get('jobs') or []) or '-'}", f"screens: {', '.join(t.get('screens') or []) or '-'}",
             f"operations: {', '.join(t.get('operations') or []) or '-'}", f"controls: {', '.join(t.get('controls') or []) or '-'}",
             f"adrs: {', '.join(t.get('adrs') or []) or '-'}", "files_likely_touched:"] + [f"  - {f}" for f in t.get("files_likely_touched") or []]
    lines += ["acceptance_tests:"] + [f"  {i}. {a}" for i, a in enumerate(t.get("acceptance_tests") or [], 1)]
    lines += [f"dod: {', '.join(t.get('dod') or [])}"]
    slice_ = body.split("## Slice", 1)[1].split("\n## ", 1)[0].strip() if "## Slice" in body else ""
    if slice_:
        lines += ["slice: " + slice_[:400]]
    return "\n".join(lines[:max_lines])


def run_build(a, project: Path) -> int:
    state = load_build(project)
    if a.action == "activate":
        if not a.ticket:
            print("build activate: --ticket required"); return 1
        if find_ticket(project, a.ticket) is None:
            print(f"build activate: {a.ticket} not found"); return 1
        state["active_ticket"] = a.ticket
        save_build(project, state)
        print(ticket_summary(project, a.ticket))
        return 0
    if a.action == "complete":
        tid = a.ticket or state.get("active_ticket")
        if not tid:
            print("build complete: no active ticket"); return 1
        if tid not in state["done"]:
            state["done"].append(tid)
        if state.get("active_ticket") == tid:
            state["active_ticket"] = None
        save_build(project, state)
        print(f"build complete: {tid} done ({len(state['done'])} total)")
        return 0
    if a.action == "index":
        state["cbm_project"] = a.name or project.name
        state["indexed_at"] = F._now()
        state["generation"] = int(state.get("generation") or 0) + 1
        save_build(project, state)
        print(f"build index: cbm_project {state['cbm_project']} generation {state['generation']}")
        return 0
    if a.action == "status":
        print(F.dump_yaml({k: state.get(k) for k in ("cbm_project", "indexed_at", "generation", "active_ticket", "done", "blockers")}))
        return 0
    print(f"build: unknown action {a.action}")
    return 1


# ----------------------------------------------------------------------------- DoD runner
def _pkg_scripts(project: Path) -> dict:
    p = project / "package.json"
    try:
        return json.loads(p.read_text(encoding="utf-8")).get("scripts") or {}
    except (OSError, json.JSONDecodeError):
        return {}


def _routes_for_ticket(project: Path, tid: str) -> list[str]:
    p = find_ticket(project, tid)
    routes = []
    if p is None:
        return routes
    t = F.parse_yaml(F.split_frontmatter(p.read_text(encoding="utf-8"))[0])
    for sc in t.get("screens") or []:
        sp = project / ".foundry" / "screens" / f"{sc}.md"
        if sp.exists():
            fm = F.parse_yaml(F.split_frontmatter(sp.read_text(encoding="utf-8"))[0])
            routes.append(fm.get("route") or f"/{sc}")
    if t.get("type") == "scaffold":
        routes = ["/"]
    return routes


def run_cmd(cmd: str, cwd: Path, env: dict | None = None, timeout: int = 1800) -> tuple[int, str, float]:
    start = time.time()
    try:
        r = subprocess.run(cmd, cwd=str(cwd), shell=True, capture_output=True, text=True, timeout=timeout, env={**os.environ, **(env or {})}, encoding="utf-8", errors="replace")
        out = (r.stdout or "") + (r.stderr or "")
        return r.returncode, out, time.time() - start
    except subprocess.TimeoutExpired as e:
        return 124, f"timeout after {timeout}s\n" + str(e.stdout or "")[-2000:], time.time() - start


def _tail(text: str, n: int = 20) -> list[str]:
    return [l.rstrip() for l in text.splitlines()[-n:]]


def run_dod(project: Path, root: Path, tid: str, only: list[str] | None = None) -> int:
    tp = find_ticket(project, tid)
    if tp is None:
        print(f"dod: ticket {tid} not found"); return 1
    t = F.parse_yaml(F.split_frontmatter(tp.read_text(encoding="utf-8"))[0])
    steps = [s for s in (t.get("dod") or DOD_STEPS)]
    steps = [s.replace("detect_changes_risk<=medium", "detect_changes_risk") for s in steps]
    if only:
        steps = [s for s in steps if s in only]
    scripts = _pkg_scripts(project)
    routes = _routes_for_ticket(project, tid)
    env = {"FOUNDRY_TICKET": tid, "FOUNDRY_ROUTES": ",".join(routes), "CI": "1"}
    records = []
    failed = []
    for step in steps:
        rec: dict[str, Any] = {"name": step, "cmd": None, "exit": None, "seconds": 0.0, "tail": [], "skipped": False}
        if step in SCRIPT_FOR:
            script = SCRIPT_FOR[step]
            if script not in scripts:
                rec.update(skipped=True, tail=[f"no package.json script '{script}'"])
            elif step in ("a11y-axe", "screenshot") and not routes:
                rec.update(skipped=True, tail=["no routes declared by the ticket's screens"])
            elif step == "integration" and not list(project.glob("apps/*/src/**/*.int.test.ts")):
                rec.update(skipped=True, tail=["no *.int.test.ts files (integration tag absent)"])
            elif step == "e2e-smoke" and not (project / "tests" / "e2e" / "smoke.spec.ts").exists():
                rec.update(skipped=True, tail=["no tests/e2e/smoke.spec.ts"])
            else:
                rec["cmd"] = f"pnpm run {script}"
                code, out, secs = run_cmd(rec["cmd"], project, env)
                rec.update(exit=code, seconds=round(secs, 1), tail=_tail(out))
        elif step == "semgrep":
            if shutil.which("semgrep"):
                rec["cmd"] = "semgrep --config p/owasp-top-ten --config p/typescript --error --quiet apps packages"
                code, out, secs = run_cmd(rec["cmd"], project, env)
                rec.update(exit=code, seconds=round(secs, 1), tail=_tail(out))
            else:
                rec.update(skipped=True, tail=["semgrep binary not on PATH (warning)"])
        elif step == "detect_changes_risk":
            cj = project / ".foundry" / "reviews" / f"{tid}.changes.json"
            if cj.exists():
                risk = str(json.loads(cj.read_text(encoding="utf-8")).get("risk", "unknown")).lower()
                rec.update(exit=0 if risk in ("low", "medium", "unknown") else 1, tail=[f"risk {risk}"])
            else:
                rec.update(skipped=True, tail=["no changes.json (detect_changes not run)"])
        elif step == "spec-review":
            rj = project / ".foundry" / "reviews" / f"{tid}.code.json"
            if rj.exists():
                verdict = json.loads(rj.read_text(encoding="utf-8")).get("verdict")
                rec.update(exit=0 if verdict == "pass" else 1, tail=[f"verdict {verdict}"])
            else:
                rec.update(skipped=True, tail=["no code review json yet"])
        else:
            rec.update(skipped=True, tail=[f"unknown step {step}"])
        records.append(rec)
        status = "skip" if rec["skipped"] else ("ok" if rec["exit"] == 0 else f"FAIL exit {rec['exit']}")
        print(f"dod {tid} {step:<20} {status:<12} {rec['seconds']:>6.1f}s  {rec['tail'][-1] if rec['tail'] else ''}"[:160])
        if not rec["skipped"] and rec["exit"] != 0:
            failed.append(step)
            for line in rec["tail"]:
                print("    " + line[:200])
        _append_metrics(project, {"ts": F._now(), "phase": 11, "ticket": tid, "event": "tool-call", "tool": f"dod:{step}", "wall_ms": int(rec["seconds"] * 1000), "gate_passed": rec["skipped"] or rec["exit"] == 0})
    passed = not failed
    status_path = project / ".foundry" / "tickets" / f"{tid}.status.yaml"
    prev = F.parse_yaml(status_path.read_text(encoding="utf-8")) if status_path.exists() else {"ticket": tid, "attempts": []}
    prev.setdefault("attempts", []).append({"at": F._now(), "passed": passed, "failed_steps": failed, "steps": [{"name": r["name"], "cmd": r["cmd"], "exit": r["exit"], "seconds": r["seconds"], "skipped": r["skipped"], "tail": r["tail"][-5:]} for r in records]})
    prev["last"] = {"passed": passed, "failed_steps": failed}
    status_path.write_text(_dump_status(prev), encoding="utf-8", newline="\n")
    print(f"dod {tid}: {'PASS' if passed else 'FAIL ' + ', '.join(failed)} ({sum(1 for r in records if r['skipped'])} skipped)")
    return 0 if passed else 1


def _dump_status(d: dict) -> str:
    out = [f"ticket: {F._yq(d['ticket'])}", f"last: {F._yq(d['last'])}", "attempts:"]
    for a in d["attempts"]:
        out.append(f"  - at: {F._yq(a['at'])}")
        out.append(f"    passed: {'true' if a['passed'] else 'false'}")
        out.append(f"    failed_steps: {F._yq(a['failed_steps'])}")
        out.append("    steps:")
        for s in a["steps"]:
            out.append(f"      - {F._yq(s)}")
    return "\n".join(out) + "\n"


def _append_metrics(project: Path, rec: dict) -> None:
    p = project / ".foundry" / "metrics.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rec) + "\n")


# ----------------------------------------------------------------------------- scaffold (T-000)
def _write(project: Path, rel: str, text: str) -> None:
    p = project / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def scaffold_files(project: Path, pack: dict, app_name: str) -> dict[str, str]:
    from foundry_build_templates import TEMPLATES
    files = {}
    for rel, text in TEMPLATES.items():
        files[rel] = text.replace("__APP_NAME__", app_name).replace("__PACK__", pack["slug"])
    return files


def run_scaffold(project: Path, root: Path, stack: str, install: bool = True) -> int:
    if stack != "nextjs-pwa":
        print(f"scaffold: stack {stack} not supported in P7a (nextjs-pwa + hono-node + postgres + prisma only)")
        return 2
    sel = F.load_selection(project)
    pack = F.load_pack(root, sel["chosen"])
    app_name = F._norm(pack["name"]).strip().replace(" ", "-") or "app"
    files = scaffold_files(project, pack, app_name)
    for rel, text in files.items():
        _write(project, rel, text)
    src = project / "prisma" / "schema.prisma"
    if src.exists():
        _write(project, "packages/db/prisma/schema.prisma", src.read_text(encoding="utf-8"))
    ds = project / "design-system" / "tailwind.tokens.css"
    if not ds.exists():
        _write(project, "design-system/tailwind.tokens.css", ":root { --color-primary: #1d4ed8; }\n")
    print(f"scaffold: wrote {len(files)} files for stack nextjs-pwa + hono-node + postgres + prisma")
    if install:
        code, out, secs = run_cmd("pnpm install --no-frozen-lockfile", project, timeout=1800)
        print(f"scaffold: pnpm install exit {code} in {secs:.0f}s")
        if code != 0:
            print("\n".join(_tail(out, 30)))
            return 1
        code, out, secs = run_cmd("pnpm exec playwright install chromium", project, timeout=1800)
        print(f"scaffold: playwright install chromium exit {code} in {secs:.0f}s")
        if code != 0:
            print("\n".join(_tail(out, 15)))
    return 0
