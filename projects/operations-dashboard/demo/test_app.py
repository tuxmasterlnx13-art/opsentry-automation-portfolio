import unittest

from app import app


class DashboardTests(unittest.TestCase):
    def test_api_contains_only_synthetic_cases(self):
        response = app.test_client().get("/api/cases")
        self.assertEqual(200, response.status_code)
        self.assertTrue(all(row["id"].startswith("DEMO-") for row in response.get_json()))


if __name__ == "__main__":
    unittest.main()
