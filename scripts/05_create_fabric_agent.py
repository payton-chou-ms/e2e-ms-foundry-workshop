"""建立 Fabric Data Agent 的舊版參考腳本。"""

import requests
from azure.identity import AzureCliCredential
from load_env import load_all_env
import os
import sys
import json
import time
import base64

# Get script directory for relative paths
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load environment from azd + project .env
load_all_env()


# ============================================================================
# Configuration
# ============================================================================

# Project settings - from .env
WORKSPACE_ID = os.getenv("FABRIC_WORKSPACE_ID")
DATA_FOLDER = os.getenv("DATA_FOLDER")

if not WORKSPACE_ID:
    print("錯誤：.env 中未設定 FABRIC_WORKSPACE_ID")
    sys.exit(1)

if not DATA_FOLDER:
    print("錯誤：.env 中未設定 DATA_FOLDER")
    print("      請先執行 01_generate_sample_data.py")
    sys.exit(1)

data_dir = os.path.abspath(DATA_FOLDER)

# Set up paths for new folder structure
config_dir = os.path.join(data_dir, "config")
if not os.path.exists(config_dir):
    config_dir = data_dir  # Fallback to old structure

# Load fabric_ids.json
fabric_ids_path = os.path.join(config_dir, "fabric_ids.json")
if not os.path.exists(fabric_ids_path):
    print("錯誤：找不到 fabric_ids.json")
    print("      請先執行 02_create_fabric_items.py")
    sys.exit(1)

with open(fabric_ids_path) as f:
    fabric_ids = json.load(f)

ONTOLOGY_ID = fabric_ids["ontology_id"]
SOLUTION_NAME = fabric_ids["solution_name"]
DATA_AGENT_NAME = f"{SOLUTION_NAME}_dataagent"

FABRIC_API = "https://api.fabric.microsoft.com/v1"

print(f"\n{'='*60}")
print("建立 Fabric Data Agent")
print(f"{'='*60}")
print(f"Workspace ID：{WORKSPACE_ID}")
print(f"Ontology ID：{ONTOLOGY_ID}")
print(f"Data Agent 名稱：{DATA_AGENT_NAME}")

# ============================================================================
# Authentication
# ============================================================================

credential = AzureCliCredential()


def get_headers():
    """Get fresh headers with token"""
    token = credential.get_token(
        "https://api.fabric.microsoft.com/.default").token
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def make_request(method, url, **kwargs):
    """Make request with retry logic for 429 rate limiting"""
    max_retries = 5
    for attempt in range(max_retries):
        response = requests.request(
            method, url, headers=get_headers(), **kwargs)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 30))
            print(f"  已遇到速率限制，等待 {retry_after} 秒...")
            time.sleep(retry_after)
            continue
        return response
    return response


def wait_for_lro(operation_url, operation_name="Operation", timeout=300):
    """Wait for long-running operation to complete"""
    start = time.time()
    while time.time() - start < timeout:
        resp = make_request("GET", operation_url)
        if resp.status_code == 200:
            result = resp.json()
            status = result.get("status", "Unknown")
            if status in ["Succeeded", "succeeded"]:
                print(f"  [OK] {operation_name} 已完成")
                return result
            elif status in ["Failed", "failed"]:
                print(f"  [FAIL] {operation_name} 失敗：{result}")
                return None
        time.sleep(3)
    print(f"  [FAIL] {operation_name} 等待逾時")
    return None


def encode_to_base64(data):
    """Encode data to base64 string"""
    if isinstance(data, dict):
        data = json.dumps(data)
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')

# ============================================================================
# Load Schema and Ontology Config for Instructions
# ============================================================================


# Load ontology config for scenario-specific instructions
config_path = os.path.join(config_dir, "ontology_config.json")
if os.path.exists(config_path):
    with open(config_path) as f:
        ontology_config = json.load(f)
    scenario_name = ontology_config.get("name", "Business Data")
    scenario_desc = ontology_config.get("description", "")
    tables = list(ontology_config.get("tables", {}).keys())
    print(f"\n情境：{scenario_name}")
else:
    ontology_config = {}
    scenario_name = "Business Data"
    scenario_desc = ""
    tables = []

prompt_path = os.path.join(config_dir, "schema_prompt.txt")
if os.path.exists(prompt_path):
    with open(prompt_path) as f:
        schema_prompt = f.read()
    print(f"已載入 schema prompt（{len(schema_prompt)} 字元）")
else:
    schema_prompt = ""

# Build scenario-specific instructions


def build_agent_instructions(config, schema):
    """Build agent instructions based on scenario"""
    scenario = config.get("scenario", "")
    name = config.get("name", "Business Data")
    desc = config.get("description", "")
    tables = config.get("tables", {})
    relationships = config.get("relationships", [])

    # Build entity descriptions
    entity_list = []
    for table_name, table_def in tables.items():
        cols = ", ".join(table_def.get("columns", []))
        entity_list.append(f"- {table_name.title()}: {cols}")

    # Build relationship descriptions
    rel_list = []
    for rel in relationships:
        rel_list.append(
            f"- {rel['from'].title()} -> {rel['to'].title()} (via {rel['fromKey']})")

    instructions = f"""你是一位協助回答 {name} 資料問題的助理。

{desc}

你可以使用一個 Ontology，其中包含：
{chr(10).join(entity_list)}

關聯：
{chr(10).join(rel_list) if rel_list else "- None defined"}

回答問題時：
1. 請根據資料提供正確答案
2. 支援聚合與 group by 類型的查詢
3. 回答要清楚、精簡，並以資料為依據
4. 如果找不到答案，請說明還缺哪些資料

{schema}

請支援在 GQL 中使用 group by。"""

    return instructions

# ============================================================================
# Step 1: Create Data Agent
# ============================================================================


print(f"\n[1/2] 建立 Data Agent...")

# Check if Data Agent already exists
url = f"{FABRIC_API}/workspaces/{WORKSPACE_ID}/items?type=DataAgent"
resp = make_request("GET", url)
existing_agent = None
if resp.status_code == 200:
    for item in resp.json().get("value", []):
        if item["displayName"] == DATA_AGENT_NAME:
            existing_agent = item
            break

data_agent_id = None
final_agent_name = DATA_AGENT_NAME

if existing_agent:
    data_agent_id = existing_agent["id"]
    print(
        f"  [OK] 使用既有 Data Agent：{DATA_AGENT_NAME} ({data_agent_id})")
else:
    # Try to create Data Agent, with suffix retry if name not available
    max_suffix = 10
    for suffix in range(max_suffix + 1):
        if suffix == 0:
            agent_name = DATA_AGENT_NAME
        else:
            agent_name = f"{DATA_AGENT_NAME}_{suffix}"

        payload = {
            "displayName": agent_name,
            "type": "DataAgent",
            "description": f"提供 {SOLUTION_NAME} Ontology 使用的 Data Agent"
        }

        url = f"{FABRIC_API}/workspaces/{WORKSPACE_ID}/items/"
        resp = make_request("POST", url, json=payload)

        if resp.status_code == 201:
            data_agent_id = resp.json()["id"]
            final_agent_name = agent_name
            print(f"  [OK] 已建立 Data Agent：{agent_name} ({data_agent_id})")
            break
        elif resp.status_code == 202:
            result = wait_for_lro(resp.headers.get(
                "Location"), "建立 Data Agent")
            if result:
                resource_location = result.get("resourceLocation")
                if resource_location:
                    res_resp = make_request("GET", resource_location)
                    data_agent_id = res_resp.json()["id"]
                    final_agent_name = agent_name
                    print(
                        f"  [OK] 已建立 Data Agent：{agent_name} ({data_agent_id})")
                    break
        elif resp.status_code == 400:
            error_data = resp.json()
            if error_data.get("errorCode") == "ItemDisplayNameNotAvailableYet":
                print(f"  名稱 '{agent_name}' 目前不可用，改用帶 suffix 的名稱重試...")
                continue
            else:
                print(f"  [FAIL] 建立 Data Agent 失敗：{resp.status_code}")
                print(f"    回應：{resp.text}")
                sys.exit(1)
        else:
            print(f"  [FAIL] 建立 Data Agent 失敗：{resp.status_code}")
            print(f"    回應：{resp.text}")
            sys.exit(1)

    if not data_agent_id:
        print(f"  [FAIL] 重試 {max_suffix} 次後仍無法建立 Data Agent")
        sys.exit(1)

# ============================================================================
# Step 2: Update Data Agent Definition with Ontology Source
# ============================================================================

print(f"\n[2/2] 設定 Data Agent 的 Ontology 資料來源...")

# Build scenario-specific instructions
agent_instructions = build_agent_instructions(ontology_config, schema_prompt)

# Data Agent configuration
data_agent_config = {
    "version": "1.0",
    "instructions": agent_instructions,
    "dataSources": [
        {
            "type": "Ontology",
            "workspaceId": WORKSPACE_ID,
            "itemId": ONTOLOGY_ID
        }
    ]
}

update_payload = {
    "definition": {
        "parts": [
            {
                "path": "dataAgent.json",
                "payload": encode_to_base64(data_agent_config),
                "payloadType": "InlineBase64"
            }
        ]
    }
}

url = f"{FABRIC_API}/workspaces/{WORKSPACE_ID}/items/{data_agent_id}/updateDefinition"
resp = make_request("POST", url, json=update_payload)

if resp.status_code in [200, 202]:
    if resp.status_code == 202:
        wait_for_lro(resp.headers.get("Location"), "更新 Definition")
    print(f"  [OK] 已把 Data Agent 設定為使用 Ontology 資料來源")
else:
    print(f"  ⚠ 無法透過 API 更新 Data Agent definition：{resp.status_code}")
    print(f"    回應：{resp.text}")
    print("    你可能需要到 Fabric 入口網站手動設定 Ontology 資料來源：")
    print(f"    1. 到 workspace 開啟 '{final_agent_name}'")
    print(f"    2. 把 Ontology 加成 data source")

# ============================================================================
# Save Data Agent ID
# ============================================================================

fabric_ids["data_agent_id"] = data_agent_id
fabric_ids["data_agent_name"] = final_agent_name
with open(fabric_ids_path, "w") as f:
    json.dump(fabric_ids, f, indent=2)

# Update .env with FABRIC_AGENT_ID
env_path = os.path.join(script_dir, "..", ".env")
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        env_content = f.read()

    lines = env_content.split("\n")
    updated = False
    for i, line in enumerate(lines):
        if line.startswith("FABRIC_AGENT_ID="):
            lines[i] = f"FABRIC_AGENT_ID={data_agent_id}"
            updated = True
            break

    if updated:
        with open(env_path, "w") as f:
            f.write("\n".join(lines))
        print(f"[OK] 已更新 .env：FABRIC_AGENT_ID={data_agent_id}")

# ============================================================================
# Summary
# ============================================================================

print(f"""
{'='*60}
Fabric Data Agent Created!
{'='*60}

Fabric Data Agent 已建立！

Data Agent 名稱：{final_agent_name}
Data Agent ID：{data_agent_id}
Ontology 來源：{ONTOLOGY_ID}

已儲存 ID 到：{fabric_ids_path}

下一步：
    選項 A - 在 AI Foundry 中建立使用 Fabric 連線的 agent：
        1. 在 AI Foundry 把這個 Data Agent 加成 Fabric connection
        2. 建立會使用 fabric_dataagent 工具的 agent
    3. Run 06_test_fabric_agent.py

    選項 B - 直接使用 Foundry Agent（較簡單）：
    python scripts/07_create_foundry_agent.py
    python scripts/08_test_foundry_agent.py
""")
