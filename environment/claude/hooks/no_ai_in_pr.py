"""Claude Code PreToolUse hook: block a GitHub PR, issue or release command whose text names an AI helper or a co-author.

User rule: commits and PRs are the user's own. Commit messages are checked by the git commit-msg hook (~/.githooks), which
sees the exact message. Git never sees PR text, so this hook covers gh. It searches the whole command without parsing the
shell: a rare false block on a gh command is cheaper than a missed one. Keep the word list in step with
~/.githooks/_check_message.sh.
"""
import json
import re
import sys

GH = re.compile(r"\bgh\s+(?:pr|issue|release)\s+(?:create|edit|comment|review|merge)\b")
# File names and the PR's branch (Claude Code names worktree branches claude/...) are not text about the change.
ALLOWED = re.compile(r"CLAUDE\.md|\.claude\b|(?:--head|-H)[\s=]+\S+", re.IGNORECASE)
# Whole words only, so "Regenerated", "philanthropic" or "generated with TRELLIS" pass.
FORBIDDEN = re.compile(r"co-authored-by|(?<![a-z])(?:claude|anthropic)(?![a-z])|(?<![a-z])generated (?:with|by) ai(?![a-z])"
                       r"|ai-generated|\U0001F916", re.IGNORECASE)


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace"))
        command = str((data.get("tool_input") or {}).get("command") or "")
    except Exception:
        return 0
    if not GH.search(command):
        return 0
    found = FORBIDDEN.search(ALLOWED.sub("", command))
    if not found:
        return 0
    sys.stderr.write(f"BLOCKED: this GitHub text contains '{found.group(0)}'. PRs, issues and releases are the user's own: "
                     "no co-author, no mention of Claude, Claude Code, Anthropic or AI. Rewrite it and run it again.\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
