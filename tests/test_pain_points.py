#!/usr/bin/env python3
"""
Validation tests for the 6 domain pain-point cards in references/pain-points.md.

Every card's inspection_cmd must be a runnable command: if it invokes a skill
script (scripts/<name>.py), that script must exist in the skill tree. Cards are
also checked against the required fields of PainPointCardSchema.
"""

import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "codex-doc-first-development"
PAIN_POINTS_MD = SKILL_ROOT / "references" / "pain-points.md"

REQUIRED_CARD_FIELDS = [
    "card_id",
    "title",
    "category",
    "trigger_rules",
    "inspection_cmd",
    "version",
    "last_validated",
]


def extract_cards(content: str) -> list:
    """Extract the 6 pain-point card JSON blocks from pain-points.md."""
    cards = []
    for match in re.finditer(r"```json\s*\n(\{.*?\n\})\s*\n```", content, re.DOTALL):
        cards.append(json.loads(match.group(1)))
    return cards


class TestPainPointCards(unittest.TestCase):
    def setUp(self):
        self.cards = extract_cards(PAIN_POINTS_MD.read_text(encoding="utf-8"))

    def test_six_cards_present(self):
        self.assertEqual(len(self.cards), 6, f"expected 6 cards, found {len(self.cards)}")

    def test_cards_match_schema_required_fields(self):
        for card in self.cards:
            card_id = card.get("card_id", "<unknown>")
            for field in REQUIRED_CARD_FIELDS:
                self.assertIn(field, card, f"card {card_id} missing required field: {field}")
            rules = card["trigger_rules"]
            self.assertIn("mandatory_keywords", rules, f"card {card_id} trigger_rules missing mandatory_keywords")
            self.assertIn("pattern_contexts", rules, f"card {card_id} trigger_rules missing pattern_contexts")

    def test_card_ids_unique_and_categories_match(self):
        ids = [c["card_id"] for c in self.cards]
        self.assertEqual(len(ids), len(set(ids)), "duplicate card_id found")
        for card in self.cards:
            self.assertEqual(card["card_id"], card["category"])

    def test_inspection_cmd_scripts_exist(self):
        # Collect every script available across skill directories (the main
        # skill plus companion skills, before and after the split).
        available = set()
        for scripts_dir in SKILL_ROOT.parent.glob("*/scripts"):
            if scripts_dir.is_dir():
                available.update(p.name for p in scripts_dir.glob("*.py"))

        for card in self.cards:
            cmd = card["inspection_cmd"]
            if not cmd.startswith("python "):
                self.fail(f"card {card['card_id']} inspection_cmd must start with 'python ': {cmd!r}")
            referenced = re.findall(r"scripts/(\w+\.py)", cmd)
            for script in referenced:
                self.assertIn(
                    script,
                    available,
                    f"card {card['card_id']} inspection_cmd references missing script: {script}",
                )

    def test_inspection_cmd_has_no_unknown_flags(self):
        # verify_runtime_trace.py only accepts --mode goal|plan|build
        for card in self.cards:
            cmd = card["inspection_cmd"]
            if "verify_runtime_trace.py" in cmd:
                mode_match = re.search(r"--mode\s+(\S+)", cmd)
                if mode_match:
                    self.assertIn(
                        mode_match.group(1),
                        {"goal", "plan", "build"},
                        f"card {card['card_id']} uses invalid --mode value",
                    )


if __name__ == "__main__":
    unittest.main()
