"""根據 Ontology 產生最佳化 schema prompt。"""

import argparse
import os
import sys
import json

# Load environment from azd + project .env
from load_env import load_all_env
load_all_env()

# ============================================================================
# Configuration
# ============================================================================

p = argparse.ArgumentParser(description="產生最佳化 schema prompt")
p.add_argument("--from-fabric", action="store_true", help="從 Fabric API 讀取")
p.add_argument("--from-config", action="store_true", help="使用本機設定（預設）")
p.add_argument("--data-folder", default=os.getenv("DATA_FOLDER"),
               help="資料資料夾路徑（預設讀取 .env）")
args = p.parse_args()

# Default to config if neither specified
if not args.from_fabric:
    args.from_config = True

data_dir = args.data_folder
if not data_dir:
    print("錯誤：未設定 DATA_FOLDER。")
    print("      請先執行 01_generate_sample_data.py，或自行傳入 --data-folder")
    sys.exit(1)

data_dir = os.path.abspath(data_dir)

# Set up paths for new folder structure
config_dir = os.path.join(data_dir, "config")
if not os.path.exists(config_dir):
    config_dir = data_dir  # Fallback to old structure

print(f"\n{'='*60}")
print("產生最佳化 Schema Prompt")
print(f"{'='*60}")

# ============================================================================
# Load Schema
# ============================================================================

schema_data = None

if args.from_config:
    print("\n來源：本機 ontology_config.json")
    config_path = os.path.join(config_dir, "ontology_config.json")

    if not os.path.exists(config_path):
        print(f"錯誤：找不到設定檔：{config_path}")
        print("      請先執行 01_generate_sample_data.py")
        sys.exit(1)

    with open(config_path) as f:
        config = json.load(f)

    # Convert config to schema format
    schema_data = {
        "name": config["name"],
        "description": config["description"],
        "tables": {},
        "relationships": config.get("relationships", [])
    }

    for table_name, table_def in config["tables"].items():
        schema_data["tables"][table_name] = {
            "columns": [
                {"name": col, "type": table_def["types"].get(col, "String")}
                for col in table_def["columns"]
            ],
            "key": table_def["key"]
        }

elif args.from_fabric:
    print("\n來源：Fabric Ontology API")

    # Check for fabric_ids.json
    ids_path = os.path.join(config_dir, "fabric_ids.json")
    if not os.path.exists(ids_path):
        print("錯誤：找不到 fabric_ids.json")
        print("      請先執行 02_create_fabric_items.py")
        sys.exit(1)

    with open(ids_path) as f:
        fabric_ids = json.load(f)

    # Fetch from Fabric API
    from azure.identity import AzureCliCredential
    import requests
    import time
    import base64

    WORKSPACE_ID = fabric_ids["workspace_id"]
    ONTOLOGY_ID = fabric_ids["ontology_id"]
    FABRIC_API = "https://api.fabric.microsoft.com/v1"

    credential = AzureCliCredential()
    token = credential.get_token(
        "https://api.fabric.microsoft.com/.default").token
    headers = {"Authorization": f"Bearer {token}"}

    # Use POST to getDefinition (async operation)
    url = f"{FABRIC_API}/workspaces/{WORKSPACE_ID}/ontologies/{ONTOLOGY_ID}/getDefinition"
    resp = requests.post(url, headers=headers)

    # Handle async operation (202)
    if resp.status_code == 202:
        location = resp.headers.get("Location")
        retry_after = int(resp.headers.get("Retry-After", 2))
        print(f"  等待非同步作業完成...")

        for attempt in range(15):
            time.sleep(retry_after)
            poll_resp = requests.get(location, headers=headers)

            if poll_resp.status_code == 200:
                poll_data = poll_resp.json()
                if poll_data.get("status") == "Succeeded":
                    resp = poll_resp
                    break
                elif poll_data.get("status") == "Failed":
                    print(f"錯誤：作業失敗：{poll_data}")
                    sys.exit(1)
            elif poll_resp.status_code != 202:
                print(f"錯誤：輪詢失敗：{poll_resp.status_code} {poll_resp.text}")
                sys.exit(1)

    # Parse definition parts
    parts = []
    if resp.status_code == 200:
        definition = resp.json().get("definition", {})
        parts = definition.get("parts", [])

    # If no parts from API, fall back to local config
    if not parts:
        print("  注意：Ontology API 沒有回傳 definition parts，改用本機設定")
        config_path = os.path.join(data_dir, "ontology_config.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                config = json.load(f)

            schema_data = {
                "name": config["name"],
                "description": config["description"],
                "tables": {},
                "relationships": config.get("relationships", [])
            }

            for table_name, table_def in config["tables"].items():
                schema_data["tables"][table_name] = {
                    "columns": [
                        {"name": col, "type": table_def["types"].get(
                            col, "String")}
                        for col in table_def["columns"]
                    ],
                    "key": table_def["key"]
                }
        else:
            print("錯誤：找不到 ontology_config.json")
            sys.exit(1)
    else:
        # Parse Fabric ontology definition from parts
        schema_data = {"name": "", "description": "",
                       "tables": {}, "relationships": []}

        for part in parts:
            path = part.get("path", "")
            payload = base64.b64decode(part.get("payload", "")).decode("utf-8")

            try:
                content = json.loads(payload)
            except:
                continue

            # EntityType definition (Ontology format uses numeric IDs in path)
            if "/definition.json" in path and "EntityTypes/" in path:
                entity_name = content.get("name", "")
                table_name = entity_name.lower()

                columns = []
                key_prop_id = content.get("entityIdParts", [None])[0]
                key = None

                for prop in content.get("properties", []):
                    col_type = prop.get("valueType", "String")
                    columns.append({
                        "name": prop["name"],
                        "type": col_type
                    })
                    if prop.get("id") == key_prop_id:
                        key = prop["name"]

                if columns:
                    schema_data["tables"][table_name] = {
                        "columns": columns, "key": key}

            # RelationshipType definition
            elif "/definition.json" in path and "RelationshipTypes/" in path:
                schema_data["relationships"].append({
                    "name": content.get("name"),
                    "from": content.get("source", {}).get("entityTypeId", ""),
                    "to": content.get("target", {}).get("entityTypeId", "")
                })

    print(f"  已抓取 Ontology：{fabric_ids['ontology_name']}")

# ============================================================================
# Generate Optimized Prompt
# ============================================================================


def build_optimized_prompt(schema):
    """Build token-efficient schema prompt"""
    lines = []
    lines.append("=== DATABASE SCHEMA ===")
    lines.append("")

    # Tables and columns in compact format
    for table_name, table_def in schema["tables"].items():
        cols = []
        for col in table_def["columns"]:
            type_abbrev = {
                "String": "str",
                "BigInt": "int",
                "Double": "num",
                "Boolean": "bool",
                "DateTime": "date"
            }.get(col["type"], col["type"][:3].lower())

            key_marker = "*" if col["name"] == table_def.get("key") else ""
            cols.append(f"{col['name']}{key_marker}:{type_abbrev}")

        lines.append(f"{table_name}({', '.join(cols)})")

    # Relationships
    if schema.get("relationships"):
        lines.append("")
        lines.append("JOINS:")
        for rel in schema["relationships"]:
            lines.append(
                f"  {rel['from']}.{rel['fromKey']} -> {rel['to']}.{rel['toKey']}")

    # SQL hints
    lines.append("")
    lines.append("RULES:")
    lines.append("- 使用 T-SQL 語法")
    lines.append("- 主鍵欄位以 * 標記")
    lines.append("- 型別：str=string, int=integer, num=decimal")

    return "\n".join(lines)


prompt_text = build_optimized_prompt(schema_data)

# Save prompt
prompt_path = os.path.join(config_dir, "schema_prompt.txt")
with open(prompt_path, "w") as f:
    f.write(prompt_text)

# Also save full schema as JSON for reference
schema_path = os.path.join(config_dir, "schema.json")
with open(schema_path, "w") as f:
    json.dump(schema_data, f, indent=2)

# ============================================================================
# Summary
# ============================================================================

print(f"\n已產生 prompt（{len(prompt_text)} 字元）：")
print("-" * 40)
print(prompt_text)
print("-" * 40)

print(f"""
已儲存檔案：
    - {prompt_path}（提供 agent 指示使用）
    - {schema_path}（完整 schema JSON）

估計 token 數：約 {len(prompt_text.split())}

下一步：
    - 執行 05_create_fabric_agent.py，建立使用 Fabric Data Agent 工具的 Foundry agent
    - 或執行 07_create_sql_agent.py，建立使用 pyodbc SQL 工具的 agent
""")
