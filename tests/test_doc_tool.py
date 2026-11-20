"""Tests for the open and touched commands of hawk-docs' doc-tool.py: python -m unittest discover -s tests"""
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "skills" / "hawk-docs" / "scripts" / "doc-tool.py"


class DocToolCase(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.root = Path(self.folder.name)

    def tearDown(self):
        self.folder.cleanup()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8", newline="\n")
        return path

    def run_tool(self, *args):
        result = subprocess.run(
            [sys.executable, str(TOOL), *args],
            cwd=self.root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True)


class OpenTests(DocToolCase):
    def test_lists_open_questions_and_unfinished_work_items(self):
        self.write(
            "docs/plan.md",
            """
            # Plan

            ## Work items

            - **W1. Import** — status `done`.
            - **W2. Export** — status `in progress`.
            - **W3. Old idea** — status `excluded`.

            ## 7. Open questions

            - Which format?
              - CSV or JSON.
            - Who owns it?

            ## Open it

            - How to open the editor.

            ```
            ## Open questions
            - inside a code block
            ```
            """,
        )
        output = self.run_tool("open", "docs")
        self.assertIn("docs/plan.md:6: status in progress: - **W2. Export**", output)
        self.assertIn("docs/plan.md:11: open: - Which format?", output)
        self.assertIn("docs/plan.md:13: open: - Who owns it?", output)
        for closed in ("W1. Import", "W3. Old idea", "CSV or JSON", "How to open", "inside a code block"):
            self.assertNotIn(closed, output)
        self.assertIn("3 open questions or unfinished work items.", output)

    def test_reads_a_status_column_and_ignores_other_tables(self):
        self.write(
            "docs/plan.md",
            """
            | Item | Status |
            |---|---|
            | Import | done (checked) |
            | Export | needs decision |
            | Notes | replaced by row 3 |

            | Status | Meaning |
            |---|---|
            | fixed | the agent changed it |
            """,
        )
        output = self.run_tool("open", "docs")
        self.assertIn("docs/plan.md:4: status needs decision: | Export | needs decision |", output)
        self.assertIn("1 open questions or unfinished work items.", output)

    def test_a_status_label_wins_over_status_words_in_the_text(self):
        self.write(
            "docs/plan.md",
            """
            - **W1. Export** — needs decision from the owner first. Status: done.
            - **W2. Import** — the parser tests are done. Status: `approved`.
            - **W3. Notes** — waiting approval, then done
            """,
        )
        output = self.run_tool("open", "docs")
        self.assertNotIn("W1. Export", output)
        self.assertIn("docs/plan.md:2: status approved:", output)
        self.assertNotIn("W3. Notes", output)

    def test_reads_a_bold_status_label(self):
        self.write("docs/plan.md", "- **W1. Export** **Status:** done. Needs decision text\n")
        self.assertIn("Nothing open.", self.run_tool("open", "docs"))

    def test_reads_labels_in_italics_and_code(self):
        self.write(
            "docs/plan.md",
            "- W1: one\n  `Status`: approved\n  Verification: done when green\n"
            "- W2: two\n  _Status:_ in progress\n  Verification: tests done\n",
        )
        output = self.run_tool("open", "docs")
        self.assertIn("docs/plan.md:1: status approved:", output)
        self.assertIn("docs/plan.md:4: status in progress:", output)

    def test_reads_a_status_in_underscore_italics(self):
        self.write("docs/plan.md", "- **W1. Export** — Status: _approved_\n")
        self.assertIn("docs/plan.md:1: status approved:", self.run_tool("open", "docs"))

    def test_lists_a_work_item_under_an_open_heading_once(self):
        self.write("docs/plan.md", "## Open work\n\n- **W1. Export** — status `in progress`.\n")
        output = self.run_tool("open", "docs")
        self.assertIn("docs/plan.md:3: open:", output)
        self.assertIn("1 open questions or unfinished work items.", output)

    def test_skips_skill_records(self):
        self.write("docs/generated/hawk-build/plan.md", "## Open questions\n\n- Still open?\n")
        self.assertIn("Nothing open.", self.run_tool("open", "docs"))


class TouchedTests(DocToolCase):
    def setUp(self):
        super().setUp()
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.write("src/parser.py", "VALUE = 1\n")
        self.write("docs/area.md", "# Area\n\nThe parser lives in `src/parser.py`.\nDecision REVIEW-3 applies.\n")
        self.write("docs/other.md", "# Other\n\nNothing related.\n")
        self.git("add", ".")
        self.git("commit", "-q", "-m", "Start")

    def test_lists_lines_that_mention_changed_files(self):
        self.write("src/parser.py", "VALUE = 2\n")
        output = self.run_tool("touched", "docs")
        self.assertIn("docs/area.md:3: src/parser.py: The parser", output)
        self.assertNotIn("other.md", output)

    def test_lists_untracked_files_and_given_names(self):
        self.write("src/writer.py", "VALUE = 3\n")
        self.write("docs/writer.md", "# Writer\n\nSee writer.py.\n")
        output = self.run_tool("touched", "--name", "REVIEW-3", "docs")
        self.assertIn("docs/area.md:4: REVIEW-3:", output)
        self.assertIn("docs/writer.md:3: writer.py:", output)

    def test_finds_root_files_and_non_latin_names_from_a_subfolder(self):
        self.write("top.py", "VALUE = 1\n")
        self.write("src/файл.py", "VALUE = 1\n")
        self.write("docs/notes.md", "# Notes\n\nSee top.py and src/файл.py.\n")
        result = subprocess.run(
            [sys.executable, str(TOOL), "touched", "."],
            cwd=self.root / "docs",
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        hits = result.stdout.splitlines()[0].split(": ")[1].split(", ")
        self.assertEqual(sorted(hits), sorted(["top.py", "src/файл.py"]))

    def test_a_root_file_does_not_match_a_longer_path(self):
        self.write("README.md", "# Changed\n")
        self.write("docs/links.md", "# Links\n\nSee docs/README.md.\nSee the [root](../README.md).\nEach area has a README.md.\n")
        output = self.run_tool("touched", "docs")
        self.assertNotIn("links.md:3", output)
        self.assertNotIn("links.md:5", output)
        self.assertIn("docs/links.md:4: README.md:", output)

    def test_a_file_name_without_extension_is_not_matched_as_a_word(self):
        self.write("bin/build", "echo\n")
        self.write("docs/steps.md", "# Steps\n\nRun the build first.\nOr run bin/build.\n")
        output = self.run_tool("touched", "docs")
        self.assertNotIn("steps.md:3", output)
        self.assertIn("docs/steps.md:4: bin/build:", output)

    def test_refuses_an_option_as_the_base(self):
        result = subprocess.run(
            [sys.executable, str(TOOL), "touched", "--base=--output=x", "docs"],
            cwd=self.root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 2)

    def test_a_changed_doc_does_not_match_itself(self):
        self.write("docs/area.md", "# Area\n\nSee area.md for the parser.\n")
        self.assertIn("No doc line mentions them.", self.run_tool("touched", "docs"))

    def test_compares_with_an_earlier_revision(self):
        self.write("src/parser.py", "VALUE = 2\n")
        self.git("commit", "-q", "-am", "Change parser")
        self.assertIn("No doc line mentions them.", self.run_tool("touched", "docs"))
        self.assertIn("docs/area.md:3:", self.run_tool("touched", "--base", "HEAD~1", "docs"))


if __name__ == "__main__":
    unittest.main()
