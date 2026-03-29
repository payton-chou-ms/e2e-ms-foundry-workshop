"""16b - 最小化的 Microsoft Agent Framework Magentic 範例。

這是一支獨立的小範例，用來示範 workshop 中以程式碼為主的
multi-agent orchestration 路線。

請先安裝 preview 套件：
    pip install --pre \
        "agent-framework-core==1.0.0rc5" \
        "agent-framework-azure-ai==1.0.0rc5" \
        "agent-framework-orchestrations==1.0.0b260319"

執行方式：
    python scripts/16b_agent_framework_magentic_example.py
    python scripts/16b_agent_framework_magentic_example.py --question "請為高優先客服佇列事故整理一份簡短應變包。"
"""

import argparse
import asyncio
import os

from agent_framework import Agent, AgentResponseUpdate, Message
from agent_framework.azure import AzureAIClient
from agent_framework.orchestrations import MagenticBuilder, MagenticProgressLedger
from azure.identity.aio import DefaultAzureCredential

from load_env import load_all_env


DEFAULT_QUESTION = (
    "入口網站發版後，高優先客服佇列的流量突然暴增到平常的 4 倍。"
    "請整理一份精簡的應變包，涵蓋立即分流動作、營運負責人在接下來 15 分鐘內應確認的事項、"
    "升級通報條件，以及一段安全可用的對客說明。"
)

TRIAGE_MANAGER_INSTRUCTIONS = """你是客服佇列事故的分流協調 manager。

你的工作是把任務拆成最小且有用的子任務，決定下一步該交給哪個 specialist，並追蹤使用者的需求是否已經被完整回答。

優先順序：
- 先理解營運面發生了什麼事。
- 再請另一位 specialist 產出安全可用的對客溝通草稿。
- 一旦使用者已經拿到完整且可執行的應變包，就停止。

如果其他 agent 更適合處理某部分工作，不要全部自己做完。"""

QUEUE_OPS_INSTRUCTIONS = """你是客服佇列營運 specialist。

請聚焦在：
- 可能的營運成因
- 立即可執行的分流動作
- 接下來 15 分鐘內要確認的重點
- 哪些條件出現時應該升級通報

回答要精簡，而且以行動為導向。"""

CUSTOMER_COMMS_INSTRUCTIONS = """你是對客溝通 specialist。

請把事故背景轉成：
- 一段簡短的對客說明
- 一段客服人員可直接使用的話術
- 一段簡短的狀態頁更新內容

語氣要冷靜、基於事實、讓人安心。
除非題目明確提供時程，否則不要承諾恢復時間。"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--question",
        default=DEFAULT_QUESTION,
        help="送進 Magentic workflow 的問題。",
    )
    return parser.parse_args()


def get_required_env(*names):
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    raise ValueError(
        f"缺少必要的環境變數。已嘗試：{', '.join(names)}"
    )


def create_client(credential, project_endpoint, model_deployment_name):
    return AzureAIClient(
        credential=credential,
        project_endpoint=project_endpoint,
        model_deployment_name=model_deployment_name,
    )


def create_agents(triage_manager_client, queue_ops_client, customer_comms_client):
    triage_manager_agent = Agent(
        name="triage-manager-agent",
        description="負責規劃並協調客服佇列事故應變的 manager。",
        instructions=TRIAGE_MANAGER_INSTRUCTIONS,
        client=triage_manager_client,
    )

    queue_ops_agent = Agent(
        name="queue-ops-agent",
        description="專注客服佇列分流與事故營運應變的 specialist。",
        instructions=QUEUE_OPS_INSTRUCTIONS,
        client=queue_ops_client,
    )

    customer_comms_agent = Agent(
        name="customer-comms-agent",
        description="專注安全對客訊息與客服話術的 specialist。",
        instructions=CUSTOMER_COMMS_INSTRUCTIONS,
        client=customer_comms_client,
    )

    return triage_manager_agent, queue_ops_agent, customer_comms_agent


def print_orchestrator_event(event_data):
    event_name = getattr(getattr(event_data, "event_type", None), "name", "UNKNOWN")
    print(f"\n[Magentic 事件] {event_name}")

    content = getattr(event_data, "content", None)
    if isinstance(content, Message):
        print(content.text)
    elif isinstance(content, MagenticProgressLedger):
        print(content.to_dict())
    elif content is not None:
        print(content)


def extract_final_text(final_output_data):
    if isinstance(final_output_data, list) and final_output_data:
        last_item = final_output_data[-1]
        return getattr(last_item, "text", str(last_item))

    if hasattr(final_output_data, "messages"):
        messages = getattr(final_output_data, "messages")
        if messages:
            return getattr(messages[-1], "text", str(messages[-1]))

    return getattr(final_output_data, "text", str(final_output_data))


async def main():
    args = parse_args()
    load_all_env()

    project_endpoint = get_required_env(
        "AZURE_AI_PROJECT_ENDPOINT",
        "FOUNDRY_PROJECT_ENDPOINT",
    )
    model_deployment_name = get_required_env(
        "AZURE_AI_MODEL_DEPLOYMENT_NAME",
        "FOUNDRY_MODEL_DEPLOYMENT_NAME",
        "AZURE_CHAT_MODEL",
    )

    async with (
        DefaultAzureCredential() as credential,
        create_client(credential, project_endpoint, model_deployment_name) as triage_manager_client,
        create_client(credential, project_endpoint, model_deployment_name) as queue_ops_client,
        create_client(credential, project_endpoint, model_deployment_name) as customer_comms_client,
    ):
        triage_manager_agent, queue_ops_agent, customer_comms_agent = create_agents(
            triage_manager_client,
            queue_ops_client,
            customer_comms_client,
        )

        workflow = MagenticBuilder(
            participants=[queue_ops_agent, customer_comms_agent],
            manager_agent=triage_manager_agent,
            intermediate_outputs=True,
            max_round_count=8,
            max_stall_count=2,
            max_reset_count=1,
        ).build()

        last_message_id = None
        final_output_data = None

        async for event in workflow.run(args.question, stream=True):
            if event.type == "output" and isinstance(event.data, AgentResponseUpdate):
                message_id = event.data.message_id
                if message_id != last_message_id:
                    if last_message_id is not None:
                        print("\n")
                    executor_id = getattr(event, "executor_id", "agent")
                    print(f"[{executor_id}]", end=" ", flush=True)
                    last_message_id = message_id
                print(event.data, end="", flush=True)
            elif event.type == "magentic_orchestrator":
                print_orchestrator_event(event.data)
            elif event.type == "output":
                final_output_data = event.data

        if final_output_data is not None:
            print("\n\n=== 最終答案 ===")
            print(extract_final_text(final_output_data))


if __name__ == "__main__":
    asyncio.run(main())