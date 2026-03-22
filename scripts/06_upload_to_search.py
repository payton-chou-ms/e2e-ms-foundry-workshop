"""把 PDF 文件上傳到 Azure AI Search。"""

from pypdf import PdfReader
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    AzureOpenAIVectorizer,
    AzureOpenAIVectorizerParameters,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch,
)
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents import SearchClient
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential
import os
import sys
import json
import re
from pathlib import Path

# Load environment from azd + project .env
from load_env import load_all_env, get_required_env, print_env_status
load_all_env()


# ============================================================================
# Configuration
# ============================================================================

# Azure services - from azd environment
AZURE_AI_ENDPOINT = os.getenv("AZURE_AI_ENDPOINT") or os.getenv(
    "AZURE_AI_PROJECT_ENDPOINT", "").split("/api/projects")[0]
AZURE_AI_SEARCH_ENDPOINT = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
EMBEDDING_MODEL = os.getenv("AZURE_EMBEDDING_MODEL") or os.getenv(
    "EMBEDDING_MODEL", "text-embedding-3-large")

# Project settings - from .env
DATA_FOLDER = os.getenv("DATA_FOLDER")
SOLUTION_NAME = os.getenv("SOLUTION_NAME") or os.getenv(
    "SOLUTION_PREFIX") or os.getenv("AZURE_ENV_NAME", "demo")

INDEX_NAME = f"{SOLUTION_NAME}-documents"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

if not AZURE_AI_SEARCH_ENDPOINT:
    print("錯誤：.env 中未設定 AZURE_AI_SEARCH_ENDPOINT")
    sys.exit(1)

if not DATA_FOLDER:
    print("錯誤：.env 中未設定 DATA_FOLDER")
    print("      請先執行 01_generate_sample_data.py")
    sys.exit(1)

data_dir = Path(DATA_FOLDER)
if not data_dir.exists():
    print(f"錯誤：找不到資料資料夾：{data_dir}")
    sys.exit(1)

# Set up paths for new folder structure (config/, tables/, documents/)
config_dir = data_dir / "config"
docs_dir = data_dir / "documents"

# Fallback to old structure if config dir doesn't exist
if not config_dir.exists():
    config_dir = data_dir
if not docs_dir.exists():
    docs_dir = data_dir  # Fallback to root data folder

print(f"\n{'='*60}")
print("把 PDF 檔上傳到 Azure AI Search")
print(f"{'='*60}")
print(f"Search Endpoint：{AZURE_AI_SEARCH_ENDPOINT}")
print(f"AI Endpoint：{AZURE_AI_ENDPOINT}")
print(f"Embedding 模型：{EMBEDDING_MODEL}")
print(f"索引名稱：{INDEX_NAME}")
print(f"資料資料夾：{data_dir}")

# ============================================================================
# Azure OpenAI Client
# ============================================================================


def get_openai_client():
    """Create Azure OpenAI client using AI endpoint."""
    if not AZURE_AI_ENDPOINT:
        raise ValueError("未設定 AZURE_AI_PROJECT_ENDPOINT")

    credential = DefaultAzureCredential()
    token = credential.get_token(
        "https://cognitiveservices.azure.com/.default")

    return AzureOpenAI(
        azure_endpoint=AZURE_AI_ENDPOINT,
        api_key=token.token,
        api_version="2024-10-21",
    )

# ============================================================================
# Azure Search Clients
# ============================================================================


def get_search_clients():
    """Create Azure Search clients."""
    credential = DefaultAzureCredential()
    index_client = SearchIndexClient(AZURE_AI_SEARCH_ENDPOINT, credential)
    search_client = SearchClient(
        AZURE_AI_SEARCH_ENDPOINT, INDEX_NAME, credential)

    return index_client, search_client

# ============================================================================
# Create Search Index
# ============================================================================


def create_index(index_client: SearchIndexClient):
    """Create or update the search index with integrated vectorizer."""

    # Embedding dimensions by model
    EMBEDDING_DIMENSIONS = {
        "text-embedding-ada-002": 1536,
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
    }
    dimensions = EMBEDDING_DIMENSIONS.get(EMBEDDING_MODEL, 1536)

    fields = [
        SearchField(name="id", type=SearchFieldDataType.String, key=True),
        SearchField(name="content",
                    type=SearchFieldDataType.String, searchable=True),
        SearchField(name="title", type=SearchFieldDataType.String,
                    searchable=True, filterable=True),
        SearchField(name="source", type=SearchFieldDataType.String,
                    filterable=True),
        SearchField(name="page_number", type=SearchFieldDataType.Int32,
                    filterable=True, sortable=True),
        SearchField(name="chunk_id",
                    type=SearchFieldDataType.Int32, sortable=True),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=dimensions,
            vector_search_profile_name="default-profile"
        ),
    ]

    # Integrated vectorizer for query-time embedding
    vectorizer = AzureOpenAIVectorizer(
        vectorizer_name="openai-vectorizer",
        parameters=AzureOpenAIVectorizerParameters(
            resource_url=AZURE_AI_ENDPOINT,
            deployment_name=EMBEDDING_MODEL,
            model_name=EMBEDDING_MODEL,
        )
    )

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="default-algorithm")],
        profiles=[VectorSearchProfile(
            name="default-profile",
            algorithm_configuration_name="default-algorithm",
            vectorizer_name="openai-vectorizer"
        )],
        vectorizers=[vectorizer]
    )

    # Semantic configuration for hybrid search
    semantic_config = SemanticConfiguration(
        name="default-semantic",
        prioritized_fields=SemanticPrioritizedFields(
            content_fields=[SemanticField(field_name="content")],
            title_field=SemanticField(field_name="title"),
        )
    )
    semantic_search = SemanticSearch(configurations=[semantic_config])

    index = SearchIndex(
        name=INDEX_NAME,
        fields=fields,
        vector_search=vector_search,
        semantic_search=semantic_search
    )

    index_client.create_or_update_index(index)
    print(f"[OK] 索引 '{INDEX_NAME}' 已就緒，並已啟用整合式 vectorizer")

# ============================================================================
# PDF Processing
# ============================================================================


def extract_pages_from_pdf(filepath: Path) -> list[tuple[int, str]]:
    """Extract text content from each page of a PDF file.

    Returns list of (page_number, text) tuples (1-indexed page numbers).
    """
    reader = PdfReader(filepath)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            pages.append((i + 1, text.strip()))
    return pages

# ============================================================================
# Text Chunking
# ============================================================================


def split_into_sentences(text: str) -> list[str]:
    """Split text into sentences, preserving sentence boundaries."""
    # Split on sentence-ending punctuation followed by space or newline
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_text_by_sentences(text: str, max_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into chunks that respect sentence boundaries.

    Chunks will not exceed max_size and will not cut mid-sentence.
    Overlap is applied by including trailing sentences from previous chunk.
    """
    sentences = split_into_sentences(text)

    if not sentences:
        return [text] if text.strip() else []

    chunks = []
    current_chunk = []
    current_length = 0
    overlap_sentences = []

    for sentence in sentences:
        sentence_len = len(sentence)

        # If single sentence exceeds max_size, include it anyway (don't break mid-sentence)
        if sentence_len > max_size:
            # Save current chunk if it has content
            if current_chunk:
                chunks.append(' '.join(current_chunk))
                overlap_sentences = current_chunk[-2:] if len(
                    current_chunk) >= 2 else current_chunk[:]

            chunks.append(sentence)
            current_chunk = []
            current_length = 0
            overlap_sentences = []
            continue

        # Check if adding this sentence would exceed max_size
        potential_length = current_length + \
            sentence_len + (1 if current_chunk else 0)

        if potential_length > max_size and current_chunk:
            # Save current chunk
            chunks.append(' '.join(current_chunk))

            # Start new chunk with overlap from previous
            overlap_text_len = sum(
                len(s) for s in overlap_sentences) + len(overlap_sentences)
            if overlap_text_len < overlap and overlap_sentences:
                current_chunk = overlap_sentences[:]
                current_length = overlap_text_len
            else:
                current_chunk = []
                current_length = 0

        # Add sentence to current chunk
        current_chunk.append(sentence)
        current_length += sentence_len + (1 if len(current_chunk) > 1 else 0)

        # Track sentences for potential overlap
        overlap_sentences = current_chunk[-2:] if len(
            current_chunk) >= 2 else current_chunk[:]

    # Don't forget the last chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# ============================================================================
# Embedding Generation
# ============================================================================


def get_embedding(client: AzureOpenAI, text: str) -> list[float]:
    """Generate embedding for text using OpenAI client."""
    response = client.embeddings.create(input=[text], model=EMBEDDING_MODEL)
    return response.data[0].embedding

# ============================================================================
# Main
# ============================================================================


def main():
    # Find PDF files in documents subfolder
    pdf_files = list(docs_dir.glob("*.pdf"))
    if not pdf_files:
        print("\n在資料資料夾中找不到 PDF 檔。")
        print(f"查找位置：{docs_dir}")
        print("請先執行 01_generate_sample_data.py 產生範例 PDF。")
        return

    print(f"\n找到 {len(pdf_files)} 個 PDF 檔")
    for pdf in pdf_files:
        print(f"  - {pdf.name}")

    # Initialize clients
    print("\n初始化用戶端...")
    openai_client = get_openai_client()
    print("[OK] OpenAI 用戶端已初始化")

    index_client, search_client = get_search_clients()
    print("[OK] Search 用戶端已初始化")

    # Create index
    print("\n建立搜尋索引...")
    create_index(index_client)

    # Process each PDF
    documents = []
    for pdf_path in pdf_files:
        print(f"\n處理中：{pdf_path.name}")

        pages = extract_pages_from_pdf(pdf_path)
        print(f"  已擷取 {len(pages)} 頁")

        for page_num, page_text in pages:
            chunks = chunk_text_by_sentences(page_text)

            for chunk_idx, chunk in enumerate(chunks):
                # ID format: filename_pagenumber_chunknumber
                doc_id = f"{pdf_path.stem}_p{page_num}_c{chunk_idx}"

                print(
                    f"  正在為 {doc_id} 產生 embedding...", end=" ", flush=True)
                embedding = get_embedding(openai_client, chunk)
                print("[OK]")

                doc = {
                    "id": doc_id,
                    "content": chunk,
                    "title": pdf_path.stem.replace("_", " ").title(),
                    "source": pdf_path.name,
                    "page_number": page_num,
                    "chunk_id": chunk_idx,
                    "embedding": embedding
                }
                documents.append(doc)

    # Upload to search
    print(f"\n正在把 {len(documents)} 個 chunk 上傳到搜尋索引...")
    result = search_client.upload_documents(documents)
    succeeded = sum(1 for r in result if r.succeeded)
    print(f"[OK] 已上傳 {succeeded}/{len(documents)} 筆文件")

    # Save index info
    search_ids_path = config_dir / "search_ids.json"
    search_info = {
        "index_name": INDEX_NAME,
        "document_count": len(documents),
        "pdf_files": [p.name for p in pdf_files]
    }
    with open(search_ids_path, "w") as f:
        json.dump(search_info, f, indent=2)
    print(f"[OK] 已把 Search 資訊寫入：{search_ids_path}")

    print(f"\n{'='*60}")
    print("上傳完成！")
    print(f"{'='*60}")
    print(f"索引：{INDEX_NAME}")
    print(f"文件數：{len(documents)}")
    print(f"\n現在可以開始用 Azure AI Search 查詢這個索引。")


if __name__ == "__main__":
    main()
