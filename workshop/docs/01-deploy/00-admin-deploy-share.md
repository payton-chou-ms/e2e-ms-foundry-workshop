# 自行部署並準備環境

如果你想自己把整套 workshop 環境準備完成，再交給其他學員或之後的自己重複使用，請走這條路徑。

## 什麼情況適合走這條路徑

- 你想從零開始部署 Azure 資源
- 你想自己建立或選擇 Fabric 工作區
- 你想整理出一套可重複使用的 workshop 環境

如果你想先快速判斷自己是否需要 Azure 部署權限，先看 [部署總覽中的 Azure 權限對照](index.md#azure-permissions)。

## 這條路徑涵蓋的內容

1. 部署 Azure 資源
2. 建立或選擇 Fabric 工作區
3. 設定共用環境
4. 執行範例情境一次
5. 將準備好的環境提供給其他學員，或留給自己後續重複使用

## 開始之前

請確認你具備：

- 目標資源群組（或其上層 scope）的 Azure 資源建立權限
- 目標資源群組（或其上層 scope）的 Azure 角色指派建立權限
- Fabric 工作區管理員或同等撰寫權限
- 所選 Azure 區域的必要模型容量與配額

## 建議執行順序

### 1. 部署 Azure 資源

請依照 [部署 Azure 資源](01-deploy-azure.md) 操作。

### 2. 建立或選擇 Fabric 工作區

請依照 [建立 Fabric 工作區](02-setup-fabric.md) 操作。

如果你要把這套環境交給其他學員或下次的自己重複使用，請再補看 [Fabric 詳細設定](fabric/workspace-settings.md)，把 workspace access、`FABRIC_WORKSPACE_ID`、執行身分與 ontology 可用性一次整理清楚。

### 3. 設定共用環境

請依照 [設定開發環境](03-configure.md) 操作。

在這個階段，記下後續操作還會用到的值，特別是：

- `FABRIC_WORKSPACE_ID`
- Fabric workspace URL
- 你希望後續重複使用的環境命名慣例
- 需要 Azure 和 Fabric 存取權的身分或群組

### 4. 建置並驗證預設情境

如果你要先把共享環境一次準備好，建議直接執行：

```bash
python scripts/admin_prepare_shared_demo.py
```

這支 wrapper 會依序完成：

- `default` scenario 的 preload
- 文件問答的 search-only 準備
- 文件問答的 Foundry-native IQ 準備

如果你想分開理解每一條路徑，再回頭看 [建置與驗證解決方案](04-run-scenario.md)。

在分享之前先執行一次預設情境。這可以確認：

- Azure 資源運作正常
- Fabric 項目可以建立
- 文件已索引
- 協調代理程式能回答範例問題

### 5. 整理給後續使用者

環境建好之後，建議你先把「下一位使用者到底要做什麼」講清楚。

最常見的差別其實只有三種：

- 誰只需要執行測試
- 誰需要重建資料或自訂情境
- 誰需要管理 Azure 資源與 Fabric 產物

在你把環境交出去之前，至少先整理好下面這些項目：

- 授予所需使用者或群組 Azure 存取權
- 授予所需使用者 Fabric 工作區存取權
- 分享所需的本機設定值
- 告知下一位使用者是只需驗證範例情境，還是也要執行自訂步驟

#### 學員的 Data Plane 權限

如果下一位使用者不只是登入 portal，而是要實際跑 agent、查 Search 或直接讀寫 Blob，還要補上資料平面權限。

| 要做的事 | 建議最小權限 | 建議範圍 |
|------|---------------|----------|
| 跑既有 agent、驗證文件/資料查詢 | `Azure AI User` | Foundry account 或 project 上層資源 |
| 查詢既有 Azure AI Search index | `Search Index Data Reader` | Search service 或單一 index |
| 重跑文件上傳，但不改 index 結構 | `Search Index Data Contributor` | Search service 或單一 index |
| 建立 / 更新 index、indexer、skillset | `Search Service Contributor` | Search service |
| 讀既有 Blob 內容 | `Storage Blob Data Reader` | Storage account 或單一 container |
| 上傳 / 覆寫 / 刪除 Blob | `Storage Blob Data Contributor` | Storage account 或單一 container |

建議做法：

- 只走參與者驗證路徑時，先給 `Azure AI User`，必要時再補 `Search Index Data Reader` 與 `Storage Blob Data Reader`
- 要重跑資料準備或知識建置流程時，再補 `Search Service Contributor`、`Search Index Data Contributor`、`Storage Blob Data Contributor`
- 要走 Fabric 路徑時，另外還要確認 Fabric workspace role 是否足夠

官方文件：

- Foundry authentication / authorization：<https://learn.microsoft.com/azure/foundry/concepts/authentication-authorization-foundry>
- Foundry built-in roles：<https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry>
- Azure AI Search RBAC：<https://learn.microsoft.com/azure/search/search-security-rbac>
- Blob 以 Microsoft Entra ID 授權：<https://learn.microsoft.com/azure/storage/blobs/authorize-access-azure-active-directory>
- Fabric workspace roles：<https://learn.microsoft.com/fabric/fundamentals/roles-workspaces>

## 建議保留給下一次操作的資訊

下次不管是你自己回來接手，還是換另一位學員接手，至少要留下面這些資訊：

- 專案來源位置或網址
- 預期的登入身分或租用戶
- `FABRIC_WORKSPACE_ID`
- 應從 [參與者執行與驗證](00-participant-run-validate.md) 開始，還是從後續自訂頁面開始

## 何時算是完成這條路徑

當你或另一位學員可以直接開啟專案、登入、完成範例驗證，而且不需要重新部署 Azure，這條路徑就算完成

---

[← 部署總覽](index.md) | [部署 Azure 資源 →](01-deploy-azure.md)
