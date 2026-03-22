# 部署解決方案

本節是讓範例情境端到端運作的入口。

如果你現在的目標只是把 workshop 跑通，這一節最重要的工作只有兩件事：選對你的起點，然後完成那條路徑需要的最少步驟。

## 選擇適合你的起點

### 管理員部署

如果你想自己把整套 Azure 與 Fabric 環境準備完成，請走這條路徑。

你將會：

- 使用 `azd up` 部署 Azure 資源
- 建立或選擇 Fabric 工作區
- 設定共用環境
- 確認後續使用這套環境的人需要哪些存取權限
- 整理出一個可直接使用的環境

[前往管理員部署](00-admin-deploy-share.md)

### 參與者執行與驗證

如果 Azure 資源和 Fabric 工作區已經為你準備好，請走這條路徑。

你將會：

- 開啟 repo 並使用指定身分登入
- 設定本機組態
- 執行範例情境
- 測試協調代理程式（Orchestrator Agent）並驗證輸出

[前往參與者執行與驗證](00-participant-run-validate.md)

## Azure 權限對照 { #azure-permissions }

如果你只想跑通 workshop，和如果你要負責部署整套環境，所需的 Azure 權限層級並不一樣。

先用最簡單的方式判斷：

- 你只需要登入、設定 `.env`、跑範例，通常就是學員路徑
- 你需要建立 Azure 資源或幫別人準備共用環境，才是管理員路徑

| 情境 | 典型操作 | Azure 權限重點 | 明確不需要的權限 | 什麼時候代表你不屬於這條路徑 |
|------|----------|----------------|------------------|------------------------------|
| **學員只要跑 workshop** | 登入、設定本機 `.env`、驗證既有情境、測試 agent | 需要已被授予現成環境的存取權，並能登入正確租用戶與使用既有 Azure 資源 | 不需要 `Owner`、不需要 `Contributor`、不需要 `User Access Administrator`、不需要 `Role Based Access Control Administrator`、不需要 `Microsoft.Authorization/roleAssignments/write` | 如果你要自己跑 `azd up`、重建角色指派、建立新的 Azure 資源，或替其他人開權限，就不再是這條路徑 |
| **管理員要能部署** | 執行 `azd up`、建立資源、建立 RBAC 指派、整理共用環境 | 需要同時具備「資源建立 / 更新」與「角色指派建立」兩類權限。最直接是 `Owner`；較常見的最小組合是 `Contributor` + `User Access Administrator`，或 `Contributor` + `Role Based Access Control Administrator` | 不適合只有 `Contributor` 單獨使用 | 如果你無法建立 Azure 資源，或無法在目標 scope 建立角色指派，部署通常會在 Bicep 建立 RBAC 時失敗 |

補充判斷方式：

- 如果環境已經有人幫你準備好，而你只需要登入並執行範例，請走「參與者執行與驗證」
- 如果你要從零佈建 Azure 資源，或要幫別人準備可重複使用的環境，請走「管理員部署」

## 架構

![Architecture Diagram](../assets/architecture.png)

這張圖的目的不是要你在部署前把所有元件背起來，而是幫你知道前面跑通的主流程，背後大致依賴哪些能力。

第一次看時，只要先分成兩層理解就夠了：

### Workshop 主流程

- Foundry 中的提示詞代理程式（prompt agent）
- 用於結構化資料的 SQL 工具
- 用於非結構化知識的文件搜尋工具
- Foundry IQ 與 Fabric IQ 作為兩條資料接地路徑

### 主流程背後的六個技術主題

| 主軸 | 部署意義 |
|------|----------|
| **Foundry Model** | 主流程需要哪些模型，哪些只是延伸選配 |
| **Foundry Agent** | agent 定義怎麼被建立並在後續測試中重複使用 |
| **Foundry Tool** | 主流程依賴哪些工具，以及它們怎麼被限制在安全範圍內 |
| **Foundry IQ + Fabric IQ** | 文件與資料如何成為回答問題的依據 |
| **Foundry Control Plane** | 背後有哪些 Azure 資源在支撐整個體驗 |
| **多代理程式延伸** | 主線看懂後，如何再延伸成多角色工作流 |

換句話說，你前面操作時看到的是一個簡潔的對話式 PoC；這張圖只是幫你知道，背後有哪些主要能力在支撐它。

- **Microsoft Fabric** 提供資料層，讓 agent 可以回答結構化資料問題
- **Microsoft Foundry** 負責保存 agent 定義與模型部署
- **Azure AI Search** 提供文件搜尋與片段擷取能力
- **Application Insights** 在需要時可接收追蹤資料，但不是主流程必要條件

!!! tip "卡住了？問 Copilot"
    使用 GitHub Copilot Chat（`Ctrl+I`）協助排除錯誤

!!! note "唯一內容來源"
    這個 MkDocs 站台就是 workshop 的正式文件
    產生的 PDF 與站台輸出為次要產物

---

[← 快速開始](../00-get-started/workshop-flow.md) | [管理員部署 →](00-admin-deploy-share.md)
