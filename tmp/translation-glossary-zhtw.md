# translation-glossary-zhtw

## 目的

這份術語表用來統一本 repo 在繁體中文文件中的專有名詞、產品名稱與常用技術詞。

使用原則：

1. 產品正式名稱優先保留英文。
2. 一般技術概念可翻譯，但首次出現可採「中文（英文）」。
3. 同一個詞在全站只使用一種主要譯法，避免混用。
4. 指令、環境變數、檔名、API 名稱、SDK 類別名一律不翻。

## 優先用語

| 英文 | 建議繁中 | 使用規則 |
| --- | --- | --- |
| Azure | Azure | 產品名稱不翻 |
| Azure AI Foundry | Azure AI Foundry | 產品正式名稱不翻 |
| Microsoft Fabric | Microsoft Fabric | 產品正式名稱不翻 |
| Foundry IQ | Foundry IQ | 功能名稱不翻 |
| Fabric IQ | Fabric IQ | 功能名稱不翻 |
| Azure AI Search | Azure AI Search | 產品正式名稱不翻 |
| Azure AI Services | Azure AI Services | 產品正式名稱不翻 |
| Application Insights | Application Insights | 產品正式名稱不翻 |
| GitHub Codespaces | GitHub Codespaces | 產品正式名稱不翻 |
| VS Code | VS Code | 產品名稱不翻 |
| Azure Developer CLI | Azure Developer CLI | 首次可寫 Azure Developer CLI（azd） |
| azd | azd | 指令名稱不翻 |
| ontology | 本體 | 首次可寫 本體（ontology） |
| business ontology | 商業本體 | 若語境強調 Fabric IQ，可首次寫 商業本體（business ontology） |
| workspace | 工作區 | 用於一般說明；若是產品 UI 名稱可保留 Workspace |
| Fabric workspace | Fabric 工作區 | 產品名稱保留，通用名詞翻譯 |
| deployment | 部署 | 動詞 deploy 可譯為 部署 |
| deploy | 部署 | 指文件敘述時翻譯；CLI 指令不翻 |
| share | 分享 | 用於分享環境、分享給參與者 |
| participant | 參與者 | 用於 workshop 角色 |
| operator | 操作者 | 用於負責執行腳本的人 |
| admin | 管理員 | 若是 Azure admin / platform admin 依上下文補前綴 |
| lakehouse | Lakehouse | 專有概念建議保留英文 |
| warehouse | Warehouse | 專有概念建議保留英文 |
| semantic search | 語意搜尋 | 技術概念可翻 |
| embeddings | 向量嵌入 | 若語境偏模型可首次寫 向量嵌入（embeddings） |
| vector index | 向量索引 | 技術概念可翻 |
| agent | 代理程式 | 一般技術敘述用；若是產品功能名稱可保留 Agent |
| orchestrator agent | 協調代理程式 | 首次可寫 協調代理程式（Orchestrator Agent） |
| data agent | 資料代理程式 | 首次可寫 資料代理程式（Data Agent） |
| natural language query | 自然語言查詢 | 技術概念可翻 |
| prompt | 提示詞 | 若語境偏 Prompt Engineering 可保留 prompt |
| schema | 結構描述 | 可依上下文簡化為 schema |
| sample scenario | 範例情境 | 文件內固定用法 |
| use case | 使用案例 | 固定用法 |
| quick start | 快速開始 | 標題可直接翻 |
| troubleshooting | 疑難排解 | 標題固定用法 |
| cleanup | 清理 | 標題可譯為 清理資源 或 清理 |
| source of truth | 唯一內容來源 | 文件治理用語 |
| generated artifact | 產生物 | 也可依語境寫 建置產物 |
| build output | 建置輸出 | 與產生物區分時使用 |
| path | 路徑 | 文件中的使用流程路徑也可譯為 路徑 |

## 固定不翻項目

以下內容一律保持原文：

1. 指令與參數
2. 檔名、資料夾名稱、路徑
3. 環境變數
4. API 路徑
5. SDK 類別名稱與程式碼符號
6. 連結 URL

示例：

- `azd up`
- `FABRIC_WORKSPACE_ID`
- `workshop/docs/01-deploy/04-run-scenario.md`
- `DefaultAzureCredential`

## 建議譯法偏好

### 優先保留英文

- Azure AI Foundry
- Microsoft Fabric
- Foundry IQ
- Fabric IQ
- Lakehouse
- Warehouse
- Agent

### 優先翻譯為中文

- deployment → 部署
- participant → 參與者
- troubleshooting → 疑難排解
- permissions → 權限
- prerequisites → 先決條件
- cleanup → 清理

## 常見混用提醒

| 不建議混用 | 建議統一 |
| --- | --- |
| 工作空間 / 工作區 | 工作區 |
| 語義搜尋 / 語意搜尋 | 語意搜尋 |
| 向量化 / 嵌入 / embedding | 依上下文區分，預設用 向量嵌入 |
| 部署資源 / 佈署資源 | 部署資源 |
| 代理 / 代理人 / agent | 預設用 代理程式，必要時保留 Agent |

## 後續維護規則

1. 新術語先加到這份文件，再開始大量翻譯。
2. 若同一術語因產品正式名稱與一般敘述需不同譯法，請在此文件補充使用條件。
3. reviewer 看到新詞時，先回到這份文件確認，不要在單篇文件內自行決定。