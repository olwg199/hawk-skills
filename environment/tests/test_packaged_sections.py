"""The doc sections packaged into rules.md match docs/: python -m unittest discover -s environment/tests"""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("sync", ROOT / "scripts" / "sync-agent-instructions.py")
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class PackagedSectionsTest(unittest.TestCase):
    def test_rules_sections_match_their_docs(self):
        for name, heading, target in sync.SECTIONS:
            with self.subTest(section=f"{name}#{heading}"):
                text = (ROOT / target).read_text(encoding="utf-8")
                filled = sync.fill_section(text, name, heading)
                self.assertIsNotNone(filled, f"{target} has no markers for {name}#{heading}")
                self.assertEqual(filled, text, "run python3 scripts/sync-agent-instructions.py --write")
                self.assertIn(sync.section_body(name, heading)[0].strip(), text)

    def test_fill_replaces_only_the_marked_block(self):
        name, heading, _ = sync.SECTIONS[0]
        marker = sync.start_marker(name, heading)
        text = f"1. **Rule.**\n    {marker}\n    old line\n    {sync.END_MARKER}\n2. **Next.**\n"
        filled = sync.fill_section(text, name, heading)
        self.assertNotIn("old line", filled)
        self.assertTrue(filled.startswith(f"1. **Rule.**\n    {marker}\n    "))
        self.assertTrue(filled.endswith(f"    {sync.END_MARKER}\n2. **Next.**\n"))
        self.assertIsNone(sync.fill_section("no markers here\n", name, heading))


if __name__ == "__main__":
    unittest.main()
