# Foundry IQ：文件智慧

## 概要

Foundry IQ 這一頁講的是「文件怎麼變成可以被 agent 查詢的知識」。

如果用 Microsoft 官方文件的語言來說，Foundry IQ 的核心價值不是「把 PDF 丟進模型」，而是先建立一層**可檢索、可引用、可治理的 knowledge layer**，再讓 agent 用這層知識來回答問題。

在這個工作坊裡，我們用比較容易看懂的方式把這個概念拆開：

1. 把文件整理成可搜尋內容
2. 上傳到 Azure AI Search
3. agent 在需要時呼叫 `search_documents`
4. 再把找到的段落整理成答案

所以你可以把這頁理解成兩層：

1. **官網層的 Foundry IQ 重點**：grounding、citations、knowledge layer、retrieval
2. **workshop 的實作層**：Azure AI Search + 本機 `search_documents` 工具

## 這頁要學什麼

看完這頁，你應該知道：

- 官網所說的 Foundry IQ 到底在解什麼問題
- 文件是怎麼被放進搜尋系統的
- agent 什麼時候會去查文件
- 為什麼最後的回答可以帶出來源資訊

## 先抓住官網的四個核心重點

Microsoft 官方文件裡，Foundry IQ / 文件型 grounding 最值得記住的其實只有四件事：

| 重點 | 用白話怎麼理解 |
|------|----------------|
| **Grounding** | 不是讓模型自由發揮，而是先拿回和問題相關的企業內容，再據此回答 |
| **Citations** | 回答不只要像真的，還要能指出來源、標題、頁碼或 URL |
| **Retrieval layer** | 文件先進入一個可搜尋的知識層，而不是每次都把整份文件直接塞進 prompt |
| **Search quality** | 好不好用，不只看模型，也看 chunking、vector search、hybrid search、semantic ranking |

## 這頁在 workshop 裡對應什麼

官方語境下，Foundry IQ 比較接近一個「給 agent 使用的知識檢索層」。

而在這個 workshop 中，我們目前採用的是比較透明、比較適合教學的做法：

- 用 Azure AI Search 當文件知識層
- 用 `search_documents` 當 agent 的文件檢索工具
- 由本機 runtime 直接執行搜尋並回傳來源 metadata

這代表：

1. **概念上**，這一頁講的是 Foundry IQ 的核心能力
2. **實作上**，這個 workshop 主要示範的是 Azure AI Search 支撐的 classic RAG / grounded retrieval 路徑

## 官網為什麼一直強調 Azure AI Search

因為在官方架構裡，Azure AI Search 很常扮演 RAG 或 Foundry IQ 背後的檢索層。它的關鍵能力包括：

- **vector search**：讓語意相近但字面不同的內容也能被找到
- **hybrid search**：把 keyword search 和 vector search 同時跑，再合併排序
- **semantic ranking**：在取回結果後再做語意重排，提升前幾筆結果品質
- **metadata retrieval**：讓回傳結果不只是內容片段，還帶來源與引用資訊

對 workshop 來說，這些能力最重要的意義不是名詞本身，而是：

1. 你問「停機通知政策」時，不必完全打中 PDF 原文
2. agent 回答時可以附上來源與頁碼
3. 文件型問答比較容易人工驗證

## 主要功能

| 功能 | 你可以怎麼理解 |
|------|----------------|
| 文件索引 | 把文件內容整理後放進 Azure AI Search |
| Grounded retrieval | 問題來時，不是直接猜答案，而是先檢索相關內容 |
| 引用段落 | 搜尋結果會附上來源、標題、頁碼 |
| Search quality | 可結合 vector、hybrid 與 semantic search 改善召回與排序 |
| Microsoft Entra ID 驗證 | 腳本可用 Azure 身分呼叫 Search 與 Foundry |
| 多格式支援 | PDF、Word、PowerPoint 與一般文字都能處理 |

## 文件路徑怎麼運作

```
使用者：「長時間 outage 時，我們通知客戶的政策是什麼？」

┌─────────────────────────────────────────────────────────────┐
│  Step 1：匯入                                                │
│  Workshop 腳本：                                            │
│  • 從 PDF 擷取文字                                          │
│  • 依句子切塊                                               │
│  • 產生向量嵌入                                             │
│  • 將內容片段與 metadata 上傳到 Azure AI Search             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2：工具呼叫                                            │
│  Agent 判斷這個問題需要文件證據                             │
│  並發出 `search_documents(query=...)`                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3：搜尋                                                │
│  本機執行階段呼叫 Azure AI Search                            │
│  並回傳 content + source/title/page metadata                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 4：整理回答                                            │
│  Agent 讀取回傳段落後                                       │
│  以 grounded wording 與可見 citation metadata 形成答案       │
└─────────────────────────────────────────────────────────────┘
```

這張圖對照官網概念時，可以簡化成一句話：

- **Foundry IQ 的價值在於，先把知識檢索做好，再把 grounding 結果交給 agent 組答案。**

## 為什麼這條路徑重要

因為很多企業問題不是在資料表裡，而是在文件裡，例如：

- 政策
- 作業流程
- 例外處理規則
- FAQ

如果 agent 只會查資料、不會查文件，就很難回答這類問題。

## 你應該記住的重點

這個工作坊不是把文件直接塞給模型，而是先透過 Azure AI Search 建立可搜尋的知識層，再讓 agent 在需要時查詢。這樣比較透明，也比較容易驗證答案來源。

這也正是官方 Foundry IQ / RAG 文件一直在強調的核心：

1. **知識要先被整理成可檢索的形態**
2. **檢索結果要能附帶 citation**
3. **回答品質很大一部分來自 retrieval quality，而不是只靠模型本身**

## 先記住這三件事

1. 文件不是直接貼給模型，而是先進入可搜尋的知識層
2. agent 需要時才會呼叫文件工具，不是每題都先做搜尋
3. 文件答案保留來源與頁碼，所以比較容易人工驗證

## 官方觀點下，Foundry IQ 和 classic RAG 有什麼關係

官方文件現在把文件型 grounding 大致看成兩種路徑：

| 路徑 | 你可以怎麼理解 |
|------|----------------|
| **Foundry IQ / agentic retrieval** | 更高階、對 agent 更友善的 knowledge retrieval 體驗 |
| **classic RAG** | 應用自己負責檢索編排，通常直接呼叫 Azure AI Search |

這個 workshop 比較接近後者：

- 由我們自己的腳本決定文件如何被切塊、上傳、搜尋
- `search_documents` 明確暴露檢索行為
- 你可以直接看到回傳的內容片段與 metadata

這樣做的優點是：

1. 教學上比較透明
2. 除錯時比較容易知道問題出在 indexing、retrieval 還是 agent reasoning
3. 比較容易讓學員理解 citation 是怎麼來的

## 文件處理管線

```
PDFs/Word/PPT → Text Extraction → Chunking → Embedding → Vector Index
```

- **分塊**：把大文件切成較小的可檢索片段，避免把整份文件一次塞給模型
- **向量嵌入**：Azure OpenAI text-embedding-3-large（3072 維度）
- **索引**：Azure AI Search index，包含內容、標題、來源、頁碼與向量欄位

官網語境下，這一段最重要的不是記 token 數，而是知道：

1. **chunking 影響召回品質**
2. **embedding 讓檢索不只看關鍵字**
3. **metadata 讓回答能附引用**

## 在官方架構裡，什麼會影響文件問答品質

如果把 Foundry IQ 的重點濃縮成實務判斷，大概就是下面四件事：

| 影響因素 | 為什麼重要 |
|----------|------------|
| **內容切塊** | chunk 太大會混雜主題，太小又會失去上下文 |
| **檢索策略** | keyword、vector、hybrid、semantic ranking 會直接影響召回品質 |
| **metadata 設計** | 沒有 title/source/page，citation 就會很弱 |
| **內容範圍** | 如果索引裡根本沒有對應內容，再好的模型也補不出正確答案 |

### 搜尋設定

```python
results = search_client.search(
    search_text=query,
    query_type="semantic",
    semantic_configuration_name="default-semantic",
    select=["content", "title", "source", "page_number"],
)
```

在 workshop 中，這段程式碼想表達的重點是：

1. 搜尋不是只回傳 `content`
2. 我們刻意把 `title`、`source`、`page_number` 一起帶回來
3. 這樣 agent 才能回答得 grounded，而且讓人有機會驗證來源

## 這一頁真正要帶走的結論

如果你只想記一句話，請記這句：

**Foundry IQ 的本質不是「讓模型讀文件」，而是「讓 agent 先拿回可信的文件證據，再用那些證據回答」。**

這個 workshop 雖然用的是比較透明的 Azure AI Search + local runtime 路徑，但它示範的正是同一個核心思想。

## 官方延伸閱讀

- [Retrieval-augmented generation (RAG) in Azure AI Search](https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview)
- [Vector search in Azure AI Search](https://learn.microsoft.com/azure/search/vector-search-overview)
- [Quickstart: Vector search](https://learn.microsoft.com/azure/search/search-get-started-vector)
- [Connect an Azure AI Search index to Foundry agents](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/ai-search)

---

[← 概觀](index.md) | [Fabric IQ：資料 →](02-fabric-iq.md)
