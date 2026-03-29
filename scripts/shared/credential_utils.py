"""Credential helpers for local workshop scripts."""

import os
import subprocess

from azure.identity import AzureCliCredential, AzureDeveloperCliCredential, ChainedTokenCredential, DefaultAzureCredential


def _resolve_tenant_id_from_subscription(subscription_id: str) -> str | None:
    try:
        completed = subprocess.run(
            [
                "az",
                "account",
                "show",
                "--subscription",
                subscription_id,
                "--query",
                "tenantId",
                "-o",
                "tsv",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

    tenant_id = completed.stdout.strip()
    return tenant_id or None


def _resolve_cli_tenant_id() -> str | None:
    explicit_tenant_id = os.getenv("AZURE_TENANT_ID", "").strip()
    if explicit_tenant_id:
        return explicit_tenant_id

    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID", "").strip()
    if subscription_id:
        return _resolve_tenant_id_from_subscription(subscription_id)

    return None


def get_credential():
    """Prefer Azure Developer CLI, then Azure CLI, then the remaining default credential chain."""
    cli_tenant_id = _resolve_cli_tenant_id()
    developer_cli_credential = AzureDeveloperCliCredential(
        tenant_id=cli_tenant_id) if cli_tenant_id else AzureDeveloperCliCredential()
    cli_credential = AzureCliCredential(
        tenant_id=cli_tenant_id) if cli_tenant_id else AzureCliCredential()

    return ChainedTokenCredential(
        developer_cli_credential,
        cli_credential,
        DefaultAzureCredential(
            exclude_cli_credential=True,
            exclude_developer_cli_credential=True,
        ),
    )
