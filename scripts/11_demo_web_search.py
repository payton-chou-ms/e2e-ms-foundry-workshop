"""11 - Optional demo: Web Search tool.

This demo validates the GA Web Search tool path for Foundry agents. If the SDK
surface is unavailable or the feature is not enabled in the project, it prints
SKIP instead of failing the workshop flow.
"""

import argparse
import os

from load_env import load_all_env
from optional_demo_utils import finish_skip, resolve_env_value, safe_delete_agent_version

load_all_env()

IMPORT_ERROR = None

try:
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import PromptAgentDefinition
    # SDK renamed WebSearchTool → WebSearchPreviewTool
    try:
        from azure.ai.projects.models import WebSearchPreviewTool
    except ImportError:
        from azure.ai.projects.models import WebSearchTool as WebSearchPreviewTool
except ImportError as exc:  # pragma: no cover - runtime dependent
    IMPORT_ERROR = exc


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        default="What are the latest public updates to Microsoft Foundry agent tools?",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()

    if IMPORT_ERROR is not None:
        finish_skip(
            "Web Search tool types are not available in the installed azure-ai-projects package.",
            strict=args.strict,
        )

    endpoint, endpoint_name = resolve_env_value("AZURE_AI_PROJECT_ENDPOINT")
    if not endpoint:
        finish_skip("AZURE_AI_PROJECT_ENDPOINT is not configured.",
                    strict=args.strict)

    model = os.getenv("AZURE_CHAT_MODEL") or os.getenv(
        "MODEL_DEPLOYMENT") or "gpt-5.4-mini"

    print("\n" + "=" * 60)
    print("Web Search Demo")
    print("=" * 60)
    print(f"Endpoint source: {endpoint_name}")
    print(f"Model: {model}")

    project = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )
    openai = project.get_openai_client()
    agent = None

    try:
        agent = project.agents.create_version(
            agent_name="WorkshopWebSearchDemo",
            definition=PromptAgentDefinition(
                model=model,
                instructions="You are a helpful assistant that can search the public web.",
                tools=[WebSearchPreviewTool()],
            ),
            description="Public web search demo.",
        )
        print(f"Agent created (name: {agent.name}, version: {agent.version})")

        stream = openai.responses.create(
            stream=True,
            tool_choice="required",
            input=args.prompt,
            extra_body={"agent_reference": {
                "name": agent.name, "type": "agent_reference"}},
        )

        for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)
            elif event.type == "response.output_item.done":
                item = event.item
                if item.type == "message" and item.content and item.content[-1].type == "output_text":
                    for annotation in item.content[-1].annotations:
                        if annotation.type == "url_citation":
                            print(f"\n[Citation] {annotation.url}")
            elif event.type == "response.completed":
                print("\n\n[Completed]")
                print(event.response.output_text)
    except Exception as exc:
        finish_skip(
            f"web search is not available in this environment yet ({exc})",
            strict=args.strict,
        )
    finally:
        if agent is not None:
            safe_delete_agent_version(project, agent)


if __name__ == "__main__":
    main()
