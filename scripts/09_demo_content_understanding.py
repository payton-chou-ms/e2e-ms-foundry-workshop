"""Azure Content Understanding optional demo。"""

import argparse
import os
from pathlib import Path

from load_env import load_all_env
from optional_demo_utils import (
    finish_skip,
    format_env_source,
    print_demo_header,
    resolve_env_value,
)

load_all_env()

IMPORT_ERROR = None

try:
    from azure.ai.contentunderstanding import ContentUnderstandingClient
    from azure.ai.contentunderstanding.models import DocumentContent
    from azure.core.credentials import AzureKeyCredential
    from azure.core.exceptions import ClientAuthenticationError, HttpResponseError
    from azure.identity import DefaultAzureCredential
except ImportError as exc:  # pragma: no cover - exercised via runtime environment
    IMPORT_ERROR = exc


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        help="本機 PDF 或 Office 文件路徑。預設使用 workshop 產生的 PDF。",
    )
    parser.add_argument(
        "--processing-location",
        choices=["geography", "dataZone", "global"],
        help="選填：覆蓋 Content Understanding 的 processing location。",
    )
    parser.add_argument(
        "--max-markdown-chars",
        type=int,
        default=1200,
        help="要列印的分析結果 markdown 最大字數。",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="遇到 skip 條件時回傳結束碼 1，而不是成功結束。",
    )
    return parser.parse_args()


def resolve_default_file():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    data_folder = os.getenv("DATA_FOLDER")
    if data_folder:
        candidate_root = Path(data_folder)
        if not candidate_root.is_absolute():
            candidate_root = project_root / candidate_root
    else:
        candidate_root = project_root / "data" / "default"

    documents_dir = candidate_root / "documents"
    preferred_names = [
        "outage_management_policies.pdf",
        "customer_service_policies.pdf",
        "ticket_management_policies.pdf",
    ]

    for name in preferred_names:
        candidate = documents_dir / name
        if candidate.exists():
            return candidate

    pdf_files = sorted(documents_dir.glob("*.pdf"))
    if pdf_files:
        return pdf_files[0]

    return None


def build_skip_message(error):
    error_text = str(error)
    lowered = error_text.lower()
    status_code = getattr(error, "status_code", None)

    if isinstance(error, ClientAuthenticationError) or status_code in {401, 403}:
        return (
            "驗證或授權尚未就緒。請先用 Azure 身分登入，並確認呼叫者在 Foundry 資源上具有 Cognitive Services User 權限。"
        )

    if "model" in lowered and "deployment" in lowered:
        return (
            "尚未設定 Content Understanding 預設模型 deployment。執行 demo 前，請先把 gpt-4.1-mini 與主要的 text-embedding-3-large deployment 設成資源預設值。"
        )

    if "default" in lowered and "deployment" in lowered:
        return (
            "缺少 Content Understanding 預設值。請先到設定頁面，或先完成資源層級的預設設定後再執行 demo。"
        )

    if "defaultsnotset" in lowered:
        return (
            "尚未設定 Content Understanding 預設值。請先設定預設值，再重新執行。"
        )

    if "region" in lowered or "location" in lowered or status_code == 400:
        return (
            "目前的資源區域或 processing location 不支援這項能力。請改用支援的區域，或移除 processing location override。"
        )

    if status_code in {429, 503}:
        return "配額、容量或暫時性的服務可用性問題，導致這個 demo 無法執行。"

    return f"目前這個環境還無法使用這項選用能力（{error_text}）"


def summarize_document(content, max_markdown_chars):
    markdown = getattr(content, "markdown", "") or ""
    excerpt = markdown[:max_markdown_chars]
    if len(markdown) > max_markdown_chars:
        excerpt += "\n\n... [truncated]"

    print("\n[SUCCESS] Content Understanding 分析完成")
    print(
        f"文件類型：{getattr(content, 'mime_type', None) or '（未知）'}")

    if isinstance(content, DocumentContent):
        start_page = getattr(content, "start_page_number", None)
        end_page = getattr(content, "end_page_number", None)
        if start_page and end_page:
            print(f"頁碼範圍：{start_page} 到 {end_page}")

        pages = getattr(content, "pages", None) or []
        tables = getattr(content, "tables", None) or []
        figures = getattr(content, "figures", None) or []

        print(f"頁數：{len(pages)}")
        print(f"表格數：{len(tables)}")
        print(f"圖片數：{len(figures)}")

    print("\nMarkdown 摘要：")
    print("=" * 60)
    print(excerpt or "（沒有回傳 markdown）")
    print("=" * 60)


def main():
    args = parse_args()

    if args.file:
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = Path(__file__).resolve().parent.parent / file_path
    else:
        file_path = resolve_default_file()

    print_demo_header(
        title="Content Understanding 示範",
        description="使用 prebuilt-documentSearch analyzer 分析 workshop 的本機 PDF。",
        env_items=[
            {"name": "CONTENTUNDERSTANDING_ENDPOINT",
                "value": os.getenv("CONTENTUNDERSTANDING_ENDPOINT")},
            {"name": "CONTENT_UNDERSTANDING_ENDPOINT",
                "value": os.getenv("CONTENT_UNDERSTANDING_ENDPOINT")},
            {"name": "AZURE_AI_ENDPOINT",
                "value": os.getenv("AZURE_AI_ENDPOINT")},
            {"name": "CONTENTUNDERSTANDING_KEY", "value": os.getenv(
                "CONTENTUNDERSTANDING_KEY"), "mask": True},
            {"name": "CONTENT_UNDERSTANDING_KEY", "value": os.getenv(
                "CONTENT_UNDERSTANDING_KEY"), "mask": True},
            {"name": "AZURE_AI_KEY", "value": os.getenv(
                "AZURE_AI_KEY"), "mask": True},
            {"name": "DATA_FOLDER", "value": os.getenv("DATA_FOLDER")},
        ],
    )
    print(f"輸入檔案：{file_path or '（找不到）'}")
    print("Analyzer：prebuilt-documentSearch")
    if args.processing_location:
        print(f"Processing location override：{args.processing_location}")

    if IMPORT_ERROR is not None:
        finish_skip(
            "尚未安裝 azure-ai-contentunderstanding。請執行 'pip install -r requirements.txt'。",
            strict=args.strict,
        )

    endpoint, endpoint_name = resolve_env_value(
        "CONTENTUNDERSTANDING_ENDPOINT",
        "CONTENT_UNDERSTANDING_ENDPOINT",
        "AZURE_AI_ENDPOINT",
    )
    endpoint_source = format_env_source(
        endpoint_name,
        "AZURE_AI_ENDPOINT",
    )
    if not endpoint:
        finish_skip(
            "找不到 Content Understanding endpoint。請設定 CONTENTUNDERSTANDING_ENDPOINT、CONTENT_UNDERSTANDING_ENDPOINT，或直接沿用 AZURE_AI_ENDPOINT。",
            strict=args.strict,
        )

    key, key_name = resolve_env_value(
        "CONTENTUNDERSTANDING_KEY",
        "CONTENT_UNDERSTANDING_KEY",
        "AZURE_AI_KEY",
    )
    credential_source = format_env_source(
        key_name,
        "AZURE_AI_KEY",
    )

    if not file_path or not file_path.exists():
        finish_skip(
            "找不到這個 demo 需要的本機 PDF。請先產生範例資料，或自行提供 --file。",
            strict=args.strict,
        )

    credential = AzureKeyCredential(key) if key else DefaultAzureCredential()
    client = ContentUnderstandingClient(
        endpoint=endpoint, credential=credential)

    print(f"Endpoint 來源：{endpoint_source}")
    print(f"憑證來源：{credential_source if key_name else 'DefaultAzureCredential'}")
    if args.processing_location:
        print(f"Processing location：{args.processing_location}")

    try:
        with open(file_path, "rb") as file_handle:
            file_bytes = file_handle.read()

        poller = client.begin_analyze_binary(
            analyzer_id="prebuilt-documentSearch",
            binary_input=file_bytes,
            processing_location=args.processing_location,
        )
        operation_id = getattr(poller, "operation_id", None)
        if operation_id:
            print(f"Operation ID：{operation_id}")

        result = poller.result()
        if not getattr(result, "contents", None):
            finish_skip(
                "分析已完成，但沒有回傳內容。這項能力可能還沒完全設定好。",
                strict=args.strict,
            )

        summarize_document(result.contents[0], args.max_markdown_chars)
    except (ClientAuthenticationError, HttpResponseError) as exc:
        # Auto-configure defaults if they haven't been set
        inner = getattr(exc, "error", None)
        inner_code = getattr(inner, "code", "") or ""
        inner_msg = str(getattr(inner, "message", "")) if inner else ""
        if "DefaultsNotSet" in inner_code or "DefaultsNotSet" in inner_msg or "DefaultsNotSet" in str(exc):
            print("尚未設定 Content Understanding 預設值，正在自動補上設定...")
            try:
                client.update_defaults(model_deployments={
                    "gpt-4.1-mini": "gpt-4.1-mini",
                    "text-embedding-3-large": "text-embedding-3-large",
                })
                print("預設值設定完成，重新執行分析...")
                poller = client.begin_analyze_binary(
                    analyzer_id="prebuilt-documentSearch",
                    binary_input=file_bytes,
                    processing_location=args.processing_location,
                )
                result = poller.result()
                if not getattr(result, "contents", None):
                    finish_skip(
                        "補上預設值後分析已完成，但仍沒有回傳內容。",
                        strict=args.strict,
                    )
                summarize_document(result.contents[0], args.max_markdown_chars)
            except (ClientAuthenticationError, HttpResponseError) as retry_exc:
                finish_skip(build_skip_message(retry_exc), strict=args.strict)
        else:
            finish_skip(build_skip_message(exc), strict=args.strict)
    finally:
        close_method = getattr(credential, "close", None)
        if callable(close_method):
            close_method()


if __name__ == "__main__":
    main()
