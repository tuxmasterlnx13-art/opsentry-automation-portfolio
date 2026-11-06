import unittest

from fraudguard.engine import Settings, analyze, validate_columns
from fraudguard.sample import SAMPLE_ROWS


class EngineTests(unittest.TestCase):
    def test_sample_finds_explainable_patterns(self):
        findings, errors = analyze(SAMPLE_ROWS)
        self.assertEqual([], errors)
        by_id = {item.transaction_id: item for item in findings}
        self.assertIn("Importe igual o superior", by_id["DEMO-100"].reasons[0])
        self.assertIn("Alta velocidad", " ".join(by_id["DEMO-104"].reasons))
        self.assertIn("Cambio rápido de país", " ".join(by_id["DEMO-103"].reasons))
        self.assertIn("Dispositivo compartido", " ".join(by_id["DEMO-202"].reasons))

    def test_duplicate_ids_are_high_risk(self):
        row = dict(SAMPLE_ROWS[0])
        findings, _ = analyze([row, dict(row)])
        self.assertTrue(all(item.level == "Alto" for item in findings))

    def test_invalid_rows_are_reported_not_crashed(self):
        row = dict(SAMPLE_ROWS[0], amount="not-a-number")
        findings, errors = analyze([row])
        self.assertEqual([], findings)
        self.assertEqual(1, len(errors))

    def test_missing_columns_are_listed(self):
        self.assertIn("device_id", validate_columns(["transaction_id"]))

    def test_custom_threshold_is_respected(self):
        row = dict(SAMPLE_ROWS[0], amount="100")
        [finding], _ = analyze([row], Settings(high_amount=__import__("decimal").Decimal("50")))
        self.assertGreater(finding.score, 0)


if __name__ == "__main__":
    unittest.main()

