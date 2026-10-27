#!/usr/bin/env python3
"""Check, move, extract, find repeats in, and drop decisions from Markdown docs.

Commands that change files only preview their changes unless --apply is given.
Exit codes: 0 done or nothing found, 1 problems or repeats found, 2 usage or read error.
"""

import argparse
import functools
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote


FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
SETEXT = re.compile(r"^\s{0,3}(=+|-+)\s*$")
NOT_PARAGRAPH = re.compile(r"^\s*([|>#*+-]|\d+[.)]\s|$)")
CODE_SPAN = re.compile(r"(`+)(.+?)\1")
LINK = re.compile(
    r"!?\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*(<[^>]*>|(?:[^()\s]|\([^()\s]*\))+)"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*\)"
)
REFERENCE = re.compile(r"^\s{0,3}\[(?!\^)[^\]]+\]:\s*(<[^>]*>|\S+)")
SCHEME = re.compile(r"^([a-zA-Z][a-zA-Z0-9+.-]*:|//)")
HTML_ANCHOR = re.compile(r"<a\s+(?:id|name)=[\"']([^\"']+)[\"']", re.IGNORECASE)
ATTR_ANCHOR = re.compile(r"\{#([^}\s]+)\}")
ANCHOR_LINE = re.compile(r"^\s*(?:<a\s+(?:id|name)=[\"'][^\"']+[\"']\s*>\s*</a>\s*)+$", re.IGNORECASE)
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$")
TABLE_ROW = re.compile(r"^\s*\|")
SENTENCE_END = re.compile(r"(?<=[.!?;])\s+")


class ToolError(Exception):
    pass


class Doc:
    """A Markdown file kept as lines, saved back with its own line endings and byte-order mark."""

    def __init__(self, path, lines=None, newline="\n"):
        self.path = absolute(path)
        self.bom = False
        self.newline = newline
        self.changed = lines is not None
        if lines is not None:
            self.lines = lines
            return
        try:
            raw = self.path.read_bytes()
            text = raw.decode("utf-8-sig")
        except (OSError, UnicodeDecodeError) as error:
            raise ToolError(f"cannot read {show(self.path)}: {error}") from error
        self.bom = raw.startswith(b"\xef\xbb\xbf")
        self.newline = "\r\n" if "\r\n" in text else "\n"
        self.lines = text.replace("\r\n", "\n").split("\n")

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        text = ("﻿" if self.bom else "") + self.newline.join(self.lines)
        self.path.write_bytes(text.encode("utf-8"))


def absolute(path):
    return Path(os.path.normpath(os.path.abspath(path)))


def show(path):
    try:
        return os.path.relpath(path).replace(os.sep, "/")
    except ValueError:
        return str(path)


@functools.lru_cache(maxsize=None)
def names_in(folder):
    return set(os.listdir(folder))


def exists_exact(path):
    """True when the path exists with exactly this letter case below the current folder (Windows ignores case)."""
    if not path.exists():
        return False
    root = absolute(Path.cwd())
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return True
    folder = root
    for part in parts:
        if part not in names_in(str(folder)):
            return False
        folder = folder / part
    return True


def outside_fences(lines):
    """Yield (index, line) for lines outside fenced code; a fence closes only on its own marker, at least as long."""
    fence = None
    for index, line in enumerate(lines):
        match = FENCE.match(line)
        if fence:
            marker = match.group(2) if match else ""
            if marker[:1] == fence[0] and len(marker) >= len(fence) and not match.group(3).strip():
                fence = None
            continue
        if match and not (match.group(2)[0] == "`" and "`" in match.group(3)):
            fence = match.group(2)
            continue
        yield index, line


def mask_code(line):
    return CODE_SPAN.sub(lambda match: " " * len(match.group(0)), line)


def link_targets(line):
    """Yield (start, end, target) for each link target on a line, outside inline code."""
    masked = mask_code(line)
    spans = [(match.start(1), match.end(1)) for match in LINK.finditer(masked)]
    reference = REFERENCE.match(masked)
    if reference:
        spans.append((reference.start(1), reference.end(1)))
    for start, end in spans:
        raw = line[start:end]
        yield start, end, raw[1:-1] if raw.startswith("<") else raw


def slug(heading):
    """GitHub-style anchor for a heading's text."""
    text = ATTR_ANCHOR.sub("", heading)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("`", "").replace("*", "").replace("~", "").strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def headings(lines):
    """(index, level, anchor) for every ATX or setext heading, with GitHub's -1, -2 suffixes for repeats."""
    found = []
    previous = None
    for index, line in outside_fences(lines):
        atx = HEADING.match(line)
        setext = SETEXT.match(line)
        if atx:
            found.append((index, len(atx.group(1)), atx.group(2)))
        elif setext and previous and previous[0] == index - 1 and not NOT_PARAGRAPH.match(previous[1]):
            found.append((index - 1, 1 if setext.group(1)[0] == "=" else 2, previous[1].strip()))
        previous = (index, line)
    seen = {}
    result = []
    for index, level, text in found:
        explicit = ATTR_ANCHOR.findall(text)
        base = explicit[0] if explicit else slug(text)
        count = seen.get(base, 0)
        seen[base] = count + 1
        result.append((index, level, base if count == 0 else f"{base}-{count}"))
    return result


def anchors(lines):
    names = {anchor for _, _, anchor in headings(lines)}
    for _, line in outside_fences(lines):
        names.update(HTML_ANCHOR.findall(line))
    return {name.lower() for name in names}


def resolve(owner, target):
    """(file, anchor) a relative link from owner points to, or None for external links."""
    if SCHEME.match(target):
        return None
    path_part, _, anchor = target.partition("#")
    path_part = unquote(path_part)
    if not path_part:
        return owner, unquote(anchor)
    if path_part.startswith("/"):
        return absolute(Path.cwd() / path_part.lstrip("/")), unquote(anchor)
    return absolute(owner.parent / path_part), unquote(anchor)


def render(owner, file, anchor):
    relative = "" if file == owner else os.path.relpath(file, owner.parent).replace(os.sep, "/")
    if anchor:
        return f"{relative}#{anchor}"
    return relative or file.name


def rewrite_links(doc, old_owner, new_owner, mapping, indexes):
    """Rewrite link targets on the given lines (outside fenced code) for a move; return [(line, old, new)]."""
    changes = []
    prose = {index for index, _ in outside_fences(doc.lines)}
    for index in indexes:
        if index not in prose:
            continue
        line = doc.lines[index]
        new_line = line
        for start, end, target in sorted(link_targets(line), reverse=True):
            resolved = resolve(old_owner, target)
            if resolved is None:
                continue
            wanted = mapping(*resolved) or resolved
            if resolve(new_owner, target) == wanted:
                continue
            replacement = render(new_owner, *wanted)
            if new_line[start] == "<" or " " in replacement:
                replacement = f"<{replacement}>"
            new_line = new_line[:start] + replacement + new_line[end:]
        if new_line != line:
            doc.lines[index] = new_line
            doc.changed = True
            changes.append((index + 1, line, new_line))
    return changes


def is_record(path):
    """True for a skill working record: a file under a generated/ folder."""
    return "generated" in absolute(path).parts


def expand(paths, records=False):
    """Markdown files from the given files and folders; folders skip skill records unless records is set."""
    files = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(p for p in sorted(path.rglob("*.md")) if records or not is_record(p))
        elif path.is_file():
            files.append(path)
        else:
            raise ToolError(f"not found: {raw}")
    return files


def load_all(paths, extra=(), records=False):
    docs = {}
    for path in [*expand(paths, records), *extra]:
        doc_path = absolute(path)
        if doc_path not in docs:
            docs[doc_path] = Doc(doc_path)
    return docs


def id_pattern(text):
    try:
        return re.compile(rf"(?<![\w-])(?:{text})(?![\w-])")
    except re.error as error:
        raise ToolError(f"invalid --pattern: {error}") from error


def row_id(line, pattern):
    """The ID a decision-log line defines: the first ID of a table row or heading, or the ID a list item starts with."""
    match = pattern.search(line)
    if not match:
        return None
    if TABLE_ROW.match(line) or HEADING.match(line):
        return match.group(0)
    item = LIST_ITEM.match(line)
    if item and re.fullmatch(r"[*_`\[]*", line[item.start(1):match.start()]):
        return match.group(0)
    return None


def section_span(lines, found, heading, level):
    """(start, end) of a heading's section: from its anchor lines above it to the next heading of the same or a
    higher level, leaving that heading's anchor lines and the file's final newline in place."""
    end = next((i for i, lv, _ in found if i > heading and lv <= level), len(lines))
    while end > heading + 1 and ANCHOR_LINE.match(lines[end - 1]):
        end -= 1
    if end == len(lines) and end > heading + 1 and lines[-1] == "":
        end -= 1
    start = heading
    while start > 0 and ANCHOR_LINE.match(lines[start - 1]):
        start -= 1
    return start, end


def item_end(lines, index):
    """Index after a list item and its continuation lines: indented lines, blank lines before indented ones, and
    lazy continuation lines that start nothing new."""
    indent = len(lines[index]) - len(lines[index].lstrip())
    end = index + 1
    while end < len(lines):
        line = lines[end]
        if not line.strip():
            following = next((rest for rest in lines[end:] if rest.strip()), "")
            if len(following) - len(following.lstrip()) <= indent:
                break
        elif len(line) - len(line.lstrip()) <= indent and (
            LIST_ITEM.match(line) or HEADING.match(line) or TABLE_ROW.match(line)
        ):
            break
        end += 1
    return end


def row_span(doc, index):
    """(start, end) of the lines a decision row takes: a table row alone, a heading with its section, a list item
    with its continuation lines."""
    heading = HEADING.match(doc.lines[index])
    if heading:
        return section_span(doc.lines, headings(doc.lines), index, len(heading.group(1)))
    if LIST_ITEM.match(doc.lines[index]):
        return index, item_end(doc.lines, index)
    return index, index + 1


def register_rows(docs, pattern):
    """{ID: [(doc, index)]} for every decision-log line that defines an ID; prose lines that mention one are not rows."""
    rows = {}
    for doc in docs.values():
        for index, line in outside_fences(doc.lines):
            defined = row_id(line, pattern)
            if defined:
                rows.setdefault(defined, []).append((doc, index))
    return rows


def print_changes(doc, changes):
    for number, old, new in changes:
        print(f"{show(doc.path)}:{number}:\n  - {old.strip()}\n  + {new.strip()}")


def finish(docs, apply, extra_note=""):
    changed = [doc for doc in docs if doc.changed]
    if apply:
        for doc in changed:
            doc.save()
        print(f"Applied: {len(changed)} files written.{extra_note}")
    else:
        print(f"Preview only: {len(changed)} files would change.{extra_note} Run again with --apply to write.")
    return 0


def cmd_check(args):
    pattern = id_pattern(args.pattern) if args.pattern else None
    registers = load_all(args.register)
    known = set(register_rows(registers, pattern)) if pattern else set()
    problems = []
    anchor_cache = {}
    checked = {"docs": 0, "ids": 0, "links": 0}
    for doc in load_all(args.docs, records=True).values():
        checked["docs"] += 1
        cites = pattern and doc.path not in registers and not is_record(doc.path)
        for index, line in outside_fences(doc.lines):
            where = f"{show(doc.path)}:{index + 1}"
            if cites:
                for cited in dict.fromkeys(match.group(0) for match in pattern.finditer(line)):
                    checked["ids"] += 1
                    if cited not in known:
                        problems.append(f"{where}: ID {cited} is not in the decision logs")
            for _, _, target in link_targets(line):
                resolved = resolve(doc.path, target)
                if resolved is None:
                    continue
                checked["links"] += 1
                file, anchor = resolved
                if not exists_exact(file):
                    problems.append(f"{where}: broken link {target}: file not found (or wrong letter case)")
                elif anchor and file.is_file() and file.suffix.lower() == ".md":
                    if file not in anchor_cache:
                        anchor_cache[file] = anchors(Doc(file).lines)
                    if anchor.lower() not in anchor_cache[file]:
                        problems.append(f"{where}: broken link {target}: no heading or anchor '{anchor}' in {file.name}")
    for problem in problems:
        print(problem)
    summary = f"{checked['docs']} docs, {checked['ids']} ID citations, {checked['links']} links checked"
    print(f"{len(problems)} problems found ({summary})." if problems else f"No problems ({summary}).")
    return 1 if problems else 0


def cmd_move(args):
    src, dst = absolute(args.src), absolute(args.dst)
    if not src.is_file():
        raise ToolError(f"not found: {args.src}")
    if args.dst.endswith(("/", "\\")) or dst.is_dir():
        dst = dst / src.name
    if dst.suffix.lower() != ".md":
        raise ToolError(f"destination must be a .md file or a folder: {args.dst}")
    if dst.exists():
        raise ToolError(f"already exists: {show(dst)}")
    docs = load_all(args.docs, extra=[src], records=True)
    mapping = lambda file, anchor: (dst, anchor) if file == src else None
    print(f"move {show(src)} -> {show(dst)}")
    for doc in docs.values():
        new_owner = dst if doc.path == src else doc.path
        print_changes(doc, rewrite_links(doc, doc.path, new_owner, mapping, range(len(doc.lines))))
    moved = docs[src]
    moved.path, moved.changed = dst, True
    result = finish(docs.values(), args.apply)
    if args.apply:
        src.unlink()
    return result


def cmd_extract(args):
    src, dst = absolute(args.src), absolute(args.dst)
    wanted = args.anchor.lstrip("#").lower()
    if dst == src or dst.suffix.lower() != ".md":
        raise ToolError(f"destination must be another .md file: {args.dst}")
    docs = load_all(args.docs, extra=[src] + ([dst] if dst.exists() else []), records=True)
    source = docs[src]
    found = headings(source.lines)
    match = next(((i, level) for i, level, anchor in found if anchor.lower() == wanted), None)
    if match is None:
        raise ToolError(f"no heading with anchor '{wanted}' in {show(src)}")
    start, end = section_span(source.lines, found, *match)
    section = range(start, end)
    moved_anchors = {anchor.lower() for i, _, anchor in found if start <= i < end}
    for index in section:
        moved_anchors.update(name.lower() for name in HTML_ANCHOR.findall(source.lines[index]))
    mapping = lambda file, anchor: (dst, anchor) if file == src and anchor.lower() in moved_anchors else None
    print(f"extract {show(src)}#{wanted} (lines {start + 1}-{end}) -> {show(dst)}")
    for doc in docs.values():
        if doc is source:
            print_changes(doc, rewrite_links(doc, src, dst, mapping, section))
            rest = [i for i in range(len(doc.lines)) if i not in section]
            print_changes(doc, rewrite_links(doc, src, src, mapping, rest))
        else:
            print_changes(doc, rewrite_links(doc, doc.path, doc.path, mapping, range(len(doc.lines))))
    moved = source.lines[start:end]
    while moved and not moved[-1].strip():
        moved.pop()
    del source.lines[start:end]
    while start < len(source.lines) and start > 0 and not source.lines[start].strip() and not source.lines[start - 1].strip():
        del source.lines[start]
    source.changed = True
    if dst in docs:
        target = docs[dst]
        while target.lines and not target.lines[-1].strip():
            target.lines.pop()
        target.lines += [""] + moved + [""]
        target.changed = True
    else:
        docs[dst] = Doc(dst, moved + [""], source.newline)
    return finish(docs.values(), args.apply)


def cmd_dupes(args):
    places = {}
    for doc in load_all(args.docs).values():
        for number, text in prose_units(doc.lines):
            key = " ".join(re.sub(r"[^\w ]", " ", text.lower()).split())
            if len(key.split()) >= args.min_words:
                places.setdefault(key, []).append((show(doc.path), number, text))
    repeats = [found for found in places.values() if len(found) > 1]
    for found in repeats:
        text = found[0][2]
        print(f"Repeated in {len(found)} places: \"{text[:120]}{'…' if len(text) > 120 else ''}\"")
        for path, number, _ in found:
            print(f"  {path}:{number}")
    print(f"{len(repeats)} repeated sentences or list items found." if repeats else "No repeats found.")
    return 1 if repeats else 0


def prose_units(lines):
    """(line number, sentence) for prose paragraphs and list items, outside fences, headings and tables."""
    heading_lines = {index for index, _, _ in headings(lines)}
    block, start, last = [], None, None

    def flush():
        if not block:
            return []
        text = " ".join(block)
        text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text).replace("`", "").replace("**", "")
        return [(start + 1, sentence.strip()) for sentence in SENTENCE_END.split(text) if sentence.strip()]

    units = []
    for index, line in outside_fences(lines):
        item = LIST_ITEM.match(line)
        breaks = last is None or index != last + 1
        last = index
        if index in heading_lines or SETEXT.match(line) or TABLE_ROW.match(line) or not line.strip():
            units += flush()
            block, start = [], None
            continue
        if item or breaks or not block:
            units += flush()
            block, start = [], index
        block.append(item.group(1) if item else line.strip())
    units += flush()
    return units


def cmd_drop(args):
    pattern = id_pattern(args.pattern)
    if not pattern.fullmatch(args.id):
        raise ToolError(f"{args.id} does not match --pattern")
    registers = load_all(args.register)
    rows = register_rows(registers, pattern).get(args.id)
    if not rows:
        raise ToolError(f"{args.id} has no row in the decision logs")
    citation = re.compile(rf"(?<![\w-]){re.escape(args.id)}(?![\w-])")
    plain = re.compile(rf"\s?\(\s*{re.escape(args.id)}\s*\)")
    docs = load_all(args.docs)
    docs.update(registers)
    for doc, index, start, end in [(doc, index, *row_span(doc, index)) for doc, index in rows]:
        more = f" (and {end - start - 1} more lines)" if end - start > 1 else ""
        print(f"{show(doc.path)}:{index + 1}: delete row{more}\n  - {doc.lines[index].strip()}")
        doc.lines[start:end] = [None] * (end - start)
        doc.changed = True
    by_hand = 0
    for doc in docs.values():
        for index, line in enumerate(doc.lines):
            if line is None or not citation.search(line):
                continue
            new_line = plain.sub("", line)
            if new_line != line:
                print(f"{show(doc.path)}:{index + 1}: remove citation\n  - {line.strip()}\n  + {new_line.strip()}")
                doc.lines[index] = new_line
                doc.changed = True
            if citation.search(new_line):
                by_hand += 1
                print(f"{show(doc.path)}:{index + 1}: rewrite by hand: {new_line.strip()}")
    for doc in docs.values():
        doc.lines = [line for line in doc.lines if line is not None]
    note = f" {by_hand} lines still cite {args.id} and need rewriting." if by_hand else ""
    return finish(docs.values(), args.apply, note)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)

    check = commands.add_parser("check", help="list unknown decision IDs and broken links or anchors")
    check.add_argument("--register", action="append", default=[], help="decision log file or folder (repeatable)")
    check.add_argument("--pattern", help="regular expression for one decision ID, for example '(?:REVIEW|BILLING)-\\d+'")
    check.add_argument("docs", nargs="+", help="Markdown files or folders to check")

    move = commands.add_parser("move", help="move a doc and fix every link to it")
    move.add_argument("src")
    move.add_argument("dst")
    move.add_argument("docs", nargs="+", help="docs whose links to fix (files or folders)")
    move.add_argument("--apply", action="store_true")

    extract = commands.add_parser("extract", help="move the section under a heading into another doc")
    extract.add_argument("src")
    extract.add_argument("anchor", help="the heading's anchor, for example permissions")
    extract.add_argument("dst")
    extract.add_argument("docs", nargs="+", help="docs whose links to fix (files or folders)")
    extract.add_argument("--apply", action="store_true")

    dupes = commands.add_parser("dupes", help="list sentences and list items repeated across docs")
    dupes.add_argument("docs", nargs="+")
    dupes.add_argument("--min-words", type=int, default=8)

    drop = commands.add_parser("drop", help="delete an obsolete decision and its plain citations")
    drop.add_argument("id")
    drop.add_argument("--register", action="append", required=True, help="decision log file or folder (repeatable)")
    drop.add_argument("--pattern", required=True, help="regular expression for one decision ID")
    drop.add_argument("docs", nargs="+", help="docs whose citations to remove (files or folders)")
    drop.add_argument("--apply", action="store_true")

    args = parser.parse_args()
    if args.command == "check" and bool(args.register) != bool(args.pattern):
        parser.error("--register and --pattern go together")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    handler = {"check": cmd_check, "move": cmd_move, "extract": cmd_extract, "dupes": cmd_dupes, "drop": cmd_drop}
    try:
        return handler[args.command](args)
    except (ToolError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
