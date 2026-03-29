"""Best-effort deployment of optional Foundry models after azd provision."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time

from load_env import load_all_env

load_all_env()

IMAGE_DEPLOYMENT_ENV_VARS = (
    "AZURE_IMAGE_MODEL_DEPLOYMENT",
    "AZURE_IMAGE_MODEL_NAME",
    "AZURE_IMAGE_MODEL_VERSION",
    "AZURE_IMAGE_MODEL_SKU",
    "AZURE_IMAGE_MODEL_CAPACITY",
)
PLAYWRIGHT_WORKSPACE_ENV_VARS = (
    "AZURE_PLAYWRIGHT_WORKSPACE_NAME",
    "AZURE_PLAYWRIGHT_WORKSPACE_RESOURCE_ID",
    "AZURE_PLAYWRIGHT_WORKSPACE_ID",
    "AZURE_PLAYWRIGHT_LOCATION",
    "AZURE_PLAYWRIGHT_DATAPLANE_URI",
    "AZURE_PLAYWRIGHT_BROWSER_ENDPOINT",
    "AZURE_PLAYWRIGHT_AUTH_MODE",
)
PLAYWRIGHT_AUTH_MODE_VALUE = "Playwright Service Access Token (manual token generation still required)"

BEST_EFFORT_OPENAI_MODELS_ENV = "AZURE_BEST_EFFORT_OPENAI_MODEL_DEPLOYMENTS"
READY_OPENAI_MODELS_ENV = "AZURE_READY_BEST_EFFORT_OPENAI_MODEL_DEPLOYMENTS"
FAILED_OPENAI_MODELS_ENV = "AZURE_FAILED_BEST_EFFORT_OPENAI_MODEL_DEPLOYMENTS"
FAILED_OPENAI_MODEL_DETAILS_ENV = "AZURE_FAILED_BEST_EFFORT_OPENAI_MODEL_DEPLOYMENT_DETAILS"
OPENAI_MODELS_STATUS_ENV = "AZURE_BEST_EFFORT_OPENAI_MODEL_DEPLOYMENTS_STATUS"

BEST_EFFORT_MODEL_NAME_ALIASES = {
    "gpt-5.2-codex": "gpt-5-codex",
    "gpt-5.3-codex": "gpt-5-codex",
    "gpt-5.2": "gpt-5",
    "gpt-5.4": "gpt-5",
    "gpt-5.4-pro": "gpt-5-pro",
}

DEFAULT_BEST_EFFORT_OPENAI_MODELS = [
    {
        "deploymentName": "gpt-5-nano",
        "modelName": "gpt-5-nano",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
    {
        "deploymentName": "gpt-4.1-nano",
        "modelName": "gpt-4.1-nano",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
    {
        "deploymentName": "gpt-4o-mini",
        "modelName": "gpt-4o-mini",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
    {
        "deploymentName": "o3-mini",
        "modelName": "o3-mini",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
    {
        "deploymentName": "gpt-5.3-chat",
        "modelName": "gpt-5.3-chat",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
    {
        "deploymentName": "gpt-5-pro",
        "modelName": "gpt-5-pro",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
    {
        "deploymentName": "gpt-5-codex",
        "modelName": "gpt-5-codex",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
    {
        "deploymentName": "gpt-5.1-codex-mini",
        "modelName": "gpt-5.1-codex-mini",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
    {
        "deploymentName": "gpt-5.1-codex",
        "modelName": "gpt-5.1-codex",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
    {
        "deploymentName": "gpt-5",
        "modelName": "gpt-5",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
    {
        "deploymentName": "gpt-5.1",
        "modelName": "gpt-5.1",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
    {
        "deploymentName": "gpt-5-mini",
        "modelName": "gpt-5-mini",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
    {
        "deploymentName": "gpt-5.4-nano",
        "modelName": "gpt-5.4-nano",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
    {
        "deploymentName": "gpt-5.4-mini",
        "modelName": "gpt-5.4-mini",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
]


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, check=False)


def set_env_value(name: str, value: str):
    run_command(["azd", "env", "set", name, value])


def unset_env_value(name: str):
    run_command(["azd", "env", "unset", name])


def set_json_env_value(name: str, value):
    set_env_value(name, json.dumps(
        value, ensure_ascii=False, separators=(",", ":")))


def clear_image_deployment_vars(status: str):
    for env_name in IMAGE_DEPLOYMENT_ENV_VARS:
        unset_env_value(env_name)

    set_env_value("AZURE_IMAGE_MODEL_STATUS", status)


def clear_playwright_workspace_vars(status: str):
    for env_name in PLAYWRIGHT_WORKSPACE_ENV_VARS:
        unset_env_value(env_name)

    set_env_value("AZURE_PLAYWRIGHT_STATUS", status)


def get_required_env(name: str) -> str:
    value = (os.getenv(name) or "").strip()
    if not value:
        raise ValueError(f"缺少必要環境變數：{name}")
    return value


def parse_json_env(name: str):
    raw_value = (os.getenv(name) or "").strip()
    if not raw_value:
        return None

    try:
        return json.loads(raw_value)
    except json.JSONDecodeError:
        return None


def is_truthy_env(name: str, default: bool) -> bool:
    raw_value = (os.getenv(name) or "").strip()
    if not raw_value:
        return default

    return raw_value.casefold() not in {"0", "false", "no", "off"}


def wait_for_account(resource_group: str, account_name: str):
    for attempt in range(1, 11):
        result = run_command(
            [
                "az",
                "cognitiveservices",
                "account",
                "show",
                "--resource-group",
                resource_group,
                "--name",
                account_name,
                "--query",
                "properties.provisioningState",
                "--output",
                "tsv",
                "--only-show-errors",
            ]
        )
        if result.returncode == 0 and result.stdout.strip().lower() == "succeeded":
            return

        if attempt < 10:
            time.sleep(15)

    raise RuntimeError("AI Services account 尚未進入 Succeeded 狀態")


def deployment_exists(resource_group: str, account_name: str, deployment_name: str) -> bool:
    result = run_command(
        [
            "az",
            "cognitiveservices",
            "account",
            "deployment",
            "show",
            "--resource-group",
            resource_group,
            "--name",
            account_name,
            "--deployment-name",
            deployment_name,
            "--only-show-errors",
            "--output",
            "json",
        ]
    )
    return result.returncode == 0


def get_playwright_workspace_url(resource_id: str) -> str:
    return f"https://management.azure.com{resource_id}?api-version=2025-09-01"


def playwright_workspace_exists(resource_id: str) -> bool:
    result = run_command(
        [
            "az",
            "rest",
            "--method",
            "get",
            "--url",
            get_playwright_workspace_url(resource_id),
            "--output",
            "json",
            "--only-show-errors",
        ]
    )
    return result.returncode == 0


def get_playwright_workspace(resource_id: str) -> dict:
    result = run_command(
        [
            "az",
            "rest",
            "--method",
            "get",
            "--url",
            get_playwright_workspace_url(resource_id),
            "--output",
            "json",
            "--only-show-errors",
        ]
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(message or "無法取得 Playwright Workspace")

    try:
        payload = json.loads(result.stdout or "{}")
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive guard
        raise RuntimeError("Playwright Workspace 回應格式無法解析") from exc

    if not isinstance(payload, dict):  # pragma: no cover - defensive guard
        raise RuntimeError("Playwright Workspace 回應格式不正確")

    return payload


def create_playwright_workspace(resource_id: str, location: str) -> subprocess.CompletedProcess[str]:
    body = {
        "location": location,
        "properties": {
            "localAuth": "Enabled",
            "regionalAffinity": "Enabled",
        },
    }
    return run_command(
        [
            "az",
            "rest",
            "--method",
            "put",
            "--url",
            get_playwright_workspace_url(resource_id),
            "--body",
            json.dumps(body, ensure_ascii=False, separators=(",", ":")),
            "--output",
            "json",
            "--only-show-errors",
        ]
    )


def set_playwright_workspace_env(workspace: dict):
    properties = workspace.get("properties") or {}
    resource_id = str(workspace.get("id") or "").strip()
    workspace_name = str(workspace.get("name") or "").strip()
    workspace_id = str(properties.get("workspaceId") or "").strip()
    location = str(workspace.get("location") or "").strip()
    dataplane_uri = str(properties.get("dataplaneUri") or "").strip()
    if not workspace_name:
        workspace_name = (os.getenv("AZURE_PLAYWRIGHT_WORKSPACE_NAME") or "").strip()
    if not workspace_name and resource_id:
        workspace_name = resource_id.rstrip("/").split("/")[-1]
    browser_endpoint = ""
    if dataplane_uri:
        browser_endpoint = f"{dataplane_uri.replace('https://', 'wss://')}/browsers"

    set_env_value("AZURE_PLAYWRIGHT_WORKSPACE_NAME", workspace_name)
    set_env_value("AZURE_PLAYWRIGHT_WORKSPACE_RESOURCE_ID", resource_id)
    set_env_value("AZURE_PLAYWRIGHT_WORKSPACE_ID", workspace_id)
    set_env_value("AZURE_PLAYWRIGHT_LOCATION", location)
    set_env_value("AZURE_PLAYWRIGHT_DATAPLANE_URI", dataplane_uri)
    set_env_value("AZURE_PLAYWRIGHT_BROWSER_ENDPOINT", browser_endpoint)
    set_env_value("AZURE_PLAYWRIGHT_AUTH_MODE", PLAYWRIGHT_AUTH_MODE_VALUE)
    set_env_value("AZURE_PLAYWRIGHT_STATUS", "ready")


def deploy_playwright_workspace(resource_group: str, subscription_id: str):
    if not is_truthy_env("AZURE_DEPLOY_BROWSER_AUTOMATION", True):
        print("[SKIP] AZURE_DEPLOY_BROWSER_AUTOMATION=false，略過 Playwright Workspace deployment")
        clear_playwright_workspace_vars("disabled")
        return

    workspace_name = (os.getenv("AZURE_PLAYWRIGHT_WORKSPACE_NAME") or "").strip()
    workspace_location = (os.getenv("AZURE_PLAYWRIGHT_LOCATION") or "").strip()
    workspace_resource_id = (os.getenv("AZURE_PLAYWRIGHT_WORKSPACE_RESOURCE_ID") or "").strip()
    if not workspace_name or not workspace_location:
        print("[SKIP] 缺少 Playwright Workspace metadata，略過 optional deployment")
        clear_playwright_workspace_vars("disabled")
        return

    if not workspace_resource_id:
        workspace_resource_id = (
            f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}"
            f"/providers/Microsoft.LoadTestService/playwrightWorkspaces/{workspace_name}"
        )

    try:
        print("[INFO] 嘗試部署 Playwright Workspace，不阻斷 azd up")

        if playwright_workspace_exists(workspace_resource_id):
            print(f"[OK] Playwright Workspace '{workspace_name}' 已存在")
            set_playwright_workspace_env(get_playwright_workspace(workspace_resource_id))
            return

        result = create_playwright_workspace(workspace_resource_id, workspace_location)
        if result.returncode == 0:
            print(f"[OK] Playwright Workspace '{workspace_name}' 已建立")
            set_playwright_workspace_env(get_playwright_workspace(workspace_resource_id))
            return

        stderr = (result.stderr or result.stdout or "").strip()
        print("[WARN] Playwright Workspace deployment 失敗，將繼續後續流程")
        if stderr:
            print(stderr)
        clear_playwright_workspace_vars("failed")
    except Exception as exc:
        print("[WARN] Playwright Workspace deployment 發生例外，將繼續後續流程")
        print(str(exc))
        clear_playwright_workspace_vars("failed")


def create_deployment(
    resource_group: str,
    account_name: str,
    deployment_name: str,
    model_name: str,
    model_version: str,
    sku_name: str,
    capacity: str,
):
    args = [
        "az",
        "cognitiveservices",
        "account",
        "deployment",
        "create",
        "--resource-group",
        resource_group,
        "--name",
        account_name,
        "--deployment-name",
        deployment_name,
        "--model-format",
        "OpenAI",
        "--model-name",
        model_name,
        "--sku-name",
        sku_name,
        "--sku-capacity",
        capacity,
        "--only-show-errors",
        "--output",
        "json",
    ]
    if model_version:
        args.extend([
            "--model-version",
            model_version,
        ])

    return run_command(args)


def get_best_effort_openai_models():
    configured_models = parse_json_env(BEST_EFFORT_OPENAI_MODELS_ENV)
    if isinstance(configured_models, list):
        return configured_models

    return DEFAULT_BEST_EFFORT_OPENAI_MODELS


def normalize_model_name(model_name: str) -> str:
    return model_name.strip().casefold()


def build_model_catalog_index(models: list[dict]) -> dict[str, list[dict]]:
    catalog_index: dict[str, list[dict]] = {}

    for item in models:
        model_name = str(item.get("name") or "").strip()
        if not model_name:
            continue

        catalog_index.setdefault(
            normalize_model_name(model_name), []).append(item)

    return catalog_index


def list_account_models(resource_group: str, account_name: str) -> list[dict]:
    result = run_command(
        [
            "az",
            "cognitiveservices",
            "account",
            "list-models",
            "--resource-group",
            resource_group,
            "--name",
            account_name,
            "--only-show-errors",
            "--output",
            "json",
        ]
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(message or "無法取得 AI Services account model catalog")

    try:
        models = json.loads(result.stdout or "[]")
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive guard
        raise RuntimeError("AI Services account model catalog 格式無法解析") from exc

    if not isinstance(models, list):  # pragma: no cover - defensive guard
        raise RuntimeError("AI Services account model catalog 格式不正確")

    return models


def choose_model_entry(entries: list[dict], requested_version: str) -> dict | None:
    if not entries:
        return None

    if requested_version:
        for item in entries:
            if str(item.get("version") or "").strip() == requested_version:
                return item
        return None

    default_entries = [
        item for item in entries if item.get("isDefaultVersion")]
    if default_entries:
        return default_entries[0]

    if len(entries) == 1:
        return entries[0]

    lifecycle_rank = {
        "generallyavailable": 2,
        "preview": 1,
    }

    return max(
        entries,
        key=lambda item: (
            lifecycle_rank.get(
                str(item.get("lifecycleStatus") or "").casefold(), 0),
            str(item.get("version") or ""),
        ),
    )


def resolve_requested_model(item: dict, catalog_index: dict[str, list[dict]]) -> dict:
    deployment_name = str(item.get("deploymentName")
                          or item.get("name") or "").strip()
    requested_model_name = str(item.get("modelName") or item.get(
        "model") or deployment_name).strip()
    requested_version = str(item.get("modelVersion")
                            or item.get("version") or "").strip()
    sku_name = str(item.get("skuName") or item.get(
        "sku") or "GlobalStandard").strip()
    capacity = str(item.get("capacity") or 1).strip()

    if not deployment_name or not requested_model_name:
        return {
            "status": "invalid",
            "deploymentName": deployment_name,
            "requestedModelName": requested_model_name,
            "reason": "missing-model-name",
            "message": "缺少 deploymentName 或 modelName",
        }

    normalized_name = normalize_model_name(requested_model_name)
    alias_name = BEST_EFFORT_MODEL_NAME_ALIASES.get(
        normalized_name, requested_model_name)
    catalog_entries = catalog_index.get(normalize_model_name(alias_name), [])
    if not catalog_entries:
        return {
            "status": "invalid",
            "deploymentName": deployment_name,
            "requestedModelName": requested_model_name,
            "reason": "model-not-in-catalog",
            "message": f"model '{requested_model_name}' 不在目前 account 的 list-models 裡",
        }

    entries = [
        item
        for item in catalog_entries
        if str(item.get("format") or "OpenAI").strip() == "OpenAI"
    ]
    if not entries:
        resolved_model_name = str(
            catalog_entries[0].get("name") or alias_name).strip()
        resolved_format = str(catalog_entries[0].get(
            "format") or "").strip() or "unknown"
        return {
            "status": "invalid",
            "deploymentName": deployment_name,
            "requestedModelName": requested_model_name,
            "resolvedModelName": resolved_model_name,
            "reason": "model-format-not-supported",
            "message": (
                f"model '{resolved_model_name}' 的 catalog format 是 '{resolved_format}'，"
                "這支 best-effort 腳本目前只會建立 OpenAI deployments"
            ),
        }

    selected_entry = choose_model_entry(entries, requested_version)
    if selected_entry is None:
        return {
            "status": "invalid",
            "deploymentName": deployment_name,
            "requestedModelName": requested_model_name,
            "resolvedModelName": str(entries[0].get("name") or alias_name).strip(),
            "requestedModelVersion": requested_version,
            "reason": "model-version-not-in-catalog",
            "message": (
                f"model '{requested_model_name}' 找不到版本 '{requested_version}'"
            ),
        }

    supported_sku = None
    for sku in selected_entry.get("skus", []):
        if str(sku.get("name") or "").strip().casefold() == sku_name.casefold():
            supported_sku = sku
            break

    resolved_model_name = str(selected_entry.get("name") or alias_name).strip()
    resolved_version = str(selected_entry.get("version")
                           or requested_version).strip()
    if supported_sku is None:
        return {
            "status": "invalid",
            "deploymentName": deployment_name,
            "requestedModelName": requested_model_name,
            "resolvedModelName": resolved_model_name,
            "resolvedModelVersion": resolved_version,
            "requestedModelVersion": requested_version,
            "reason": "sku-not-supported",
            "message": f"model '{resolved_model_name}' 不支援 SKU '{sku_name}'",
        }

    message = f"使用 model '{resolved_model_name}'"
    if requested_model_name != resolved_model_name:
        message = f"將 legacy model 名稱 '{requested_model_name}' 校正為 '{resolved_model_name}'"
    if not requested_version and resolved_version:
        message = f"{message} 的版本 '{resolved_version}'"

    return {
        "status": "ready",
        "deploymentName": deployment_name,
        "requestedModelName": requested_model_name,
        "requestedModelVersion": requested_version,
        "modelName": resolved_model_name,
        "modelVersion": resolved_version,
        "skuName": sku_name,
        "capacity": capacity,
        "message": message,
    }


def deploy_image_model(resource_group: str, account_name: str):
    deployment_name = (os.getenv("AZURE_IMAGE_MODEL_DEPLOYMENT") or "").strip()
    if not deployment_name:
        print("[SKIP] deployImageModel=false，略過 optional image model deployment")
        set_env_value("AZURE_IMAGE_MODEL_STATUS", "disabled")
        return

    try:
        model_name = get_required_env("AZURE_IMAGE_MODEL_NAME")
        model_version = get_required_env("AZURE_IMAGE_MODEL_VERSION")
        sku_name = (os.getenv("AZURE_IMAGE_MODEL_SKU")
                    or "GlobalStandard").strip()
        capacity = (os.getenv("AZURE_IMAGE_MODEL_CAPACITY") or "1").strip()

        print("[INFO] 嘗試部署 optional image model，不阻斷 azd up")

        if deployment_exists(resource_group, account_name, deployment_name):
            print(f"[OK] Image model deployment '{deployment_name}' 已存在")
            set_env_value("AZURE_IMAGE_MODEL_STATUS", "ready")
            return

        result = create_deployment(
            resource_group,
            account_name,
            deployment_name,
            model_name,
            model_version,
            sku_name,
            capacity,
        )
        if result.returncode == 0:
            print(f"[OK] Image model deployment '{deployment_name}' 已建立")
            set_env_value("AZURE_IMAGE_MODEL_STATUS", "ready")
            return

        stderr = (result.stderr or result.stdout or "").strip()
        print("[WARN] optional image model deployment 失敗，將繼續後續流程")
        if stderr:
            print(stderr)
        clear_image_deployment_vars("failed")
    except Exception as exc:
        print("[WARN] optional image model deployment 發生例外，將繼續後續流程")
        print(str(exc))
        clear_image_deployment_vars("failed")


def deploy_best_effort_openai_models(resource_group: str, account_name: str):
    requested_models = get_best_effort_openai_models()
    ready_deployments = []
    failed_deployments = []
    failure_details = []

    set_json_env_value(BEST_EFFORT_OPENAI_MODELS_ENV, requested_models)

    if not requested_models:
        print("[SKIP] 沒有設定 default OpenAI model bundle，略過 best-effort deployment")
        set_json_env_value(READY_OPENAI_MODELS_ENV, ready_deployments)
        set_json_env_value(FAILED_OPENAI_MODELS_ENV, failed_deployments)
        set_json_env_value(FAILED_OPENAI_MODEL_DETAILS_ENV, failure_details)
        set_env_value(OPENAI_MODELS_STATUS_ENV, "disabled")
        return

    print("[INFO] 嘗試部署 default OpenAI model bundle，不阻斷 azd up")
    catalog_index = build_model_catalog_index(
        list_account_models(resource_group, account_name))

    for item in requested_models:
        resolved_item = resolve_requested_model(item, catalog_index)
        deployment_name = str(resolved_item.get(
            "deploymentName") or "").strip()
        if resolved_item.get("status") != "ready":
            failure_details.append(resolved_item)
            if deployment_name:
                failed_deployments.append(deployment_name)
            print(
                f"[SKIP] OpenAI model deployment '{deployment_name or resolved_item.get('requestedModelName')}' 略過：{resolved_item.get('message')}"
            )
            continue

        model_name = str(resolved_item.get("modelName") or "").strip()
        model_version = str(resolved_item.get("modelVersion") or "").strip()
        sku_name = str(resolved_item.get("skuName")
                       or "GlobalStandard").strip()
        capacity = str(resolved_item.get("capacity") or 1).strip()

        if resolved_item.get("message"):
            print(
                f"[INFO] OpenAI model deployment '{deployment_name}' 解析完成：{resolved_item['message']}"
            )

        try:
            if deployment_exists(resource_group, account_name, deployment_name):
                print(f"[OK] OpenAI model deployment '{deployment_name}' 已存在")
                ready_deployments.append(deployment_name)
                continue

            result = create_deployment(
                resource_group,
                account_name,
                deployment_name,
                model_name,
                model_version,
                sku_name,
                capacity,
            )
            if result.returncode == 0:
                print(f"[OK] OpenAI model deployment '{deployment_name}' 已建立")
                ready_deployments.append(deployment_name)
                continue

            stderr = (result.stderr or result.stdout or "").strip()
            print(
                f"[WARN] OpenAI model deployment '{deployment_name}' 失敗，將繼續後續流程")
            if stderr:
                print(stderr)
            failed_deployments.append(deployment_name)
            failure_details.append(
                {
                    "status": "failed",
                    "deploymentName": deployment_name,
                    "requestedModelName": resolved_item.get("requestedModelName"),
                    "requestedModelVersion": resolved_item.get("requestedModelVersion"),
                    "modelName": model_name,
                    "modelVersion": model_version,
                    "skuName": sku_name,
                    "reason": "deployment-create-failed",
                    "message": stderr or "建立 deployment 時 Azure 回傳失敗",
                }
            )
        except Exception as exc:
            print(
                f"[WARN] OpenAI model deployment '{deployment_name}' 發生例外，將繼續後續流程")
            print(str(exc))
            failed_deployments.append(deployment_name)
            failure_details.append(
                {
                    "status": "failed",
                    "deploymentName": deployment_name,
                    "requestedModelName": resolved_item.get("requestedModelName"),
                    "requestedModelVersion": resolved_item.get("requestedModelVersion"),
                    "modelName": model_name,
                    "modelVersion": model_version,
                    "skuName": sku_name,
                    "reason": "deployment-exception",
                    "message": str(exc),
                }
            )

    set_json_env_value(READY_OPENAI_MODELS_ENV, ready_deployments)
    set_json_env_value(FAILED_OPENAI_MODELS_ENV, failed_deployments)
    set_json_env_value(FAILED_OPENAI_MODEL_DETAILS_ENV, failure_details)

    if failed_deployments and ready_deployments:
        set_env_value(OPENAI_MODELS_STATUS_ENV, "partial")
    elif failed_deployments:
        set_env_value(OPENAI_MODELS_STATUS_ENV, "failed")
    else:
        set_env_value(OPENAI_MODELS_STATUS_ENV, "ready")


def main() -> int:
    try:
        resource_group = get_required_env("AZURE_RESOURCE_GROUP")
        subscription_id = get_required_env("AZURE_SUBSCRIPTION_ID")
        account_name = get_required_env("AZURE_AI_SERVICES_NAME")
        wait_for_account(resource_group, account_name)
        deploy_playwright_workspace(resource_group, subscription_id)
        deploy_image_model(resource_group, account_name)
        deploy_best_effort_openai_models(resource_group, account_name)
        return 0
    except Exception as exc:
        print("[WARN] optional model deployment 發生例外，將繼續後續流程")
        print(str(exc))
        clear_playwright_workspace_vars("failed")
        clear_image_deployment_vars("failed")
        set_json_env_value(READY_OPENAI_MODELS_ENV, [])
        set_json_env_value(FAILED_OPENAI_MODELS_ENV, [])
        set_json_env_value(FAILED_OPENAI_MODEL_DETAILS_ENV, [])
        set_env_value(OPENAI_MODELS_STATUS_ENV, "failed")
        return 0


if __name__ == "__main__":
    sys.exit(main())
