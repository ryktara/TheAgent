#!/usr/bin/env sh
# Foundry CLI wrapper (macOS/Linux/Git Bash). Usage: scripts/foundry.sh validate
dir="$(cd "$(dirname "$0")" && pwd)"
if command -v python3 >/dev/null 2>&1; then py=python3
elif command -v python >/dev/null 2>&1; then py=python
else echo "Python 3.11+ not found on PATH" >&2; exit 127; fi
exec "$py" "$dir/foundry.py" "$@"
