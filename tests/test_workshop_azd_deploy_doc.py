import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEPLOY_DOC = REPO_ROOT / "workshop" / "docs" / "01-deploy" / "01-deploy-azure.md"


class WorkshopAzdDeployDocTests(unittest.TestCase):
    def test_deploy_doc_uses_supported_subscription_selection_flow(self):
        text = DEPLOY_DOC.read_text(encoding="utf-8")

        self.assertNotIn("azd up --subscription", text)
        self.assertNotIn("azd env new <environment-name> --subscription", text)
        self.assertIn("az account set --subscription <SUBSCRIPTION_ID>", text)


if __name__ == "__main__":
    unittest.main()