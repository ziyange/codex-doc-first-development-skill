"""Regression checks for routing, instruction drift, and installed examples."""
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "codex-doc-first-development"


class AdaptiveWorkflowTests(unittest.TestCase):
    def test_applicability_policy_is_discoverable_from_workflow_sources(self):
        sources = [MAIN / "SKILL.md", MAIN / "references/methodology.md",
                   MAIN / "references/review-gates.md", MAIN / "references/prompts.md"]
        for source in sources:
            with self.subTest(source=source.name):
                text = source.read_text(encoding="utf-8")
                self.assertIn("adaptive-workflow.md", text)
        self.assertTrue((MAIN / "references/adaptive-workflow.md").is_file())

    def test_superseded_unconditional_instructions_do_not_remain(self):
        obsolete = ["No worker may modify code without a Task Pack.",
                    "first block output MUST be `## CoT Intake Reflection`",
                    "Backend endpoints must support dynamic field filtering",
                    "Quick: minimum docs (`AGENTS.md`",
                    "A Task Pack (`TASK-###.md`) is the only artifact that authorizes code changes."]
        for skill in ROOT.glob("codex-doc-first-*"):
            for source in skill.rglob("*.md"):
                text = source.read_text(encoding="utf-8")
                for instruction in obsolete:
                    self.assertNotIn(instruction, text, str(source))

    def test_companion_cli_examples_use_owning_skill_path(self):
        for skill_name, script in [("codex-doc-first-doc-sync", "check_docs_links.py"),
                                   ("codex-doc-first-task-pack-gate", "check_task_pack.py")]:
            text = (ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")
            match = re.search(r"python (<skill-root>/scripts/" + re.escape(script) + r")", text)
            self.assertIsNotNone(match, skill_name)
            command = ROOT / skill_name / "scripts" / script
            result = subprocess.run([sys.executable, str(command), "--help"],
                                    cwd=ROOT.parent, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
