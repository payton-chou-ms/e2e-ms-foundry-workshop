import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class PlaywrightWorkspaceBestEffortInfraTests(unittest.TestCase):
    def test_main_bicep_keeps_playwright_out_of_main_deployment(self):
        content = (REPO_ROOT / "infra" / "main.bicep").read_text(encoding="utf-8")

        self.assertNotIn("module playwrightWorkspace './modules/playwright_workspace.bicep'", content)
        self.assertIn("output AZURE_PLAYWRIGHT_STATUS string = deployBrowserAutomation ? 'pending' : 'disabled'", content)
        self.assertIn("output AZURE_PLAYWRIGHT_WORKSPACE_NAME string = deployBrowserAutomation", content)
        self.assertIn("output AZURE_PLAYWRIGHT_BROWSER_ENDPOINT string = ''", content)


if __name__ == "__main__":
    unittest.main()