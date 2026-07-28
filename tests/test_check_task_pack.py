#!/usr/bin/env python3
"""
Unit tests for check_task_pack.py (v2.0.0 Benchmark Tests TC-C01 ~ TC-C02)
"""

import unittest
import tempfile
import json
from pathlib import Path
import sys
import os

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "codex-doc-first-development" / "scripts"))

from check_task_pack import check_task_pack, calculate_card_confidence


class TestCheckTaskPack(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tc_c01_binary_confidence_score(self):
        """
        TC-C01: Keyword repeated 10 times in text -> Confidence score S <= 1.0
        """
        card_rules = {
            "mandatory_keywords": ["concurrent", "async"],
            "pattern_contexts": ["lock", "shared_state"]
        }
        # Repeat keyword "concurrent" 10 times
        text = "concurrent " * 10 + " async lock shared_state"
        score = calculate_card_confidence(card_rules, text)
        
        self.assertLessEqual(score, 1.0)
        self.assertGreaterEqual(score, 0.0)
        self.assertEqual(score, 1.0)  # All 4 unique feature items hit

    def test_tc_c02_max_iterations_validation(self):
        """
        TC-C02: MAX_ITERATIONS range validation (1 <= N <= 10)
        """
        valid_task = self.temp_path / "TASK-001.md"
        valid_task.write_text("""# TASK-001: Sample Task

## Status
Planned

## Requirement IDs
- REQ-001

## Objective
Sample objective

## Context Pack
N/A

## Must Read
- docs/README.md

## Allowed Files
- src/auth/*.ts

## Forbidden Files
- src/secret.ts

## Interfaces / Contracts
N/A

## Data Constraints
N/A

## UI Constraints
N/A

## Implementation Requirements
- Implement sample logic

## Test Requirements
- Add unit tests

## Acceptance Criteria
- Tests pass

## Done Definition
Code merged

## Risks
None identified

## Output Required
Task report

MAX_ITERATIONS: 5
""", encoding="utf-8")

        issues = check_task_pack(valid_task)
        self.assertEqual(len(issues), 0, f"Expected 0 issues, got: {issues}")

        # Invalid MAX_ITERATIONS value
        invalid_task = self.temp_path / "TASK-002.md"
        invalid_task.write_text(valid_task.read_text(encoding="utf-8").replace("TASK-001", "TASK-002").replace("MAX_ITERATIONS: 5", "MAX_ITERATIONS: 99"), encoding="utf-8")
        
        issues_invalid = check_task_pack(invalid_task)
        self.assertTrue(any("MAX_ITERATIONS value 99" in issue for issue in issues_invalid))


if __name__ == "__main__":
    unittest.main()
