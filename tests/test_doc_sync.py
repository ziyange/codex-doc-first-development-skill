#!/usr/bin/env python3
"""
Unit tests for check_docs_links.py slug generation and GFM anchor semantics,
plus end-to-end link checking (moved from test_skill.py when the checker
moved into the codex-doc-first-doc-sync companion skill).

GitHub-flavored Markdown anchors (github-slugger):
- lowercase
- punctuation removed (word characters, whitespace and hyphens survive)
- underscores are KEPT (not folded into hyphens)
- each whitespace character maps to one hyphen; consecutive spaces yield
  consecutive hyphens (no collapsing)
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "codex-doc-first-doc-sync" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import check_docs_links


class TestGFMSlugGeneration(unittest.TestCase):
    def test_underscores_are_preserved(self):
        # GitHub keeps underscores: CONCURRENCY_RACE -> concurrency_race
        slugs = check_docs_links.heading_to_slugs("Card 1: CONCURRENCY_RACE")
        self.assertIn("card-1-concurrency_race", slugs)

    def test_hyphen_impersonating_underscore_is_rejected(self):
        # The historical bug: checkers that fold _ into - accepted anchors
        # that are genuinely broken on GitHub.
        slugs = check_docs_links.heading_to_slugs("Card 1: CONCURRENCY_RACE")
        self.assertNotIn("card-1-concurrency-race", slugs)

    def test_ampersand_leaves_double_hyphen(self):
        # '&' is punctuation: removed, leaving two spaces -> two hyphens.
        slugs = check_docs_links.heading_to_slugs("Matching & Confidence Rules")
        self.assertIn("matching--confidence-rules", slugs)
        self.assertNotIn("matching-confidence-rules", slugs)

    def test_slash_leaves_double_hyphen(self):
        slugs = check_docs_links.heading_to_slugs("S10 Context Pack / Task Pack Generation")
        self.assertIn("s10-context-pack--task-pack-generation", slugs)

    def test_dots_are_removed(self):
        slugs = check_docs_links.heading_to_slugs("1. Introduction")
        self.assertIn("1-introduction", slugs)

    def test_parentheses_are_removed(self):
        slugs = check_docs_links.heading_to_slugs("S16 Main-Agent Acceptance & Code-Doc Traceability")
        self.assertIn("s16-main-agent-acceptance--code-doc-traceability", slugs)

    def test_raw_lowercase_title_is_accepted(self):
        slugs = check_docs_links.heading_to_slugs("Plain Heading")
        self.assertIn("plain heading", slugs)
        self.assertIn("plain-heading", slugs)


class TestAnchorExtraction(unittest.TestCase):
    def test_extract_doc_anchors_includes_underscore_slugs(self):
        content = "# Title\n\n## Card 1: CONCURRENCY_RACE\n\n## Matching & Confidence Rules\n"
        anchors = check_docs_links.extract_doc_anchors(content)
        self.assertIn("card-1-concurrency_race", anchors)
        self.assertIn("matching--confidence-rules", anchors)


class TestLinkCheckerEndToEnd(unittest.TestCase):
    def test_valid_links_and_anchors_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            doc_a = root / "doc_a.md"
            doc_b = root / "doc_b.md"
            doc_a.write_text(
                "# Document A\n\nSee [Doc B](doc_b.md) and [Section B](doc_b.md#section-two).\n",
                encoding="utf-8",
            )
            doc_b.write_text(
                "# Document B\n\n## Section Two\n\nContent.\n",
                encoding="utf-8",
            )
            res = check_docs_links.check_docs_links(root)
            self.assertEqual(res["status"], "passed")
            self.assertEqual(res["total_issues"], 0)

    def test_broken_relative_link_and_anchor_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            doc = root / "readme.md"
            doc.write_text(
                "# Readme\n\n- [Missing File](missing.md)\n- [Bad Anchor](#non-existent)\n",
                encoding="utf-8",
            )
            res = check_docs_links.check_docs_links(root)
            self.assertEqual(res["status"], "failed")
            self.assertEqual(res["total_issues"], 2)

    def test_link_checker_cli_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "test.md").write_text("# Test\n\n[Link](missing.md)\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "check_docs_links.py"),
                    str(root),
                    "--json",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn('"status": "failed"', result.stdout)
            self.assertIn('"total_issues": 1', result.stdout)


if __name__ == "__main__":
    unittest.main()
