"""
09 - Optional demo: Azure Content Understanding

Analyze a local workshop PDF with the prebuilt-documentSearch analyzer.

Usage:
    python scripts/09_demo_content_understanding.py
    python scripts/09_demo_content_understanding.py --file data/default/documents/outage_management_policies.pdf
    python scripts/09_demo_content_understanding.py --strict

Default behavior is non-blocking for optional capability issues. The script prints
"SKIP:" and exits with code 0 when the capability is not configured.
Use --strict to convert skip conditions into exit code 1 for debugging.
"""

import argparse
import os
from pathlib import Path

from load_env import load_all_env
from optional_demo_utils import finish_skip, print_demo_header, resolve_env_value

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
        help="Path to a local PDF or Office document. Defaults to a generated workshop PDF.",
    )
    parser.add_argument(
        "--processing-location",
        choices=["geography", "dataZone", "global"],
        help="Optional Content Understanding processing location override.",
    )
    parser.add_argument(
        "--max-markdown-chars",
        type=int,
        default=1200,
        help="Maximum markdown characters to print from the analyzed document.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 on skip conditions instead of returning success.",
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
            "authentication or authorization is not ready. Sign in with Azure credentials "
            "and ensure the caller has Cognitive Services User access on the Foundry resource."
        )

    if "model" in lowered and "deployment" in lowered:
        return (
            "Content Understanding default model deployments are not configured. "
            "Configure the resource defaults for gpt-4.1-mini and the primary text-embedding-3-large deployment "
            "before running the demo."
        )

    if "default" in lowered and "deployment" in lowered:
        return (
            "Content Understanding defaults are missing. Open the Content Understanding settings "
            "page or configure resource-level defaults before running the demo."
        )

    if "defaultsnotset" in lowered:
        return (
            "Content Understanding defaults have not been configured. "
            "Run with --auto-defaults or call client.update_defaults() first."
        )

    if "region" in lowered or "location" in lowered or status_code == 400:
        return (
            "the resource region or processing location is not supported for this capability. "
            "Use a supported Content Understanding region or omit the processing location override."
        )

    if status_code in {429, 503}:
        return "quota, capacity, or temporary service availability prevented the demo from running."

    return f"optional capability is not available in this environment yet ({error_text})"


def summarize_document(content, max_markdown_chars):
    markdown = getattr(content, "markdown", "") or ""
    excerpt = markdown[:max_markdown_chars]
    if len(markdown) > max_markdown_chars:
        excerpt += "\n\n... [truncated]"

    print("\n[SUCCESS] Content Understanding analysis completed")
    print(
        f"Document type: {getattr(content, 'mime_type', None) or '(unknown)'}")

    if isinstance(content, DocumentContent):
        start_page = getattr(content, "start_page_number", None)
        end_page = getattr(content, "end_page_number", None)
        if start_page and end_page:
            print(f"Pages: {start_page} to {end_page}")

        pages = getattr(content, "pages", None) or []
        tables = getattr(content, "tables", None) or []
        figures = getattr(content, "figures", None) or []

        print(f"Page count: {len(pages)}")
        print(f"Table count: {len(tables)}")
        print(f"Figure count: {len(figures)}")

    print("\nMarkdown excerpt:")
    print("=" * 60)
    print(excerpt or "(No markdown returned)")
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
        title="Content Understanding Demo",
        description="Analyze a local workshop PDF with the prebuilt-documentSearch analyzer.",
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
    print(f"Input file: {file_path or '(not found)'}")
    print("Analyzer: prebuilt-documentSearch")
    if args.processing_location:
        print(f"Processing location override: {args.processing_location}")

    if IMPORT_ERROR is not None:
        finish_skip(
            "azure-ai-contentunderstanding is not installed. Run 'pip install -r requirements.txt'.",
            strict=args.strict,
        )

    endpoint, endpoint_name = resolve_env_value(
        "CONTENTUNDERSTANDING_ENDPOINT",
        "CONTENT_UNDERSTANDING_ENDPOINT",
        "AZURE_AI_ENDPOINT",
    )
    if not endpoint:
        finish_skip(
            "no Content Understanding endpoint was found. Set CONTENTUNDERSTANDING_ENDPOINT or reuse AZURE_AI_ENDPOINT.",
            strict=args.strict,
        )

    key, key_name = resolve_env_value(
        "CONTENTUNDERSTANDING_KEY",
        "CONTENT_UNDERSTANDING_KEY",
        "AZURE_AI_KEY",
    )

    if not file_path or not file_path.exists():
        finish_skip(
            "no local PDF was found for the demo. Generate sample data first or provide --file.",
            strict=args.strict,
        )

    credential = AzureKeyCredential(key) if key else DefaultAzureCredential()
    client = ContentUnderstandingClient(
        endpoint=endpoint, credential=credential)

    print(f"Endpoint source: {endpoint_name}")
    print(f"Credential source: {key_name or 'DefaultAzureCredential'}")
    if args.processing_location:
        print(f"Processing location: {args.processing_location}")

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
            print(f"Operation ID: {operation_id}")

        result = poller.result()
        if not getattr(result, "contents", None):
            finish_skip(
                "analysis completed but returned no content. The capability may not be fully configured.",
                strict=args.strict,
            )

        summarize_document(result.contents[0], args.max_markdown_chars)
    except (ClientAuthenticationError, HttpResponseError) as exc:
        # Auto-configure defaults if they haven't been set
        inner = getattr(exc, "error", None)
        inner_code = getattr(inner, "code", "") or ""
        inner_msg = str(getattr(inner, "message", "")) if inner else ""
        if "DefaultsNotSet" in inner_code or "DefaultsNotSet" in inner_msg or "DefaultsNotSet" in str(exc):
            print("Content Understanding defaults not configured. Auto-configuring...")
            try:
                client.update_defaults(model_deployments={
                    "gpt-4.1-mini": "gpt-4.1-mini",
                    "text-embedding-3-large": "text-embedding-3-large",
                })
                print("Defaults configured. Retrying analysis...")
                poller = client.begin_analyze_binary(
                    analyzer_id="prebuilt-documentSearch",
                    binary_input=file_bytes,
                    processing_location=args.processing_location,
                )
                result = poller.result()
                if not getattr(result, "contents", None):
                    finish_skip(
                        "analysis completed but returned no content after configuring defaults.",
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
