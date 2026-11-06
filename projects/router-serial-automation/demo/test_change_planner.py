import unittest

from change_planner import plan


class PlannerTests(unittest.TestCase):
    def test_excludes_cancelled_and_keeps_reviewable_changes(self):
        changes = plan([
            {"customer_id": "2", "field": "plan", "observed": "A", "expected": "B", "state": "active"},
            {"customer_id": "1", "field": "serial", "observed": "X", "expected": "Y", "state": "cancelled"},
        ])
        self.assertEqual(1, len(changes))
        self.assertEqual("PENDING_APPROVAL", changes[0].status)


if __name__ == "__main__":
    unittest.main()

