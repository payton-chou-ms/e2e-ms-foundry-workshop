"""12 - Optional demo: PII detection and redaction.

Uses Azure Language PII detection to show a small redact-and-explain workflow.
When the resource or credentials are unavailable, it prints SKIP and exits 0
unless --strict is used.
"""

import argparse
import os

from load_env import load_all_env
from optional_demo_utils import finish_skip, resolve_env_value

load_all_env()

IMPORT_ERROR = None

try:
    from azure.ai.textanalytics import TextAnalyticsClient
    from azure.core.credentials import AzureKeyCredential
    from azure.core.exceptions import ClientAuthenticationError, HttpResponseError
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

    if IMPORT_ERROR is not None:
        finish_skip(
            "azure-ai-textanalytics is not installed. Run 'pip install -r scripts/requirements.txt'.",
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
            "Language endpoint is not configured. Set AZURE_LANGUAGE_ENDPOINT or AZURE_AI_ENDPOINT to run the PII demo.",
            strict=args.strict,
        )

    if key:
        credential = AzureKeyCredential(key)
        cred_source = key_name
    else:
        credential = DefaultAzureCredential()
        cred_source = "DefaultAzureCredential"

    print("\n" + "=" * 60)
    print("PII Redaction Demo")
    print("=" * 60)
    print(f"Endpoint source: {endpoint_name}")
    print(f"Credential source: {cred_source}")
    print(f"Input text: {args.text}")

    client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=credential,
    )

    try:
        results = client.recognize_pii_entities(
            [args.text], language=args.language)
        result = results[0]
    except (ClientAuthenticationError, HttpResponseError) as exc:
        finish_skip(
            f"PII detection is not available in this environment yet ({exc})",
            strict=args.strict,
        )

    if result.is_error:
        finish_skip(
            f"PII detection returned an error: {result.error.message}",
            strict=args.strict,
        )

    print("\n[SUCCESS] PII entities detected")
    print(f"Redacted text: {result.redacted_text}")
    print("\nEntities:")
    for entity in result.entities:
        print(
            f"- {entity.text} | category={entity.category} | confidence={entity.confidence_score:.2f}"
        )


if __name__ == "__main__":
    main()
