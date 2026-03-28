# 快速開始與 Workshop 流程

這一頁只先幫你完成兩件事：

1. 確認你已具備 workshop 的最小前置條件
2. 先理解整體學習順序，知道該從哪一條路徑開始

## 先決條件

- 具備 Contributor 權限的 Azure subscription
- `gpt-5.4-mini` 與 `text-embedding-3-large` 的模型容量
- Microsoft Fabric 工作區（只有要延伸到 Fabric 附錄時才需要）
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

請先在你的本機環境、訓練環境或既有的開發容器中開啟這份 workshop 專案，再依照本頁與後續章節完成設定。

!!! tip "使用 GitHub Copilot 尋求協助"
    如果卡在某個步驟，可以詢問 GitHub Copilot Chat：

    - "Explain this error message"
    - "What does this script do?"
    - "How do I fix this Python error?"

    在 VS Code 中按 `Ctrl+I` 可開啟 Copilot Chat

## Workshop 流程

第一次閱讀時，只要先分清楚「先跑通、再自訂、再理解、最後清理」就夠了。

### Step 1：部署方案

請先從以下兩條路徑中擇一開始。兩條都先以 Foundry 主線為主，不需要先做 Fabric：

| 路徑 | 適用情境 | 主要頁面 |
|------|----------|----------|
| **管理員部署** | 你想自己把 Azure 與 Foundry 主線先準備完成 | [管理員部署](../01-deploy/00-admin-deploy-share.md) |
| **學員執行與驗證** | 你已拿到現成環境，只需要執行範例情境與驗證代理程式 | [學員執行與驗證](../01-deploy/00-participant-run-validate.md) |

這兩條路徑最終都會收斂到同一套 Foundry 驗證步驟。

完整部署路徑包含：

- 準備支撐 workshop 的 Azure 資源，包括 Foundry project、模型部署、AI Search、Storage、Application Insights，以及選配的 image OpenAI 與 Playwright Workspace
- 設定開發環境
- 讓代理程式對範例資料實際運作
- 約需 15 分鐘

如果你負責管理員部署，建議先把 Foundry 主線跑通。Fabric 相關設定與驗證已移到 [附錄：Fabric 延伸](../05-appendix/index.md)，等主線完成後再回頭補即可。

可以先把它理解成兩階段：

1. 先完成 Foundry path：文件問答、agent 建立、驗證
2. 之後若有需要，再補 Fabric path：資料問答、Lakehouse、Ontology、SQL grounding

### Step 2：依使用案例自訂

這一步是把預設情境換成更貼近你示範目標的內容。你可以把它理解成「把主流程保留，但把資料、文件與問題換成你的版本」。

| 產業 | 使用案例範例 | 示範問題 |
|----------|--------------|----------|
| 電信 | 網路中斷 + 服務政策 | "哪些 outage 超過我們的 SLA 門檻？" |
| 製造 | 設備資料 + 維護文件 | "哪些機台依照維護排程已經逾期？" |
| 零售 | 產品目錄 + 退貨政策 | "超過 500 美元的電子產品退貨政策是什麼？" |
| 金融 | 帳戶資料 + 放款政策 | "哪些貸款申請符合我們的核准條件？" |
| 保險 | 理賠資料 + 保單文件 | "本週提出的理賠案件，相對於 SLA 目前狀態如何？" |
| 能源 | 電網監控 + 安全規範 | "哪些變電站目前運作容量超過 80%？" |
| **你的情境** | **你的資料 + 你的文件** | **你最想先驗證的問題** |

!!! tip "PoC 前準備"
    在 PoC 前先執行 Step 2。輸入產業與簡短的使用案例描述後，AI 會依照你的情境產生更貼近實際的範例資料、文件與測試問題

!!! note "單一文件來源"
    請以 `workshop/docs/` 底下的頁面作為目前有效的操作說明
    `guides/` 與 PDF 輸出屬於發佈產生物，內容可能較精簡

### Step 3：深入解析

如果你想知道這個 PoC 背後到底是怎麼運作的，就從這一段開始。你會在這裡把主流程拆回幾個核心學習面向：

- **Foundry Model**：這個 workshop 目前用了哪些模型，哪些是主線必要，哪些是選配延伸
- **Foundry Agent**：代理程式定義存在哪裡，建立後又是怎麼被重複使用
- **Foundry Tool**：`execute_sql` 和 `search_documents` 各自負責什麼，工具邊界怎麼控制
- **Foundry IQ**：文件怎麼進 Azure AI Search，agent 又怎麼取回可引用的段落
- **Fabric IQ**：資料表、schema 與 prompt 怎麼把商業問題轉成唯讀 SQL（等主線跑通後再看附錄）
- **Foundry Control Plane**：哪些 Azure 資源在背後支撐整個體驗

如果你之後還想把這個單一 agent 的 PoC 延伸成多角色 workflow，再接著看 **多代理程式延伸**。

---

[部署方案 →](../01-deploy/index.md)
