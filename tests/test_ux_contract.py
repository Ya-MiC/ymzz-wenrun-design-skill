import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.ux_contract import error_problems, page_problems, progress_problems


class UxContractTest(unittest.TestCase):
    def test_error_accepts_a_stable_token(self):
        self.assertEqual(
            error_problems({"code": "not_found", "message": "not_found"}, {"not_found"}),
            [],
        )

    def test_error_rejects_user_copy_and_unknown_codes(self):
        problems = error_problems(
            {"code": "missing", "message": "找不到這筆資料", "user_message": "找不到這筆資料"},
            {"not_found"},
        )
        self.assertGreaterEqual(len(problems), 2)

    def test_progress_rejects_eta_and_unmeasured_percent(self):
        problems = progress_problems(
            {
                "task_id": "export_1",
                "state": "running",
                "completed": 1,
                "total": None,
                "percent": 40,
                "eta_seconds": 12,
                "cancellable": True,
            }
        )
        self.assertTrue(any("ETA" in item for item in problems))
        self.assertTrue(any("percent" in item for item in problems))

    def test_page_requires_a_cursor_when_more_remain(self):
        self.assertEqual(
            page_problems({"items": [{"id": "a"}], "next_cursor": "n", "has_more": True}),
            [],
        )
        self.assertTrue(page_problems({"items": [], "next_cursor": None, "has_more": True}))


if __name__ == "__main__":
    unittest.main()
