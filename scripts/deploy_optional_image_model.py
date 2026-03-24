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

BEST_EFFORT_OPENAI_MODELS_ENV = "AZURE_BEST_EFFORT_OPENAI_MODEL_DEPLOYMENTS"
READY_OPENAI_MODELS_ENV = "AZURE_READY_BEST_EFFORT_OPENAI_MODEL_DEPLOYMENTS"
FAILED_OPENAI_MODELS_ENV = "AZURE_FAILED_BEST_EFFORT_OPENAI_MODEL_DEPLOYMENTS"
OPENAI_MODELS_STATUS_ENV = "AZURE_BEST_EFFORT_OPENAI_MODEL_DEPLOYMENTS_STATUS"

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
        "deploymentName": "gpt-oss-120B",
        "modelName": "gpt-oss-120B",
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
        "deploymentName": "gpt-5.2-codex",
        "modelName": "gpt-5.2-codex",
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
        "deploymentName": "gpt-5.3-codex",
        "modelName": "gpt-5.3-codex",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
    {
        "deploymentName": "gpt-5.2",
        "modelName": "gpt-5.2",
        "skuName": "GlobalStandard",
        "capacity": 1,
    },
    {
        "deploymentName": "gpt-5.4",
        "modelName": "gpt-5.4",
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
    {
        "deploymentName": "gpt-5.4-pro",
        "modelName": "gpt-5.4-pro",
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
    set_env_value(name, json.dumps(value, ensure_ascii=False, separators=(",", ":")))


def clear_image_deployment_vars(status: str):
    for env_name in IMAGE_DEPLOYMENT_ENV_VARS:
        unset_env_value(env_name)

    set_env_value("AZURE_IMAGE_MODEL_STATUS", status)


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


def deploy_image_model(resource_group: str, account_name: str):
    deployment_name = (os.getenv("AZURE_IMAGE_MODEL_DEPLOYMENT") or "").strip()
    if not deployment_name:
        print("[SKIP] deployImageModel=false，略過 optional image model deployment")
        set_env_value("AZURE_IMAGE_MODEL_STATUS", "disabled")
        return

    try:
        model_name = get_required_env("AZURE_IMAGE_MODEL_NAME")
        model_version = get_required_env("AZURE_IMAGE_MODEL_VERSION")
        sku_name = (os.getenv("AZURE_IMAGE_MODEL_SKU") or "GlobalStandard").strip()
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

    set_json_env_value(BEST_EFFORT_OPENAI_MODELS_ENV, requested_models)

    if not requested_models:
        print("[SKIP] 沒有設定 default OpenAI model bundle，略過 best-effort deployment")
        set_json_env_value(READY_OPENAI_MODELS_ENV, ready_deployments)
        set_json_env_value(FAILED_OPENAI_MODELS_ENV, failed_deployments)
        set_env_value(OPENAI_MODELS_STATUS_ENV, "disabled")
        return

    print("[INFO] 嘗試部署 default OpenAI model bundle，不阻斷 azd up")

    for item in requested_models:
        deployment_name = str(item.get("deploymentName") or item.get("name") or "").strip()
        model_name = str(item.get("modelName") or item.get("model") or deployment_name).strip()
        model_version = str(item.get("modelVersion") or item.get("version") or "").strip()
        sku_name = str(item.get("skuName") or item.get("sku") or "GlobalStandard").strip()
        capacity = str(item.get("capacity") or 1).strip()

        if not deployment_name or not model_name:
            continue

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
            print(f"[WARN] OpenAI model deployment '{deployment_name}' 失敗，將繼續後續流程")
            if stderr:
                print(stderr)
            failed_deployments.append(deployment_name)
        except Exception as exc:
            print(f"[WARN] OpenAI model deployment '{deployment_name}' 發生例外，將繼續後續流程")
            print(str(exc))
            failed_deployments.append(deployment_name)

    set_json_env_value(READY_OPENAI_MODELS_ENV, ready_deployments)
    set_json_env_value(FAILED_OPENAI_MODELS_ENV, failed_deployments)

    if failed_deployments and ready_deployments:
        set_env_value(OPENAI_MODELS_STATUS_ENV, "partial")
    elif failed_deployments:
        set_env_value(OPENAI_MODELS_STATUS_ENV, "failed")
    else:
        set_env_value(OPENAI_MODELS_STATUS_ENV, "ready")


def main() -> int:
    try:
        resource_group = get_required_env("AZURE_RESOURCE_GROUP")
        account_name = get_required_env("AZURE_AI_SERVICES_NAME")
        wait_for_account(resource_group, account_name)
        deploy_image_model(resource_group, account_name)
        deploy_best_effort_openai_models(resource_group, account_name)
        return 0
    except Exception as exc:
        print("[WARN] optional model deployment 發生例外，將繼續後續流程")
        print(str(exc))
        clear_image_deployment_vars("failed")
        set_json_env_value(READY_OPENAI_MODELS_ENV, [])
        set_json_env_value(FAILED_OPENAI_MODELS_ENV, [])
        set_env_value(OPENAI_MODELS_STATUS_ENV, "failed")
        return 0


if __name__ == "__main__":
    sys.exit(main())