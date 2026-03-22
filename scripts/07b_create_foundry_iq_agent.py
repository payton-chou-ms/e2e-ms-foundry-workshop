"""建立使用 MCP knowledge base 工具的 Foundry IQ agent。"""

from azure.ai.projects import AIProjectClient
from load_env import load_all_env
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import MCPTool, PromptAgentDefinition
from pathlib import Path
import json
import os
import random
import string
import sys


def _short_prefix(length=3):
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


load_all_env()

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
MODEL = os.getenv("AZURE_CHAT_MODEL") or os.getenv(
    "MODEL_DEPLOYMENT", "gpt-5.4-mini")
DATA_FOLDER = os.getenv("DATA_FOLDER")
SOLUTION_NAME = os.getenv("SOLUTION_NAME") or os.getenv(
    "SOLUTION_PREFIX") or os.getenv("AZURE_ENV_NAME", "demo")

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
agent_name = f"{_short_prefix()}-iq-agent"

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
print(f"Agent 名稱：{agent_name}")
print(f"模型：{MODEL}")
print(f"情境：{scenario_name}")
print(f"Knowledge Base：{knowledge_base_name}")
print(f"Project Connection ID：{project_connection_id}")

project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

mcp_kb_tool = MCPTool(
    server_label="knowledge-base",
    server_url=mcp_endpoint,
    require_approval="never",
    allowed_tools=["knowledge_base_retrieve"],
    project_connection_id=project_connection_id,
)

with project_client:
    print(f"\n檢查 agent '{agent_name}' 是否已存在...")
    try:
        existing_agent = project_client.agents.get(agent_name)
        if existing_agent:
            print("  已找到既有 agent，準備刪除...")
            project_client.agents.delete(agent_name)
            print("[OK] 已刪除既有 agent")
    except Exception:
        print("  沒有找到既有 agent")

    print("\n建立 Foundry IQ agent...")
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
print("\n下一步：python scripts/08b_test_foundry_iq_agent.py")
