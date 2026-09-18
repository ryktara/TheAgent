"""SessionStart: injects .foundry/handoff.md and the active ticket summary (≤30 lines) plus the graph-first rule."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import active_ticket_frontmatter, emit, project_dir, read_payload, safe_main  # noqa: E402


def main() -> None:
    payload = read_payload()
    project = project_dir(payload)
    if not (project / ".foundry").exists():
        return
    parts = ["Foundry project detected. Graph first: use codebase-memory-mcp search_graph / trace_path / get_code_snippet for every navigation question; Grep or Read on source only when the graph returns nothing."]
    handoff = project / ".foundry" / "handoff.md"
    if handoff.exists():
        parts.append("--- .foundry/handoff.md ---")
        parts.append(handoff.read_text(encoding="utf-8")[:4000])
    fm = active_ticket_frontmatter(project)
    if fm:
        lines = fm["_text"].splitlines()
        summary = [l for l in lines if not l.startswith("---")][:30]
        parts.append(f"--- active ticket {fm.get('id')} ({fm.get('_file')}) ---")
        parts.extend(summary)
    emit({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "\n".join(parts)}})


if __name__ == "__main__":
    safe_main(main)
