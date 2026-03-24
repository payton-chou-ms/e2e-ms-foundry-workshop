"""測試 Foundry IQ agent 的互動式聊天腳本。"""

from pathlib import Path
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from load_env import load_all_env
from foundry_trace import configure_foundry_tracing
import argparse
import json
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--agent-name", default="")
parser.add_argument("--agent-id", default="")
args = parser.parse_args()

load_all_env()

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
DATA_FOLDER = os.getenv("DATA_FOLDER")

if not PROJECT_ENDPOINT:
    print("錯誤：未設定 AZURE_AI_PROJECT_ENDPOINT")
    print("      請先執行 'azd up' 部署 Azure 資源")
    sys.exit(1)

if not DATA_FOLDER:
    print("錯誤：.env 中未設定 DATA_FOLDER")
    print("      請先執行 01_generate_sample_data.py")
    sys.exit(1)

data_dir = Path(DATA_FOLDER)
config_dir = data_dir / "config"
if not config_dir.exists():
    config_dir = data_dir

agent_ids_path = config_dir / "foundry_iq_agent_ids.json"
questions_path = config_dir / "sample_questions.txt"

agent_name = args.agent_name
agent_id = args.agent_id
if agent_ids_path.exists():
    with open(agent_ids_path) as f:
        agent_ids = json.load(f)
    agent_name = agent_name or agent_ids.get("agent_name", "")
    agent_id = agent_id or agent_ids.get("agent_id", "")

if not agent_name and not agent_id:
    print("錯誤：找不到 Foundry IQ agent 參考資料")
    print("      請先執行 07b_create_foundry_iq_agent.py")
    sys.exit(1)

sample_questions = []
if questions_path.exists():
    with open(questions_path) as f:
        lines = f.read().splitlines()
    in_document_section = False
    for line in lines:
        if "DOCUMENT QUESTIONS" in line:
            in_document_section = True
            continue
        if in_document_section and line.startswith("==="):
            break
        if in_document_section and line.strip().startswith("- "):
            sample_questions.append(line.strip()[2:])

if not sample_questions:
    sample_questions = [
        "文件裡怎麼規定停機事件要通知客戶？",
        "文件裡如何定義客戶影響等級？",
    ]


def print_sample_questions():
    print("文件類範例問題：")
    for question in sample_questions:
        print(f"  - {question}")


project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

trace_session = configure_foundry_tracing(
    project_client=project_client,
    scenario_name="08b_test_foundry_iq_agent",
    service_name="e2e-ms-foundry-workshop.iq-agent-chat",
)

if trace_session.enabled:
    print("追蹤：已啟用")
elif trace_session.warning:
    print(f"追蹤：{trace_session.warning}")

openai_client = project_client.get_openai_client()

with project_client:
    with trace_session.span("get-agent"):
        agent = project_client.agents.get(agent_name or agent_id)

with trace_session.span("create-conversation"):
    conversation = openai_client.conversations.create()

print(f"\n{'='*60}")
print("Foundry IQ Agent 對話")
print(f"{'='*60}")
print(f"Agent 名稱：{agent.name}")
print_sample_questions()
print("輸入 'quit' 離開，輸入 'help' 可再次查看範例問題")


def print_citations(response):
    try:
        for item in getattr(response, "output", []) or []:
            if getattr(item, "type", "") != "message":
                continue
            for content in getattr(item, "content", []) or []:
                if getattr(content, "type", "") != "output_text":
                    continue
                annotations = getattr(content, "annotations", []) or []
                for annotation in annotations:
                    annotation_type = getattr(annotation, "type", "citation")
                    details = []
                    for field_name in ["filename", "title", "source", "url"]:
                        field_value = getattr(annotation, field_name, None)
                        if field_value:
                            details.append(str(field_value))

                    if details:
                        print(
                            f"\n  [引用:{annotation_type}] {' | '.join(details)}")
                    else:
                        print(f"\n  [引用:{annotation_type}]")
        return
    except Exception:
        return


while True:
    try:
        user_input = input("\n你：").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        break

    if not user_input:
        continue
    if user_input.lower() in ["quit", "exit", "q"]:
        break
    if user_input.lower() == "help":
        print()
        print_sample_questions()
        continue

    with trace_session.span("create-response"):
        response = openai_client.responses.create(
            conversation=conversation.id,
            input=user_input,
            extra_body={"agent_reference": {
                "name": agent.name, "type": "agent_reference"}},
        )

    print(f"\nAgent：{getattr(response, 'output_text', '')}")
    print_citations(response)
