"""PreToolUse Edit/Write guard. Never denies; adds context when a write lands outside the active ticket's predicted files."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import active_ticket_frontmatter, emit, project_dir, read_payload, safe_main  # noqa: E402


def main() -> None:
    payload = read_payload()
    if payload.get("tool_name") not in ("Edit", "Write", "MultiEdit"):
        return
    path = str((payload.get("tool_input") or {}).get("file_path") or "")
    if not path:
        return
    project = project_dir(payload)
    try:
        rel = Path(path).resolve().relative_to(project).as_posix()
    except ValueError:
        rel = Path(path).as_posix()
    fm = active_ticket_frontmatter(project)
    if not fm:
        return
    predicted = fm.get("files_likely_touched") or []
    if rel.startswith((".foundry/", "tests/")) or "/tests/" in rel or ".test." in rel or ".spec." in rel:
        return
    if any(rel == p or rel.startswith(p.rstrip("/") + "/") or rel.startswith(p) for p in predicted):
        return
    emit({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow",
                                 "additionalContext": f"foundry edit_guard: {rel} is outside the predicted files of the active ticket ({fm.get('id')}): {', '.join(predicted)}. Confirm the ticket needs this file, or note it in the ticket report."}})


if __name__ == "__main__":
    safe_main(main)
