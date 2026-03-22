"""Browser Automation optional demo。"""

import argparse
import json
import os

from load_env import load_all_env
from optional_demo_utils import finish_skip, print_demo_header, resolve_env_value, safe_delete_agent_version

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
    "開啟 https://learn.microsoft.com/azure/foundry/agents/how-to/tools/browser-automation，"
    "回報頁面主標題，並列出頁面提到的一項限制。"
    "不要登入、不要送出表單，也不要前往非 Microsoft 網域。"
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument(
        "--connection-id",
        help="覆蓋 Browser Automation 的 project connection ID。",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()

    print_demo_header(
        title="Browser Automation 示範",
        description="建立一個暫時的 agent，開啟受信任的 Microsoft Learn 頁面並回報看到的內容。",
        env_items=[
            {"name": "AZURE_AI_PROJECT_ENDPOINT",
                "value": os.getenv("AZURE_AI_PROJECT_ENDPOINT")},
            {"name": "AZURE_PLAYWRIGHT_CONNECTION_ID",
                "value": os.getenv("AZURE_PLAYWRIGHT_CONNECTION_ID")},
            {"name": "AZURE_BROWSER_AUTOMATION_CONNECTION_ID",
                "value": os.getenv("AZURE_BROWSER_AUTOMATION_CONNECTION_ID")},
            {"name": "AZURE_CHAT_MODEL",
                "value": os.getenv("AZURE_CHAT_MODEL")},
        ],
    )

    if IMPORT_ERROR is not None:
        finish_skip(
            "目前安裝的 azure-ai-projects 套件不含 Browser Automation 預覽型別。",
            strict=args.strict,
        )

    endpoint, endpoint_name = resolve_env_value("AZURE_AI_PROJECT_ENDPOINT")
    if not endpoint:
        finish_skip("未設定 AZURE_AI_PROJECT_ENDPOINT。",
                    strict=args.strict)

    connection_id = args.connection_id or resolve_env_value(
        "AZURE_PLAYWRIGHT_CONNECTION_ID",
        "AZURE_BROWSER_AUTOMATION_CONNECTION_ID",
    )[0]
    if not connection_id:
        finish_skip(
            "尚未設定 Playwright workspace connection ID。請先建立 Browser Automation connection。",
            strict=args.strict,
        )

    model = os.getenv("AZURE_CHAT_MODEL") or os.getenv(
        "MODEL_DEPLOYMENT") or "gpt-5.4-mini"

    print(f"Endpoint 來源：{endpoint_name}")
    print(f"模型：{model}")
    print(f"Connection ID：{connection_id}")
    print("Prompt 範圍：只允許受信任的 Microsoft Learn 頁面")

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
                    "你是一個謹慎的瀏覽器自動化助理。"
                    "只可與受信任的文件頁面互動。"
                    "不得登入、填表或送出任何使用者資料。"
                ),
                tools=[tool],
            ),
            description="受信任網站的瀏覽器自動化示範。",
        )
        print(f"已建立 Agent（name: {agent.name}, version: {agent.version}）")

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
                    print("\n\n[Browser Automation 工具呼叫]")
                    print(f"查詢：{arguments.get('query')}")
            elif event.type == "response.completed":
                print("\n\n[完成]")
                print(event.response.output_text)
    except Exception as exc:
        finish_skip(
            f"目前這個環境還無法使用 browser automation（{exc}）",
            strict=args.strict,
        )
    finally:
        if agent is not None:
            safe_delete_agent_version(project, agent)


if __name__ == "__main__":
    main()
