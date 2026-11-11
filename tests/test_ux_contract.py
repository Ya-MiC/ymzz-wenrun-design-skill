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

    def test_error_rejects_nested_user_copy(self):
        problems = error_problems(
            {
                "code": "not_found",
                "message": "not_found",
                "details": {"note": [{"user_message": "找不到這筆資料"}]},
            },
            {"not_found"},
        )
        self.assertTrue(any("user copy" in item for item in problems))

    def test_error_requires_message_in_the_enum(self):
        codes = {"not_found", "invalid_input"}
        self.assertEqual(
            error_problems({"code": "not_found", "message": "invalid_input"}, codes),
            [],
        )
        problems = error_problems({"code": "not_found", "message": "made_up"}, codes)
        self.assertTrue(any("message must be one of the project enum" in item for item in problems))

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

    def test_progress_percent_stays_between_0_and_100(self):
        good = {
            "task_id": "export_1",
            "state": "running",
            "completed": 1,
            "total": 2,
            "cancellable": True,
        }
        self.assertEqual(progress_problems({**good, "percent": 0}), [])
        self.assertEqual(progress_problems({**good, "percent": 100}), [])
        self.assertEqual(progress_problems({**good, "percent": 50.0}), [])
        for value in (500, -1, True, "50", float("nan")):
            problems = progress_problems({**good, "percent": value})
            self.assertTrue(any("0 to 100" in item for item in problems), value)

    def test_finished_progress_is_not_cancellable(self):
        for state in ("succeeded", "failed", "cancelled"):
            problems = progress_problems(
                {
                    "task_id": "export_1",
                    "state": state,
                    "completed": 2,
                    "total": 2,
                    "cancellable": True,
                }
            )
            self.assertTrue(any("not cancellable" in item for item in problems), state)
        self.assertEqual(
            progress_problems(
                {
                    "task_id": "export_1",
                    "state": "succeeded",
                    "completed": 2,
                    "total": 2,
                    "cancellable": False,
                }
            ),
            [],
        )

    def test_page_requires_a_cursor_when_more_remain(self):
        self.assertEqual(
            page_problems({"items": [{"id": "a"}], "next_cursor": "n", "has_more": True}),
            [],
        )
        self.assertTrue(page_problems({"items": [], "next_cursor": None, "has_more": True}))


if __name__ == "__main__":
    unittest.main()
