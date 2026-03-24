# 部署基礎架構

!!! info "主要適用對象"
    本頁主要供**管理員部署**路徑使用
    如果已有人為你準備好環境，請從 [參與者執行與驗證](00-participant-run-validate.md) 開始

如果你是第一次負責這條路徑，請把目標縮小成三件事：登入正確租用戶、用正確權限執行 `azd up`、確認資源真的建立成功。

## 開啟專案目錄

建議優先使用 GitHub 帳號直接開啟 Codespaces：

- [Open in GitHub Codespaces](https://codespaces.new/payton-chou-ms/e2e-ms-foundry-workshop)

如果你偏好本機開發，再使用 VS Code Dev Container：

- [Open in VS Code Dev Containers](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/payton-chou-ms/e2e-ms-foundry-workshop)

如果你已經是在課程提供的環境、壓縮封裝或內部鏡像中操作，只要切換到專案根目錄後再繼續下面步驟即可。

## 登入 Azure

```bash
azd auth login --tenant-id <TENANT_ID>  --use-device-code
```

如果你還沒拿到 `TENANT_ID`，可參考 Microsoft 官方說明：

- [How to find your Microsoft Entra tenant ID](https://learn.microsoft.com/entra/fundamentals/how-to-find-tenant)

這會開啟瀏覽器進行驗證，並直接把登入範圍鎖定到你要使用的 Tenant

如果你不熟 `--use-device-code` 的流程，可以直接照下面做：

1. 在終端機執行上面的 `azd auth login` 指令
2. 終端機會顯示一組一次性的登入代碼，以及要開啟的登入網址
3. 用瀏覽器打開畫面提示的網址，通常是 `https://microsoft.com/devicelogin`
4. 貼上剛剛那組代碼，登入你要部署使用的 Azure 帳號
5. 看到成功訊息後回到終端機，等待 `azd` 完成登入

如果你的開發環境無法自動跳出登入視窗，這種方式通常比互動式瀏覽器登入更穩定。

!!! warning "部署權限"
    這份 workshop 模板會在部署過程中建立 Azure 角色指派，所以部署身分不能只有資源建立權限

    實務上請用下列其中一種權限模型：

    - `Owner`：最直接，既能建立資源，也能建立角色指派
    - `Contributor` + `User Access Administrator`：較符合最小權限原則
    - `Contributor` + `Role Based Access Control Administrator`：同樣可行，適合把資源建立與 RBAC 指派拆開管理
    - 等效的自訂角色組合：同時涵蓋資源寫入，以及 `Microsoft.Authorization/roleAssignments/write`

    如果你只有 `Contributor`，部署通常會失敗，因為它不能建立 Azure RBAC 角色指派

!!! note "這個模板實際會建立哪些 RBAC 指派"
    目前的 Bicep 模板會在部署期間建立多組角色指派，包含：

    - 對 **Foundry project 的 managed identity** 指派 Search 與 Storage 相關角色
    - 對 **Azure AI Search 的 managed identity** 指派 `Cognitive Services OpenAI User` 與 `Storage Blob Data Reader`
    - 對 **執行部署的使用者身分** 指派 `Cognitive Services User`、`Azure AI User`、`Search Index Data Contributor`、`Search Service Contributor`、`Storage Blob Data Contributor`

    你可以把這段理解成：部署不只是「把資源建出來」，也會順便把執行 workshop 主流程所需的存取補齊

## 部署資源

```bash
azd up --subscription <SUBSCRIPTION_ID>
```

如果你還沒拿到 `SUBSCRIPTION_ID`，可參考 Microsoft 官方說明：

- [Get subscription and tenant IDs in the Azure portal](https://learn.microsoft.com/azure/azure-portal/get-subscription-tenant-id)

依照提示選擇你的環境名稱與位置。

建議範例：

- Environment name：`fdry-payton-1`
- Azure location：`eastus2`
- Resource Group: Create new
- AI deployment location：`eastus2`
- Resource Group Name: rg-fdry-payton-1

`Environment name` 會對應到模板參數 `environmentName`，這個值必須在 3 到 20 個字元之間，所以不要直接填成完整的 resource group 名稱。


對第一次部署來說，最簡單的做法就是：

1. 在 `azd auth login` 時直接指定 `--tenant-id`
2. 在 `azd up` 時直接指定 `--subscription`

這樣就不用先登入一次、再手動切 Tenant、再另外切 Subscription。

!!! tip "gpt-5.4-mini 的區域建議"
    如果你要使用目前 repo 的預設模型 `gpt-5.4-mini`，建議把 **AI deployment location** 設為 `eastus2`

    如果你想讓設定最單純，主區域與 AI deployment location 都直接使用 `eastus2` 即可。這樣和本頁前面的建議範例一致，也比較不容易在重跑時搞混

### 其他常見情境

如果你後面還需要直接執行 Azure CLI 指令，例如 `az account list` 或 `az account show`，再另外登入 Azure CLI 即可：

```bash
az login --tenant <TENANT_ID>
```

如果你想把環境設定固定下來，避免之後重跑時忘記區域或 subscription，可以再做下面這一步：

```bash
azd env set AZURE_LOCATION eastus2
azd env set AZURE_ENV_AI_DEPLOYMENTS_LOCATION eastus2
azd up --subscription <SUBSCRIPTION_ID>
```

如果你已經用 Azure CLI 登入，只想切到正確的訂用帳戶，也可以先這樣做：

```bash
az account set --subscription <SUBSCRIPTION_ID>
azd up
```

如果部署途中看到 `AADSTS50076` 或 `reauthentication required`，通常代表這次操作被要求補做 MFA。這時直接重新登入 `az` / `azd` 並完成驗證即可：

如果在部署、更新資源設定或手動補角色時看到 `RequestDisallowedByAzure`，通常更接近 Azure Policy、deny assignment 或組織治理限制，而不是單純登入過期。這時應先檢查 policy / deny assignment，再決定是否需要調整模板或請管理員放行。

```bash
azd auth logout
azd auth login --tenant-id <TENANT_ID> --use-device-code
```

如果看到 `environmentName` 驗證失敗或 `Length of the value should be less than or equal to '20'`，代表你輸入的 Environment name 太長。請改成 20 個字元以內的短名稱，例如 `fdry-payton-1`。

### 想避免每次重選？

你也可以先建立 azd 環境，把 subscription 固定下來：

```bash
azd env new <environment-name> --subscription <SUBSCRIPTION_ID> --location <AZURE_LOCATION>
azd up --environment <environment-name>
```

第一次成功部署後，`azd` 會把這次環境使用的 `AZURE_SUBSCRIPTION_ID` 和 `AZURE_TENANT_ID` 寫進 `.azure/<env>/.env`。

這次部署除了主要 chat 和 embedding 模型，也會額外建立：

- `gpt-4.1-mini`
- 盡力而為地嘗試建立一個部署在 Foundry account 內的 `gpt-image-1.5` model deployment，用於 `13_demo_image_generation.py`。如果該區域或 quota 不允許，`azd up` 仍會完成，只有影像示範會被略過
- 一個 Playwright Workspace，用於 `10_demo_browser_automation.py`。它會優先使用你選的 Azure location；如果該區域不支援 Playwright Workspace，才會自動改用 `eastus`

!!! note "Retail scenario 的 Blob 上傳需求"
    `data/retail_launch_incident/prepare_search_and_blob_assets.py` 會從本機或 Codespaces 直接呼叫 Blob data plane。
    因此 storage account 需要保留 `Public network access = Enabled`，並以 Microsoft Entra ID 授權。
    如果你的組織會在部署後自動把 storage account 改成 `Disabled`，這支 script 會在 Blob 上傳階段失敗，即使 RBAC 已經完整。

!!! warning "請等待完成"
    部署大約需要 7-8 分鐘。請在看到成功訊息之後再繼續操作

## 驗證部署

在 [Azure Portal](https://portal.azure.com/) 中確認你的資源群組至少包含下列資源。這一步的目的不是逐一檢查細節，而是確認主流程需要的骨幹都有出現：

- Microsoft Foundry
- Foundry project
- Azure AI Search
- Storage Account
- Application Insights
- Log Analytics workspace
- Playwright Workspace

!!! note "補充說明"
    chat、embedding 與其他選配模型部署會掛在 Microsoft Foundry 底下，
    不一定會在資源群組清單中以獨立頂層資源顯示

## 環境變數

部署完成後，Azure 端點會自動儲存到 `.azure/<env>/.env`，並由腳本自動載入。

!!! note "無需手動設定"
    你不需要手動設定 Azure 連線字串。腳本會自動從 azd 環境讀取

!!! note "Browser Automation 先不用現在處理"
    `azd up` 只會先建立 Playwright Workspace。
    等你真的要測 `10_demo_browser_automation.py` 時，再去完成 Browser Automation connection 設定即可。

---
## 學員的 Data Plane 權限

部署完需要再給學員權限；但要確認他們有足夠的 **data plane** 存取，否則腳本會在呼叫 Foundry、Search 或 Blob 時出現 `403`

| 要做的事 | 建議最小權限 | 建議指派範圍 |
|------|---------------|---------------|
| 只跑既有 workshop、測試既有 agent、驗證文件/資料查詢 | `Azure AI User` | Foundry account 或對應 project 上層資源 |
| 要查詢既有 Azure AI Search index | `Search Index Data Reader` | Search service，或更小範圍的單一 index |
| 要重跑既有文件上傳，但不改 index 結構 | `Search Index Data Contributor` | Search service，或單一 index |
| 要建立 / 更新 index、indexer、skillset | `Search Service Contributor` | Search service |
| 只需要讀既有 Blob 內容 | `Storage Blob Data Reader` | Storage account，或單一 container |
| 要上傳 / 覆寫 / 刪除 Blob | `Storage Blob Data Contributor` | Storage account，或單一 container |

### 建議怎麼給

如果學員只是要走「參與者執行與驗證」路徑，建議先從下面這組最小權限開始：

- `Azure AI User`
- `Search Index Data Reader`
- 如果腳本或流程會直接讀 Blob，再補 `Storage Blob Data Reader`

如果學員不只是測試，而是要重跑資料準備或知識建置流程，再加上：

- `Search Service Contributor`
- `Search Index Data Contributor`
- `Storage Blob Data Contributor`

### 這個 workshop 怎麼理解最合理

- **Foundry IQ / agent 執行**：以 `Azure AI User` 為主，這是學員跑 prompt agent、呼叫既有模型與 project data actions 的最小角色
- **Azure AI Search 查詢**：如果只是查既有內容，`Search Index Data Reader` 即可
- **Azure AI Search 重建**：如果要重跑 `prepare_search_and_blob_assets.py` 或 `upload_to_search` 類流程，因為腳本會建立或更新 index，所以需要 `Search Service Contributor`；文件寫入本身仍需要 `Search Index Data Contributor`
- **Blob Storage**：只有在學員的流程真的會直接對 Blob 做讀寫時才需要；純 agent 問答不一定會直接需要 Blob data plane 權限
- **Fabric IQ**：這部分主要不是 Azure RBAC，而是 **Fabric workspace role**。如果學員要走 Fabric 路徑，還要另外確認他們在 Fabric workspace 內至少看得到對應項目

### 官方文件

- Foundry authentication / authorization：<https://learn.microsoft.com/azure/foundry/concepts/authentication-authorization-foundry>
- Foundry built-in roles：<https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry>
- `Azure AI User` 內建角色定義：<https://learn.microsoft.com/azure/role-based-access-control/built-in-roles/ai-machine-learning#azure-ai-user>
- Azure AI Search role-based access：<https://learn.microsoft.com/azure/search/search-security-rbac>
- Azure AI Search 啟用 data plane RBAC：<https://learn.microsoft.com/azure/search/search-security-enable-roles>
- `Search Index Data Reader` / `Search Index Data Contributor` / `Search Service Contributor` 角色定義：<https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#ai-+-machine-learning>
- Blob 以 Microsoft Entra ID 授權：<https://learn.microsoft.com/azure/storage/blobs/authorize-access-azure-active-directory>
- 指派 Blob data access 角色：<https://learn.microsoft.com/azure/storage/blobs/assign-azure-role-data-access>
- `Storage Blob Data Reader` / `Storage Blob Data Contributor` 角色定義：<https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#storage>
- Fabric workspace roles：<https://learn.microsoft.com/fabric/fundamentals/roles-workspaces>
- Give users access to Fabric workspaces：<https://learn.microsoft.com/fabric/fundamentals/give-access-workspaces>


[← 管理員部署](00-admin-deploy-share.md) | [建立 Fabric 工作區 →](02-setup-fabric.md)
