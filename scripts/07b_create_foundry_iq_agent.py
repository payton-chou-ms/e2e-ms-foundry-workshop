"""
07b - Create Foundry IQ agent with MCP knowledge base tool
Creates a prompt agent that uses Azure AI Search knowledge-base retrieval
through the Foundry MCP tool surface.

Usage:
    python 07b_create_foundry_iq_agent.py

Prerequisites:
    - Run 01_generate_sample_data.py
    - Run 06b_upload_to_foundry_knowledge.py

The script stores metadata in config/foundry_iq_agent_ids.json.
"""

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
    print("ERROR: AZURE_AI_PROJECT_ENDPOINT not set")
    print("       Run 'azd up' to deploy Azure resources")
    sys.exit(1)

if not DATA_FOLDER:
    print("ERROR: DATA_FOLDER not set in .env")
    print("       Run 01_generate_sample_data.py first")
    sys.exit(1)

data_dir = Path(DATA_FOLDER)
config_dir = data_dir / "config"
if not config_dir.exists():
    config_dir = data_dir

config_path = config_dir / "ontology_config.json"
knowledge_ids_path = config_dir / "knowledge_ids.json"
foundry_iq_agent_ids_path = config_dir / "foundry_iq_agent_ids.json"

if not config_path.exists():
    print("ERROR: ontology_config.json not found")
    print("       Run 01_generate_sample_data.py first")
    sys.exit(1)

if not knowledge_ids_path.exists():
    print("ERROR: knowledge_ids.json not found")
    print("       Run 06b_upload_to_foundry_knowledge.py first")
    sys.exit(1)

with open(config_path) as f:
    ontology_config = json.load(f)

with open(knowledge_ids_path) as f:
    knowledge_ids = json.load(f)

knowledge_base_name = knowledge_ids.get("knowledge_base_name")
project_connection_id = knowledge_ids.get("project_connection_id")
mcp_endpoint = knowledge_ids.get("mcp_endpoint")
if not knowledge_base_name:
    print("ERROR: knowledge_base_name missing in knowledge_ids.json")
    sys.exit(1)
if not project_connection_id:
    print("ERROR: project_connection_id missing in knowledge_ids.json")
    sys.exit(1)
if not mcp_endpoint:
    print("ERROR: mcp_endpoint missing in knowledge_ids.json")
    sys.exit(1)

scenario_name = ontology_config.get("name", "Business Data")
scenario_desc = ontology_config.get("description", "")
agent_name = f"{_short_prefix()}-iq-agent"

instructions = f"""You are a helpful assistant for {scenario_name}.

{scenario_desc}

You must use the attached knowledge base MCP tool to answer every document question.
You must never answer from general knowledge when the question is asking about this scenario.
If the knowledge base does not contain enough evidence, say you do not know.
Prefer concise grounded answers and preserve citations from the knowledge base output.
"""

print(f"\n{'='*60}")
print("Create Foundry IQ Agent")
print(f"{'='*60}")
print(f"Project Endpoint: {PROJECT_ENDPOINT}")
print(f"Agent Name: {agent_name}")
print(f"Model: {MODEL}")
print(f"Scenario: {scenario_name}")
print(f"Knowledge Base: {knowledge_base_name}")
print(f"Project Connection ID: {project_connection_id}")

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
    print(f"\nChecking if agent '{agent_name}' already exists...")
    try:
        existing_agent = project_client.agents.get(agent_name)
        if existing_agent:
            print("  Found existing agent, deleting...")
            project_client.agents.delete(agent_name)
            print("[OK] Deleted existing agent")
    except Exception:
        print("  No existing agent found")

    print("\nCreating Foundry IQ agent...")
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

print("\n[OK] Agent created successfully!")
print(f"  Agent ID: {agent.id}")
print(f"  Agent Name: {agent.name}")
print(f"[OK] Agent metadata saved to: {foundry_iq_agent_ids_path}")
print("\nNext: python scripts/08b_test_foundry_iq_agent.py")
