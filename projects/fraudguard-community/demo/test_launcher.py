import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fraudguard.launcher import load_or_create_config


class LauncherTests(unittest.TestCase):
    def test_local_mode_does_not_create_hidden_access_key(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"LOCALAPPDATA": directory}):
            config, visible = load_or_create_config()
            self.assertIsNone(visible)
            self.assertNotIn("access_key_hash", config)

    def test_lan_mode_creates_and_can_reset_visible_key(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"LOCALAPPDATA": directory}):
            first, first_key = load_or_create_config(require_access_key=True)
            second, second_key = load_or_create_config(require_access_key=True, reset_access_key=True)
            self.assertTrue(first_key.startswith("FG-"))
            self.assertTrue(second_key.startswith("FG-"))
            self.assertNotEqual(first["access_key_hash"], second["access_key_hash"])
            saved = json.loads((Path(directory) / "GuardianCommunity" / "config.json").read_text())
            self.assertEqual(second["access_key_hash"], saved["access_key_hash"])


if __name__ == "__main__":
    unittest.main()
