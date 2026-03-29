"""Optional demo 共用輔助函式。"""

import json
import os
import sys


def finish_skip(message, strict=False):
    print(f"略過：{message}")
    sys.exit(1 if strict else 0)


def mask_secret_value(value):
    if value is None or value == "":
        return "（未設定）"

    text = str(value)
    if len(text) <= 6:
        return "*" * len(text)

    visible = 3 if len(text) > 10 else 2
    masked = max(4, len(text) - (visible * 2))
    return f"{text[:visible]}{'*' * masked}{text[-visible:]}"


def is_sensitive_env_name(name):
    upper_name = name.upper()
    return any(token in upper_name for token in ["KEY", "TOKEN", "SECRET", "PASSWORD"])


def format_env_value(name, value, mask=False):
    if value is None or value == "":
        return "（未設定）"

    if mask or is_sensitive_env_name(name):
        return "（已設定，已遮罩）"

    return "（已設定）"


def print_demo_header(title, description, env_items=None):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(f"示範內容：{description}")

    if env_items:
        print("\n環境變數：")
        for item in env_items:
            name = item["name"]
            value = item.get("value")
            mask = item.get("mask", False)
            print(f"  - {name} = {format_env_value(name, value, mask)}")


def resolve_env_value(*names):
    for name in names:
        value = os.getenv(name)
        if value:
            return value, name

    return None, None


def format_env_source(selected_name, *fallback_names):
    if not selected_name:
        return "（未設定）"

    if selected_name not in fallback_names:
        return selected_name

    return (
        f"{selected_name}（優先使用的專用變數未設，已 fallback 到 {selected_name}）"
    )


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

    def _is_image_model(model_name):
        lower = (model_name or "").lower()
        return "image" in lower or "dall-e" in lower

    summaries = parse_json_env("AZURE_DEPLOYED_MODEL_SUMMARIES") or []
    for item in summaries:
        deployment_name = item.get("deploymentName") or item.get("name")
        model_name = item.get("modelName") or item.get("model") or ""
        if deployment_name and _is_image_model(model_name):
            return deployment_name, "AZURE_DEPLOYED_MODEL_SUMMARIES"

    optional_deployments = parse_json_env(
        "AZURE_OPTIONAL_MODEL_DEPLOYMENTS") or []
    for item in optional_deployments:
        deployment_name = item.get("deploymentName")
        model_name = item.get("modelName") or ""
        if deployment_name and _is_image_model(model_name):
            return deployment_name, "AZURE_OPTIONAL_MODEL_DEPLOYMENTS"

    return None, None


def safe_delete_agent_version(project_client, agent):
    try:
        project_client.agents.delete_version(
            agent_name=agent.name,
            agent_version=agent.version,
        )
        print("已清除暫時建立的 agent 版本")
    except Exception as exc:
        print(f"警告：無法刪除暫時建立的 agent 版本：{exc}")
