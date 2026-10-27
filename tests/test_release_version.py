"""Exercise the non-npm changeset release CLI in isolated repositories."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / ".github/scripts/release_version.py"
PACKAGE = "codex-doc-first-development-skill"


class ReleaseVersionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("pyproject.toml", f'[project]\nname = "{PACKAGE}"\nversion = "2.3.0"\n')
        self.write("codex-doc-first-development/SKILL.md", "# Codex Doc-First Development (v2.3.0 Released)\n")
        self.write("README.md", "# Skill (v2.3.0 正式版)\n\n## v2.3.0 总览\n")
        self.write("CHANGELOG.md", "# Changelog\n\n## [2.3.0] - 2026-10-25\n\nOld entry.\n")
        self.write(".changeset/config.json", "{}\n")

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def changeset(self, name, bump="patch", summary="Repair release automation."):
        self.write(f".changeset/{name}.md", f'---\n"{PACKAGE}": {bump}\n---\n\n{summary}\n')

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def run_cli(self, *args):
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), "--json", *args],
                                capture_output=True, text=True, encoding="utf-8")
        return result

    def test_preview_is_read_only_and_highest_bump_wins(self):
        self.changeset("repair")
        self.changeset("adaptive", "minor", "Adapt task workflows.")
        before = self.snapshot()
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = json.loads(result.stdout)
        self.assertEqual(plan["next_version"], "2.4.0")
        self.assertEqual(len(plan["changesets"]), 2)
        self.assertEqual(self.snapshot(), before)

    def test_apply_syncs_versions_history_and_consumes_only_changesets(self):
        self.changeset("repair")
        self.changeset("adaptive", "minor", "Adapt task workflows.")
        self.write(".changeset/README.md", "Instructions, not a changeset.\n")
        result = self.run_cli("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ("pyproject.toml", "codex-doc-first-development/SKILL.md", "README.md"):
            self.assertIn("2.4.0", (self.root / name).read_text(encoding="utf-8"))
        history = (self.root / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## [2.4.0]", history)
        self.assertIn("Adapt task workflows.", history)
        self.assertIn("## [2.3.0] - 2026-10-25", history)
        self.assertFalse((self.root / ".changeset/repair.md").exists())
        self.assertTrue((self.root / ".changeset/README.md").exists())
        before = self.snapshot()
        result = self.run_cli("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["pending"])
        self.assertEqual(self.snapshot(), before)

    def test_semver_bumps(self):
        for bump, expected in (("patch", "2.3.1"), ("minor", "2.4.0"), ("major", "3.0.0")):
            with self.subTest(bump=bump):
                self.changeset("release", bump)
                result = self.run_cli()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["next_version"], expected)

    def test_bad_changeset_fails_before_any_write(self):
        for text in ("not a changeset", f'---\n"{PACKAGE}": typo\n---\nSummary',
                     '---\n"other-package": minor\n---\nSummary',
                     f'---\n"{PACKAGE}": patch\n---\n'):
            with self.subTest(text=text):
                self.write(".changeset/bad.md", text)
                before = self.snapshot()
                result = self.run_cli("--apply")
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(json.loads(result.stdout)["status"], "error")
                self.assertEqual(self.snapshot(), before)

    def test_version_drift_fails_without_consuming_changesets(self):
        self.changeset("release")
        self.write("codex-doc-first-development/SKILL.md", "# Skill (v2.2.0 Released)\n")
        before = self.snapshot()
        result = self.run_cli("--apply")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
