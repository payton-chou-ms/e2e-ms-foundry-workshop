"""Analyze a local file with Azure Content Understanding using inline data upload."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]


def _env_file_has_core_azure_values(env_path: Path) -> bool:
    try:
        content = env_path.read_text(encoding="utf-8")
    except OSError:
        return False

    return any(
        token in content
        for token in (
            "AZURE_AI_PROJECT_ENDPOINT=",
            "AZURE_AI_SEARCH_ENDPOINT=",
            "AZURE_AI_ENDPOINT=",
        )
    )


def load_all_env() -> None:
    azure_dir = ROOT_DIR / ".azure"
    shell_env_name = os.environ.get("AZURE_ENV_NAME", "").strip()
    default_env_name = ""

    config_path = azure_dir / "config.json"
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))
        default_env_name = str(config.get("defaultEnvironment", "")).strip()

    candidate_env_names: list[str] = []
    if shell_env_name:
        candidate_env_names.append(shell_env_name)
    if default_env_name and default_env_name not in candidate_env_names:
        candidate_env_names.append(default_env_name)

    for env_name in candidate_env_names:
        env_path = azure_dir / env_name / ".env"
        if env_path.exists() and _env_file_has_core_azure_values(env_path):
            load_dotenv(env_path)
            break

    project_env = ROOT_DIR / ".env"
    if project_env.exists():
        load_dotenv(project_env, override=False)


def resolve_env_value(*names: str) -> tuple[str | None, str | None]:
    for name in names:
        value = os.getenv(name)
        if value:
            return value, name
    return None, None


load_all_env()

IMPORT_ERROR = None

try:
    from azure.ai.contentunderstanding import ContentUnderstandingClient
    from azure.core.credentials import AzureKeyCredential
    from azure.identity import DefaultAzureCredential
except ImportError as exc:  # pragma: no cover - depends on local runtime
    IMPORT_ERROR = exc


class LiveCuError(RuntimeError):
    """Expected live Azure Content Understanding failure."""


def create_content_understanding_client() -> ContentUnderstandingClient:
    if IMPORT_ERROR is not None:
        raise LiveCuError(
            "缺少 Azure SDK。請先安裝 requirements.txt，至少需要 azure-ai-contentunderstanding 與 azure-identity。"
        ) from IMPORT_ERROR

    endpoint, _ = resolve_env_value(
        "CONTENTUNDERSTANDING_ENDPOINT",
        "CONTENT_UNDERSTANDING_ENDPOINT",
        "AZURE_AI_ENDPOINT",
    )
    if not endpoint:
        raise LiveCuError(
            "找不到 Content Understanding endpoint。請設定 CONTENTUNDERSTANDING_ENDPOINT，或直接沿用 AZURE_AI_ENDPOINT。"
        )

    key, _ = resolve_env_value(
        "CONTENTUNDERSTANDING_KEY",
        "CONTENT_UNDERSTANDING_KEY",
        "AZURE_AI_KEY",
    )
    credential = AzureKeyCredential(key) if key else DefaultAzureCredential()
    return ContentUnderstandingClient(endpoint=endpoint, credential=credential)


def _primitive_or_none(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    return None


def result_to_dict(value: Any) -> Any:
    primitive = _primitive_or_none(value)
    if primitive is not None:
        return primitive
    if isinstance(value, list):
        return [result_to_dict(item) for item in value]
    if isinstance(value, dict):
        return {key: result_to_dict(item) for key, item in value.items()}
    if hasattr(value, "as_dict"):
        try:
            return result_to_dict(value.as_dict())
        except TypeError:
            pass
    if hasattr(value, "items"):
        try:
            return {key: result_to_dict(item) for key, item in value.items()}
        except Exception:
            pass
    if hasattr(value, "__dict__"):
        return {
            key: result_to_dict(item)
            for key, item in vars(value).items()
            if not key.startswith("_")
        }
    return repr(value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="要直接以 data upload 分析的本機文件路徑。")
    parser.add_argument(
        "--analyzer-id",
        default="prebuilt-layout",
        help="Content Understanding analyzer id。預設為 prebuilt-layout。",
    )
    parser.add_argument(
        "--processing-location",
        choices=["geography", "dataZone", "global"],
        help="選填：覆蓋 Content Understanding 的 processing location。",
    )
    parser.add_argument("--output-json", help="將完整分析結果寫到指定 JSON 路徑。")
    parser.add_argument(
        "--max-markdown-chars",
        type=int,
        default=1200,
        help="終端顯示的 markdown 最大字數。",
    )
    parser.add_argument(
        "--poll-timeout-seconds",
        type=int,
        default=600,
        help="等待 Content Understanding 分析完成的最長秒數。",
    )
    return parser.parse_args()


def summarize_markdown(markdown: str, max_chars: int) -> str:
    excerpt = markdown[:max_chars]
    if len(markdown) > max_chars:
        excerpt += "\n\n... [truncated]"
    return excerpt


def extract_markdown(result, source_name: str) -> str:
    contents = getattr(result, "contents", None) or []
    if not contents:
        raise LiveCuError(
            f"Azure Content Understanding 沒有回傳內容：{source_name}。"
            "這代表 data upload 請求已送達，但服務沒有產生可用內容。"
        )

    markdown = getattr(contents[0], "markdown", "") or ""
    normalized = markdown.strip()
    if not normalized or normalized == "```text\n\n```":
        raise LiveCuError(
            f"Azure Content Understanding markdown 為空：{source_name}。"
            "這代表 data upload 模式可避開 Blob 權限問題，但目前服務仍未對該文件產生可用 markdown。"
        )
    return markdown


def main() -> None:
    args = parse_args()
    file_path = Path(args.file)
    if not file_path.is_absolute():
        file_path = Path(__file__).resolve().parent.parent.parent / file_path
    file_path = file_path.resolve()

    if not file_path.exists():
        raise SystemExit(f"找不到檔案：{file_path}")

    try:
        print(f"[INFO] 準備以 data upload 分析：{file_path}", flush=True)
        client = create_content_understanding_client()

        with open(file_path, "rb") as handle:
            file_bytes = handle.read()

        print("[INFO] 呼叫 Azure Content Understanding (data upload)", flush=True)
        poller = client.begin_analyze_binary(
            analyzer_id=args.analyzer_id,
            binary_input=file_bytes,
            processing_location=args.processing_location,
        )

        operation_id = getattr(poller, "operation_id", None)
        result = poller.result(timeout=args.poll_timeout_seconds)
        markdown = extract_markdown(result, source_name=file_path.name)

        print("[SUCCESS] Data upload analyze 完成")
        print(f"檔案：{file_path}")
        if operation_id:
            print(f"Operation ID：{operation_id}")

        print("\nMarkdown 摘要：")
        print("=" * 60)
        print(summarize_markdown(markdown, args.max_markdown_chars))
        print("=" * 60)

        if args.output_json:
            output_path = Path(args.output_json)
            if not output_path.is_absolute():
                output_path = Path.cwd() / output_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "file": str(file_path),
                "input_mode": "data-upload",
                "analyzer_id": args.analyzer_id,
                "operation_id": operation_id,
                "result": result_to_dict(result),
            }
            output_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"JSON 已寫出：{output_path}")
    except Exception as error:
        raise SystemExit(f"[ERROR] {error}") from error


if __name__ == "__main__":
    main()
