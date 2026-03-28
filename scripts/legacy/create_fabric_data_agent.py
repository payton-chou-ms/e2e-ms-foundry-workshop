"""建立 Fabric Data Agent 的舊版參考腳本。"""

import argparse
import base64
import json
import os
import sys
import time

import requests
from azure.identity import AzureCliCredential

SCRIPTS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, SCRIPTS_ROOT)

from shared.load_env import load_all_env
from shared.scenario_utils import resolve_data_paths, resolve_scenario


script_dir = os.path.dirname(os.path.abspath(__file__))
load_all_env()

parser = argparse.ArgumentParser(description="建立 Fabric Data Agent")
parser.add_argument("--scenario", default=os.getenv("SCENARIO_KEY", ""), help="要使用的情境 key（優先於 DATA_FOLDER）")
parser.add_argument("--data-folder", default=os.getenv("DATA_FOLDER"), help="資料資料夾路徑（預設讀取 .env）")
args = parser.parse_args()

WORKSPACE_ID = os.getenv("FABRIC_WORKSPACE_ID")
if not WORKSPACE_ID:
    print("錯誤：.env 中未設定 FABRIC_WORKSPACE_ID")
    sys.exit(1)

scenario = resolve_scenario(args.scenario or None, args.data_folder, require_capability="fabricIq")
paths = resolve_data_paths(scenario)
data_dir = scenario["absoluteDataFolder"]
config_dir = os.fspath(paths["config_dir"])

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
print(f"Scenario：{scenario['key']}")
print(f"Workspace ID：{WORKSPACE_ID}")
print(f"Ontology ID：{ONTOLOGY_ID}")
print(f"Data Agent 名稱：{DATA_AGENT_NAME}")

credential = AzureCliCredential()


def get_headers():
    token = credential.get_token("https://api.fabric.microsoft.com/.default").token
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}



def make_request(method, url, **kwargs):
    max_retries = 5
    for attempt in range(max_retries):
        response = requests.request(method, url, headers=get_headers(), **kwargs)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 30))
            print(f"  已遇到速率限制，等待 {retry_after} 秒...")
            time.sleep(retry_after)
            continue
        return response
    return response



def wait_for_lro(operation_url, operation_name="Operation", timeout=300):
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
    if isinstance(data, dict):
        data = json.dumps(data)
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")


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



def build_agent_instructions(config, schema):
    scenario = config.get("scenario", "")
    name = config.get("name", "Business Data")
    desc = config.get("description", "")
    tables = config.get("tables", {})
    relationships = config.get("relationships", [])

    entity_list = []
    for table_name, table_def in tables.items():
        cols = ", ".join(table_def.get("columns", []))
        entity_list.append(f"- {table_name.title()}: {cols}")

    rel_list = []
    for rel in relationships:
        rel_list.append(f"- {rel['from'].title()} -> {rel['to'].title()} (via {rel['fromKey']})")

    instructions = f"""你是一位協助回答 {name} 資料問題的助理。

{desc}

你可以使用一個 Ontology，其中包含：
{chr(10).join(entity_list)}

關聯：
{chr(10).join(rel_list) if rel_list else '- None defined'}

回答問題時：
1. 請根據資料提供正確答案
2. 支援聚合與 group by 類型的查詢
3. 回答要清楚、精簡，並以資料為依據
4. 如果找不到答案，請說明還缺哪些資料

{schema}

請支援在 GQL 中使用 group by。"""

    return instructions


print(f"\n[1/2] 建立 Data Agent...")

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
    print(f"  [OK] 使用既有 Data Agent：{DATA_AGENT_NAME} ({data_agent_id})")
else:
    create_url = f"{FABRIC_API}/workspaces/{WORKSPACE_ID}/items"
    instructions = build_agent_instructions(ontology_config, schema_prompt)
    definition = {
        "displayName": DATA_AGENT_NAME,
        "type": "DataAgent",
        "definition": {
            "parts": [
                {
                    "path": "agent-definition.json",
                    "payload": encode_to_base64(
                        {
                            "version": "1.0",
                            "ontologyId": ONTOLOGY_ID,
                            "name": DATA_AGENT_NAME,
                            "description": scenario_desc,
                            "instructions": instructions,
                        }
                    ),
                    "payloadType": "InlineBase64",
                }
            ]
        },
    }

    create_resp = make_request("POST", create_url, json=definition)
    if create_resp.status_code == 202:
        operation_url = create_resp.headers.get("Location") or create_resp.headers.get("x-ms-operation-id")
        if operation_url and not operation_url.startswith("http"):
            operation_url = f"{FABRIC_API}{operation_url}"
        result = wait_for_lro(operation_url, operation_name="建立 Data Agent") if operation_url else None
        if result and result.get("id"):
            data_agent_id = result["id"]
        else:
            print("  [FAIL] 建立 Data Agent 失敗")
            sys.exit(1)
    elif create_resp.status_code in [200, 201]:
        result = create_resp.json()
        data_agent_id = result.get("id")
    else:
        print(f"  [FAIL] 建立 Data Agent 失敗：{create_resp.status_code}")
        print(create_resp.text)
        sys.exit(1)

print(f"\n[2/2] 寫入 Data Agent 參考資訊...")

agent_ids_path = os.path.join(config_dir, "fabric_data_agent_ids.json")
with open(agent_ids_path, "w") as f:
    json.dump(
        {
            "data_agent_id": data_agent_id,
            "data_agent_name": final_agent_name,
            "scenario": scenario["key"],
            "data_folder": data_dir,
        },
        f,
        ensure_ascii=False,
        indent=2,
    )

fabric_ids["data_agent_id"] = data_agent_id
fabric_ids["data_agent_name"] = final_agent_name
with open(fabric_ids_path, "w") as f:
    json.dump(fabric_ids, f, ensure_ascii=False, indent=2)

repo_root = os.path.dirname(SCRIPTS_ROOT)
env_path = os.path.join(repo_root, ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        env_lines = f.read().splitlines()

    updated = False
    for index, line in enumerate(env_lines):
        if line.startswith("FABRIC_AGENT_ID="):
            env_lines[index] = f"FABRIC_AGENT_ID={data_agent_id}"
            updated = True
            break

    if not updated:
        env_lines.append(f"FABRIC_AGENT_ID={data_agent_id}")

    with open(env_path, "w", encoding="utf-8") as f:
        f.write("\n".join(env_lines) + "\n")

print(f"  [OK] 已寫入：{agent_ids_path}")
print(f"  [OK] 已更新：{fabric_ids_path}")
if os.path.exists(env_path):
    print(f"  [OK] 已更新：{env_path} (FABRIC_AGENT_ID)")
print(f"\n{'='*60}")
print("Fabric Data Agent 建立完成")
print(f"{'='*60}")
print(f"Data Agent ID：{data_agent_id}")
print("\n此腳本屬於 legacy 參考路徑，一般 workshop 主流程不需執行。")
