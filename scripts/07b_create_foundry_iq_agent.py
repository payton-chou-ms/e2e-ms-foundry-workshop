"""維護者入口：建立使用 MCP knowledge base 工具的 Foundry IQ agent。"""

from azure.ai.projects import AIProjectClient
from credential_utils import get_credential
from load_env import load_all_env
from azure.ai.projects.models import MCPTool, PromptAgentDefinition
from foundry_trace import configure_foundry_tracing
from scenario_utils import build_deployment_name, resolve_data_paths, resolve_scenario
from pathlib import Path
import argparse
import json
import os
import sys


load_all_env()

parser = argparse.ArgumentParser(
    description="建立使用 MCP knowledge base 工具的 Foundry IQ agent")
parser.add_argument("--scenario", default=os.getenv("SCENARIO_KEY", ""),
                    help="要使用的情境 key（優先於 DATA_FOLDER）")
parser.add_argument("--data-folder", default=os.getenv("DATA_FOLDER"),
                    help="資料資料夾路徑（預設讀取 .env）")
args = parser.parse_args()

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
MODEL = os.getenv("AZURE_CHAT_MODEL") or os.getenv(
    "MODEL_DEPLOYMENT", "gpt-5.4-mini")
SOLUTION_NAME = os.getenv("SOLUTION_NAME") or os.getenv(
    "SOLUTION_PREFIX") or os.getenv("AZURE_ENV_NAME", "demo")

if not PROJECT_ENDPOINT:
    print("錯誤：未設定 AZURE_AI_PROJECT_ENDPOINT")
    print("      請先執行 'azd up' 部署 Azure 資源")
    sys.exit(1)

scenario = resolve_scenario(args.scenario or None,
                            args.data_folder, require_capability="foundryIq")
paths = resolve_data_paths(scenario)
data_dir = Path(scenario["absoluteDataFolder"])
config_dir = paths["config_dir"]

config_path = config_dir / "ontology_config.json"
knowledge_ids_path = config_dir / "knowledge_ids.json"
foundry_iq_agent_ids_path = config_dir / "foundry_iq_agent_ids.json"

if not config_path.exists():
    print("錯誤：找不到 ontology_config.json")
    print("      請先執行 01_generate_sample_data.py")
    sys.exit(1)

if not knowledge_ids_path.exists():
    print("錯誤：找不到 knowledge_ids.json")
    print("      請先執行 06b_upload_to_foundry_knowledge.py")
    sys.exit(1)

with open(config_path) as f:
    ontology_config = json.load(f)

with open(knowledge_ids_path) as f:
    knowledge_ids = json.load(f)

knowledge_base_name = knowledge_ids.get("knowledge_base_name")
project_connection_id = knowledge_ids.get("project_connection_id")
mcp_endpoint = knowledge_ids.get("mcp_endpoint")
if not knowledge_base_name:
    print("錯誤：knowledge_ids.json 裡缺少 knowledge_base_name")
    sys.exit(1)
if not project_connection_id:
    print("錯誤：knowledge_ids.json 裡缺少 project_connection_id")
    sys.exit(1)
if not mcp_endpoint:
    print("錯誤：knowledge_ids.json 裡缺少 mcp_endpoint")
    sys.exit(1)

scenario_name = ontology_config.get("name", "Business Data")
scenario_desc = ontology_config.get("description", "")
agent_name = build_deployment_name(SOLUTION_NAME, scenario, "iq")

instructions = f"""你是一位協助處理 {scenario_name} 問題的助理。

{scenario_desc}

凡是文件相關問題，都必須使用附加的 knowledge base MCP 工具回答。
當問題與這個情境有關時，不可以只靠一般常識作答。
如果 knowledge base 沒有足夠證據，請直接說不知道。
請優先給出精簡且有依據的回答，並保留 knowledge base 回傳的引用資訊。
"""

print(f"\n{'='*60}")
print("建立 Foundry IQ Agent")
print(f"{'='*60}")
print(f"Project Endpoint：{PROJECT_ENDPOINT}")
print(f"Scenario：{scenario['key']}")
print(f"Agent 名稱：{agent_name}")
print(f"模型：{MODEL}")
print(f"情境：{scenario_name}")
print(f"Knowledge Base：{knowledge_base_name}")
print(f"Project Connection ID：{project_connection_id}")

project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=get_credential(),
)

trace_session = configure_foundry_tracing(
    project_client=project_client,
    scenario_name="07b_create_foundry_iq_agent",
    service_name="e2e-ms-foundry-workshop.iq-agent-create",
)

if trace_session.enabled:
    print("[OK] 已啟用 Foundry tracing")
elif trace_session.warning:
    print(f"警告：{trace_session.warning}")

mcp_kb_tool = MCPTool(
    server_label="kb",
    server_url=mcp_endpoint,
    require_approval="never",
    allowed_tools=["knowledge_base_retrieve"],
    project_connection_id=project_connection_id,
)

with project_client:
    print(f"\n檢查 agent '{agent_name}' 是否已存在...")
    try:
        with trace_session.span("get-existing-agent"):
            existing_agent = project_client.agents.get(agent_name)
        if existing_agent:
            print("  已找到既有 agent，準備刪除...")
            with trace_session.span("delete-existing-agent"):
                project_client.agents.delete(agent_name)
            print("[OK] 已刪除既有 agent")
    except Exception:
        print("  沒有找到既有 agent")

    print("\n建立 Foundry IQ agent...")
    with trace_session.span("create-agent"):
        agent = project_client.agents.create_version(
            agent_name=agent_name,
            definition=PromptAgentDefinition(
                model=MODEL,
                instructions=instructions,
                tools=[mcp_kb_tool],
            ),
        )

agent_metadata = {
    "agent_id": agent.id,
    "agent_name": agent.name,
    "scenario_key": scenario["key"],
    "knowledge_type": knowledge_ids.get("knowledge_type", "azure_search_knowledge_base"),
    "knowledge_base_name": knowledge_base_name,
    "project_connection_id": project_connection_id,
    "mcp_endpoint": mcp_endpoint,
}
with open(foundry_iq_agent_ids_path, "w") as f:
    json.dump(agent_metadata, f, indent=2)

print("\n[OK] Agent 建立成功！")
print(f"  Agent ID：{agent.id}")
print(f"  Agent 名稱：{agent.name}")
print(f"[OK] 已把 Agent 中繼資料寫入：{foundry_iq_agent_ids_path}")
print("\n下一步：python scripts/participant_validate_foundry_iq.py")
