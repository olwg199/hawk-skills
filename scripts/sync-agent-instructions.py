#!/usr/bin/env python3
"""Package the shared skill references; check for drift by default."""

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALL_SKILLS = tuple(sorted(path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")))
PACKAGES = (
    ("agent-instruction-layout.md", ("hawk-knowledge-transfer", "hawk-quick-review")),
    ("report-format.md", ALL_SKILLS),
)


def notice(name):
    return (
        f"<!-- Packaged from docs/{name} in hawk-skills. "
        "Edit that source and run scripts/sync-agent-instructions.py --write. -->\n\n"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="refresh packaged copies")
    mode.add_argument("--check", action="store_true", help="check packaged copies (default)")
    args = parser.parse_args()
    stale = []
    total = 0
    for name, skills in PACKAGES:
        expected = notice(name) + (ROOT / "docs" / name).read_text(encoding="utf-8")
        for skill in skills:
            total += 1
            path = ROOT / "skills" / skill / "references" / name
            if not path.is_file() or path.read_text(encoding="utf-8") != expected:
                stale.append((path, expected))
    if args.write:
        for path, expected in stale:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected.encode("utf-8"))
        print(f"Refreshed {len(stale)} packaged references.")
        return 0
    if stale:
        print("Shared references are out of sync:")
        for path, _ in stale:
            print(f"- {path.relative_to(ROOT)}")
        print("Run python3 scripts/sync-agent-instructions.py --write.")
        return 1
    print(f"All {total} packaged references match their shared sources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
