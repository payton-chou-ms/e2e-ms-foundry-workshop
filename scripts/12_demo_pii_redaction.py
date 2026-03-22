"""PII 偵測與遮罩 optional demo。"""

import argparse
import os
import time

from load_env import load_all_env
from optional_demo_utils import finish_skip, print_demo_header, resolve_env_value

load_all_env()

IMPORT_ERROR = None

try:
    from azure.ai.textanalytics import TextAnalyticsClient
    from azure.core.credentials import AzureKeyCredential
    from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ServiceRequestError
    from azure.identity import DefaultAzureCredential
except ImportError as exc:  # pragma: no cover - runtime dependent
    IMPORT_ERROR = exc


DEFAULT_TEXT = (
    "Customer Jane Doe can be reached at jane.doe@contoso.com or 425-555-0199. "
    "Her outage account number is 987654321 and her address is 1 Microsoft Way, Redmond, WA."
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default=DEFAULT_TEXT)
    parser.add_argument("--language", default="en")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()

    print_demo_header(
        title="PII 遮罩示範",
        description="把一小段文字送到 Azure Language，展示遮罩後結果與偵測到的敏感資訊實體。",
        env_items=[
            {"name": "AZURE_LANGUAGE_ENDPOINT",
                "value": os.getenv("AZURE_LANGUAGE_ENDPOINT")},
            {"name": "LANGUAGE_ENDPOINT",
                "value": os.getenv("LANGUAGE_ENDPOINT")},
            {"name": "AZURE_AI_ENDPOINT",
                "value": os.getenv("AZURE_AI_ENDPOINT")},
            {"name": "AZURE_LANGUAGE_KEY", "value": os.getenv(
                "AZURE_LANGUAGE_KEY"), "mask": True},
            {"name": "LANGUAGE_KEY", "value": os.getenv(
                "LANGUAGE_KEY"), "mask": True},
            {"name": "AZURE_AI_KEY", "value": os.getenv(
                "AZURE_AI_KEY"), "mask": True},
        ],
    )

    if IMPORT_ERROR is not None:
        finish_skip(
            "尚未安裝 azure-ai-textanalytics。請執行 'pip install -r requirements.txt'。",
            strict=args.strict,
        )

    endpoint, endpoint_name = resolve_env_value(
        "AZURE_LANGUAGE_ENDPOINT",
        "LANGUAGE_ENDPOINT",
        "AZURE_AI_ENDPOINT",
    )
    key, key_name = resolve_env_value(
        "AZURE_LANGUAGE_KEY",
        "LANGUAGE_KEY",
        "AZURE_AI_KEY",
    )

    if not endpoint:
        finish_skip(
            "尚未設定 Language endpoint。請設定 AZURE_LANGUAGE_ENDPOINT 或 AZURE_AI_ENDPOINT 後再執行 PII demo。",
            strict=args.strict,
        )

    if key:
        credential = AzureKeyCredential(key)
        cred_source = key_name
    else:
        credential = DefaultAzureCredential()
        cred_source = "DefaultAzureCredential"

    print(f"Endpoint 來源：{endpoint_name}")
    print(f"憑證來源：{cred_source}")
    print(f"輸入文字：{args.text}")

    client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=credential,
    )

    try:
        last_error = None
        for attempt in range(3):
            try:
                results = client.recognize_pii_entities(
                    [args.text], language=args.language)
                result = results[0]
                break
            except ServiceRequestError as exc:
                last_error = exc
                if attempt == 2:
                    raise
                time.sleep(2)
        else:
            raise last_error
    except (ClientAuthenticationError, HttpResponseError, ServiceRequestError) as exc:
        finish_skip(
            f"目前這個環境還無法使用 PII 偵測（{exc}）",
            strict=args.strict,
        )

    if result.is_error:
        finish_skip(
            f"PII 偵測回傳錯誤：{result.error.message}",
            strict=args.strict,
        )

    print("\n[SUCCESS] 已偵測到 PII 實體")
    print(f"遮罩後文字：{result.redacted_text}")
    print("\n實體清單：")
    for entity in result.entities:
        print(
            f"- {entity.text} | 類別={entity.category} | 信心分數={entity.confidence_score:.2f}"
        )


if __name__ == "__main__":
    main()
