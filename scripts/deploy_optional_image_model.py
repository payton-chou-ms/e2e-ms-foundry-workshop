"""Best-effort deployment of the optional image model after azd provision."""

from __future__ import annotations

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


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, check=False)


def set_env_value(name: str, value: str):
    run_command(["azd", "env", "set", name, value])


def unset_env_value(name: str):
    run_command(["azd", "env", "unset", name])


def clear_image_deployment_vars(status: str):
    for env_name in IMAGE_DEPLOYMENT_ENV_VARS:
        unset_env_value(env_name)

    set_env_value("AZURE_IMAGE_MODEL_STATUS", status)


def get_required_env(name: str) -> str:
    value = (os.getenv(name) or "").strip()
    if not value:
        raise ValueError(f"缺少必要環境變數：{name}")
    return value


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
    return run_command(
        [
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
            "--model-version",
            model_version,
            "--sku-name",
            sku_name,
            "--sku-capacity",
            capacity,
            "--only-show-errors",
            "--output",
            "json",
        ]
    )


def main() -> int:
    deployment_name = (os.getenv("AZURE_IMAGE_MODEL_DEPLOYMENT") or "").strip()
    if not deployment_name:
        print("[SKIP] deployImageModel=false，略過 optional image model deployment")
        set_env_value("AZURE_IMAGE_MODEL_STATUS", "disabled")
        return 0

    try:
        resource_group = get_required_env("AZURE_RESOURCE_GROUP")
        account_name = get_required_env("AZURE_AI_SERVICES_NAME")
        model_name = get_required_env("AZURE_IMAGE_MODEL_NAME")
        model_version = get_required_env("AZURE_IMAGE_MODEL_VERSION")
        sku_name = (os.getenv("AZURE_IMAGE_MODEL_SKU") or "GlobalStandard").strip()
        capacity = (os.getenv("AZURE_IMAGE_MODEL_CAPACITY") or "1").strip()

        print("[INFO] 嘗試部署 optional image model，不阻斷 azd up")
        wait_for_account(resource_group, account_name)

        if deployment_exists(resource_group, account_name, deployment_name):
            print(f"[OK] Image model deployment '{deployment_name}' 已存在")
            set_env_value("AZURE_IMAGE_MODEL_STATUS", "ready")
            return 0

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
            return 0

        stderr = (result.stderr or result.stdout or "").strip()
        print("[WARN] optional image model deployment 失敗，將繼續後續流程")
        if stderr:
            print(stderr)
        clear_image_deployment_vars("failed")
        return 0
    except Exception as exc:
        print("[WARN] optional image model deployment 發生例外，將繼續後續流程")
        print(str(exc))
        clear_image_deployment_vars("failed")
        return 0


if __name__ == "__main__":
    sys.exit(main())