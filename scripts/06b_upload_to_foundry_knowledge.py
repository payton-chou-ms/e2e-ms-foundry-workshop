"""
06b - Upload documents to Foundry-native File Search knowledge
Creates or replaces a Foundry/OpenAI vector store from the current DATA_FOLDER documents.

Usage:
    python 06b_upload_to_foundry_knowledge.py

Prerequisites:
    - Run 01_generate_sample_data.py (creates PDF files in data folder)
    - AZURE_AI_PROJECT_ENDPOINT available from azd

This script stores metadata in config/knowledge_ids.json.
"""

from pathlib import Path
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from load_env import load_all_env
import json
import os
import sys

load_all_env()

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
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
vector_store_name = f"{SOLUTION_NAME}-foundry-iq-store"


def load_existing_metadata():
    if knowledge_ids_path.exists():
        with open(knowledge_ids_path) as f:
            return json.load(f)
    return {}


def main():
    pdf_files = sorted(docs_dir.glob("*.pdf"))
    if not pdf_files:
        print("ERROR: No PDF files found for Foundry-native ingestion")
        print(f"       Looked in: {docs_dir}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("Upload Documents to Foundry-native File Search")
    print(f"{'='*60}")
    print(f"Project Endpoint: {PROJECT_ENDPOINT}")
    print(f"Vector Store Name: {vector_store_name}")
    print(f"Data Folder: {data_dir}")
    print(f"Documents Folder: {docs_dir}")
    print(f"PDF Files: {len(pdf_files)}")

    project_client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(),
    )
    openai_client = project_client.get_openai_client()

    existing = load_existing_metadata()
    existing_store_id = existing.get("vector_store_id")
    if existing_store_id:
        try:
            print(f"\nDeleting previous vector store: {existing_store_id}")
            openai_client.vector_stores.delete(existing_store_id)
            print("[OK] Deleted previous vector store")
        except Exception as exc:
            print(f"WARNING: Could not delete previous vector store: {exc}")

    print("\nCreating vector store...")
    vector_store = openai_client.vector_stores.create(
        name=vector_store_name,
        description=f"Foundry IQ file-search store for {SOLUTION_NAME}",
    )
    print(f"[OK] Vector store created: {vector_store.id}")

    uploaded_files = []
    for pdf_path in pdf_files:
        print(f"Uploading {pdf_path.name}...", end=" ", flush=True)
        with pdf_path.open("rb") as file_handle:
            uploaded = openai_client.vector_stores.files.upload_and_poll(
                vector_store_id=vector_store.id,
                file=file_handle,
            )
        uploaded_files.append(
            {
                "filename": pdf_path.name,
                "vector_store_file_id": getattr(uploaded, "id", ""),
                "status": getattr(uploaded, "status", "unknown"),
            }
        )
        print("[OK]")

    metadata = {
        "knowledge_type": "foundry_file_search",
        "vector_store_name": vector_store_name,
        "vector_store_id": vector_store.id,
        "document_count": len(pdf_files),
        "source_folder": str(docs_dir),
        "uploaded_files": uploaded_files,
        "status": "ready",
    }

    with open(knowledge_ids_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"[OK] Knowledge metadata saved to: {knowledge_ids_path}")
    print(f"\n{'='*60}")
    print("Foundry-native File Search Ready")
    print(f"{'='*60}")
    print(f"Vector Store ID: {vector_store.id}")
    print(f"Next: python scripts/07b_create_foundry_iq_agent.py")


if __name__ == "__main__":
    main()
