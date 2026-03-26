# 部署基礎架構

!!! info "主要適用對象"
    本頁主要供**管理員部署**路徑使用。
    如果環境已經有人幫你準備好，請直接改看 [參與者執行與驗證](00-participant-run-validate.md)。

這一頁的主線只有三件事：登入正確租用戶、執行 `azd up`、確認骨幹資源都有建立成功。

## 超速部署

```bash
az login --tenant <TENANT_ID> --use-device-code
azd auth login --tenant-id <TENANT_ID> --use-device-code
azd up --subscription <SUBSCRIPTION_ID>
```

如果你只想先把環境建起來，先跑上面三行就夠了。

## 主線步驟

### 1. 開啟專案

建議優先使用 Codespaces；若你偏好本機，再使用 VS Code Dev Container。

- [Open in GitHub Codespaces](https://codespaces.new/payton-chou-ms/e2e-ms-foundry-workshop)
- [Open in VS Code Dev Containers](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/payton-chou-ms/e2e-ms-foundry-workshop)

如果你已經在課程提供的環境或現成鏡像中操作，只要切到專案根目錄即可。

### 2. 登入 Azure

```bash
azd auth login --tenant-id <TENANT_ID> --use-device-code
```

如果你還沒拿到 `TENANT_ID`，可參考官方說明：

- [How to find your Microsoft Entra tenant ID](https://learn.microsoft.com/entra/fundamentals/how-to-find-tenant)

!!! warning "部署權限"
    這份模板在部署時會建立 Azure RBAC 角色指派，所以部署身分不能只有資源建立權限。

    實務上請使用下列其中一種權限模型：

    - `Owner`
    - `Contributor` + `User Access Administrator`
    - `Contributor` + `Role Based Access Control Administrator`

### 3. 執行 `azd up`

```bash
azd up --subscription <SUBSCRIPTION_ID>
```

如果你還沒拿到 `SUBSCRIPTION_ID`，可參考：

- [Get subscription and tenant IDs in the Azure portal](https://learn.microsoft.com/azure/azure-portal/get-subscription-tenant-id)

第一次部署建議值：

- Environment name：`fdry-payton-1`
- Azure location：`eastus2`
- AI deployment location：`eastus2`
- Resource Group：Create new

`Environment name` 會對應到模板參數 `environmentName`，長度必須介於 3 到 20 個字元之間。

### 4. 驗證部署

到 [Azure Portal](https://portal.azure.com/) 檢查資源群組至少有下面這些骨幹資源：

- Microsoft Foundry
- Foundry project
- Azure AI Search
- Storage Account
- Application Insights
- Log Analytics workspace
- Playwright Workspace（若 `AZURE_DEPLOY_BROWSER_AUTOMATION=true`）
- 多個 scenario 對應的 Blob containers

chat、embedding 與其他選配模型會掛在 Microsoft Foundry 底下，不一定會以獨立頂層資源顯示。

## 部署後你通常要接著做什麼

部署完成後，Azure 端點會自動寫入 `.azure/<env>/.env`，腳本會自行載入。

如果你接下來要把共享環境一次準備好，請改跑：

```bash
python scripts/00_admin_prepare_demo.py
```

如果你還要整理給下一位使用者的資料平面權限，請改看 [管理員部署](00-admin-deploy-share.md)。

??? note "其他常見情境"
    如果部署途中看到 `AADSTS50076` 或 `reauthentication required`，通常表示這次操作被要求補做 MFA。這時直接重新登入即可：

    ```bash
    azd auth logout
    azd auth login --tenant-id <TENANT_ID> --use-device-code
    ```

    如果看到 `RequestDisallowedByAzure`，通常更接近 Azure Policy、deny assignment 或組織治理限制，而不是單純登入過期。

    如果看到 `environmentName` 太長，請改成 20 個字元以內的短名稱，例如 `fdry-payton-1`。

??? note "想避免每次重選 subscription / location"
    你可以先建立 azd 環境：

    ```bash
    azd env new <environment-name> --subscription <SUBSCRIPTION_ID> --location <AZURE_LOCATION>
    azd up --environment <environment-name>
    ```

    第一次成功部署後，`azd` 會把 `AZURE_SUBSCRIPTION_ID` 和 `AZURE_TENANT_ID` 寫進 `.azure/<env>/.env`。

??? note "azd up 會額外嘗試部署的選配模型"
    `azd up` 除了主流程需要的 chat / embedding 模型，也會 best-effort 嘗試建立一組額外模型供手動 demo 使用。

    這些部署失敗時，`azd up` 仍會完成；失敗狀態只會被記錄在 `.azure/<env>/.env`。

    其中包含：

    - `gpt-image-1.5`
    - `gpt-5-nano`
    - `gpt-4.1-nano`
    - `gpt-4o-mini`
    - `o3-mini`
    - `gpt-5.3-chat`
    - `gpt-5-pro`
    - `gpt-5-codex`
    - `gpt-5.1-codex`
    - `gpt-5.1-codex-mini`
    - `gpt-5`
    - `gpt-5.1`
    - `gpt-5-mini`
    - `gpt-5.4-nano`
    - `gpt-5.4-mini`

??? note "選配資源與補充"
    **Browser Automation**

    如果你這次不需要 `10_demo_browser_automation.py`，可在部署前先設定：

    ```bash
    azd env set AZURE_DEPLOY_BROWSER_AUTOMATION false
    ```

    之後再執行：

    ```bash
    azd up --environment <environment-name>
    ```

    **Retail scenario 的 Blob 上傳需求**

    `data/retail_launch_incident/prepare_search_and_blob_assets.py` 會直接呼叫 Blob data plane，因此 storage account 需要保留 `Public network access = Enabled`，並以 Microsoft Entra ID 授權。

    **Scenario containers 與 admin preload**

    新版部署會預先建立每個 scenario 對應的 Blob container。Azure 資源部署完成後，再手動執行 `python scripts/00_admin_prepare_demo.py` 即可把預設 demo 環境補齊。

[← 管理員部署](00-admin-deploy-share.md) | [建立 Fabric 工作區 →](02-setup-fabric.md)
