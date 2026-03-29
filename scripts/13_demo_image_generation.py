"""Image generation optional demo。"""

import argparse
import base64
import os
from pathlib import Path

import requests

from load_env import load_all_env
from optional_demo_utils import (
    finish_skip,
    format_env_source,
    print_demo_header,
    resolve_env_value,
    resolve_image_model_deployment,
)

try:
    from azure.identity import DefaultAzureCredential
except ImportError:
    DefaultAzureCredential = None

load_all_env()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        default="一張乾淨清楚的網路維運儀表板海報，包含 outage 地圖與服務健康指標。",
    )
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--quality", default="low")
    parser.add_argument(
        "--output",
        default="data/default/generated_image_demo.png",
        help="產生 PNG 的輸出路徑，可用相對或絕對路徑。",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()

    print_demo_header(
        title="影像生成示範",
        description="呼叫 Azure OpenAI 影像生成 API，並把一張 PNG 存到本機。",
        env_items=[
            {"name": "AZURE_IMAGE_OPENAI_ENDPOINT",
                "value": os.getenv("AZURE_IMAGE_OPENAI_ENDPOINT")},
            {"name": "AZURE_IMAGE_ENDPOINT",
                "value": os.getenv("AZURE_IMAGE_ENDPOINT")},
            {"name": "AZURE_OPENAI_ENDPOINT",
                "value": os.getenv("AZURE_OPENAI_ENDPOINT")},
            {"name": "AZURE_AI_ENDPOINT",
                "value": os.getenv("AZURE_AI_ENDPOINT")},
            {"name": "AZURE_IMAGE_OPENAI_API_KEY", "value": os.getenv(
                "AZURE_IMAGE_OPENAI_API_KEY"), "mask": True},
            {"name": "AZURE_IMAGE_API_KEY", "value": os.getenv(
                "AZURE_IMAGE_API_KEY"), "mask": True},
            {"name": "AZURE_OPENAI_API_KEY", "value": os.getenv(
                "AZURE_OPENAI_API_KEY"), "mask": True},
            {"name": "AZURE_AI_KEY", "value": os.getenv(
                "AZURE_AI_KEY"), "mask": True},
            {"name": "AZURE_IMAGE_MODEL_DEPLOYMENT",
                "value": os.getenv("AZURE_IMAGE_MODEL_DEPLOYMENT")},
            {"name": "AZURE_IMAGE_MODEL",
                "value": os.getenv("AZURE_IMAGE_MODEL")},
        ],
    )

    endpoint, endpoint_name = resolve_env_value(
        "AZURE_IMAGE_OPENAI_ENDPOINT",
        "AZURE_IMAGE_ENDPOINT",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_AI_ENDPOINT",
        "AZURE_AI_SERVICES_ENDPOINT",
    )
    endpoint_source = format_env_source(
        endpoint_name,
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_AI_ENDPOINT",
        "AZURE_AI_SERVICES_ENDPOINT",
    )
    key, key_name = resolve_env_value(
        "AZURE_IMAGE_OPENAI_API_KEY",
        "AZURE_IMAGE_API_KEY",
        "AZURE_OPENAI_API_KEY",
        "AZURE_AI_KEY",
    )
    credential_source = format_env_source(
        key_name,
        "AZURE_OPENAI_API_KEY",
        "AZURE_AI_KEY",
    )
    deployment, deployment_name = resolve_image_model_deployment()

    # Support AAD bearer-token auth when no API key is set
    bearer_token = None
    if not key:
        if DefaultAzureCredential is None:
            finish_skip(
                "未設定 Azure OpenAI API key，而且環境中也沒有安裝 azure-identity。",
                strict=args.strict,
            )
        try:
            cred = DefaultAzureCredential()
            bearer_token = cred.get_token(
                "https://cognitiveservices.azure.com/.default").token
            credential_source = "DefaultAzureCredential（bearer token）"
        except Exception as exc:
            finish_skip(
                f"未設定 Azure OpenAI API key，而且 AAD 驗證失敗（{exc}）。",
                strict=args.strict,
            )

    if not endpoint:
        finish_skip(
            "影像生成所需的 Azure OpenAI endpoint 尚未設定。請設定 AZURE_IMAGE_OPENAI_ENDPOINT、AZURE_IMAGE_ENDPOINT、AZURE_OPENAI_ENDPOINT、AZURE_AI_ENDPOINT 或 AZURE_AI_SERVICES_ENDPOINT。",
            strict=args.strict,
        )

    if not deployment:
        finish_skip(
            "找不到 gpt-image deployment。請新增選用的影像模型 deployment，或透過環境變數指定。",
            strict=args.strict,
        )

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = Path(__file__).resolve().parent.parent / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    url = (
        endpoint.rstrip("/")
        + f"/openai/deployments/{deployment}/images/generations?api-version=2025-04-01-preview"
    )
    body = {
        "prompt": args.prompt,
        "n": 1,
        "size": args.size,
        "quality": args.quality,
        "output_format": "png",
    }

    print(f"Endpoint 來源：{endpoint_source}")
    print(f"憑證來源：{credential_source}")
    print(f"Deployment 來源：{deployment_name}")
    print(f"Deployment：{deployment}")
    print(f"輸出位置：{output_path}")

    headers = {"Content-Type": "application/json"}
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    else:
        headers["api-key"] = key

    try:
        response = requests.post(
            url,
            headers=headers,
            json=body,
            timeout=180,
        )
    except requests.RequestException as exc:
        finish_skip(
            f"無法送出影像生成請求（{exc}）",
            strict=args.strict,
        )

    if response.status_code >= 400:
        finish_skip(
            f"目前這個環境還無法使用影像生成（{response.status_code}: {response.text[:300]}）",
            strict=args.strict,
        )

    payload = response.json()
    images = payload.get("data") or []
    if not images or not images[0].get("b64_json"):
        finish_skip(
            "影像生成沒有回傳 base64 圖片資料。",
            strict=args.strict,
        )

    image_bytes = base64.b64decode(images[0]["b64_json"])
    output_path.write_bytes(image_bytes)

    print("\n[SUCCESS] 已完成影像生成")
    print(f"已儲存檔案：{output_path}")


if __name__ == "__main__":
    main()
