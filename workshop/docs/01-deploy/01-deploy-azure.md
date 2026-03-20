# 部署基礎架構

!!! info "主要適用對象"
    本頁主要供**管理員部署**路徑使用
    如果已有人為你準備好環境，請從 [參與者執行與驗證](00-participant-run-validate.md) 開始

## 開啟專案目錄

```bash
cd nc-iq-workshop
```

如果你取得的是壓縮封裝、內部鏡像，或課程環境中已提供的專案副本，請先解壓或切換到專案根目錄，再從這裡開始執行部署步驟。

## 登入 Azure

```bash
azd auth login --tenant-id <TENANT_ID>
```

這會開啟瀏覽器進行驗證，並直接把登入範圍鎖定到你要使用的 Tenant。

!!! warning "部署權限"
    本 repository 會在部署過程中建立 Azure 角色指派，所以部署身分不能只有資源建立權限

    實務上請用下列其中一種權限模型：

    - `Owner`：最直接，既能建立資源，也能建立角色指派
    - `Contributor` + `User Access Administrator`：較符合最小權限原則
    - `Contributor` + `Role Based Access Control Administrator`：同樣可行，適合把資源建立與 RBAC 指派拆開管理
    - 等效的自訂角色組合：同時涵蓋資源寫入，以及 `Microsoft.Authorization/roleAssignments/write`

    `Contributor` 單獨使用通常會失敗，因為它不能建立 Azure RBAC 角色指派

!!! note "這個模板實際會建立哪些 RBAC 指派"
    目前的 Bicep 模板會在部署期間建立多組角色指派，包含：

    - 對 **Foundry project 的 managed identity** 指派 Search 與 Storage 相關角色
    - 對 **Azure AI Search 的 managed identity** 指派 `Cognitive Services OpenAI User` 與 `Storage Blob Data Reader`
    - 對 **執行部署的使用者身分** 指派 `Cognitive Services User`、`Azure AI User`、`Search Index Data Contributor`、`Search Service Contributor`、`Storage Blob Data Contributor`

    也就是說，部署不只是「把資源建出來」，還會順便把執行 workshop 主流程所需的資料平面 / 控制平面存取補齊

## 部署資源

```bash
azd up --subscription <SUBSCRIPTION_ID>
```

依照提示選擇你的環境名稱與位置等。

對第一次部署來說，最簡單的做法就是：

1. 在 `azd auth login` 時直接指定 `--tenant-id`
2. 在 `azd up` 時直接指定 `--subscription`

這樣就不用先登入一次、再手動切 Tenant、再另外切 Subscription。

!!! tip "gpt-5.4-mini 的區域建議"
    如果你要使用目前 repo 的預設模型 `gpt-5.4-mini`，建議把 **AI deployment location** 設為 `eastus2`

    實務上可以維持資源群組主區域為 `eastus`，但把 `AZURE_ENV_AI_DEPLOYMENTS_LOCATION` 設成 `eastus2`。這是目前這份 workshop 模板驗證過、較穩定的組合

建議的最短流程如下：

```bash
azd auth login --tenant-id <TENANT_ID>
azd up --subscription <SUBSCRIPTION_ID>
```

如果你後面還需要直接執行 Azure CLI 指令，例如 `az account list` 或 `az account show`，再另外登入 Azure CLI 即可：

```bash
az login --tenant <TENANT_ID>
```

如果你要在 azd 環境裡明確固定這個設定，可以先這樣做：

```bash
azd env set AZURE_LOCATION eastus
azd env set AZURE_ENV_AI_DEPLOYMENTS_LOCATION eastus2
azd up --subscription <SUBSCRIPTION_ID>
```

如果你已經用 Azure CLI 登入，只想切換到正確的訂用帳戶，也可以先這樣做：

```bash
az account set --subscription <SUBSCRIPTION_ID>
azd up
```

### Subscription 與 Tenant 從哪裡拿？

你可以用 Azure Portal 或 Azure CLI 取得。

**從 Azure Portal：**

- **Subscription ID**：到 **Subscriptions**，打開目標訂用帳戶，在 Overview / Essentials 查看 **Subscription ID**
- **Tenant ID**：到 **Microsoft Entra ID**，在 Overview / Basic information 查看 **Tenant ID**

官網入口：

- **Subscriptions**：https://portal.azure.com/#view/Microsoft_Azure_Billing/SubscriptionsBlade
- **Microsoft Entra ID**：https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/Overview

**從 Azure CLI：**

```bash
# 列出你目前可用的訂用帳戶與對應 tenant
az account list --output table

# 查看目前預設中的 subscription / tenant
az account show
```

如果你有多個 tenant，先指定 tenant 再查看會更清楚：

```bash
az login --tenant <TENANT_ID>
az account list --output table
```

### 想避免每次重選？

你也可以在建立 azd 環境時先把 subscription 固定下來：

```bash
azd env new <environment-name> --subscription <SUBSCRIPTION_ID> --location <AZURE_LOCATION>
azd up --environment <environment-name>
```

第一次成功部署後，`azd` 會把這次環境使用的 `AZURE_SUBSCRIPTION_ID` 與 `AZURE_TENANT_ID` 寫進 `.azure/<env>/.env`。

這個部署現在除了主要 chat + embedding 模型外，也會一併建立 Content Understanding 需要的延伸聊天模型：

- `gpt-4.1-mini`

主要的 `text-embedding-3-large` 會同時作為工作坊主路徑與 Content Understanding 預設所使用的 embedding 部署。

此外，部署流程也會自動建立兩個選配能力所需的控制平面資源：

- 一個專用的 image-capable Azure OpenAI resource，用於 `13_demo_image_generation.py`
- 一個 Playwright Workspace，用於 `10_demo_browser_automation.py`

!!! warning "請等待完成"
    部署大約需要 7-8 分鐘。請在看到成功訊息之後再繼續操作

## 驗證部署

在 [Azure Portal](https://portal.azure.com/) 中確認你的資源群組至少包含下列資源：

- Microsoft Foundry
- Foundry project
- Azure AI Search
- Storage Account
- Application Insights
- Log Analytics workspace

如果你使用目前預設的完整部署設定，還會另外看到：

- Dedicated image-capable Azure OpenAI resource
- Playwright Workspace

!!! note "補充說明"
    chat、embedding 與其他選配模型部署會掛在 Microsoft Foundry 底下，
    不一定會在資源群組清單中以獨立頂層資源顯示

## 環境變數

部署完成後，Azure 端點會自動儲存到 `.azure/<env>/.env`，並由腳本自動載入。

!!! note "無需手動設定"
    你不需要手動設定 Azure 連線字串。腳本會自動從 azd 環境讀取

!!! note "Browser Automation 的最後一段仍需手動"
    `azd up` 會自動建立 Playwright Workspace，但 Browser Automation 仍需要你手動補完 Foundry project 中的 Browser Automation connection

    - **從哪邊拿資料**：到 Azure Portal 的 Playwright Workspace，進入 **Settings** > **Access Management** 產生一次性的 **Access token**；再到 Workspace 的 **Overview** 複製 **Browser endpoint**（`wss://...`）
    - **貼到哪邊**：到 Foundry project 的 **Build** > **Tools** > **Connect a tool** > **Browser Automation**，把 **Browser endpoint** 貼到 *Playwright workspace region endpoint*，把 **Access token** 貼到 *Access token*
    - **最後要保存的值**：connection 建好後，將該工具頁面上的 **Project connection ID** 寫入專案根目錄 `.env` 的 `AZURE_PLAYWRIGHT_CONNECTION_ID`
    - **官網連結**：
      [Browser Automation setup](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/browser-automation#set-up-browser-automation)
      [Manage Playwright workspaces](https://aka.ms/pww/docs/manage-workspaces)
      [Generate Playwright access token](https://aka.ms/pww/docs/manage-access-tokens)

---

[← 管理員部署](00-admin-deploy-share.md) | [建立 Fabric 工作區 →](02-setup-fabric.md)
