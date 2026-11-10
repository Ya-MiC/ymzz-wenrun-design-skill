import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WenrunSkillTest(unittest.TestCase):
    def test_package_matches_source_palette(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_wenrun.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
