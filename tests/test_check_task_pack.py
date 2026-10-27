#!/usr/bin/env python3
"""
Unit tests for check_task_pack.py (Task Pack gate, MAX_ITERATIONS, warnings)
"""

import unittest
import tempfile
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "codex-doc-first-development" / "scripts"))

from check_task_pack import check_task_pack, collect_warnings, detect_dummy_test_patterns


class TestCheckTaskPack(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_detect_dummy_test_patterns(self):
        code_snippet = """
        def test_foo():
            assert True

        def test_bar():
            # assert result == 42
            self.assertTrue(True)
        """
        findings = detect_dummy_test_patterns(code_snippet)
        self.assertGreaterEqual(len(findings), 3)
        self.assertTrue(any("assert True" in f for f in findings))
        self.assertTrue(any("assertTrue(True)" in f for f in findings))
        self.assertTrue(any("Commented out" in f for f in findings))

    def test_collect_warnings_detects_dummy_tests_in_test_requirements(self):
        task = self.temp_path / "TASK-003.md"
        task.write_text("""# TASK-003: Sample Task

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
```python
def test_foo():
    assert True
```

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

        warnings = collect_warnings(task.read_text(encoding="utf-8"))
        self.assertTrue(any("assert True" in w for w in warnings))
        # Dummy patterns are warnings, never issues: the pack itself is valid.
        self.assertEqual(check_task_pack(task), [])

    def test_collect_warnings_flags_legacy_missing_max_iterations(self):
        task = self.temp_path / "TASK-004.md"
        task.write_text("""# TASK-004: Legacy Task

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
""", encoding="utf-8")

        warnings = collect_warnings(task.read_text(encoding="utf-8"))
        self.assertTrue(any("MAX_ITERATIONS heading missing" in w for w in warnings))

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
        invalid_text = (
            valid_task.read_text(encoding="utf-8")
            .replace("TASK-001", "TASK-002")
            .replace("MAX_ITERATIONS: 5", "MAX_ITERATIONS: 99")
        )
        invalid_task.write_text(invalid_text, encoding="utf-8")
        
        issues_invalid = check_task_pack(invalid_task)
        self.assertTrue(any("MAX_ITERATIONS value 99" in issue for issue in issues_invalid))


if __name__ == "__main__":
    unittest.main()
