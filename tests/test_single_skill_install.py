"""Verify the documented one-directory installation without sibling skills."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "codex-doc-first-development"


class SingleSkillInstallTests(unittest.TestCase):
    def test_repository_distributes_exactly_one_skill(self):
        entries = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.glob("codex-doc-first-*/SKILL.md"))
        self.assertEqual(entries, ["codex-doc-first-development/SKILL.md"])

    def test_all_gates_work_from_only_the_copied_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installed = root / "skills" / SKILL.name
            shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            project = root / "project"
            shutil.copytree(ROOT / "tests/fixtures", project)
            (project / "docs").mkdir()
            (project / "docs/README.md").write_text("# Docs\n\n[Task](../valid_task_pack.md)\n", encoding="utf-8")
            commands = [
                ("check_docs_links.py", [str(project / "docs"), "--json"]),
                ("check_task_pack.py", [str(project / "valid_task_pack.md"), "--json"]),
                ("verify_runtime_trace.py", ["--trace", str(project / "valid_trace.json"),
                                             "--permission-log", str(project / "valid_audit.log"),
                                             "--task-pack", str(project / "valid_task_pack.md"), "--json"]),
            ]
            for script, args in commands:
                with self.subTest(script=script):
                    result = subprocess.run([sys.executable, str(installed / "scripts" / script), *args],
                                            cwd=project, capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    payload = json.loads(result.stdout)
                    self.assertTrue(payload.get("status") == "passed" or payload.get("exit_code") == 0)

    def test_main_skill_has_no_sibling_skill_dependency(self):
        for path in SKILL.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for suffix in ("doc-sync", "task-pack-gate", "ui-ux-prototyping", "start"):
                self.assertNotIn(f"codex-doc-first-{suffix}", text, str(path))
            self.assertIsNone(re.search(r'Call the Skill tool with "codex-doc-first-development"', text), str(path))

    def test_each_checker_has_one_source_owner(self):
        for script in ("check_docs_links.py", "check_task_pack.py"):
            self.assertEqual(list(ROOT.glob(f"codex-doc-first-*/scripts/{script}")), [SKILL / "scripts" / script])

    def test_doc_card_command_works_from_downstream_project(self):
        cards = [json.loads(block) for block in re.findall(
            r"```json\s*\n(\{.*?\n\})\s*\n```",
            (SKILL / "references/pain-points.md").read_text(encoding="utf-8"), re.DOTALL)]
        command = next(card["inspection_cmd"] for card in cards if "check_docs_links.py" in card["inspection_cmd"])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installed = root / "installed skill"
            shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            project = root / "target project"
            (project / "docs").mkdir(parents=True)
            (project / "docs/README.md").write_text("# Docs\n", encoding="utf-8")
            arguments = [part.replace("<skill-root>", str(installed)).replace("<project-root>", str(project))
                         for part in command.split()]
            arguments[0] = sys.executable
            result = subprocess.run(arguments, cwd=project, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "passed")


if __name__ == "__main__":
    unittest.main()
