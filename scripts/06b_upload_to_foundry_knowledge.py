"""
06b - Provision Foundry IQ knowledge base
Ensures the workshop documents are indexed in Azure AI Search, then creates or
updates the Azure AI Search knowledge source, knowledge base, and Foundry MCP
project connection used by the Foundry IQ agent path.

Usage:
    python 06b_upload_to_foundry_knowledge.py

Prerequisites:
    - Run 01_generate_sample_data.py
    - Azure resources deployed via azd

This script stores metadata in config/knowledge_ids.json.
"""

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
    print("ERROR: AZURE_AI_PROJECT_ENDPOINT not set")
    print("       Run 'azd up' to deploy Azure resources")
    sys.exit(1)

if not PROJECT_RESOURCE_ID:
    print("ERROR: AZURE_AI_PROJECT_RESOURCE_ID not set")
    print("       Run 'azd up' to deploy Azure resources")
    sys.exit(1)

if not SEARCH_ENDPOINT:
    print("ERROR: AZURE_AI_SEARCH_ENDPOINT not set")
    print("       Run 'azd up' to deploy Azure resources")
    sys.exit(1)

if not DATA_FOLDER:
    print("ERROR: DATA_FOLDER not set in .env")
    print("       Run 01_generate_sample_data.py first")
    sys.exit(1)

data_dir = Path(DATA_FOLDER)
if not data_dir.exists():
    print(f"ERROR: Data folder not found: {data_dir}")
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
    print("\nEnsuring the Azure AI Search index is populated...")
    subprocess.run([sys.executable, str(script_path)], check=True)


def load_search_metadata():
    if not search_ids_path.exists():
        print("ERROR: search_ids.json not found after search ingestion")
        print("       06_upload_to_search.py must complete successfully first")
        sys.exit(1)

    with open(search_ids_path) as f:
        search_ids = json.load(f)

    index_name = search_ids.get("index_name")
    if not index_name:
        print("ERROR: index_name missing in search_ids.json")
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
        print("ERROR: No PDF files found for Foundry IQ ingestion")
        print(f"       Looked in: {docs_dir}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("Provision Foundry IQ Knowledge Base")
    print(f"{'='*60}")
    print(f"Project Endpoint: {PROJECT_ENDPOINT}")
    print(f"Project Resource ID: {PROJECT_RESOURCE_ID}")
    print(f"Search Endpoint: {SEARCH_ENDPOINT}")
    print(f"Knowledge Source: {knowledge_source_name}")
    print(f"Knowledge Base: {knowledge_base_name}")
    print(f"Project Connection: {project_connection_name}")
    print(f"Data Folder: {data_dir}")
    print(f"Documents Folder: {docs_dir}")
    print(f"PDF Files: {len(pdf_files)}")

    run_search_ingestion()
    search_ids = load_search_metadata()
    index_name = search_ids["index_name"]

    credential = DefaultAzureCredential()
    index_client = SearchIndexClient(SEARCH_ENDPOINT, credential)

    print("\nCreating or updating knowledge source...")
    create_knowledge_source(index_client, index_name)
    print(f"[OK] Knowledge source '{knowledge_source_name}' ready")

    print("\nCreating or updating knowledge base...")
    create_knowledge_base(index_client)
    print(f"[OK] Knowledge base '{knowledge_base_name}' ready")

    mcp_endpoint = (
        f"{SEARCH_ENDPOINT}/knowledgebases/{knowledge_base_name}/mcp"
        f"?api-version={KNOWLEDGE_BASE_MCP_API_VERSION}"
    )

    print("\nCreating or updating Foundry project connection...")
    project_connection_id = create_project_connection(mcp_endpoint)
    print(f"[OK] Project connection '{project_connection_name}' ready")

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

    print(f"[OK] Knowledge metadata saved to: {knowledge_ids_path}")
    print(f"\n{'='*60}")
    print("Foundry IQ Knowledge Base Ready")
    print(f"{'='*60}")
    print(f"Search Index: {index_name}")
    print(f"Knowledge Base: {knowledge_base_name}")
    print(f"Project Connection ID: {project_connection_id}")
    print("Next: python scripts/07b_create_foundry_iq_agent.py")


if __name__ == "__main__":
    main()
