"""Helpers for configuring Content Understanding default model deployments."""

from __future__ import annotations

import os


DEFAULT_MODEL_DEPLOYMENTS = {
    "gpt-4.1-mini": "gpt-4.1-mini",
    "text-embedding-3-large": "text-embedding-3-large",
}


def ensure_content_understanding_defaults(endpoint: str | None = None) -> tuple[bool, str]:
    """Ensure Content Understanding defaults exist for the current environment."""
    resolved_endpoint = endpoint or os.getenv("AZURE_AI_ENDPOINT")
    if not resolved_endpoint:
        return False, "未設定 AZURE_AI_ENDPOINT"

    try:
        from azure.ai.contentunderstanding import ContentUnderstandingClient
        from azure.identity import DefaultAzureCredential

        client = ContentUnderstandingClient(
            endpoint=resolved_endpoint,
            credential=DefaultAzureCredential(),
        )

        try:
            defaults = client.get_defaults()
            if isinstance(defaults, dict) and defaults.get("modelDeployments"):
                return True, "已設定"
        except Exception:
            pass

        client.update_defaults(model_deployments=DEFAULT_MODEL_DEPLOYMENTS)
        return True, "已補上設定"
    except Exception as exc:
        return False, str(exc)