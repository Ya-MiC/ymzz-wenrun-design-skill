import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WenrunSkillTest(unittest.TestCase):
    def test_pillow_is_a_declared_test_dependency(self):
        requirements = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8")
        self.assertIn("Pillow", requirements)
        workflow = (ROOT / ".github/workflows/test.yml").read_text(encoding="utf-8")
        self.assertIn("pull_request:", workflow)
        self.assertIn("ubuntu-latest", workflow)
        self.assertIn("requirements-dev.txt", workflow)
        self.assertIn("unittest discover -s tests -v", workflow)
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(license_text.startswith("MIT License"))

    def test_package_matches_source_palette(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_wenrun.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
