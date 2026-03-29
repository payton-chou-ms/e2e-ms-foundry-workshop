import importlib.util
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import call, patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
SCRIPT_PATH = SCRIPTS_DIR / "deploy_optional_model.py"


def load_script_module():
    sys.path.insert(0, str(SCRIPTS_DIR))
    spec = importlib.util.spec_from_file_location(
        "deploy_optional_model_script",
        SCRIPT_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:  # pragma: no cover - defensive guard
        raise RuntimeError("Failed to load deploy_optional_model module")
    spec.loader.exec_module(module)
    return module


class DeployOptionalModelTests(unittest.TestCase):
    def test_resolve_requested_model_uses_latest_version_when_default_is_missing(self):
        module = load_script_module()
        catalog_index = module.build_model_catalog_index(
            [
                {
                    "name": "gpt-5.3-chat",
                    "version": "2026-02-10",
                    "isDefaultVersion": False,
                    "lifecycleStatus": "Preview",
                    "skus": [{"name": "GlobalStandard"}],
                },
                {
                    "name": "gpt-5.3-chat",
                    "version": "2026-03-03",
                    "isDefaultVersion": False,
                    "lifecycleStatus": "Preview",
                    "skus": [{"name": "GlobalStandard"}],
                },
            ]
        )

        resolved = module.resolve_requested_model(
            {
                "deploymentName": "gpt-5.3-chat",
                "modelName": "gpt-5.3-chat",
                "skuName": "GlobalStandard",
                "capacity": 1,
            },
            catalog_index,
        )

        self.assertEqual(resolved["status"], "ready")
        self.assertEqual(resolved["modelVersion"], "2026-03-03")

    def test_resolve_requested_model_prefers_default_version_when_present(self):
        module = load_script_module()
        catalog_index = module.build_model_catalog_index(
            [
                {
                    "name": "gpt-4o-mini",
                    "version": "2024-07-18",
                    "isDefaultVersion": True,
                    "lifecycleStatus": "GenerallyAvailable",
                    "skus": [{"name": "GlobalStandard"}],
                },
                {
                    "name": "gpt-4o-mini",
                    "version": "2024-06-01",
                    "isDefaultVersion": False,
                    "lifecycleStatus": "GenerallyAvailable",
                    "skus": [{"name": "GlobalStandard"}],
                },
            ]
        )

        resolved = module.resolve_requested_model(
            {
                "deploymentName": "gpt-4o-mini",
                "modelName": "gpt-4o-mini",
                "skuName": "GlobalStandard",
                "capacity": 1,
            },
            catalog_index,
        )

        self.assertEqual(resolved["status"], "ready")
        self.assertEqual(resolved["modelVersion"], "2024-07-18")

    def test_resolve_requested_model_rejects_unsupported_sku(self):
        module = load_script_module()
        catalog_index = module.build_model_catalog_index(
            [
                {
                    "name": "gpt-5-pro",
                    "version": "2025-10-06",
                    "isDefaultVersion": False,
                    "lifecycleStatus": "GenerallyAvailable",
                    "skus": [{"name": "GlobalStandard"}],
                },
            ]
        )

        resolved = module.resolve_requested_model(
            {
                "deploymentName": "gpt-5-pro",
                "modelName": "gpt-5-pro",
                "skuName": "Standard",
                "capacity": 1,
            },
            catalog_index,
        )

        self.assertEqual(resolved["status"], "invalid")
        self.assertEqual(resolved["reason"], "sku-not-supported")

    def test_resolve_requested_model_rejects_missing_catalog_entry(self):
        module = load_script_module()
        resolved = module.resolve_requested_model(
            {
                "deploymentName": "gpt-5.4-pro",
                "modelName": "gpt-5.4-pro",
                "skuName": "GlobalStandard",
                "capacity": 1,
            },
            {},
        )

        self.assertEqual(resolved["status"], "invalid")
        self.assertEqual(resolved["reason"], "model-not-in-catalog")

    def test_deploy_playwright_workspace_continues_when_quota_is_exhausted(self):
        module = load_script_module()

        with patch.dict(
            os.environ,
            {
                "AZURE_DEPLOY_BROWSER_AUTOMATION": "true",
                "AZURE_PLAYWRIGHT_WORKSPACE_NAME": "pww-demo",
                "AZURE_PLAYWRIGHT_LOCATION": "eastus",
                "AZURE_PLAYWRIGHT_WORKSPACE_RESOURCE_ID": "/subscriptions/sub/resourceGroups/rg/providers/Microsoft.LoadTestService/playwrightWorkspaces/pww-demo",
            },
            clear=False,
        ):
            with patch.object(module, "playwright_workspace_exists", return_value=False):
                with patch.object(
                    module,
                    "create_playwright_workspace",
                    return_value=module.subprocess.CompletedProcess(
                        args=["az"],
                        returncode=1,
                        stdout="",
                        stderr="WorkspacesLimitExceeded: The maximum limit for workspaces per region in this subscription has been exceeded.",
                    ),
                ):
                    with patch.object(module, "clear_playwright_workspace_vars") as clear_vars:
                        with patch.object(module, "set_env_value") as set_env_value:
                            module.deploy_playwright_workspace("rg-demo", "sub-demo")

        clear_vars.assert_called_once_with("failed")
        set_env_value.assert_not_called()

    def test_deploy_playwright_workspace_marks_ready_when_existing_workspace_is_found(self):
        module = load_script_module()

        with patch.dict(
            os.environ,
            {
                "AZURE_DEPLOY_BROWSER_AUTOMATION": "true",
                "AZURE_PLAYWRIGHT_WORKSPACE_NAME": "pww-demo",
                "AZURE_PLAYWRIGHT_LOCATION": "eastus",
                "AZURE_PLAYWRIGHT_WORKSPACE_RESOURCE_ID": "/subscriptions/sub/resourceGroups/rg/providers/Microsoft.LoadTestService/playwrightWorkspaces/pww-demo",
            },
            clear=False,
        ):
            with patch.object(module, "playwright_workspace_exists", return_value=True):
                with patch.object(
                    module,
                    "get_playwright_workspace",
                    return_value={
                        "id": "/subscriptions/sub/resourceGroups/rg/providers/Microsoft.LoadTestService/playwrightWorkspaces/pww-demo",
                        "location": "eastus",
                        "properties": {
                            "workspaceId": "workspace-id",
                            "dataplaneUri": "https://pww-demo.playwright.microsoft.com",
                        },
                    },
                ):
                    with patch.object(module, "set_env_value") as set_env_value:
                        module.deploy_playwright_workspace("rg-demo", "sub-demo")

        set_env_value.assert_has_calls(
            [
                call("AZURE_PLAYWRIGHT_WORKSPACE_NAME", "pww-demo"),
                call("AZURE_PLAYWRIGHT_WORKSPACE_RESOURCE_ID", "/subscriptions/sub/resourceGroups/rg/providers/Microsoft.LoadTestService/playwrightWorkspaces/pww-demo"),
                call("AZURE_PLAYWRIGHT_WORKSPACE_ID", "workspace-id"),
                call("AZURE_PLAYWRIGHT_LOCATION", "eastus"),
                call("AZURE_PLAYWRIGHT_DATAPLANE_URI", "https://pww-demo.playwright.microsoft.com"),
                call("AZURE_PLAYWRIGHT_BROWSER_ENDPOINT", "wss://pww-demo.playwright.microsoft.com/browsers"),
                call("AZURE_PLAYWRIGHT_AUTH_MODE", "Playwright Service Access Token (manual token generation still required)"),
                call("AZURE_PLAYWRIGHT_STATUS", "ready"),
            ],
            any_order=False,
        )


if __name__ == "__main__":
    unittest.main()
