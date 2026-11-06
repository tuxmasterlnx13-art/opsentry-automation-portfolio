import unittest

from ip_guard import Candidate, build_plan


class PlanTests(unittest.TestCase):
    def test_blocks_duplicates_and_out_of_range_values(self):
        plan = build_plan([
            Candidate("A", "192.0.2.10", "100.64.1.10"),
            Candidate("B", "192.0.2.11", "100.64.1.10"),
            Candidate("C", "192.0.2.12", "192.0.2.20"),
        ])
        self.assertEqual([False, False, False], [item.approved for item in plan])

    def test_approves_unique_candidate_for_pilot(self):
        [decision] = build_plan([Candidate("A", "192.0.2.10", "100.64.1.10")])
        self.assertTrue(decision.approved)
        self.assertEqual("eligible for pilot", decision.reason)


if __name__ == "__main__":
    unittest.main()

