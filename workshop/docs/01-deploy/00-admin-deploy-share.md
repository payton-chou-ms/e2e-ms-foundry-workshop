# 管理員部署與分享

當一個人或團隊負責部署方案並為其他人準備環境時，請走這條路徑。

## 適用對象

- 平台管理員
- 方案負責人
- Workshop 主持人
- 準備可重複使用 demo 環境的技術銷售人員

## 這條路徑涵蓋的內容

1. 部署 Azure 資源。
2. 建立或選擇 Fabric 工作區。
3. 設定共用環境。
4. 執行範例情境一次。
5. 將準備好的環境分享給操作者或參與者。

## 開始之前

請確認你具備：

- 訂用帳戶與資源群組的 Azure 部署權限。
- 如果使用提供的 Bicep 範本，需要建立 Azure 角色指派的權限。
- Fabric 工作區管理員或同等撰寫權限。
- 所選 Azure 區域的必要模型容量與配額。

!!! warning "Contributor 可能不足"
    基礎架構會建立 Azure RBAC 角色指派。
    在許多訂用帳戶中，部署身分需要 `Owner`、`User Access Administrator`，或其他包含 `Microsoft.Authorization/roleAssignments/write` 的角色。

## 建議執行順序

### 1. 部署 Azure 資源

請依照 [部署 Azure 資源](01-deploy-azure.md) 操作。

### 2. 建立或選擇 Fabric 工作區

請依照 [建立 Fabric 工作區](02-setup-fabric.md) 操作。

### 3. 設定共用環境

請依照 [設定開發環境](03-configure.md) 操作。

在這個階段，記下後續使用者需要的值，特別是：

- `FABRIC_WORKSPACE_ID`
- 你希望參與者重複使用的環境命名慣例
- 應授予 Azure 和 Fabric 存取權的身分或群組

### 4. 建置並驗證預設情境

請依照 [建置解決方案](04-run-scenario.md) 操作。

在分享之前先執行一次預設情境。這可以確認：

- Azure 資源運作正常
- Fabric 項目可以建立
- 文件已索引
- 協調代理程式能回答範例問題

### 5. 分享給參與者或操作者

目前的 repo 不會自動化所有協作步驟。在交接環境之前，請決定：

- 誰只能執行測試
- 誰可以重建資料或自訂情境
- 誰可以管理 Azure 資源與 Fabric 產物

最低交接清單：

- 授予所需使用者或群組 Azure 存取權。
- 授予所需使用者 Fabric 工作區存取權。
- 分享所需的本機設定值。
- 告知參與者是否只需驗證範例情境，還是也應執行自訂步驟。

## 應分享給下一位使用者的資訊

- Repository URL
- 預期的登入身分或租用戶
- `FABRIC_WORKSPACE_ID`
- 應從 [參與者執行與驗證](00-participant-run-validate.md) 開始，還是從後續自訂頁面開始

## 何時算是完成這條路徑

當另一位使用者可以開啟 repo、登入，並執行範例驗證流程而不需要重新部署 Azure 時，就算完成。

---

[← 部署總覽](index.md) | [參與者執行與驗證 →](00-participant-run-validate.md)
