"""Tests for the PR hook and the git commit-msg check: python -m unittest discover -s environment/tests"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ENV = Path(__file__).resolve().parent.parent
PR_HOOK = ENV / "claude" / "hooks" / "no_ai_in_pr.py"
CHECK = ENV / "git-hooks" / "_check_message.sh"

# (command, blocked)
COMMANDS = [
    ('gh pr create --title "Fix the hook" --body "Done."', False),
    ('gh pr create --title "Fix" --body "Made by Claude"', True),
    ("gh pr create --title Fix --body @'\nIt's done.\n\nCo-authored-by: Someone\n'@", True),
    ('gh pr edit 3 --body "Generated with AI"', True),
    ('gh pr edit 3 --body "Regenerated with new seed"', False),
    ('gh pr create --title "Support philanthropic donors page"', False),
    ('gh issue comment 4 --body "ask anthropic"', True),
    ('gh pr create --head claude/fix-hooks --title "Fix hooks"', False),
    ('gh pr create --title "Update CLAUDE.md and .claude/settings"', False),
    ('gh pr view 3 --json title', False),
    ('git commit -m "Claude"', False),
    ("cat environment/claude/rules.md", False),
]
# (message, rejected)
MESSAGES = [
    ("Move environment/claude/rules.md.\n", False),
    ("Edit claude.md and the .Claude folder.\n", False),
    ("Merge branch 'claude/foo' into main\n", False),
    ("Fix the hook.\n# ------------------------ >8 ------------------------\ndiff --git a/x b/x\n+claude\n", False),
    ("Update a/b.md c/d.md and claude/x.py\n", False),
    ("Add Claude/Codex support\n", True),
    ("Fix.\n\nCo-authored-by: X <x@y>\n", True),
    ("See https://claude.ai/code\n", True),
    ("Generated with AI\n", True),
    ("Fix \U0001F916\n", True),
]
# Plain sentences both checks must judge the same way: (text, forbidden).
PARITY = [
    ("Regenerated with new seed", False),
    ("Add mesh generated with TRELLIS", False),
    ("Support philanthropic donors page", False),
    ("Rename Claudette sample", False),
    ("Fix review notes from Claude", True),
    ("Thanks Anthropic", True),
    ("Generated with AI", True),
    ("Co-authored-by: Someone", True),
    ("Add ai-generated textures", True),
]


def pr_hook(command):
    stdin = json.dumps({"tool_input": {"command": command}})
    return subprocess.run([sys.executable, "-I", str(PR_HOOK)], input=stdin, capture_output=True, text=True).returncode


def commit_check(message):
    with tempfile.NamedTemporaryFile("wb", delete=False) as f:
        f.write(message.encode("utf-8"))
    try:
        return subprocess.run(["sh", str(CHECK), Path(f.name).as_posix()], capture_output=True).returncode
    finally:
        os.unlink(f.name)


class PrHookTest(unittest.TestCase):
    def test_commands(self):
        for command, blocked in COMMANDS:
            with self.subTest(command=command):
                self.assertEqual(pr_hook(command), 2 if blocked else 0)

    def test_bad_input_passes(self):
        code = subprocess.run([sys.executable, "-I", str(PR_HOOK)], input=b"not json", capture_output=True).returncode
        self.assertEqual(code, 0)


@unittest.skipUnless(shutil.which("sh"), "needs sh")
class CommitMessageTest(unittest.TestCase):
    def test_messages(self):
        for message, rejected in MESSAGES:
            with self.subTest(message=message):
                self.assertEqual(commit_check(message), 1 if rejected else 0)

    def test_both_checks_agree_on_plain_text(self):
        for text, forbidden in PARITY:
            with self.subTest(text=text):
                self.assertEqual(commit_check(text + "\n"), 1 if forbidden else 0)
                self.assertEqual(pr_hook(f'gh pr create --title "{text}"'), 2 if forbidden else 0)


if __name__ == "__main__":
    unittest.main()
