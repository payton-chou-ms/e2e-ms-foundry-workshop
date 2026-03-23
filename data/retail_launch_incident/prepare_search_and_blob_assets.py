"""Prepare retail incident knowledge assets in Blob Storage and Azure AI Search."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys

from azure.identity import get_bearer_token_provider
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    AzureOpenAIVectorizer,
    AzureOpenAIVectorizerParameters,
    HnswAlgorithmConfiguration,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch,
    VectorSearch,
    VectorSearchProfile,
)
from azure.core.exceptions import HttpResponseError, ResourceExistsError, ResourceNotFoundError
from azure.storage.blob import BlobServiceClient, ContentSettings
from openai import AzureOpenAI
from pypdf import PdfReader

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from credential_utils import get_credential
from load_env import load_all_env

load_all_env()


SCENARIO_DIR = Path(__file__).resolve().parent
CONFIG_DIR = SCENARIO_DIR / "config"
DOCS_DIR = SCENARIO_DIR / "documents"
TABLES_DIR = SCENARIO_DIR / "tables"
SEARCH_IDS_PATH = CONFIG_DIR / "search_ids.json"

AZURE_AI_ENDPOINT = os.getenv("AZURE_AI_ENDPOINT") or os.getenv(
    "AZURE_AI_PROJECT_ENDPOINT", ""
).split("/api/projects")[0]
AZURE_AI_SEARCH_ENDPOINT = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
AZURE_STORAGE_BLOB_ENDPOINT = os.getenv("AZURE_STORAGE_BLOB_ENDPOINT")
AZURE_STORAGE_BLOB_CONTAINER = os.getenv("AZURE_STORAGE_BLOB_CONTAINER", "default")
EMBEDDING_MODEL = os.getenv("AZURE_EMBEDDING_MODEL") or os.getenv(
    "EMBEDDING_MODEL", "text-embedding-3-large"
)
SOLUTION_NAME = os.getenv("SOLUTION_NAME") or os.getenv(
    "SOLUTION_PREFIX"
) or os.getenv("AZURE_ENV_NAME", "demo")


def normalize_knowledge_source_name(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9-]", "-", value.lower())
    normalized = re.sub(r"-+", "-", normalized).strip("-")
    if len(normalized) < 2:
        normalized = f"ks-{normalized}".strip("-")
    return normalized[:100].rstrip("-")

SCENARIO_KEY = SCENARIO_DIR.name.replace("-", "_")
DOCUMENT_INDEX_NAME = f"{SOLUTION_NAME}-{SCENARIO_KEY}-documents"
TABLE_INDEX_NAME = f"{SOLUTION_NAME}-{SCENARIO_KEY}-tables"
DOCUMENT_SOURCE_NAME = normalize_knowledge_source_name(
    f"{SOLUTION_NAME}-{SCENARIO_KEY}-documents-source"
)
TABLE_SOURCE_NAME = normalize_knowledge_source_name(
    f"{SOLUTION_NAME}-{SCENARIO_KEY}-tables-source"
)
SEMANTIC_CONFIGURATION_NAME = "default-semantic"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

EMBEDDING_DIMENSIONS = {
    "text-embedding-ada-002": 1536,
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
}


def require_env(name: str, value: str | None):
    if value:
        return value

    print(f"錯誤：未設定 {name}")
    print("      請先執行 'azd up' 部署 Azure 資源，並確認 .env 設定完成")
    sys.exit(1)


def get_openai_client() -> AzureOpenAI:
    credential = get_credential()
    return AzureOpenAI(
        azure_endpoint=AZURE_AI_ENDPOINT,
        azure_ad_token_provider=get_bearer_token_provider(
            credential, "https://cognitiveservices.azure.com/.default"
        ),
        api_version="2024-10-21",
    )


def get_search_index_client() -> SearchIndexClient:
    credential = get_credential()
    return SearchIndexClient(AZURE_AI_SEARCH_ENDPOINT, credential)


def get_search_client(index_name: str) -> SearchClient:
    credential = get_credential()
    return SearchClient(AZURE_AI_SEARCH_ENDPOINT, index_name, credential)


def get_blob_service_client() -> BlobServiceClient:
    credential = get_credential()
    return BlobServiceClient(account_url=AZURE_STORAGE_BLOB_ENDPOINT, credential=credential)


def create_search_index(index_client: SearchIndexClient, index_name: str):
    dimensions = EMBEDDING_DIMENSIONS.get(EMBEDDING_MODEL, 1536)
    fields = [
        SearchField(name="id", type=SearchFieldDataType.String, key=True),
        SearchField(name="content", type=SearchFieldDataType.String, searchable=True),
        SearchField(
            name="title",
            type=SearchFieldDataType.String,
            searchable=True,
            filterable=True,
        ),
        SearchField(name="source", type=SearchFieldDataType.String, filterable=True),
        SearchField(name="source_path", type=SearchFieldDataType.String, filterable=True),
        SearchField(name="record_type", type=SearchFieldDataType.String, filterable=True),
        SearchField(
            name="page_number",
            type=SearchFieldDataType.Int32,
            filterable=True,
            sortable=True,
        ),
        SearchField(
            name="chunk_id",
            type=SearchFieldDataType.Int32,
            filterable=True,
            sortable=True,
        ),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=dimensions,
            vector_search_profile_name="default-profile",
        ),
    ]

    vectorizer = AzureOpenAIVectorizer(
        vectorizer_name="openai-vectorizer",
        parameters=AzureOpenAIVectorizerParameters(
            resource_url=AZURE_AI_ENDPOINT,
            deployment_name=EMBEDDING_MODEL,
            model_name=EMBEDDING_MODEL,
        ),
    )

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="default-algorithm")],
        profiles=[
            VectorSearchProfile(
                name="default-profile",
                algorithm_configuration_name="default-algorithm",
                vectorizer_name="openai-vectorizer",
            )
        ],
        vectorizers=[vectorizer],
    )

    semantic_config = SemanticConfiguration(
        name=SEMANTIC_CONFIGURATION_NAME,
        prioritized_fields=SemanticPrioritizedFields(
            content_fields=[SemanticField(field_name="content")],
            title_field=SemanticField(field_name="title"),
        ),
    )

    index = SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search,
        semantic_search=SemanticSearch(configurations=[semantic_config]),
    )
    index_client.create_or_update_index(index)


def extract_pages_from_pdf(filepath: Path) -> list[tuple[int, str]]:
    reader = PdfReader(filepath)
    pages: list[tuple[int, str]] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text and text.strip():
            pages.append((index, text.strip()))
    return pages


def split_into_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def chunk_text_by_sentences(
    text: str, max_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP
) -> list[str]:
    sentences = split_into_sentences(text)
    if not sentences:
        return [text] if text.strip() else []

    chunks: list[str] = []
    current_chunk: list[str] = []
    current_length = 0
    overlap_sentences: list[str] = []

    for sentence in sentences:
        sentence_len = len(sentence)
        if sentence_len > max_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                overlap_sentences = current_chunk[-2:] if len(current_chunk) >= 2 else current_chunk[:]

            chunks.append(sentence)
            current_chunk = []
            current_length = 0
            overlap_sentences = []
            continue

        potential_length = current_length + sentence_len + (1 if current_chunk else 0)
        if potential_length > max_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            overlap_length = sum(len(item) for item in overlap_sentences) + len(overlap_sentences)
            if overlap_length < overlap and overlap_sentences:
                current_chunk = overlap_sentences[:]
                current_length = overlap_length
            else:
                current_chunk = []
                current_length = 0

        current_chunk.append(sentence)
        current_length += sentence_len + (1 if len(current_chunk) > 1 else 0)
        overlap_sentences = current_chunk[-2:] if len(current_chunk) >= 2 else current_chunk[:]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def get_embedding(client: AzureOpenAI, text: str) -> list[float]:
    response = client.embeddings.create(input=[text], model=EMBEDDING_MODEL)
    return response.data[0].embedding


def upload_pdf_blobs(blob_service_client: BlobServiceClient, pdf_files: list[Path]) -> list[dict[str, str]]:
    container_client = blob_service_client.get_container_client(AZURE_STORAGE_BLOB_CONTAINER)
    try:
        container_client.get_container_properties()
    except ResourceNotFoundError:
        print("錯誤：找不到預期的 Blob container")
        print(f"      Container：{AZURE_STORAGE_BLOB_CONTAINER}")
        print("      請先確認 azd up 已成功建立 storage-connection 與 default container")
        sys.exit(1)

    blob_prefix = f"{SCENARIO_DIR.name}/documents/"
    for existing_blob in container_client.list_blobs(name_starts_with=blob_prefix):
        container_client.delete_blob(existing_blob.name)

    uploaded_files: list[dict[str, str]] = []
    for pdf_file in pdf_files:
        blob_name = f"{SCENARIO_DIR.name}/documents/{pdf_file.name}"
        with pdf_file.open("rb") as handle:
            container_client.upload_blob(
                name=blob_name,
                data=handle,
                overwrite=True,
                content_settings=ContentSettings(content_type="application/pdf"),
            )

        uploaded_files.append(
            {
                "name": pdf_file.name,
                "blob_name": blob_name,
                "blob_url": f"{AZURE_STORAGE_BLOB_ENDPOINT.rstrip('/')}/{AZURE_STORAGE_BLOB_CONTAINER}/{blob_name}",
            }
        )

    return uploaded_files


def build_pdf_documents(openai_client: AzureOpenAI, pdf_files: list[Path]) -> list[dict[str, object]]:
    documents: list[dict[str, object]] = []
    for pdf_path in pdf_files:
        pages = extract_pages_from_pdf(pdf_path)
        for page_number, page_text in pages:
            chunks = chunk_text_by_sentences(page_text)
            for chunk_index, chunk in enumerate(chunks):
                documents.append(
                    {
                        "id": f"doc-{pdf_path.stem}-p{page_number}-c{chunk_index}",
                        "content": chunk,
                        "title": pdf_path.stem.replace("_", " ").title(),
                        "source": pdf_path.name,
                        "source_path": f"documents/{pdf_path.name}",
                        "record_type": "document_chunk",
                        "page_number": page_number,
                        "chunk_id": chunk_index,
                        "embedding": get_embedding(openai_client, chunk),
                    }
                )
    return documents


def row_to_content(table_name: str, row_number: int, row: dict[str, str]) -> str:
    pairs = [f"{key}: {value}" for key, value in row.items() if value not in (None, "")]
    return f"Table {table_name}, row {row_number}. " + " | ".join(pairs)


def build_table_documents(openai_client: AzureOpenAI, csv_files: list[Path]) -> list[dict[str, object]]:
    documents: list[dict[str, object]] = []
    for csv_path in csv_files:
        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row_number, row in enumerate(reader, start=1):
                content = row_to_content(csv_path.stem, row_number, row)
                documents.append(
                    {
                        "id": f"table-{csv_path.stem}-r{row_number}",
                        "content": content,
                        "title": csv_path.stem.replace("_", " ").title(),
                        "source": csv_path.name,
                        "source_path": f"tables/{csv_path.name}#row={row_number}",
                        "record_type": "table_row",
                        "page_number": row_number,
                        "chunk_id": 0,
                        "embedding": get_embedding(openai_client, content),
                    }
                )
    return documents


def upload_documents(search_client: SearchClient, documents: list[dict[str, object]]):
    existing_ids = [result["id"] for result in search_client.search(search_text="*", select=["id"])]
    if existing_ids:
        search_client.delete_documents(documents=[{"id": doc_id} for doc_id in existing_ids])

    if not documents:
        return 0

    result = search_client.upload_documents(documents)
    failed_ids = [item.key for item in result if not item.succeeded]
    if failed_ids:
        print("錯誤：部分 Search 文件上傳失敗")
        print(f"      失敗筆數：{len(failed_ids)}")
        print(f"      前 10 筆失敗 ID：{failed_ids[:10]}")
        sys.exit(1)

    return len(documents)


def write_metadata(
    blob_files: list[dict[str, str]],
    pdf_documents: list[dict[str, object]],
    table_documents: list[dict[str, object]],
    pdf_files: list[Path],
    csv_files: list[Path],
):
    metadata = {
        "search_type": "scenario_multi_index",
        "scenario": SCENARIO_DIR.name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "blob_endpoint": AZURE_STORAGE_BLOB_ENDPOINT,
        "blob_container": AZURE_STORAGE_BLOB_CONTAINER,
        "blob_prefix": f"{SCENARIO_DIR.name}/documents",
        "blob_files": blob_files,
        "index_name": DOCUMENT_INDEX_NAME,
        "document_count": len(pdf_documents),
        "pdf_files": [pdf_file.name for pdf_file in pdf_files],
        "table_files": [csv_file.name for csv_file in csv_files],
        "indexes": [
            {
                "name": DOCUMENT_INDEX_NAME,
                "kind": "document_chunks",
                "knowledge_source_name": DOCUMENT_SOURCE_NAME,
                "document_count": len(pdf_documents),
                "source_files": [pdf_file.name for pdf_file in pdf_files],
                "source_data_fields": ["content", "title", "source", "page_number", "chunk_id"],
                "search_fields": ["content", "title"],
                "semantic_configuration_name": SEMANTIC_CONFIGURATION_NAME,
            },
            {
                "name": TABLE_INDEX_NAME,
                "kind": "table_rows",
                "knowledge_source_name": TABLE_SOURCE_NAME,
                "document_count": len(table_documents),
                "source_files": [csv_file.name for csv_file in csv_files],
                "source_data_fields": ["content", "title", "source", "page_number", "chunk_id"],
                "search_fields": ["content", "title"],
                "semantic_configuration_name": SEMANTIC_CONFIGURATION_NAME,
            },
        ],
    }

    with SEARCH_IDS_PATH.open("w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2, ensure_ascii=False)


def main():
    require_env("AZURE_AI_PROJECT_ENDPOINT or AZURE_AI_ENDPOINT", AZURE_AI_ENDPOINT)
    require_env("AZURE_AI_SEARCH_ENDPOINT", AZURE_AI_SEARCH_ENDPOINT)
    require_env("AZURE_STORAGE_BLOB_ENDPOINT", AZURE_STORAGE_BLOB_ENDPOINT)

    if not DOCS_DIR.exists() or not TABLES_DIR.exists():
        print("錯誤：Retail Launch Incident 資料夾結構不完整")
        print(f"      預期 documents：{DOCS_DIR}")
        print(f"      預期 tables：{TABLES_DIR}")
        sys.exit(1)

    pdf_files = sorted(DOCS_DIR.glob("*.pdf"))
    csv_files = sorted(TABLES_DIR.glob("*.csv"))
    if not pdf_files and not csv_files:
        print("錯誤：找不到可上傳的 PDF 或 CSV 檔")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("準備 Retail Launch Incident 知識資產")
    print(f"{'='*60}")
    print(f"Scenario：{SCENARIO_DIR.name}")
    print(f"Blob Endpoint：{AZURE_STORAGE_BLOB_ENDPOINT}")
    print(f"Blob Container：{AZURE_STORAGE_BLOB_CONTAINER}")
    print(f"文件索引：{DOCUMENT_INDEX_NAME}")
    print(f"表格索引：{TABLE_INDEX_NAME}")
    print(f"PDF 檔數：{len(pdf_files)}")
    print(f"CSV 檔數：{len(csv_files)}")

    openai_client = get_openai_client()
    index_client = get_search_index_client()
    blob_service_client = get_blob_service_client()

    print("\n建立或更新搜尋索引...")
    create_search_index(index_client, DOCUMENT_INDEX_NAME)
    create_search_index(index_client, TABLE_INDEX_NAME)
    print("[OK] 搜尋索引已就緒")

    print("\n上傳 PDF 原檔到 Blob Storage...")
    try:
        blob_files = upload_pdf_blobs(blob_service_client, pdf_files)
    except HttpResponseError as exc:
        print("錯誤：Blob Storage 存取失敗")
        print(f"      ErrorCode：{exc.error_code or exc.__class__.__name__}")
        print("      這個 workshop 需使用 Microsoft Entra ID 直接寫入 Blob。")
        print("      請確認 storage account 已啟用 Public network access，且目前使用者具備 Blob data plane 權限。")
        raise
    print(f"[OK] 已上傳 {len(blob_files)} 份 PDF 原檔")

    print("\n建立 PDF 檢索文件...")
    pdf_documents = build_pdf_documents(openai_client, pdf_files)
    doc_search_client = get_search_client(DOCUMENT_INDEX_NAME)
    uploaded_pdf_documents = upload_documents(doc_search_client, pdf_documents)
    print(f"[OK] 已上傳 {uploaded_pdf_documents}/{len(pdf_documents)} 個 PDF chunk")

    print("\n建立 CSV 檢索文件...")
    table_documents = build_table_documents(openai_client, csv_files)
    table_search_client = get_search_client(TABLE_INDEX_NAME)
    uploaded_table_documents = upload_documents(table_search_client, table_documents)
    print(f"[OK] 已上傳 {uploaded_table_documents}/{len(table_documents)} 個 CSV row 文件")

    write_metadata(blob_files, pdf_documents, table_documents, pdf_files, csv_files)
    print(f"[OK] 已把 metadata 寫入：{SEARCH_IDS_PATH}")
    print(f"\n{'='*60}")
    print("Retail Launch Incident 資產準備完成")
    print(f"{'='*60}")
    print(f"下一步：python {REPO_ROOT / 'scripts' / '06b_upload_to_foundry_knowledge.py'}")


if __name__ == "__main__":
    main()
