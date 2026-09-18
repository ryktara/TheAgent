"""SessionStart: injects the handoff frontmatter + next_command (≤15 lines) and the graph-first rule."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import build_state, emit, project_dir, read_payload, safe_main  # noqa: E402


def main() -> None:
    payload = read_payload()
    project = project_dir(payload)
    if not (project / ".foundry").exists():
        return
    parts = ["Foundry project. Graph first: search_graph / trace_path / get_code_snippet before Grep or Read on source; when search_graph returns 0 rows, run index_repository once and retry."]
    handoff = project / ".foundry" / "handoff.md"
    if handoff.exists():
        text = handoff.read_text(encoding="utf-8")
        if text.startswith("---"):
            fm = text.split("---", 2)[1].strip().splitlines()[:13]
            parts.append("--- handoff ---")
            parts.extend(fm)
        else:
            parts.append("handoff.md has no frontmatter: run `python scripts/foundry.py handoff write`.")
    else:
        st = build_state(project)
        parts.append(f"no handoff.md; active_ticket={st.get('active_ticket')} done={len(st.get('done') or [])}; next: /foundry-build")
    emit({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "\n".join(parts[:15])}})


if __name__ == "__main__":
    safe_main(main)
