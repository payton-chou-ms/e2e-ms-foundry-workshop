import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEVCONTAINER_FILE = REPO_ROOT / ".devcontainer" / "devcontainer.json"


class DevcontainerAzdVersionTests(unittest.TestCase):
    def test_devcontainer_pins_azd_1_23_13(self):
        data = json.loads(DEVCONTAINER_FILE.read_text(encoding="utf-8"))
        azd_feature = data["features"]["ghcr.io/azure/azure-dev/azd:latest"]

        self.assertEqual(azd_feature["version"], "1.23.13")


if __name__ == "__main__":
    unittest.main()
