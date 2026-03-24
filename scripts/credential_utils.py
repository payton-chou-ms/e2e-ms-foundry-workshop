"""Credential helpers for local workshop scripts."""

from azure.identity import AzureCliCredential, ChainedTokenCredential, DefaultAzureCredential


def get_credential():
    """Prefer Azure CLI locally, then fall back to the default credential chain."""
    return ChainedTokenCredential(
        AzureCliCredential(),
        DefaultAzureCredential(exclude_cli_credential=True),
    )