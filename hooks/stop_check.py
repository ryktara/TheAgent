"""Stop: runs the fast DoD tier (typecheck, lint, unit) for the active ticket and reports; never blocks."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import build_state, emit, project_dir, read_payload, safe_main  # noqa: E402


def main() -> None:
    payload = read_payload()
    if payload.get("stop_hook_active"):
        return
    project = project_dir(payload)
    tid = build_state(project).get("active_ticket")
    if not tid or not (project / "package.json").exists():
        return
    foundry = Path(__file__).resolve().parents[1] / "scripts" / "foundry.py"
    r = subprocess.run([sys.executable, str(foundry), "dod", "--ticket", tid, "--tier", "fast", "--dir", str(project)],
                       capture_output=True, text=True, timeout=280, encoding="utf-8", errors="replace")
    tail = "\n".join((r.stdout or "").splitlines()[-6:])
    emit({"systemMessage": f"foundry stop_check ({tid}, fast tier): exit {r.returncode}\n{tail}"})


if __name__ == "__main__":
    safe_main(main)
