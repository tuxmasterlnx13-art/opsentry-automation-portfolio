import unittest
from datetime import date

from report import markdown_report


class ReportTests(unittest.TestCase):
    def test_output_is_stable_and_counted(self):
        result = markdown_report([
            {"status": "open"}, {"status": "resolved"}, {"status": "open"}
        ], date(2026, 1, 2))
        self.assertIn("Total records: 3", result)
        self.assertIn("- open: 2", result)


if __name__ == "__main__":
    unittest.main()

