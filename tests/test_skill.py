from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "codex-doc-first-development"


def load_module(name: str, relative: str):
    path = SKILL_ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fenced_template(markdown: str, heading: str) -> str:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*$\n+```(?:markdown)?\n(.*?)^```$",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(markdown)
    if not match:
        raise AssertionError(f"missing fenced template: {heading}")
    return match.group(1).strip()


checker = load_module("check_task_pack", "scripts/check_task_pack.py")
scaffolder = load_module("scaffold_docs", "scripts/scaffold_docs.py")


VALID_TASK = """# TASK-001: Add CSV export

## Status
ready

## Requirement IDs
- REQ-001

## Objective
Export the filtered dashboard rows as UTF-8 CSV.

## Context Pack

### Must Read
- docs/requirements.md
- docs/architecture.md

### Allowed Files
- src/export.py
- tests/test_export.py

### Forbidden Files
- None outside Allowed Files.

### Interfaces / Contracts
- Preserve the existing export function signature.

### Data Constraints
- Preserve visible row order and UTF-8 text.

### UI Constraints
- Not applicable: this task only changes export logic.

## Implementation Requirements
- Escape commas, quotes, and newlines according to RFC 4180.

## Test Requirements
- Run `python -m unittest tests.test_export`.

## Acceptance Criteria
- Filtered rows are exported in visible order with the expected columns.

## Done Definition
- Acceptance criteria are met and required checks pass.

## Risks
- Spreadsheet formula injection is neutralized.

## Output Required
- Changed files.
- Test commands and results.
- Notes and risks.
"""


class TaskPackTests(unittest.TestCase):
    def test_valid_task_pack_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "TASK-001.md"
            path.write_text(VALID_TASK, encoding="utf-8")
            self.assertEqual(checker.check_task_pack(path), [])

    def test_scaffolded_task_requires_completion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scaffolder.scaffold(root, "quick", "001", False)
            issues = checker.check_task_pack(root / "docs/delivery/TASK-001.md")
            self.assertTrue(any("Objective" in issue for issue in issues))
            self.assertTrue(any("Allowed Files" in issue for issue in issues))
            self.assertTrue(any("Interfaces / Contracts" in issue for issue in issues))

    def test_missing_file_has_clean_cli_error(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SKILL_ROOT / "scripts/check_task_pack.py"),
                "missing-task-pack.md",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("file not found", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_heading_and_filename_id_mismatch_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "TASK-001.md"
            text = VALID_TASK.replace("# TASK-001:", "# TASK-002:")
            path.write_text(text + "\n## Risks\n- Duplicate.\n", encoding="utf-8")
            issues = checker.check_task_pack(path)
            self.assertTrue(any("does not match filename" in issue for issue in issues))
            self.assertIn("duplicate heading: Risks", issues)


class ScaffoldTests(unittest.TestCase):
    def test_strict_optional_docs_are_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scaffolder.scaffold(root, "strict", "001", False)
            self.assertTrue((root / "docs/delivery/locks.yml").is_file())
            self.assertTrue((root / "docs/verification/quality-gate.md").is_file())
            self.assertFalse((root / "docs/api.md").exists())
            self.assertFalse((root / "docs/security.md").exists())
            self.assertFalse((root / "docs/decisions/ADR-0001-example.md").exists())

            scaffolder.scaffold(
                root, "strict", "001", False, include=("api", "security")
            )
            self.assertTrue((root / "docs/api.md").is_file())
            self.assertTrue((root / "docs/security.md").is_file())

    def test_dry_run_does_not_create_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "not-created"
            planned = scaffolder.scaffold(
                root, "standard", "001", False, dry_run=True
            )
            self.assertGreater(len(planned), 0)
            self.assertFalse(root.exists())

    def test_invalid_phase_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "at least three digits"):
                scaffolder.scaffold(Path(directory), "standard", "phase-one", False)

    def test_optional_docs_are_rejected_outside_strict_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "only valid"):
                scaffolder.scaffold(
                    Path(directory), "standard", "001", False, include=("api",)
                )

    def test_existing_files_are_preserved_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agents = root / "AGENTS.md"
            agents.write_text("user content\n", encoding="utf-8")
            scaffolder.scaffold(root, "quick", "001", False)
            self.assertEqual(agents.read_text(encoding="utf-8"), "user content\n")
            scaffolder.scaffold(root, "quick", "001", True)
            self.assertIn("# AGENTS.md", agents.read_text(encoding="utf-8"))


class PackageTests(unittest.TestCase):
    def test_skill_metadata_and_references(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(len(skill.splitlines()), 500)
        frontmatter = skill.split("---", 2)[1]
        keys = {
            line.split(":", 1)[0].strip()
            for line in frontmatter.splitlines()
            if ":" in line
        }
        self.assertEqual(keys, {"name", "description"})
        self.assertIn("name: codex-doc-first-development", frontmatter)
        self.assertEqual(SKILL_ROOT.name, "codex-doc-first-development")

        references = set(re.findall(r"`(references/[^`]+)`", skill))
        self.assertGreater(len(references), 0)
        for reference in references:
            self.assertTrue((SKILL_ROOT / reference).is_file(), reference)

        openai_yaml = (SKILL_ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("$codex-doc-first-development", openai_yaml)
        short = re.search(r'^  short_description: "(.*)"$', openai_yaml, re.MULTILINE)
        self.assertIsNotNone(short)
        self.assertGreaterEqual(len(short.group(1)), 25)
        self.assertLessEqual(len(short.group(1)), 64)

    def test_script_templates_match_reference(self) -> None:
        markdown = (SKILL_ROOT / "references/templates.md").read_text(encoding="utf-8")
        expected = {
            "AGENTS.md": scaffolder.AGENTS,
            "docs/requirements.md": scaffolder.REQUIREMENTS,
            "docs/delivery/phase-001.md": scaffolder.PHASE.format(phase="001"),
            "Task Pack": scaffolder.TASK,
        }
        for heading, template in expected.items():
            self.assertEqual(fenced_template(markdown, heading), template.strip(), heading)

    def test_long_references_have_contents(self) -> None:
        for path in (SKILL_ROOT / "references").glob("*.md"):
            lines = path.read_text(encoding="utf-8").splitlines()
            if len(lines) > 100:
                self.assertIn("## Contents", lines, path.name)


if __name__ == "__main__":
    unittest.main()
