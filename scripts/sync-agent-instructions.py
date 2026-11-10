#!/usr/bin/env python3
"""Package the shared skill references and the doc sections used in environment/rules.md; check for drift by default."""

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALL_SKILLS = tuple(sorted(path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")))
PACKAGES = (
    ("agent-instruction-layout.md", ("hawk-knowledge-transfer", "hawk-quick-review")),
    ("doc-writing.md", ("hawk-build", "hawk-docs", "hawk-knowledge-transfer", "hawk-mobile-ui-builder")),
    ("report-format.md", ALL_SKILLS),
    ("rules-comparison.md", ("hawk-environment-setup", "hawk-project-rules-review")),
)
# See docs/working-with-agents.md, "Maintaining these skills".
SECTIONS = (
    ("doc-writing.md", "Core rules", "environment/rules.md"),
    ("doc-writing.md", "Code comments", "environment/rules.md"),
)
END_MARKER = "<!-- End of packaged section. -->"


def notice(name):
    return (
        f"<!-- Packaged from docs/{name} in hawk-skills. "
        "Edit that source and run scripts/sync-agent-instructions.py --write. -->\n\n"
    )


def start_marker(name, heading):
    return f'<!-- Packaged from docs/{name} "{heading}"; edit there and run scripts/sync-agent-instructions.py --write. -->'


def section_body(name, heading):
    lines = (ROOT / "docs" / name).read_text(encoding="utf-8").splitlines()
    try:
        start = lines.index(f"## {heading}") + 1
    except ValueError:
        raise SystemExit(f"docs/{name} has no '## {heading}' section.")
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    body = lines[start:end]
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    return body


def fill_section(text, name, heading):
    lines = text.split("\n")
    marker = start_marker(name, heading)
    start = next((i for i, line in enumerate(lines) if line.strip() == marker), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if lines[i].strip() == END_MARKER), None)
    if end is None:
        return None
    indent = lines[start][: len(lines[start]) - len(lines[start].lstrip())]
    body = [indent + line if line.strip() else "" for line in section_body(name, heading)]
    return "\n".join(lines[: start + 1] + body + lines[end:])


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
    targets = {}
    missing = []
    for name, heading, target in SECTIONS:
        total += 1
        path = ROOT / target
        current = targets.get(path, path.read_text(encoding="utf-8"))
        filled = fill_section(current, name, heading)
        if filled is None:
            missing.append(f"- {target}:\n  {start_marker(name, heading)}\n  {END_MARKER}")
            continue
        targets[path] = filled
    for path, expected in targets.items():
        if path.read_text(encoding="utf-8") != expected:
            stale.append((path, expected))
    if args.write:
        for path, expected in stale:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected.encode("utf-8"))
        print(f"Refreshed {len(stale)} packaged files.")
    if missing:
        print("Packaged sections have no place to go; add these two marker lines where the section belongs:")
        print("\n".join(missing))
        return 1
    if args.write:
        return 0
    if stale:
        print("Packaged files are out of sync:")
        for path, _ in stale:
            print(f"- {path.relative_to(ROOT)}")
        print("Run python3 scripts/sync-agent-instructions.py --write.")
        return 1
    print(f"All {total} packaged references and sections match their shared sources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
