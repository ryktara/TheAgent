"""PostToolUse metrics: appends one record per tool call to .foundry/metrics.jsonl (tokens_est = chars/4)."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import build_state, project_dir, read_payload, safe_main  # noqa: E402


def main() -> None:
    payload = read_payload()
    project = project_dir(payload)
    metrics = project / ".foundry" / "metrics.jsonl"
    if not metrics.parent.exists():
        return  # not a foundry project
    resp = payload.get("tool_response")
    text = resp if isinstance(resp, str) else json.dumps(resp) if resp is not None else ""
    chars = len(text)
    rec = {"ts": datetime.now(timezone.utc).replace(microsecond=0).isoformat(), "phase": 11, "event": "tool-call",
           "tool": str(payload.get("tool_name") or "?"), "ticket": build_state(project).get("active_ticket") or "",
           "tool_calls": 1, "tokens_out": chars // 4, "note": f"output_chars={chars}"}
    if not rec["ticket"]:
        rec.pop("ticket")
    with metrics.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rec) + "\n")


if __name__ == "__main__":
    safe_main(main)
