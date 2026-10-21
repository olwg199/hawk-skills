#!/usr/bin/env python3
"""Install the owner's agent environment (the hawk-skills environment/ folder) into the home folder, or check it.
Python 3.9 or later, standard library only.

  apply    (default) write the rule files and hook copies home, merge Claude settings, set the git hooks path
  check    report the state of every item and scan environment/ for private data; change nothing

Every home file this script manages is a plain copy, never a link:
  ~/.claude/CLAUDE.md, ~/.codex/AGENTS.md   environment/rules.md + environment/<agent>/rules.md + this computer's own
                                            ~/.hawk-environment/local/<agent>.md (paths, installed tools; never in git)
  ~/.claude/hooks/hawk/*                    copies of environment/claude/hooks/*
  ~/.githooks/*                             copies of environment/git-hooks/*

A file is `ok` (same as the source), `missing`, `outdated` (this script wrote it and nobody changed it since) or `CHANGED`
(edited at home, or not written by this script). A copy folder that is a link, and another git core.hooksPath, are also
CHANGED; nothing is written through such a link. apply writes missing and outdated files; a CHANGED item is replaced
only when --replace names it (--replace alone names all), after the old one is moved to
~/.hawk-environment-backups/<time>/. Files this script wrote earlier whose source is gone are removed. The state file
~/.hawk-environment-state.json remembers what was written.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent
HOME = Path.home()
STATE = HOME / ".hawk-environment-state.json"
BACKUPS = HOME / ".hawk-environment-backups"
LOCAL = HOME / ".hawk-environment" / "local"

# Rule files: agent name and home target. Built from environment/rules.md, environment/<agent>/rules.md and the local file.
RULES = (
    ("claude", ".claude/CLAUDE.md"),
    ("codex", ".codex/AGENTS.md"),
)
# Folders copied file by file: environment source -> home folder. Only the copied files belong to this script; other
# files in those folders (the user's own hooks) are left alone.
COPIES = (
    ("claude/hooks", ".claude/hooks/hawk"),
    ("git-hooks", ".githooks"),
)
HOOK_SCRIPT = ".claude/hooks/hawk/no_ai_in_pr.py"
HOOKS_PATH = "core.hooksPath"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_bytes(path):
    return path.read_bytes() if path.is_file() else None


def read_rules(path):
    """A rules file as text. A byte order mark (Windows PowerShell writes one) is dropped; a file that is not UTF-8 at all
    (PowerShell's > writes UTF-16) stops the run with a clear message before anything is changed."""
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        raise SystemExit(f"hawk-environment: {path} is not UTF-8 text; save it as UTF-8 and run again. Nothing was changed.")


def build(agent):
    """The home rule file: shared rules, then this agent's rules, then this computer's rules (each only when present)."""
    parts = [read_rules(REPO / "rules.md")]
    for extra in (REPO / agent / "rules.md", LOCAL / f"{agent}.md"):
        if extra.is_file():
            parts.append(read_rules(extra))
    return ("\n\n".join(p.strip() for p in parts if p.strip()) + "\n").encode("utf-8")


def wanted():
    """Every managed home file: {path relative to home: wanted bytes}."""
    files = {rel: build(agent) for agent, rel in RULES}
    for src, dst in COPIES:
        for path in sorted((REPO / src).iterdir()):
            if path.is_file():
                files[f"{dst}/{path.name}"] = path.read_bytes()
    return files


def load_state():
    try:
        state = json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        state = {}
    state.setdefault("files", {})
    return state


def status(rel, want, state):
    """ok, missing, outdated (written by this script and unchanged since) or CHANGED."""
    have = read_bytes(HOME / rel)
    if have is None:
        return "missing"
    if have == want:
        return "ok"
    if state["files"].get(rel) == digest(have):
        return "outdated"
    return "CHANGED"


def backup(path, stamp):
    dest = BACKUPS / stamp / path.relative_to(HOME)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), str(dest))
    return f"~/{dest.relative_to(HOME).as_posix()}"


def is_link(path):
    """A symlink or a Windows junction (works before Python 3.12, which added os.path.isjunction)."""
    if path.is_symlink():
        return True
    try:
        return bool(os.lstat(path).st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
    except (AttributeError, OSError):
        return False


def guard_links(dry, chosen, stamp):
    """A copy folder that is a link (to a dotfiles folder, say) is CHANGED: nothing is written through it unless --replace
    names it, which moves the link to the backups. Return (lines, problems, folders left as links)."""
    lines, problems, blocked = [], 0, set()
    for _, rel in COPIES:
        path = HOME / rel
        if not is_link(path):
            continue
        if chosen(f"~/{rel}") and not dry:
            lines.append(f"backed up  ~/{rel} -> {backup(path, stamp)}")
            continue
        problems += 1
        blocked.add(rel)
        lines.append(f"CHANGED    ~/{rel} is a link; nothing is written through it. apply --replace ~/{rel} moves it to "
                     "the backups")
    return lines, problems, blocked


def chooser(names):
    """Which CHANGED items --replace names: none (no --replace), all (--replace alone) or the listed ones (as ~/<path>,
    a full path under the home folder, or core.hooksPath). Return (chosen(label), set of listed labels)."""
    if names is None:
        return (lambda label: False), set()
    if not names:
        return (lambda label: True), set()
    listed = set()
    home = HOME.as_posix().lower() + "/"
    for name in names:
        name = name.replace("\\", "/")
        if name.lower().startswith(home):
            name = "~/" + name[len(home):]
        listed.add(name if name == HOOKS_PATH or name.startswith("~/") else "~/" + name.lstrip("/"))
    return (lambda label: label in listed), listed


def private_markers():
    """Strings that identify this computer or its user and must not appear in environment/."""
    marks = {str(HOME), HOME.as_posix(), HOME.name}
    if os.name == "nt":
        try:
            import ctypes
            buf = ctypes.create_unicode_buffer(1024)
            if ctypes.windll.kernel32.GetShortPathNameW(str(HOME), buf, 1024):
                marks.update({buf.value, Path(buf.value).name})
        except (AttributeError, OSError):
            pass
    return {m for m in marks if len(m) >= 3}


DRIVE_PATH = re.compile(r"\b[A-Za-z]:[\\/][^\s`'\"]*")


def privacy_scan():
    """Lines in environment/ that name this user, the home folder or an absolute drive path."""
    marks = private_markers()
    found = []
    for path in sorted(REPO.rglob("*")):
        if not path.is_file() or path.suffix == ".pyc":
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(lines, 1):
            hit = next((m for m in marks if m.lower() in line.lower()), None) or (DRIVE_PATH.search(line) or [None])[0]
            if hit:
                found.append(f"{path.relative_to(REPO).as_posix()}:{number} contains '{hit}'")
    return found


def merge_settings(dry, stamp):
    """Make sure ~/.claude/settings.json has the no-AI-attribution keys and the PR hook; keep everything else.

    Return (report line, True when the file cannot be read). Only this script's own hook command is replaced; the
    user's other hooks stay, even in the same matcher entry. The registered command runs the
    script only when it exists, because a missing script would exit 2, which Claude Code treats as "block" for every
    shell command. The old file is copied to the backups before it is rewritten."""
    path = HOME / ".claude" / "settings.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig")) if path.is_file() else {}
        want = json.loads(json.dumps(data))
        want["includeCoAuthoredBy"] = False
        want["attribution"] = {"commit": "", "pr": ""}
        hooks = want.setdefault("hooks", {})
        kept = []
        for entry in hooks.get("PreToolUse", []):
            if not entry.get("hooks"):
                kept.append(entry)
                continue
            others = [h for h in entry["hooks"] if Path(HOOK_SCRIPT).name not in str(h.get("command", ""))]
            if others:
                kept.append({**entry, "hooks": others})
    except (ValueError, AttributeError, TypeError):
        return "SETTINGS   ~/.claude/settings.json is not valid JSON or has an unexpected shape; left unchanged", True
    script = (HOME / HOOK_SCRIPT).as_posix()
    runner = "import os,runpy,sys; p=sys.argv[1]; os.path.isfile(p) and runpy.run_path(p, run_name='__main__')"
    command = f'"{Path(sys.executable).as_posix()}" -I -c "{runner}" "{script}"'
    hooks["PreToolUse"] = kept + [{"matcher": "Bash|PowerShell", "hooks": [{"type": "command", "command": command}]}]
    if want == data:
        return "settings.json already has the attribution keys and the PR hook", False
    if dry:
        return "settings.json needs the attribution keys or the PR hook (apply sets them)", False
    saved = ""
    if path.is_file():
        dest = BACKUPS / stamp / path.relative_to(HOME)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        saved = f" (old file backed up to ~/{dest.relative_to(HOME).as_posix()})"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(want, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return "settings.json: attribution keys and PR hook set" + saved, False


def git_hooks_path(dry, replace, state):
    """Return (report line, True when another hooks path is set and needs --replace)."""
    want = "~/.githooks"
    cur = subprocess.run(["git", "config", "--global", "--get", HOOKS_PATH], capture_output=True, text=True).stdout.strip()
    if cur and Path(os.path.expanduser(cur)).resolve() == (HOME / ".githooks").resolve():
        return f"git {HOOKS_PATH} already ~/.githooks", False
    if cur and not replace:
        return f"CHANGED    git {HOOKS_PATH} is {cur}; apply --replace {HOOKS_PATH} sets {want} and saves the old value", True
    if dry:
        return f"git {HOOKS_PATH} is not set (apply sets {want})", False
    if cur:
        state[f"previous {HOOKS_PATH}"] = cur
    subprocess.run(["git", "config", "--global", HOOKS_PATH, want], check=True)
    return f"git {HOOKS_PATH} set to {want}" + (f" (was {cur}, saved in ~/{STATE.name})" if cur else ""), False


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", nargs="?", default="apply", choices=("apply", "check"))
    parser.add_argument("--replace", nargs="*", metavar="ITEM",
                        help="apply: also replace these CHANGED items (~/<path> or core.hooksPath; none listed: all), "
                             "backed up first")
    args = parser.parse_args()
    dry = args.mode == "check"
    chosen, listed = chooser(None if dry else args.replace)
    state = load_state()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    # The wanted files first, so an unreadable rules file stops the run before anything is written; then the settings,
    # because the hook command they register is safe even while its script is not copied yet.
    all_files = wanted()
    settings_line, problems = merge_settings(dry, stamp)
    link_lines, link_problems, blocked = guard_links(dry, chosen, stamp)
    lines = [settings_line] + link_lines
    problems += link_problems
    known = {f"~/{rel}" for _, rel in COPIES} | {HOOKS_PATH}

    files = {rel: want for rel, want in all_files.items() if not any(rel.startswith(b + "/") for b in blocked)}
    for rel, want in files.items():
        st = status(rel, want, state)
        dst = HOME / rel
        known.add(f"~/{rel}")
        if st == "ok":
            lines.append(f"ok         ~/{rel}")
            state["files"][rel] = digest(want)
            continue
        if st == "CHANGED" and not chosen(f"~/{rel}"):
            problems += 1
            lines.append(f"CHANGED    ~/{rel} was edited at home or not written by this script; apply --replace ~/{rel} "
                         "backs it up and replaces it")
            continue
        if dry:
            lines.append(f"{st:<10} ~/{rel} (apply writes it)")
            continue
        if st == "CHANGED":
            lines.append(f"backed up  ~/{rel} -> {backup(dst, stamp)}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(want)
        if rel.startswith(".githooks/") and os.name != "nt":
            dst.chmod(0o755)
        state["files"][rel] = digest(want)
        lines.append(f"installed  ~/{rel}")

    # Files written earlier whose source is gone (a hook dropped from environment/): removed unless edited since.
    for rel in sorted(set(state["files"]) - set(all_files)):
        if any(rel.startswith(b + "/") for b in blocked):
            continue
        have = read_bytes(HOME / rel)
        if dry:
            if have is not None and digest(have) == state["files"][rel]:
                lines.append(f"stale      ~/{rel} (no longer in environment/; apply removes it)")
            continue
        if have is not None and digest(have) == state["files"][rel]:
            (HOME / rel).unlink()
            lines.append(f"removed    ~/{rel} (no longer in environment/)")
        state["files"].pop(rel)

    if ".githooks" in blocked:
        lines.append(f"git {HOOKS_PATH} not changed while ~/.githooks is a link")
    else:
        line, problem = git_hooks_path(dry, chosen(HOOKS_PATH), state)
        lines.append(line)
        problems += problem
    for name in sorted(listed - known):
        problems += 1
        lines.append(f"UNKNOWN    --replace {name}: no such item (use ~/<path> as printed, or {HOOKS_PATH})")
    for agent, _ in RULES:
        if not (LOCAL / f"{agent}.md").is_file():
            lines.append(f"note       no local rules for {agent}: ~/.hawk-environment/local/{agent}.md is missing")

    private = privacy_scan()
    lines += [f"PRIVATE    {hit} (move it to the local rules before pushing)" for hit in private]

    if not dry:
        STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print(f"hawk-environment {args.mode}")
    for line in lines:
        print("  " + line)
    if problems:
        print(f"{problems} item(s) need a decision; nothing CHANGED was replaced unless --replace named it. apply "
              "--replace <item> backs an item up and replaces it; --replace alone does that for all.")
    if private:
        print(f"{len(private)} line(s) in environment/ name this computer or its user: do not push until they are moved.")
    return 1 if problems or private else 0


if __name__ == "__main__":
    raise SystemExit(main())
