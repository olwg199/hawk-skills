#!/bin/sh
# Installs the owner's agent environment from this folder (see environment.py). macOS and Linux.
# Usage: ./install.sh [apply|check] [--replace [ITEM ...]]
# --replace (apply only) also replaces CHANGED items after backing them up: the ones listed after it
# (for example --replace ~/.claude/CLAUDE.md core.hooksPath), or all of them when none are listed.
set -e
dir=$(cd "$(dirname "$0")" && pwd)
if command -v python3 >/dev/null 2>&1; then python=python3
elif command -v python >/dev/null 2>&1; then python=python
else echo "Python 3.9 or later is required (the Claude Code PR hook runs on it too). Install it and run again." >&2; exit 1
fi
[ $# -eq 0 ] && set -- apply
exec "$python" "$dir/environment.py" "$@"
