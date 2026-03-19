# Foundry IQ：文件智慧

## 什麼是 Foundry IQ？

Foundry IQ 是 Azure AI Foundry 的統一知識層，讓代理程式能夠透過智慧檢索存取企業文件。

## 主要功能

| 功能 | 說明 |
|------|------|
| **知識庫** | 自動索引建立與文件向量化 |
| **代理式檢索** | 具備規劃、迭代與反思能力的 AI 驅動搜尋 |
| **企業安全性** | 內建 Entra ID 驗證與 Purview 整合 |
| **多格式支援** | PDF、Word、PowerPoint 及非結構化文字 |

## 代理式檢索的運作方式

與簡單的向量搜尋（尋找相似文字）不同，代理式檢索使用 AI 來：

```
User: "What's our policy for notifying customers during extended outages?"

┌─────────────────────────────────────────────────────────────┐
│  Step 1: PLAN                                               │
│  Agent decomposes into sub-queries:                         │
│  • "customer notification policy"                           │
│  • "extended outage definition"                             │
│  • "communication requirements during incidents"            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: ITERATE                                            │
│  For each sub-query:                                        │
│  • Search knowledge base                                    │
│  • Evaluate relevance of results                            │
│  • Refine search if needed                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: REFLECT                                            │
│  Before responding:                                         │
│  • Do I have enough information?                            │
│  • Are sources consistent?                                  │
│  • Can I cite specific documents?                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Response with Citations                                    │
│  "According to our Customer Service Policies (page 2),      │
│  customers must be notified within 15 minutes of a          │
│  confirmed outage. The Outage Management Policy (page 1)    │
│  defines extended outages as those exceeding 4 hours..."    │
└─────────────────────────────────────────────────────────────┘
```

## 為什麼這對客戶很重要

### 問題：簡單 RAG 無法處理複雜問題

基本的檢索增強生成（RAG）只進行一次搜尋並使用任何返回的結果。以下情況會導致失敗：

- 問題包含多個部分
- 資訊分散在多份文件中
- 直觀的搜尋詞彙與文件用語不一致

### 解決方案：代理式檢索對搜尋進行推理

代理程式的行為就像一位知識豐富的員工：

1. 理解問題的真正意圖
2. 知道要查閱多個來源
3. 調和互相矛盾的資訊
4. 在找不到答案時坦然承認

## 客戶對話要點

| 問題 | 回應 |
|------|------|
| 「為什麼不直接用搜尋？」 | 「搜尋找到的是文件。代理式檢索找到的是答案——而且知道何時需要查閱多個來源。」 |
| 「幻覺問題怎麼辦？」 | 「每個回應都引用特定文件。使用者可以點擊連結進行驗證。代理程式會說『我不知道』而非猜測。」 |
| 「能處理我們複雜的政策嗎？」 | 「規劃-迭代-反思方法能處理多部分的政策。讓我用這個範例為您展示⋯⋯」 |

## 技術細節

### 文件處理管線

```
PDFs/Word/PPT → Text Extraction → Chunking → Embedding → Vector Index
```

- **分塊**：保留句子邊界，通常 500-1000 個 token
- **向量嵌入**：Azure OpenAI text-embedding-3-large（3072 維度）
- **索引**：Azure AI Search 搭配混合式（關鍵字 + 向量）檢索

### 搜尋設定

```python
# Hybrid search combines:
# 1. Vector similarity (semantic meaning)
# 2. Keyword matching (exact terms)
# 3. Semantic ranking (re-ranking for relevance)

query_type = "vectorSemanticHybrid"
```

---

[← 概觀](index.md) | [Fabric IQ：資料 →](02-fabric-iq.md)
