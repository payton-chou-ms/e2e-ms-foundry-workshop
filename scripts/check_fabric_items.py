"""快速檢查現有 Fabric 項目。"""
import requests
from azure.identity import AzureCliCredential
from load_env import load_all_env
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
load_all_env()


credential = AzureCliCredential()
token = credential.get_token('https://api.fabric.microsoft.com/.default').token
headers = {'Authorization': f'Bearer {token}'}

workspace_id = os.getenv('FABRIC_WORKSPACE_ID')
prefix = os.getenv('SOLUTION_PREFIX', 'demo')

print(f"正在查找前綴為 {prefix} 的項目")
print()

# List lakehouses
resp = requests.get(
    f'https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items?type=Lakehouse', headers=headers)
if resp.status_code == 200:
    print('Lakehouses：')
    for item in resp.json().get('value', []):
        if prefix in item['displayName']:
            print(f"  - {item['displayName']}")

# List ontologies
resp = requests.get(
    f'https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/ontologies', headers=headers)
if resp.status_code == 200:
    print('Ontologies：')
    for item in resp.json().get('value', []):
        if prefix in item['displayName']:
            print(f"  - {item['displayName']}")
