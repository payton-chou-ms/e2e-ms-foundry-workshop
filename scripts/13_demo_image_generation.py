"""13 - Optional demo: image generation with gpt-image-1.

This demo uses the Azure OpenAI image generation REST API. If an image-capable
deployment is not configured, it prints SKIP and exits 0 unless --strict is
used.
"""

import argparse
import base64
import os
from pathlib import Path

import requests

from load_env import load_all_env
from optional_demo_utils import finish_skip, resolve_env_value, resolve_image_model_deployment

load_all_env()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        default="A clean network operations dashboard poster with outage maps and service health indicators.",
    )
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--quality", default="low")
    parser.add_argument(
        "--output",
        default="data/default/generated_image_demo.png",
        help="Relative or absolute output path for the generated PNG.",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()

    endpoint, endpoint_name = resolve_env_value(
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_AI_ENDPOINT",
        "AZURE_AI_SERVICES_ENDPOINT",
    )
    key, key_name = resolve_env_value(
        "AZURE_OPENAI_API_KEY",
        "AZURE_AI_KEY",
    )
    deployment, deployment_name = resolve_image_model_deployment()

    if not endpoint or not key:
        finish_skip(
            "Azure OpenAI endpoint/key are not configured for image generation.",
            strict=args.strict,
        )

    if not deployment:
        finish_skip(
            "no gpt-image deployment was found. Add an optional image model deployment or pass one through environment variables.",
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

    print("\n" + "=" * 60)
    print("Image Generation Demo")
    print("=" * 60)
    print(f"Endpoint source: {endpoint_name}")
    print(f"Credential source: {key_name}")
    print(f"Deployment source: {deployment_name}")
    print(f"Deployment: {deployment}")
    print(f"Output: {output_path}")

    try:
        response = requests.post(
            url,
            headers={
                "api-key": key,
                "Content-Type": "application/json",
            },
            json=body,
            timeout=180,
        )
    except requests.RequestException as exc:
        finish_skip(
            f"image generation request could not be sent ({exc})",
            strict=args.strict,
        )

    if response.status_code >= 400:
        finish_skip(
            f"image generation is not available in this environment yet ({response.status_code}: {response.text[:300]})",
            strict=args.strict,
        )

    payload = response.json()
    images = payload.get("data") or []
    if not images or not images[0].get("b64_json"):
        finish_skip(
            "image generation returned no base64 image data.",
            strict=args.strict,
        )

    image_bytes = base64.b64decode(images[0]["b64_json"])
    output_path.write_bytes(image_bytes)

    print("\n[SUCCESS] Image generated")
    print(f"Saved file: {output_path}")


if __name__ == "__main__":
    main()
