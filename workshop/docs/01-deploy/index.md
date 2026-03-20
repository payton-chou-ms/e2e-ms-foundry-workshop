# 部署解決方案

本節是讓範例情境端到端運作的入口。

部署路徑聚焦在讓 PoC 能正常運作所需的最低限度，但你所部署的架構已支援 Deep Dive 章節中更完整的六個技術主題。

## 選擇適合你的起點

### 管理員部署與分享

如果你想自己把整套 Azure 與 Fabric 環境準備完成，請走這條路徑。

你將會：

- 使用 `azd up` 部署 Azure 資源
- 建立或選擇 Fabric 工作區
- 設定共用環境
- 確認後續使用這套環境的人需要哪些存取權限
- 整理出一個可直接使用的環境

[前往管理員部署與分享](00-admin-deploy-share.md)

### 參與者執行與驗證

如果 Azure 資源和 Fabric 工作區已經為你準備好，請走這條路徑。

你將會：

- 開啟 repo 並使用指定身分登入
- 設定本機組態
- 執行範例情境
- 測試協調代理程式（Orchestrator Agent）並驗證輸出

[前往參與者執行與驗證](00-participant-run-validate.md)

## 架構

![Architecture Diagram](../assets/architecture.png)

本方案結合 Microsoft Fabric 與 Microsoft Foundry，建構一個可同時使用結構化資料與非結構化文件回答問題的 AI 解決方案。

學習這一段時，可以用兩個層次來理解：

### Workshop 主流程

- Foundry 中的提示詞代理程式（prompt agent）
- 用於結構化資料的 SQL 工具
- 用於非結構化知識的文件搜尋工具
- Foundry IQ 與 Fabric IQ 作為兩條資料接地路徑

### 主流程背後的六個技術主題

| 主軸 | 部署意義 |
|------|----------|
| **Foundry Model** | 必要的 chat + embedding 部署，選配模型擴充另外保持獨立 |
| **Foundry Agent** | 在專案範圍內建立代理程式定義，並在執行時重複使用 |
| **Foundry Tool** | 執行時依賴嚴格的 SQL + 搜尋函式工具合約 |
| **Foundry IQ + Fabric IQ** | Search 與 Fabric 資源為代理程式提供文件與資料接地 |
| **Foundry Control Plane** | Azure AI Services、Foundry 專案、Search、Storage、遙測與 RBAC 串連整個環境 |
| **Multi-Agent Extension** | 重用同一套模型、工具與接地能力，往後延伸成情境化工作流 |

換言之，你在前面操作時看到的會是一個簡潔的對話式 PoC，但部署背後其實已準備好完整的技術骨架。

- **Microsoft Fabric** 提供資料層，包括 Lakehouse、Warehouse，以及 Fabric IQ 語意層的自然語言轉 SQL
- **Microsoft Foundry** 託管提示詞代理程式、工具合約，以及 Foundry IQ 文件擷取
- **Azure AI Services** 驅動 workshop 使用的 chat 與 embedding 模型部署
- **Azure AI Search** 儲存文件向量以供語意擷取
- **Application Insights** 在啟用可觀測性時可選擇性接收追蹤資料

!!! tip "卡住了？問 Copilot"
    使用 GitHub Copilot Chat（`Ctrl+I`）協助排除錯誤。

!!! note "唯一內容來源"
    這個 MkDocs 站台就是 workshop 的正式文件。
    產生的 PDF 與站台輸出為次要產物。

---

[← 快速開始](../00-get-started/workshop-flow.md) | [管理員部署與分享 →](00-admin-deploy-share.md)
