"""建立 Fabric Lakehouse 與 Ontology。"""

import requests
from azure.identity import AzureCliCredential
import argparse
import os
import sys
import json
import time
import base64
import uuid
from datetime import datetime

SCRIPTS_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, SCRIPTS_ROOT)

# Load environment from azd + project .env
from load_env import load_all_env
from scenario_utils import build_scenario_resource_name, resolve_data_paths, resolve_scenario
load_all_env()

# Azure imports

# ============================================================================
# Configuration
# ============================================================================

p = argparse.ArgumentParser(description="建立 Fabric Lakehouse 與 Ontology")
p.add_argument("--data-folder", default=os.getenv("DATA_FOLDER"),
               help="資料資料夾路徑（預設讀取 .env）")
p.add_argument("--scenario", default=os.getenv("SCENARIO_KEY", ""),
               help="要使用的情境 key（優先於 DATA_FOLDER）")
p.add_argument("--solutionname", default=os.getenv("SOLUTION_NAME") or os.getenv("SOLUTION_PREFIX") or os.getenv("AZURE_ENV_NAME", "demo"),
               help="方案名稱前綴（預設讀取 SOLUTION_NAME 或 SOLUTION_PREFIX）")
p.add_argument("--clean", action="store_true",
               help="刪除並重新建立 Lakehouse 與 Ontology（切換情境時使用）")
args = p.parse_args()

WORKSPACE_ID = os.getenv("FABRIC_WORKSPACE_ID")
if not WORKSPACE_ID:
    print("錯誤：.env 中未設定 FABRIC_WORKSPACE_ID")
    sys.exit(1)

scenario = resolve_scenario(args.scenario or None, args.data_folder, require_capability="fabricIq")
paths = resolve_data_paths(scenario)
data_dir = scenario["absoluteDataFolder"]
config_dir = os.fspath(paths["config_dir"])
scenario_key = scenario["key"]

config_path = os.path.join(config_dir, "ontology_config.json")

if not os.path.exists(data_dir):
    print(f"錯誤：找不到資料資料夾：{data_dir}")
    sys.exit(1)

if not os.path.exists(config_path):
    print("錯誤：找不到 ontology_config.json")
    print("      請先執行 01_generate_sample_data.py")
    sys.exit(1)

base_solution_name = args.solutionname
SOLUTION_NAME = build_scenario_resource_name(base_solution_name, scenario_key)
FABRIC_API = "https://api.fabric.microsoft.com/v1"

with open(config_path) as f:
    ontology_config = json.load(f)

print(f"\n{'='*60}")
print(f"正在為 {SOLUTION_NAME} 設定 Fabric")
print(f"{'='*60}")
print(f"Scenario：{scenario_key}")
print(f"Workspace ID：{WORKSPACE_ID}")
print(f"情境：{ontology_config['name']}")
print(f"資料表：{', '.join(ontology_config['tables'].keys())}")

# ============================================================================
# Authentication
# ============================================================================

credential = AzureCliCredential()


def get_headers():
    """Get fresh headers with token"""
    token = credential.get_token(
        "https://api.fabric.microsoft.com/.default").token
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# ============================================================================
# Helper Functions
# ============================================================================


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


def wait_for_lro(operation_url, timeout=300):
    """Wait for long-running operation to complete"""
    start = time.time()
    while time.time() - start < timeout:
        resp = make_request("GET", operation_url)
        if resp.status_code == 200:
            result = resp.json()
            status = result.get("status", "Unknown")
            if status in ["Succeeded", "succeeded"]:
                # Try to get the resource from resourceLocation
                resource_location = result.get("resourceLocation")
                if resource_location:
                    res_resp = make_request("GET", resource_location)
                    if res_resp.status_code == 200:
                        return res_resp.json()
                return result
            elif status in ["Failed", "failed"]:
                raise Exception(f"作業失敗：{result}")
        time.sleep(3)
    raise TimeoutError("作業等待逾時")


def find_item(item_type, display_name):
    """Find a Fabric item by type and name"""
    url = f"{FABRIC_API}/workspaces/{WORKSPACE_ID}/items?type={item_type}"
    resp = make_request("GET", url)
    if resp.status_code == 200:
        for item in resp.json().get("value", []):
            if item["displayName"] == display_name:
                return item
    return None


def find_ontology(display_name):
    """Find an ontology by name using the ontologies endpoint"""
    url = f"{FABRIC_API}/workspaces/{WORKSPACE_ID}/ontologies"
    resp = make_request("GET", url)
    if resp.status_code == 200:
        for ont in resp.json().get("value", []):
            if ont["displayName"] == display_name:
                return ont
    return None


def delete_item(item_type, item_id, item_name):
    """Delete a Fabric item"""
    url = f"{FABRIC_API}/workspaces/{WORKSPACE_ID}/{item_type.lower()}s/{item_id}"
    resp = make_request("DELETE", url)
    if resp.status_code in [200, 202, 204]:
        print(f"  [OK] 已刪除 {item_type}：{item_name}")
        return True
    else:
        print(f"  [WARN] 無法刪除 {item_type} {item_name}：{resp.status_code}")
        return False


def delete_ontology(ontology_id, ontology_name):
    """Delete an ontology"""
    url = f"{FABRIC_API}/workspaces/{WORKSPACE_ID}/ontologies/{ontology_id}"
    resp = make_request("DELETE", url)
    if resp.status_code in [200, 202, 204]:
        print(f"  [OK] 已刪除 Ontology：{ontology_name}")
        return True
    else:
        print(f"  [WARN] 無法刪除 Ontology {ontology_name}：{resp.status_code}")
        return False


def b64encode(content):
    """Encode content to base64"""
    if isinstance(content, dict):
        content = json.dumps(content)
    if isinstance(content, str):
        content = content.encode("utf-8")
    return base64.b64encode(content).decode("utf-8")

# ============================================================================
# Step 0: Determine lakehouse/ontology names (use local tracking, minimize API calls)
# ============================================================================


# Track suffix in a GLOBAL file (scripts folder) to persist across data folder changes
script_dir = os.path.dirname(os.path.abspath(__file__))
suffix_file = os.path.join(SCRIPTS_ROOT, "fabric_suffix.txt")

if os.path.exists(suffix_file):
    with open(suffix_file, "r") as f:
        current_suffix = int(f.read().strip())
else:
    current_suffix = 1

if args.clean:
    # Just increment suffix - don't bother deleting (Fabric will clean up old ones eventually)
    new_suffix = current_suffix + 1
    print(
        f"\n[0/4] 使用新的 suffix：{new_suffix}（前一個是 {current_suffix}）")
else:
    new_suffix = current_suffix

# Save new suffix
with open(suffix_file, "w") as f:
    f.write(str(new_suffix))

lakehouse_name = f"{SOLUTION_NAME}-lakehouse-{new_suffix}"
ontology_name = f"{SOLUTION_NAME}-ontology-{new_suffix}"

# ============================================================================
# Step 1: Create Lakehouse
# ============================================================================

print(f"\n[1/4] 建立 Lakehouse...")

existing_lakehouse = find_item("Lakehouse", lakehouse_name)
if existing_lakehouse:
    lakehouse_id = existing_lakehouse["id"]
    print(
        f"  [OK] 使用既有 Lakehouse：{lakehouse_name} ({lakehouse_id})")
else:
    url = f"{FABRIC_API}/workspaces/{WORKSPACE_ID}/items"
    payload = {"displayName": lakehouse_name, "type": "Lakehouse"}
    resp = make_request("POST", url, json=payload)

    if resp.status_code == 201:
        lakehouse_id = resp.json()["id"]
        print(f"  [OK] 已建立 Lakehouse：{lakehouse_name} ({lakehouse_id})")
    elif resp.status_code == 202:
        # Long-running operation
        operation_url = resp.headers.get("Location")
        result = wait_for_lro(operation_url)
        lakehouse_id = result.get("id")
        print(f"  [OK] 已建立 Lakehouse：{lakehouse_name} ({lakehouse_id})")
    else:
        print(f"  [FAIL] 建立 Lakehouse 失敗：{resp.status_code} {resp.text}")
        sys.exit(1)

# Wait for Lakehouse to be ready
time.sleep(5)

# ============================================================================
# Step 2: Create Ontology (using dedicated ontologies API)
# ============================================================================

print(f"\n[2/4] 建立 Ontology...")

existing_ontology = find_ontology(ontology_name)
if existing_ontology:
    ontology_id = existing_ontology["id"]
    print(f"  [OK] 使用既有 Ontology：{ontology_name} ({ontology_id})")
else:
    # Generate unique IDs for entities, properties, relationships
    base_ts = int(time.time() * 1000) % 10000000000
    entity_ids = {}
    property_ids = {}
    databinding_ids = {}

    for i, (table_name, table_def) in enumerate(ontology_config["tables"].items()):
        entity_id = str(base_ts + i * 1000)
        entity_ids[table_name] = entity_id
        databinding_ids[table_name] = str(uuid.uuid4())

        property_ids[table_name] = {}
        for j, col in enumerate(table_def["columns"]):
            property_ids[table_name][col] = str(
                base_ts + 100000000 + i * 1000 + j)

    # Build platform metadata
    platform_metadata = {
        "metadata": {
            "type": "Ontology",
            "displayName": ontology_name
        }
    }

    # Empty definition.json
    definition_json = {}

    # Build definition parts
    definition_parts = [
        {
            "path": ".platform",
            "payload": b64encode(platform_metadata),
            "payloadType": "InlineBase64"
        },
        {
            "path": "definition.json",
            "payload": b64encode(definition_json),
            "payloadType": "InlineBase64"
        }
    ]

    # Type mapping
    type_map = {
        "String": "String",
        "BigInt": "BigInt",
        "Double": "Double",
        "Boolean": "Boolean",
        "DateTime": "DateTime"
    }

    # Add EntityTypes and DataBindings for each table
    for table_name, table_def in ontology_config["tables"].items():
        entity_id = entity_ids[table_name]
        entity_name = table_name.title().replace("_", "")
        key_col = table_def["key"]
        key_prop_id = property_ids[table_name][key_col]

        # Build properties
        properties = []
        for col in table_def["columns"]:
            col_type = table_def["types"].get(col, "String")
            properties.append({
                "id": property_ids[table_name][col],
                "name": col,
                "redefines": None,
                "baseTypeNamespaceType": None,
                "valueType": type_map.get(col_type, "String")
            })

        # Entity Type definition
        entity_type = {
            "id": entity_id,
            "namespace": "usertypes",
            "baseEntityTypeId": None,
            "name": entity_name,
            "entityIdParts": [key_prop_id],
            "displayNamePropertyId": key_prop_id,
            "namespaceType": "Custom",
            "visibility": "Visible",
            "properties": properties,
            "timeseriesProperties": []
        }

        definition_parts.append({
            "path": f"EntityTypes/{entity_id}/definition.json",
            "payload": b64encode(entity_type),
            "payloadType": "InlineBase64"
        })

        # Data Binding - use dataBindingConfiguration structure
        property_bindings = []
        for col in table_def["columns"]:
            property_bindings.append({
                "sourceColumnName": col,
                "targetPropertyId": property_ids[table_name][col]
            })

        data_binding = {
            "id": databinding_ids[table_name],
            "dataBindingConfiguration": {
                "dataBindingType": "NonTimeSeries",
                "propertyBindings": property_bindings,
                "sourceTableProperties": {
                    "sourceType": "LakehouseTable",
                    "workspaceId": WORKSPACE_ID,
                    "itemId": lakehouse_id,
                    "sourceTableName": table_name
                }
            }
        }

        definition_parts.append({
            "path": f"EntityTypes/{entity_id}/DataBindings/{databinding_ids[table_name]}.json",
            "payload": b64encode(data_binding),
            "payloadType": "InlineBase64"
        })

        print(f"  + Entity：{entity_name}（{len(properties)} 個屬性）")

    # Add Relationships
    for i, rel in enumerate(ontology_config.get("relationships", [])):
        from_table = rel["from"]
        to_table = rel["to"]
        from_entity_id = entity_ids[from_table]
        to_entity_id = entity_ids[to_table]
        rel_id = str(base_ts + 900000 + i)
        contextualization_id = str(uuid.uuid4())

        # Relationship Type
        relationship_type = {
            "id": rel_id,
            "namespace": "usertypes",
            "name": rel["name"],
            "namespaceType": "Custom",
            "source": {"entityTypeId": from_entity_id},
            "target": {"entityTypeId": to_entity_id}
        }

        definition_parts.append({
            "path": f"RelationshipTypes/{rel_id}/definition.json",
            "payload": b64encode(relationship_type),
            "payloadType": "InlineBase64"
        })

        # Relationship Contextualization (how to join the data)
        # The dataBindingTable should be the table that contains the foreign key
        # For a relationship from A -> B where B has a FK to A:
        #   - dataBindingTable = B (the table with the FK column)
        #   - sourceKeyRefBindings = maps FK column to source entity's PK property
        #   - targetKeyRefBindings = maps target's PK column to target entity's PK property

        # PK of source entity (e.g., drivers.id)
        from_key = ontology_config["tables"][from_table]["key"]
        from_key_prop_id = property_ids[from_table][from_key]

        # FK column in target table (e.g., orders.driver_id)
        to_key_col = rel["toKey"]
        # PK of target entity (e.g., orders.id)
        to_table_pk = ontology_config["tables"][to_table]["key"]
        to_key_prop_id = property_ids[to_table][to_table_pk]

        contextualization = {
            "id": contextualization_id,
            "dataBindingTable": {
                "workspaceId": WORKSPACE_ID,
                "itemId": lakehouse_id,
                # Use target table (the one with FK)
                "sourceTableName": to_table,
                "sourceType": "LakehouseTable"
            },
            "sourceKeyRefBindings": [
                # FK col -> source PK prop
                {"sourceColumnName": to_key_col,
                    "targetPropertyId": from_key_prop_id}
            ],
            "targetKeyRefBindings": [
                # target PK col -> target PK prop
                {"sourceColumnName": to_table_pk,
                    "targetPropertyId": to_key_prop_id}
            ]
        }

        definition_parts.append({
            "path": f"RelationshipTypes/{rel_id}/Contextualizations/{contextualization_id}.json",
            "payload": b64encode(contextualization),
            "payloadType": "InlineBase64"
        })

        print(f"  + 關聯：{from_table} -> {to_table}")

    # Create Ontology using dedicated ontologies endpoint
    ontology_payload = {
        "displayName": ontology_name,
        "description": f"Ontology for {ontology_config['name']} scenario",
        "definition": {
            "parts": definition_parts
        }
    }

    url = f"{FABRIC_API}/workspaces/{WORKSPACE_ID}/ontologies"
    resp = make_request("POST", url, json=ontology_payload)

    if resp.status_code == 201:
        ontology_id = resp.json()["id"]
        print(f"  [OK] 已建立 Ontology：{ontology_name} ({ontology_id})")
    elif resp.status_code == 202:
        operation_url = resp.headers.get("Location")
        result = wait_for_lro(operation_url)
        ontology_id = result.get("id")
        # If ID wasn't in LRO result, fetch it from the ontologies list
        if not ontology_id:
            created_ont = find_ontology(ontology_name)
            ontology_id = created_ont["id"] if created_ont else None
        print(f"  [OK] 已建立 Ontology：{ontology_name} ({ontology_id})")
    else:
        if resp.status_code == 403 and "FeatureNotAvailable" in resp.text:
            print("  [FAIL] 建立 Ontology 失敗：403")
            print(
                "    回應：目前的 Fabric workspace 尚未啟用 Ontology 功能。")
            print(
                "    建議：請改用有啟用 Ontology 的 Fabric workspace，或以 --foundry-only 執行 workshop。")
            sys.exit(1)
        print(f"  [FAIL] 建立 Ontology 失敗：{resp.status_code}")
        print(f"    回應：{resp.text}")
        sys.exit(1)

# Wait for Ontology to be ready
time.sleep(3)

# ============================================================================
# Step 3: Save IDs for later scripts
# ============================================================================

print(f"\n[3/4] 儲存設定...")

ids_path = os.path.join(config_dir, "fabric_ids.json")
fabric_ids = {
    "lakehouse_id": lakehouse_id,
    "lakehouse_name": lakehouse_name,
    "ontology_id": ontology_id,
    "ontology_name": ontology_name,
    "workspace_id": WORKSPACE_ID,
    "scenario_key": scenario_key,
    "data_folder": scenario["dataFolder"],
    "base_solution_name": base_solution_name,
    "solution_name": SOLUTION_NAME,
    "created_at": datetime.now().isoformat()
}
with open(ids_path, "w") as f:
    json.dump(fabric_ids, f, indent=2)
print(f"  [OK] 已儲存 fabric_ids.json")

# ============================================================================
# Summary
# ============================================================================

print(f"\n{'='*60}")
print("Fabric 設定完成！")
print(f"{'='*60}")
print(f"""
Lakehouse：{lakehouse_name}
  ID: {lakehouse_id}

Ontology：{ontology_name}
  ID: {ontology_id}
    Entities：{', '.join([t.title().replace('_', '') for t in ontology_config['tables'].keys()])}

已儲存 ID 到：{ids_path}

下一步：把資料載入 Fabric
  python scripts/03_load_fabric_data.py

載入資料後：
    1. 開啟 Fabric 入口網站，確認 Lakehouse 已有資料
    2. 把 CSV 載入資料表（Lakehouse > Get data > Load to Tables）
  3. Run: python scripts/04_generate_agent_prompt.py

仍需手動處理：
    - 在 Fabric 入口網站建立 Data Agent，並綁定到 Ontology
    - （目前 Data Agent API 還不支援完整 definition 設定）
""")
