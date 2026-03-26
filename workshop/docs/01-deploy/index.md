# 部署解決方案

本節是讓範例情境端到端運作的入口。

這一節只要先做兩件事：選對起點，完成那條路徑需要的最少步驟。

## 選擇適合你的起點

如果你只想先決定自己該看哪一頁，先看下面這張表。

| 你現在要做什麼 | 直接去看 |
|------------------|------------|
| 自己部署 Azure 與 Fabric | [管理員部署](00-admin-deploy-share.md) |
| 環境已準備好，只要執行與驗證 | [參與者執行與驗證](00-participant-run-validate.md) |

### 管理員部署

如果你想自己把整套 Azure 與 Fabric 環境準備完成，請走這條路徑。

你將會：

- 使用 `azd up` 部署 Azure 資源
- 建立或選擇 Fabric 工作區
- 完成 Fabric 詳細設定檢查
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

| 情境 | 典型操作 | Azure 權限重點 | 明確需要的權限 |
|------|----------|----------------|------------------|
| **學員只要跑 workshop** | 登入、設定本機 `.env`、驗證既有情境、測試 agent | 只需要使用既有環境，不需要負責部署或 RBAC 指派 | `Azure AI User` |
| **管理員要能部署** | 執行 `azd up`、建立資源、建立 RBAC 指派、整理共用環境 | 需要同時具備「建立 / 更新資源」與「建立角色指派」兩類能力 | `Owner`，或 `Contributor` + `User Access Administrator`，或 `Contributor` + `Role Based Access Control Administrator` |

補充判斷方式：

- 如果環境已經有人幫你準備好，而你只需要登入並執行範例，請走「參與者執行與驗證」
- 如果你要從零佈建 Azure 資源，或要幫別人準備可重複使用的環境，請走「管理員部署」

官方文件：

- `Azure AI User` 角色說明：<https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles>
- `Azure AI User` 內建角色定義：<https://learn.microsoft.com/azure/role-based-access-control/built-in-roles/ai-machine-learning#azure-ai-user>
- 管理員替學員授與 `Azure AI User` 的官方步驟：<https://learn.microsoft.com/azure/foundry/tutorials/quickstart-create-foundry-resources#for-administrators---grant-access>
- 用 Azure Portal 指派 RBAC 角色的官方步驟：<https://learn.microsoft.com/azure/role-based-access-control/role-assignments-portal>
- 可授與角色的管理員權限說明：<https://learn.microsoft.com/azure/role-based-access-control/role-assignments-portal#prerequisites>

## 架構

![Architecture Diagram](../assets/architecture.png)

這張圖的目的不是要你先背架構，而是讓你知道主流程背後主要依賴哪些能力。

第一次看時，只要先記住：

- Microsoft Foundry 負責模型與 agent
- Azure AI Search 負責文件搜尋
- Microsoft Fabric 負責資料層
- Application Insights 是選配追蹤能力

如果你想理解更多技術拆解，再回頭看 [深入解析](../03-understand/index.md)。

---

[← 快速開始](../00-get-started/index.md) | [管理員部署 →](00-admin-deploy-share.md)
