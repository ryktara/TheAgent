"""PreToolUse Bash guard (SEC-AGT-02, SEC-AGT-03). Denies destructive or secret-leaking commands; allows everything else."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import emit, read_payload, safe_main  # noqa: E402

DENY = [
    (r"\brm\s+-[a-z]*r[a-z]*f?\s+(/|~|\$HOME|\.\.?)(\s|$)", "recursive delete of a root, home or repo-level path"),
    (r"\brm\s+-[a-z]*r[a-z]*f?\s+/", "recursive delete under /"),
    (r"\bgit\s+push\b.*(--force|-f\b|--force-with-lease)", "force push"),
    (r"\bgit\s+push\b.*\+\S+", "force push via refspec"),
    (r"\bcurl\b[^|]*\|\s*(ba)?sh\b", "piping a download into a shell"),
    (r"\bwget\b[^|]*\|\s*(ba)?sh\b", "piping a download into a shell"),
    (r"\biex\s*\(.*(irm|Invoke-WebRequest)", "PowerShell download-and-execute"),
    (r"(>|>>|\btee\b)\s*\S*\.env(\.[a-z]+)?\b(?!\.example)", "writing to a .env file"),
    (r"(>|>>|\btee\b)\s*\S*(secrets?|credentials?)[^\s]*", "writing to a secrets file"),
    (r"\bnpm\s+publish\b|\bpnpm\s+publish\b|\byarn\s+publish\b", "publishing a package"),
    (r"\bgit\s+reset\s+--hard\b", "hard reset discards work"),
    (r"\bdrop\s+(database|table)\b", "dropping a database or table"),
]


def main() -> None:
    payload = read_payload()
    if payload.get("tool_name") != "Bash":
        return
    cmd = str((payload.get("tool_input") or {}).get("command") or "")
    for pattern, reason in DENY:
        if re.search(pattern, cmd, re.I):
            emit({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                         "permissionDecisionReason": f"foundry bash_guard: {reason} (SEC-AGT-02). Command: {cmd[:120]}"}})
            return
    # allowed: say nothing (fail open)


if __name__ == "__main__":
    safe_main(main)
