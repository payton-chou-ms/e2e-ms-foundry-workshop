import importlib.util
import sys
import unittest
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
