# Foundry IQ：文件智慧

## 什麼是 Foundry IQ？

在這個 workshop 裡，Foundry IQ 指的是「文件接地」這條路徑：先把 PDF 文件整理、切塊並上傳到 Azure AI Search，再讓 Foundry agent 透過 `search_documents` 工具取回帶來源資訊的段落。

## 主要功能

| 功能 | 說明 |
|------|------|
| **文件索引** | 由腳本建立 Azure AI Search index，並寫入頁面與來源欄位 |
| **引用段落** | `search_documents` 回傳包含來源、標題與頁碼的片段 |
| **Entra ID 驗證** | Workshop 腳本以 Azure 身分直接呼叫 Search 與 Foundry |
| **多格式支援** | PDF、Word、PowerPoint 及非結構化文字 |

## 目前 workshop 的文件路徑

目前的主路徑不是 Foundry 原生 agentic retrieval，而是下列可檢視、可追蹤的流程：

```
User: "What's our policy for notifying customers during extended outages?"

┌─────────────────────────────────────────────────────────────┐
│  Step 1: INGEST                                             │
│  Workshop script:                                           │
│  • Extracts text from PDFs                                  │
│  • Chunks by sentences                                      │
│  • Generates embeddings                                     │
│  • Uploads chunks to Azure AI Search                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: TOOL CALL                                           │
│  Agent decides the question needs document evidence         │
│  and emits `search_documents(query=...)`                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: SEARCH                                              │
│  Local runtime calls Azure AI Search with semantic search   │
│  and returns source/title/page metadata                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 4: SYNTHESIZE                                          │
│  Agent reads returned passages and answers with             │
│  grounded wording and visible citation metadata             │
└─────────────────────────────────────────────────────────────┘
```

## 為什麼這對客戶很重要

### 為什麼這樣的設計值得展示

這條路徑的重點不是宣稱平台自動替你做完整知識推理，而是讓客戶清楚看見：

- 文件如何被索引
- agent 何時決定需要文件證據
- runtime 實際送出了什麼搜尋
- 最終答案引用的是哪個來源與頁碼

### 目前頁面應如何對外說明

比較精準的說法是：

1. 文件接地目前由 Azure AI Search 提供索引與檢索
2. Foundry agent 透過受控函式工具決定何時查文件
3. 本機 runtime 負責把搜尋結果回傳給 agent
4. 引用資訊來自實際索引欄位，而不是隱藏的黑盒流程

## 客戶對話要點

| 問題 | 回應 |
|------|------|
| 「為什麼不直接用搜尋？」 | 「因為 workshop 不只示範搜尋本身，而是示範 agent 如何在需要時呼叫文件工具，並把可引用的段落整合回答案。」 |
| 「幻覺問題怎麼辦？」 | 「文件答案來自實際搜尋結果，結果裡保留 source、title 與 page metadata，方便人工驗證。」 |
| 「能處理我們複雜的政策嗎？」 | 「可以先從目前的 Search-grounded 路徑示範；如果後續要進一步擴成更複雜的檢索策略，那是下一階段延伸，而不是本 workshop 目前已經自動具備的能力。」 |

## 技術細節

### 文件處理管線

```
PDFs/Word/PPT → Text Extraction → Chunking → Embedding → Vector Index
```

- **分塊**：保留句子邊界，通常 500-1000 個 token
- **向量嵌入**：Azure OpenAI text-embedding-3-large（3072 維度）
- **索引**：Azure AI Search index，包含內容、標題、來源、頁碼與向量欄位

### 搜尋設定

```python
results = search_client.search(
    search_text=query,
    query_type="semantic",
    semantic_configuration_name="default-semantic",
    select=["content", "title", "source", "page_number"],
)
```

---

[← 概觀](index.md) | [Fabric IQ：資料 →](02-fabric-iq.md)
