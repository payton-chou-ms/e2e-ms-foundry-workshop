"""Shared helpers for optional capability demos.

These demos should never block the workshop's primary SQL + search path.
"""

import json
import os
import sys


def finish_skip(message, strict=False):
    print(f"SKIP: {message}")
    sys.exit(1 if strict else 0)


def resolve_env_value(*names):
    for name in names:
        value = os.getenv(name)
        if value:
            return value, name

    return None, None


def parse_json_env(name):
    value = os.getenv(name)
    if not value:
        return None

    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def resolve_image_model_deployment():
    direct_value, direct_name = resolve_env_value(
        "AZURE_IMAGE_MODEL_DEPLOYMENT",
        "AZURE_IMAGE_MODEL",
    )
    if direct_value:
        return direct_value, direct_name

    summaries = parse_json_env("AZURE_DEPLOYED_MODEL_SUMMARIES") or []
    for item in summaries:
        deployment_name = item.get("deploymentName") or item.get("name")
        model_name = (item.get("modelName") or item.get("model") or "").lower()
        if deployment_name and "image" in model_name:
            return deployment_name, "AZURE_DEPLOYED_MODEL_SUMMARIES"

    optional_deployments = parse_json_env(
        "AZURE_OPTIONAL_MODEL_DEPLOYMENTS") or []
    for item in optional_deployments:
        deployment_name = item.get("deploymentName")
        model_name = (item.get("modelName") or "").lower()
        if deployment_name and "image" in model_name:
            return deployment_name, "AZURE_OPTIONAL_MODEL_DEPLOYMENTS"

    return None, None


def safe_delete_agent_version(project_client, agent):
    try:
        project_client.agents.delete_version(
            agent_name=agent.name,
            agent_version=agent.version,
        )
        print("Cleaned up temporary agent version")
    except Exception as exc:
        print(f"WARNING: could not delete temporary agent version: {exc}")
