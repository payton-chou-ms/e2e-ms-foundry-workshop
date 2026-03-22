"""建立 Foundry IQ knowledge base。"""

from pathlib import Path
import json
import os
import subprocess
import sys

import requests
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    KnowledgeBase,
    KnowledgeRetrievalMinimalReasoningEffort,
    KnowledgeRetrievalOutputMode,
    KnowledgeSourceReference,
    SearchIndexFieldReference,
    SearchIndexKnowledgeSource,
    SearchIndexKnowledgeSourceParameters,
)

from load_env import load_all_env

load_all_env()

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
PROJECT_RESOURCE_ID = os.getenv("AZURE_AI_PROJECT_RESOURCE_ID")
SEARCH_ENDPOINT = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
DATA_FOLDER = os.getenv("DATA_FOLDER")
SOLUTION_NAME = os.getenv("SOLUTION_NAME") or os.getenv(
    "SOLUTION_PREFIX") or os.getenv("AZURE_ENV_NAME", "demo")

CONNECTION_API_VERSION = "2025-10-01-preview"
KNOWLEDGE_BASE_MCP_API_VERSION = "2025-11-01-preview"
SEMANTIC_CONFIGURATION_NAME = "default-semantic"

if not PROJECT_ENDPOINT:
    print("錯誤：未設定 AZURE_AI_PROJECT_ENDPOINT")
    print("      請先執行 'azd up' 部署 Azure 資源")
    sys.exit(1)

if not PROJECT_RESOURCE_ID:
    print("錯誤：未設定 AZURE_AI_PROJECT_RESOURCE_ID")
    print("      請先執行 'azd up' 部署 Azure 資源")
    sys.exit(1)

if not SEARCH_ENDPOINT:
    print("錯誤：未設定 AZURE_AI_SEARCH_ENDPOINT")
    print("      請先執行 'azd up' 部署 Azure 資源")
    sys.exit(1)

if not DATA_FOLDER:
    print("錯誤：.env 中未設定 DATA_FOLDER")
    print("      請先執行 01_generate_sample_data.py")
    sys.exit(1)

data_dir = Path(DATA_FOLDER)
if not data_dir.exists():
    print(f"錯誤：找不到資料資料夾：{data_dir}")
    sys.exit(1)

config_dir = data_dir / "config"
docs_dir = data_dir / "documents"
if not config_dir.exists():
    config_dir = data_dir
if not docs_dir.exists():
    docs_dir = data_dir

knowledge_ids_path = config_dir / "knowledge_ids.json"
search_ids_path = config_dir / "search_ids.json"
knowledge_source_name = f"{SOLUTION_NAME}-foundry-iq-source"
knowledge_base_name = f"{SOLUTION_NAME}-foundry-iq-kb"
project_connection_name = f"{SOLUTION_NAME}-foundry-iq-connection"


def run_search_ingestion():
    script_path = Path(__file__).with_name("06_upload_to_search.py")
    print("\n確認 Azure AI Search 索引已完成載入...")
    subprocess.run([sys.executable, str(script_path)], check=True)


def load_search_metadata():
    if not search_ids_path.exists():
        print("錯誤：搜尋匯入後仍找不到 search_ids.json")
        print("      請先成功完成 06_upload_to_search.py")
        sys.exit(1)

    with open(search_ids_path) as f:
        search_ids = json.load(f)

    index_name = search_ids.get("index_name")
    if not index_name:
        print("錯誤：search_ids.json 裡缺少 index_name")
        sys.exit(1)

    return search_ids


def get_connection_resource_type(project_resource_id: str) -> str:
    if "/providers/Microsoft.CognitiveServices/accounts/" in project_resource_id:
        return "Microsoft.CognitiveServices/accounts/projects/connections"
    if "/providers/Microsoft.MachineLearningServices/workspaces/" in project_resource_id:
        return "Microsoft.MachineLearningServices/workspaces/connections"
    return "Microsoft.CognitiveServices/accounts/projects/connections"


def create_knowledge_source(index_client: SearchIndexClient, index_name: str):
    knowledge_source = SearchIndexKnowledgeSource(
        name=knowledge_source_name,
        description=f"Workshop document knowledge source for {SOLUTION_NAME}",
        search_index_parameters=SearchIndexKnowledgeSourceParameters(
            search_index_name=index_name,
            source_data_fields=[
                SearchIndexFieldReference(name="content"),
                SearchIndexFieldReference(name="title"),
                SearchIndexFieldReference(name="source"),
                SearchIndexFieldReference(name="page_number"),
                SearchIndexFieldReference(name="chunk_id"),
            ],
            search_fields=[
                SearchIndexFieldReference(name="content"),
                SearchIndexFieldReference(name="title"),
            ],
            semantic_configuration_name=SEMANTIC_CONFIGURATION_NAME,
        ),
    )
    return index_client.create_or_update_knowledge_source(knowledge_source)


def create_knowledge_base(index_client: SearchIndexClient):
    knowledge_base = KnowledgeBase(
        name=knowledge_base_name,
        description=f"Workshop Foundry IQ knowledge base for {SOLUTION_NAME}",
        knowledge_sources=[KnowledgeSourceReference(
            name=knowledge_source_name)],
        retrieval_reasoning_effort=KnowledgeRetrievalMinimalReasoningEffort(),
        output_mode=KnowledgeRetrievalOutputMode.EXTRACTIVE_DATA,
    )
    return index_client.create_or_update_knowledge_base(knowledge_base)


def create_project_connection(mcp_endpoint: str):
    credential = DefaultAzureCredential()
    bearer_token_provider = get_bearer_token_provider(
        credential, "https://management.azure.com/.default")
    headers = {
        "Authorization": f"Bearer {bearer_token_provider()}",
        "Content-Type": "application/json",
    }
    connection_url = (
        f"https://management.azure.com{PROJECT_RESOURCE_ID}/connections/"
        f"{project_connection_name}?api-version={CONNECTION_API_VERSION}"
    )
    body = {
        "name": project_connection_name,
        "type": get_connection_resource_type(PROJECT_RESOURCE_ID),
        "properties": {
            "authType": "ProjectManagedIdentity",
            "category": "RemoteTool",
            "target": mcp_endpoint,
            "isSharedToAll": True,
            "audience": "https://search.azure.com/",
            "metadata": {"ApiType": "Azure"},
        },
    }

    response = requests.put(
        connection_url, headers=headers, json=body, timeout=60)
    response.raise_for_status()
    payload = response.json() if response.content else {}
    return payload.get("id") or f"{PROJECT_RESOURCE_ID}/connections/{project_connection_name}"


def main():
    pdf_files = sorted(docs_dir.glob("*.pdf"))
    if not pdf_files:
        print("錯誤：找不到可供 Foundry IQ 匯入的 PDF 檔")
        print(f"      查找位置：{docs_dir}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("建立 Foundry IQ Knowledge Base")
    print(f"{'='*60}")
    print(f"Project Endpoint：{PROJECT_ENDPOINT}")
    print(f"Project Resource ID：{PROJECT_RESOURCE_ID}")
    print(f"Search Endpoint：{SEARCH_ENDPOINT}")
    print(f"Knowledge Source：{knowledge_source_name}")
    print(f"Knowledge Base：{knowledge_base_name}")
    print(f"Project Connection：{project_connection_name}")
    print(f"資料資料夾：{data_dir}")
    print(f"文件資料夾：{docs_dir}")
    print(f"PDF 檔數：{len(pdf_files)}")

    run_search_ingestion()
    search_ids = load_search_metadata()
    index_name = search_ids["index_name"]

    credential = DefaultAzureCredential()
    index_client = SearchIndexClient(SEARCH_ENDPOINT, credential)

    print("\n建立或更新 knowledge source...")
    create_knowledge_source(index_client, index_name)
    print(f"[OK] Knowledge source '{knowledge_source_name}' 已就緒")

    print("\n建立或更新 knowledge base...")
    create_knowledge_base(index_client)
    print(f"[OK] Knowledge base '{knowledge_base_name}' 已就緒")

    mcp_endpoint = (
        f"{SEARCH_ENDPOINT}/knowledgebases/{knowledge_base_name}/mcp"
        f"?api-version={KNOWLEDGE_BASE_MCP_API_VERSION}"
    )

    print("\n建立或更新 Foundry project connection...")
    project_connection_id = create_project_connection(mcp_endpoint)
    print(f"[OK] Project connection '{project_connection_name}' 已就緒")

    metadata = {
        "knowledge_type": "azure_search_knowledge_base",
        "search_endpoint": SEARCH_ENDPOINT,
        "search_index_name": index_name,
        "knowledge_source_name": knowledge_source_name,
        "knowledge_base_name": knowledge_base_name,
        "project_connection_name": project_connection_name,
        "project_connection_id": project_connection_id,
        "mcp_endpoint": mcp_endpoint,
        "document_count": search_ids.get("document_count", 0),
        "pdf_files": search_ids.get("pdf_files", []),
        "source_folder": str(docs_dir),
        "status": "ready",
    }

    with open(knowledge_ids_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"[OK] 已把 knowledge 中繼資料寫入：{knowledge_ids_path}")
    print(f"\n{'='*60}")
    print("Foundry IQ Knowledge Base 已就緒")
    print(f"{'='*60}")
    print(f"Search Index：{index_name}")
    print(f"Knowledge Base：{knowledge_base_name}")
    print(f"Project Connection ID：{project_connection_id}")
    print("下一步：python scripts/07b_create_foundry_iq_agent.py")


if __name__ == "__main__":
    main()
