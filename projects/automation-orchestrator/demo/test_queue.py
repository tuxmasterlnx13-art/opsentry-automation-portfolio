import tempfile
import unittest
from pathlib import Path

from queue import WorkQueue


class QueueTests(unittest.TestCase):
    def test_claim_is_exclusive(self):
        with tempfile.TemporaryDirectory() as directory:
            queue = WorkQueue(Path(directory) / "queue.sqlite3")
            queue.add("001")
            self.assertEqual("001", queue.claim("worker-a"))
            self.assertIsNone(queue.claim("worker-b"))
            self.assertFalse(queue.complete("001", "worker-b"))
            self.assertTrue(queue.complete("001", "worker-a"))


if __name__ == "__main__":
    unittest.main()

