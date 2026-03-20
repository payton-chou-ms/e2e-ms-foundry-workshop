"""10 - Optional demo: Browser Automation tool.

This demo is intentionally constrained to a trusted Microsoft documentation page.
If the required preview SDK surface or Playwright connection is unavailable, it
prints SKIP and exits successfully unless --strict is used.
"""

import argparse
import json
import os

from load_env import load_all_env
from optional_demo_utils import finish_skip, resolve_env_value, safe_delete_agent_version

load_all_env()

IMPORT_ERROR = None

try:
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import (
        PromptAgentDefinition,
        BrowserAutomationToolParameters,
        BrowserAutomationToolConnectionParameters,
    )
    # SDK renamed BrowserAutomationPreviewTool → BrowserAutomationAgentTool
    try:
        from azure.ai.projects.models import BrowserAutomationAgentTool
    except ImportError:
        from azure.ai.projects.models import BrowserAutomationPreviewTool as BrowserAutomationAgentTool
except ImportError as exc:  # pragma: no cover - runtime dependent
    IMPORT_ERROR = exc


DEFAULT_PROMPT = (
    "Open https://learn.microsoft.com/azure/foundry/agents/how-to/tools/browser-automation, "
    "report the main page heading, and list one limitation mentioned on the page. "
    "Do not sign in, submit forms, or navigate to non-Microsoft domains."
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument(
        "--connection-id",
        help="Override the Browser Automation project connection ID.",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()

    if IMPORT_ERROR is not None:
        finish_skip(
            "Browser Automation preview types are not available in the installed azure-ai-projects package.",
            strict=args.strict,
        )

    endpoint, endpoint_name = resolve_env_value("AZURE_AI_PROJECT_ENDPOINT")
    if not endpoint:
        finish_skip("AZURE_AI_PROJECT_ENDPOINT is not configured.",
                    strict=args.strict)

    connection_id = args.connection_id or resolve_env_value(
        "AZURE_PLAYWRIGHT_CONNECTION_ID",
        "AZURE_BROWSER_AUTOMATION_CONNECTION_ID",
    )[0]
    if not connection_id:
        finish_skip(
            "no Playwright workspace connection ID is configured. Create a Browser Automation connection first.",
            strict=args.strict,
        )

    model = os.getenv("AZURE_CHAT_MODEL") or os.getenv(
        "MODEL_DEPLOYMENT") or "gpt-5.4-mini"

    print("\n" + "=" * 60)
    print("Browser Automation Demo")
    print("=" * 60)
    print(f"Endpoint source: {endpoint_name}")
    print(f"Model: {model}")
    print(f"Connection ID: {connection_id}")
    print("Prompt scope: trusted Microsoft Learn page only")

    project = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )
    openai = project.get_openai_client()

    tool = BrowserAutomationAgentTool(
        browser_automation_preview=BrowserAutomationToolParameters(
            connection=BrowserAutomationToolConnectionParameters(
                project_connection_id=connection_id,
            )
        )
    )

    agent = None
    try:
        agent = project.agents.create_version(
            agent_name="WorkshopBrowserAutomationDemo",
            definition=PromptAgentDefinition(
                model=model,
                instructions=(
                    "You are a cautious browser automation assistant. "
                    "Only interact with trusted documentation pages. "
                    "Never log in, fill forms, or submit user data."
                ),
                tools=[tool],
            ),
            description="Trusted-site browser automation demo.",
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
                if item.type == "browser_automation_preview_call":
                    arguments_str = getattr(item, "arguments", "{}")
                    arguments = json.loads(arguments_str)
                    print("\n\n[Browser Automation tool call]")
                    print(f"Query: {arguments.get('query')}")
            elif event.type == "response.completed":
                print("\n\n[Completed]")
                print(event.response.output_text)
    except Exception as exc:
        finish_skip(
            f"browser automation is not available in this environment yet ({exc})",
            strict=args.strict,
        )
    finally:
        if agent is not None:
            safe_delete_agent_version(project, agent)


if __name__ == "__main__":
    main()
