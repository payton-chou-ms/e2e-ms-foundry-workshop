import importlib.util
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"


def load_shared_module(module_relative_path: str, module_name: str):
    sys.path.insert(0, str(SCRIPTS_DIR))
    module_path = SCRIPTS_DIR / module_relative_path
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:  # pragma: no cover - defensive guard
        raise RuntimeError(f"Failed to load {module_relative_path}")
    spec.loader.exec_module(module)
    return module


class SharedCredentialUtilsTests(unittest.TestCase):
    def test_get_credential_prefers_azure_developer_cli_before_azure_cli(self):
        module = load_shared_module("shared/credential_utils.py", "shared_credential_utils_azd_first")

        with patch.dict(os.environ, {"AZURE_TENANT_ID": "tenant-explicit"}, clear=False):
            with patch.object(module, "AzureDeveloperCliCredential") as azure_developer_cli_credential:
                with patch.object(module, "AzureCliCredential") as azure_cli_credential:
                    with patch.object(module, "DefaultAzureCredential") as default_credential:
                        with patch.object(module, "ChainedTokenCredential") as chained_credential:
                            module.get_credential()

        azure_developer_cli_credential.assert_called_once_with(tenant_id="tenant-explicit")
        azure_cli_credential.assert_called_once_with(tenant_id="tenant-explicit")
        default_credential.assert_called_once_with(exclude_cli_credential=True, exclude_developer_cli_credential=True)
        chained_credential.assert_called_once_with(
            azure_developer_cli_credential.return_value,
            azure_cli_credential.return_value,
            default_credential.return_value,
        )

    def test_get_credential_prefers_explicit_azure_tenant_id(self):
        module = load_shared_module("shared/credential_utils.py", "shared_credential_utils_explicit")

        with patch.dict(os.environ, {"AZURE_TENANT_ID": "tenant-explicit"}, clear=False):
            with patch.object(module, "AzureDeveloperCliCredential") as azure_developer_cli_credential:
                with patch.object(module, "AzureCliCredential") as azure_cli_credential:
                    with patch.object(module, "DefaultAzureCredential") as default_credential:
                        with patch.object(module, "ChainedTokenCredential") as chained_credential:
                            module.get_credential()

        azure_developer_cli_credential.assert_called_once_with(tenant_id="tenant-explicit")
        azure_cli_credential.assert_called_once_with(tenant_id="tenant-explicit")
        default_credential.assert_called_once_with(exclude_cli_credential=True, exclude_developer_cli_credential=True)
        chained_credential.assert_called_once_with(
            azure_developer_cli_credential.return_value,
            azure_cli_credential.return_value,
            default_credential.return_value,
        )

    def test_get_credential_resolves_tenant_from_subscription_when_needed(self):
        module = load_shared_module("shared/credential_utils.py", "shared_credential_utils_subscription")

        with patch.dict(os.environ, {"AZURE_SUBSCRIPTION_ID": "sub-123"}, clear=True):
            with patch.object(module, "_resolve_tenant_id_from_subscription", return_value="tenant-from-sub") as resolver:
                with patch.object(module, "AzureDeveloperCliCredential") as azure_developer_cli_credential:
                    with patch.object(module, "AzureCliCredential") as azure_cli_credential:
                        with patch.object(module, "DefaultAzureCredential") as default_credential:
                            with patch.object(module, "ChainedTokenCredential") as chained_credential:
                                module.get_credential()

        resolver.assert_called_once_with("sub-123")
        azure_developer_cli_credential.assert_called_once_with(tenant_id="tenant-from-sub")
        azure_cli_credential.assert_called_once_with(tenant_id="tenant-from-sub")
        default_credential.assert_called_once_with(exclude_cli_credential=True, exclude_developer_cli_credential=True)
        chained_credential.assert_called_once_with(
            azure_developer_cli_credential.return_value,
            azure_cli_credential.return_value,
            default_credential.return_value,
        )


if __name__ == "__main__":
    unittest.main()