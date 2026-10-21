"""Tests for environment.py, run against a throwaway home folder: python -m unittest discover -s environment/tests"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ENV = Path(__file__).resolve().parent.parent
SCRIPT = ENV / "environment.py"


def is_link(path):
    return path.is_symlink() or (hasattr(os.path, "isjunction") and os.path.isjunction(path))


def make_link(link, target):
    link.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], check=True, capture_output=True)
    else:
        link.symlink_to(target, target_is_directory=True)


class EnvironmentTest(unittest.TestCase):
    def setUp(self):
        self.home = Path(tempfile.mkdtemp())
        self.env = dict(os.environ, HOME=str(self.home), USERPROFILE=str(self.home),
                        GIT_CONFIG_GLOBAL=str(self.home / ".gitconfig"))

    def tearDown(self):
        # A linked hooks folder must be removed as a link, never followed.
        path = self.home / ".githooks"
        if is_link(path):
            os.rmdir(path) if os.name == "nt" else os.unlink(path)
        shutil.rmtree(self.home, ignore_errors=True)

    def run_env(self, *args):
        p = subprocess.run([sys.executable, str(SCRIPT), *args], env=self.env, capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr

    def path(self, rel):
        return self.home / rel

    def settings(self):
        return json.loads(self.path(".claude/settings.json").read_text(encoding="utf-8"))

    def backups(self, name):
        return list((self.home / ".hawk-environment-backups").rglob(name))

    def test_fresh_apply_then_check_is_clean(self):
        code, out = self.run_env("apply")
        self.assertEqual(code, 0, out)
        for rel in (".claude/CLAUDE.md", ".codex/AGENTS.md", ".claude/hooks/hawk/no_ai_in_pr.py", ".githooks/commit-msg"):
            self.assertTrue(self.path(rel).is_file(), rel)
        self.assertIn((ENV / "rules.md").read_text(encoding="utf-8").strip()[:40],
                      self.path(".claude/CLAUDE.md").read_text(encoding="utf-8"))
        code, out = self.run_env("check")
        self.assertEqual(code, 0, out)
        self.assertNotIn("CHANGED", out)
        self.assertNotIn("  missing ", out)

    def test_local_rules_are_appended_and_updated(self):
        local = self.path(".hawk-environment/local/claude.md")
        local.parent.mkdir(parents=True)
        local.write_text("- local rule one\n", encoding="utf-8")
        self.run_env("apply")
        self.assertIn("local rule one", self.path(".claude/CLAUDE.md").read_text(encoding="utf-8"))
        local.write_text("- local rule two\n", encoding="utf-8")
        code, out = self.run_env("check")
        self.assertIn("outdated", out)
        self.assertNotIn("CHANGED", out)
        code, out = self.run_env("apply")
        self.assertEqual(code, 0, out)
        self.assertIn("local rule two", self.path(".claude/CLAUDE.md").read_text(encoding="utf-8"))

    def test_local_rules_with_a_byte_order_mark_or_in_utf16(self):
        local = self.path(".hawk-environment/local/claude.md")
        local.parent.mkdir(parents=True)
        local.write_bytes(b"\xef\xbb\xbf- local rule\n")
        code, out = self.run_env("apply")
        self.assertEqual(code, 0, out)
        text = self.path(".claude/CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("- local rule", text)
        self.assertNotIn("﻿", text)
        local.write_bytes("- other rule\n".encode("utf-16"))
        before = self.path(".claude/CLAUDE.md").read_bytes()
        code, out = self.run_env("apply")
        self.assertEqual(code, 1, out)
        self.assertIn("is not UTF-8 text", out)
        self.assertNotIn("Traceback", out)
        self.assertEqual(self.path(".claude/CLAUDE.md").read_bytes(), before)

    def test_home_edit_is_kept_until_replace_and_then_backed_up(self):
        self.run_env("apply")
        rules = self.path(".claude/CLAUDE.md")
        rules.write_text(rules.read_text(encoding="utf-8") + "- home edit\n", encoding="utf-8")
        code, out = self.run_env("check")
        self.assertEqual(code, 1, out)
        self.assertIn("CHANGED    ~/.claude/CLAUDE.md", out)
        code, out = self.run_env("apply")
        self.assertEqual(code, 1, out)
        self.assertIn("home edit", rules.read_text(encoding="utf-8"))
        code, out = self.run_env("apply", "--replace")
        self.assertEqual(code, 0, out)
        self.assertNotIn("home edit", rules.read_text(encoding="utf-8"))
        self.assertIn("home edit", self.backups("CLAUDE.md")[0].read_text(encoding="utf-8"))

    def test_files_not_written_by_the_script_are_changed_and_others_untouched(self):
        self.path(".codex").mkdir()
        self.path(".codex/AGENTS.md").write_text("my own codex rules\n", encoding="utf-8")
        self.path(".githooks").mkdir()
        self.path(".githooks/commit-msg").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        self.path(".claude/hooks").mkdir(parents=True)
        self.path(".claude/hooks/mine.py").write_text("print(1)\n", encoding="utf-8")
        code, out = self.run_env("check")
        self.assertEqual(code, 1, out)
        self.assertIn("CHANGED    ~/.codex/AGENTS.md", out)
        self.assertIn("CHANGED    ~/.githooks/commit-msg", out)
        code, out = self.run_env("apply", "--replace")
        self.assertEqual(code, 0, out)
        self.assertTrue(self.backups("AGENTS.md") and self.backups("commit-msg"))
        self.assertEqual(self.path(".claude/hooks/mine.py").read_text(encoding="utf-8"), "print(1)\n")

    def test_files_dropped_from_environment_are_removed(self):
        self.run_env("apply")
        stale = self.path(".githooks/old-hook")
        stale.write_bytes(b"#!/bin/sh\n")
        state_path = self.path(".hawk-environment-state.json")
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["files"][".githooks/old-hook"] = hashlib.sha256(b"#!/bin/sh\n").hexdigest()
        state_path.write_text(json.dumps(state), encoding="utf-8")
        code, out = self.run_env("apply")
        self.assertEqual(code, 0, out)
        self.assertFalse(stale.exists())

    def test_settings_keep_user_hooks_and_are_backed_up(self):
        user = {"theme": "dark", "hooks": {"PreToolUse": [{"matcher": "Bash|PowerShell", "hooks": [
            {"type": "command", "command": "echo a"},
            {"type": "command", "command": "old-python -I -c x old/.claude/hooks/hawk/no_ai_in_pr.py"}]}]}}
        self.path(".claude").mkdir()
        # Windows PowerShell 5.1 writes UTF-8 with a byte order mark.
        self.path(".claude/settings.json").write_bytes(b"\xef\xbb\xbf" + json.dumps(user).encode("utf-8"))
        code, out = self.run_env("apply")
        self.assertEqual(code, 0, out)
        text = json.dumps(self.settings())
        self.assertIn("echo a", text)
        self.assertNotIn("old-python", text)
        self.assertEqual(text.count("no_ai_in_pr.py"), 1)
        self.assertEqual(self.settings()["theme"], "dark")
        self.assertEqual(self.settings()["attribution"], {"commit": "", "pr": ""})
        self.assertTrue(self.backups("settings.json"))
        code, out = self.run_env("apply")
        self.assertIn("settings.json already has", out)

    def test_invalid_settings_are_a_problem_and_left_alone(self):
        self.path(".claude").mkdir()
        self.path(".claude/settings.json").write_text("{not json", encoding="utf-8")
        code, out = self.run_env("apply")
        self.assertEqual(code, 1, out)
        self.assertIn("SETTINGS", out)
        self.assertEqual(self.path(".claude/settings.json").read_text(encoding="utf-8"), "{not json")

    def test_registered_hook_blocks_ai_pr_text_and_passes_when_script_is_missing(self):
        self.run_env("apply")
        command = self.settings()["hooks"]["PreToolUse"][-1]["hooks"][0]["command"]
        stdin = json.dumps({"tool_input": {"command": 'gh pr create --title "Made by Claude"'}})
        shells = [None] + ([shutil.which("sh")] if os.name == "nt" and shutil.which("sh") else [])
        for shell in shells:
            def run():
                args = [shell, "-c", command] if shell else command
                return subprocess.run(args, shell=shell is None, input=stdin, capture_output=True, text=True).returncode
            with self.subTest(shell=shell or "default"):
                self.assertEqual(run(), 2)
                script = self.path(".claude/hooks/hawk/no_ai_in_pr.py")
                script.rename(script.with_suffix(".bak"))
                try:
                    self.assertEqual(run(), 0)
                finally:
                    script.with_suffix(".bak").rename(script)

    def test_autocrlf_is_set_and_another_value_needs_replace(self):
        code, out = self.run_env("apply")
        self.assertEqual(code, 0, out)
        get = lambda: subprocess.run(["git", "config", "--global", "--get", "core.autocrlf"], env=self.env,
                                     capture_output=True, text=True).stdout.strip()
        self.assertEqual(get(), "input")
        subprocess.run(["git", "config", "--global", "core.autocrlf", "true"], env=self.env, check=True)
        code, out = self.run_env("check")
        self.assertEqual(code, 1, out)
        self.assertIn("CHANGED    git core.autocrlf is true", out)
        code, out = self.run_env("apply", "--replace", "core.autocrlf")
        self.assertEqual(code, 0, out)
        self.assertEqual(get(), "input")
        state = json.loads(self.path(".hawk-environment-state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["previous core.autocrlf"], "true")

    def test_other_git_hooks_path_needs_replace_and_is_saved(self):
        subprocess.run(["git", "config", "--global", "core.hooksPath", "/other/hooks"], env=self.env, check=True)
        code, out = self.run_env("check")
        self.assertEqual(code, 1, out)
        self.assertIn("CHANGED    git core.hooksPath", out)
        code, out = self.run_env("apply", "--replace")
        self.assertEqual(code, 0, out)
        state = json.loads(self.path(".hawk-environment-state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["previous core.hooksPath"], "/other/hooks")

    def test_nothing_is_written_through_a_linked_hooks_folder_until_replace_names_it(self):
        dotfiles = self.path("dotfiles/githooks")
        dotfiles.mkdir(parents=True)
        (dotfiles / "pre-commit").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        make_link(self.path(".githooks"), dotfiles)
        code, out = self.run_env("apply")
        self.assertEqual(code, 1, out)
        self.assertIn("CHANGED    ~/.githooks is a link", out)
        self.assertEqual([p.name for p in dotfiles.iterdir()], ["pre-commit"])
        self.assertTrue(self.path(".claude/hooks/hawk/no_ai_in_pr.py").is_file())
        code, out = self.run_env("apply", "--replace", "~/.githooks")
        self.assertEqual(code, 0, out)
        self.assertFalse(is_link(self.path(".githooks")))
        self.assertTrue(self.path(".githooks/commit-msg").is_file())
        self.assertEqual([p.name for p in dotfiles.iterdir()], ["pre-commit"])

    def test_replace_takes_only_the_named_items(self):
        for rel, text in ((".claude/CLAUDE.md", "my claude rules\n"), (".codex/AGENTS.md", "my codex rules\n")):
            self.path(rel).parent.mkdir(parents=True, exist_ok=True)
            self.path(rel).write_text(text, encoding="utf-8")
        code, out = self.run_env("apply", "--replace", "~/.codex/AGENTS.md")
        self.assertEqual(code, 1, out)
        self.assertEqual(self.path(".claude/CLAUDE.md").read_text(encoding="utf-8"), "my claude rules\n")
        self.assertNotEqual(self.path(".codex/AGENTS.md").read_text(encoding="utf-8"), "my codex rules\n")
        self.assertTrue(self.backups("AGENTS.md"))
        self.assertFalse(self.backups("CLAUDE.md"))
        code, out = self.run_env("apply", "--replace", "~/.claude/CLAUDE.mdx")
        self.assertEqual(code, 1, out)
        self.assertIn("UNKNOWN    --replace ~/.claude/CLAUDE.mdx", out)


if __name__ == "__main__":
    unittest.main()
