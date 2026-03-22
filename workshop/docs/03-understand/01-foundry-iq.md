# Foundry IQ：文件智慧

## 概要

Foundry IQ 這一頁講的是「文件怎麼變成可以被 agent 查詢的知識」。

在這個工作坊裡，流程很直接：

1. 把文件整理成可搜尋內容
2. 上傳到 Azure AI Search
3. agent 在需要時呼叫 `search_documents`
4. 再把找到的段落整理成答案

## 這頁要學什麼

看完這頁，你應該知道：

- 文件是怎麼被放進搜尋系統的
- agent 什麼時候會去查文件
- 為什麼最後的回答可以帶出來源資訊

## 主要功能

| 功能 | 你可以怎麼理解 |
|------|----------------|
| 文件索引 | 把文件內容整理後放進 Azure AI Search |
| 引用段落 | 搜尋結果會附上來源、標題、頁碼 |
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
│  • 將內容片段上傳到 Azure AI Search                         │
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
│  本機執行階段以語意搜尋呼叫 Azure AI Search                  │
│  並回傳 source/title/page metadata                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 4：整理回答                                            │
│  Agent 讀取回傳段落後                                       │
│  以 grounded wording 與可見 citation metadata 形成答案       │
└─────────────────────────────────────────────────────────────┘
```

## 為什麼這條路徑重要

因為很多企業問題不是在資料表裡，而是在文件裡，例如：

- 政策
- 作業流程
- 例外處理規則
- FAQ

如果 agent 只會查資料、不會查文件，就很難回答這類問題。

## 你應該記住的重點

這個工作坊不是把文件直接塞給模型，而是先透過 Azure AI Search 建立可搜尋的知識層，再讓 agent 在需要時查詢。這樣比較透明，也比較容易驗證答案來源。

## 先記住這三件事

1. 文件不是直接貼給模型，而是先進入可搜尋的知識層
2. agent 需要時才會呼叫文件工具，不是每題都先做搜尋
3. 文件答案保留來源與頁碼，所以比較容易人工驗證

## 文件處理管線

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

## 官方延伸閱讀

- [Vector search in Azure AI Search](https://learn.microsoft.com/azure/search/vector-search-overview)
- [Quickstart: Vector search](https://learn.microsoft.com/azure/search/search-get-started-vector)
- [Connect an Azure AI Search index to Foundry agents](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/ai-search)

---

[← 概觀](index.md) | [Fabric IQ：資料 →](02-fabric-iq.md)
