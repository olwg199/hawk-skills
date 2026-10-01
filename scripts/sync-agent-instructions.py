#!/usr/bin/env python3
"""Package the shared instruction layout; check for drift by default."""

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/agent-instruction-layout.md"
TARGETS = tuple(
    ROOT / "skills" / name / "references/agent-instruction-layout.md"
    for name in ("hawk-knowledge-transfer", "hawk-quick-review")
)
NOTICE = (
    "<!-- Packaged from docs/agent-instruction-layout.md in hawk-skills. "
    "Edit that source and run scripts/sync-agent-instructions.py --write. -->\n\n"
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="refresh packaged copies")
    mode.add_argument("--check", action="store_true", help="check packaged copies (default)")
    args = parser.parse_args()
    expected = NOTICE + SOURCE.read_text(encoding="utf-8")
    stale = [
        path for path in TARGETS
        if not path.is_file() or path.read_text(encoding="utf-8") != expected
    ]
    if args.write:
        for path in stale:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected.encode("utf-8"))
        print(f"Refreshed {len(stale)} packaged instruction references.")
        return 0
    if stale:
        print("Shared instruction references are out of sync:")
        for path in stale:
            print(f"- {path.relative_to(ROOT)}")
        print("Run python3 scripts/sync-agent-instructions.py --write.")
        return 1
    print("Both packaged instruction references match the shared source.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
