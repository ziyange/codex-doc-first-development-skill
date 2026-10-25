#!/usr/bin/env python3
"""
Unit tests for check_docs_links.py slug generation and GFM anchor semantics.

GitHub-flavored Markdown anchors (github-slugger):
- lowercase
- punctuation removed (word characters, whitespace and hyphens survive)
- underscores are KEPT (not folded into hyphens)
- each whitespace character maps to one hyphen; consecutive spaces yield
  consecutive hyphens (no collapsing)
"""

import unittest
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "codex-doc-first-development" / "scripts"
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


if __name__ == "__main__":
    unittest.main()
