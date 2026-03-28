"""把資料載入 Fabric Lakehouse。"""

import requests
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import AzureCliCredential
import argparse
import os
import sys
import json
import time

SCRIPTS_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, SCRIPTS_ROOT)

# Load environment from azd + project .env
from load_env import load_all_env
from scenario_utils import resolve_data_paths, resolve_scenario
load_all_env()

# Azure imports

# ============================================================================
# Configuration
# ============================================================================

p = argparse.ArgumentParser(description="把資料載入 Fabric Lakehouse")
p.add_argument("--data-folder", default=os.getenv("DATA_FOLDER"),
               help="資料資料夾路徑（預設讀取 .env）")
p.add_argument("--scenario", default=os.getenv("SCENARIO_KEY", ""),
               help="要使用的情境 key（優先於 DATA_FOLDER）")
p.add_argument("--skip-tables", action="store_true",
               help="略過載入 Delta 資料表（只上傳檔案）")
args = p.parse_args()

scenario = resolve_scenario(args.scenario or None, args.data_folder, require_capability="fabricIq")
paths = resolve_data_paths(scenario)
data_dir = scenario["absoluteDataFolder"]
config_dir = os.fspath(paths["config_dir"])
tables_dir = os.fspath(paths["tables_dir"])
scenario_key = scenario["key"]

# Check for required files
config_path = os.path.join(config_dir, "ontology_config.json")
fabric_ids_path = os.path.join(config_dir, "fabric_ids.json")

# Fallback to old structure if config dir doesn't exist
if not os.path.exists(config_dir):
    config_dir = data_dir
    tables_dir = data_dir
    config_path = os.path.join(data_dir, "ontology_config.json")
    fabric_ids_path = os.path.join(data_dir, "fabric_ids.json")

if not os.path.exists(config_path):
    print("錯誤：找不到 ontology_config.json")
    print("      請先執行 01_generate_sample_data.py")
    sys.exit(1)

if not os.path.exists(fabric_ids_path):
    print("錯誤：找不到 fabric_ids.json")
    print("      請先執行 02_create_fabric_items.py")
    sys.exit(1)

with open(config_path) as f:
    ontology_config = json.load(f)

with open(fabric_ids_path) as f:
    fabric_ids = json.load(f)

# Get workspace_id from environment (not config file for security)
WORKSPACE_ID = os.getenv("FABRIC_WORKSPACE_ID")
if not WORKSPACE_ID:
    print("錯誤：.env 中未設定 FABRIC_WORKSPACE_ID")
    sys.exit(1)

LAKEHOUSE_ID = fabric_ids["lakehouse_id"]
LAKEHOUSE_NAME = fabric_ids["lakehouse_name"]
FABRIC_API = "https://api.fabric.microsoft.com/v1"
ONELAKE_URL = "onelake.dfs.fabric.microsoft.com"

print(f"\n{'='*60}")
print("把資料載入 Fabric Lakehouse")
print(f"{'='*60}")
print(f"Scenario：{scenario_key}")
print(f"資料資料夾：{data_dir}")
print(f"Workspace：{WORKSPACE_ID}")
print(f"Lakehouse：{LAKEHOUSE_NAME}")
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


def make_request(method, url, **kwargs):
    """Make request with retry logic for 429 rate limiting"""
    max_retries = 5
    for attempt in range(max_retries):
        response = requests.request(
            method, url, headers=get_headers(), **kwargs)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 30))
            print(f"    已遇到速率限制，等待 {retry_after} 秒...")
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
                print(f"    [OK] {operation_name} 已完成")
                return result
            elif status in ["Failed", "failed"]:
                print(f"    [FAIL] {operation_name} 失敗：{result}")
                return None
        time.sleep(3)
    print(f"    [FAIL] {operation_name} 等待逾時")
    return None

# ============================================================================
# Step 1: Get Workspace Name (needed for OneLake path)
# ============================================================================


print(f"\n[1/3] 取得 workspace 資訊...")
resp = make_request("GET", f"{FABRIC_API}/workspaces/{WORKSPACE_ID}")
if resp.status_code != 200:
    print(f"  [FAIL] 無法取得 workspace 資訊：{resp.text}")
    sys.exit(1)
workspace_name = resp.json()["displayName"]
print(f"  Workspace 名稱：{workspace_name}")

# ============================================================================
# Step 2: Upload CSV Files
# ============================================================================

print(f"\n[2/3] 上傳 CSV 到 Lakehouse...")

# Setup OneLake connection (use workspace NAME, not ID)
account_url = f"https://{ONELAKE_URL}"
service_client = DataLakeServiceClient(account_url, credential=credential)
file_system_client = service_client.get_file_system_client(workspace_name)

# Get directory client for Lakehouse Files folder
data_path = f"{LAKEHOUSE_NAME}.Lakehouse/Files"
directory_client = file_system_client.get_directory_client(data_path)

uploaded_files = []
for table_name in ontology_config["tables"].keys():
    csv_file = f"{table_name}.csv"
    csv_path = os.path.join(tables_dir, csv_file)

    if not os.path.exists(csv_path):
        print(f"  [FAIL] 找不到 CSV：{csv_file}")
        continue

    try:
        print(f"  正在上傳 {csv_file}...")
        file_client = directory_client.get_file_client(csv_file)
        with open(csv_path, "rb") as f:
            file_client.upload_data(f, overwrite=True)

        file_size = os.path.getsize(csv_path)
        print(f"  [OK] {csv_file} 已上傳（{file_size:,} bytes）")
        uploaded_files.append(csv_file)
    except Exception as e:
        print(f"  [FAIL] 上傳 {csv_file} 失敗：{e}")
        sys.exit(1)

# Wait for files to be available in OneLake
    print("  等待檔案在 OneLake 中可用...")
time.sleep(10)

# ============================================================================
# Step 3: Load CSV Files as Delta Tables
# ============================================================================

if args.skip_tables:
    print(f"\n[3/3] 略過資料表載入（--skip-tables）")
else:
    print(f"\n[3/3] 把 CSV 載入成 Delta 資料表...")

    tables_url = f"{FABRIC_API}/workspaces/{WORKSPACE_ID}/lakehouses/{LAKEHOUSE_ID}/tables"

    for table_name in ontology_config["tables"].keys():
        csv_file = f"{table_name}.csv"
        print(f"  正在把 {csv_file} 載入成資料表 '{table_name}'...")

        load_table_url = f"{tables_url}/{table_name}/load"
        load_payload = {
            "relativePath": f"Files/{csv_file}",
            "pathType": "File",
            "mode": "Overwrite",
            "formatOptions": {
                "format": "Csv",
                "header": True,
                "delimiter": ","
            }
        }

        resp = make_request("POST", load_table_url, json=load_payload)

        if resp.status_code == 200:
            print(f"  [OK] 資料表 '{table_name}' 載入成功")
        elif resp.status_code == 202:
            operation_url = resp.headers.get("Location")
            wait_for_lro(operation_url, f"資料表 '{table_name}' 載入")
        else:
            print(f"  ⚠ 資料表載入回傳狀態碼：{resp.status_code}")
            print(f"    回應內容：{resp.text}")

    # Wait for tables to be indexed
    print("  等待資料表完成索引...")
    time.sleep(30)

# ============================================================================
# Summary
# ============================================================================

print(f"\n{'='*60}")
print("資料載入完成！")
print(f"{'='*60}")
print(f"""
已上傳 {len(uploaded_files)} 個檔案：{', '.join(uploaded_files)}
已載入資料表：{', '.join(ontology_config['tables'].keys())}

下一步：產生 schema prompt
  python scripts/04_generate_agent_prompt.py

之後若要重新載入資料（例如改用新的或更大的資料集）：
  python scripts/01_generate_sample_data.py --scenario <SCENARIO> --size medium
  python scripts/03_load_fabric_data.py
""")
