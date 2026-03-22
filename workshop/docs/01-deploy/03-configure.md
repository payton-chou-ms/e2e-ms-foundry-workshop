# 設定開發環境

!!! info "兩條路徑都會使用"
    如果你是自己部署環境，本頁會幫你把環境接好
    如果你拿到的是現成環境，本頁會幫你把本機 checkout 連接上去

## Python 環境

!!! note "如果你使用 Dev Container 或 Codespaces"
    這份 workshop 的 Dev Container 會在建立環境時自動安裝 `scripts/requirements.txt` 與 `workshop/requirements.txt`
    如果你是用 Dev Container 或 Codespaces 開啟專案，通常可以直接跳過下面的安裝步驟
    只有在你是本機 Python 環境、或想重新安裝相依套件時，才需要手動執行

### 建立並啟用

```bash
python -m venv .venv
```

=== "Windows"

    ```powershell
    .venv\Scripts\activate
    ```

=== "macOS/Linux"

    ```bash
    source .venv/bin/activate
    ```

### 安裝相依套件

=== "本機快速安裝（選用）"

    ```bash
    pip install uv && uv pip install -r scripts/requirements.txt
    ```

=== "本機標準安裝"

    ```bash
    pip install -r scripts/requirements.txt
    ```

=== "如果你也要本機建置文件站台"

    ```bash
    pip install -r scripts/requirements.txt -r workshop/requirements.txt
    ```

!!! note "目前沒有根目錄 requirements.txt"
    Workshop 腳本相依套件在 `scripts/requirements.txt`，MkDocs 站台相依套件在 `workshop/requirements.txt`

!!! note "`uv` 不是 Dev Container 的預設必要前提"
    如果你想用 `uv`，可以像上面那樣先安裝再使用
    但對第一次操作的同仁來說，直接執行標準安裝就夠了

### 驗證設定

```bash
python -c "import azure.ai.projects; print('Ready!')"
```

## 設定 Fabric

### 取得工作區 ID

1. 前往 [Microsoft Fabric](https://app.fabric.microsoft.com/)
2. 開啟你的工作區
3. 從 URL 複製工作區 ID：

```
https://app.fabric.microsoft.com/groups/{workspace-id}/...
```

### 更新環境檔案

將 `.env.example` 複製為 `.env` 並更新 Fabric 設定：

```bash
cp .env.example .env
```

編輯專案根目錄的 `.env`：

```env
# --- Microsoft Fabric (required) ---
FABRIC_WORKSPACE_ID=your-workspace-id-here

# --- Data Folder (pre-populated with default scenario) ---
DATA_FOLDER=data/default
```

如果你是第一次跑 workshop，建議先只填 `FABRIC_WORKSPACE_ID`，其他資料產生設定先保留 `.env.example` 的預設值即可。

### AI 資料產生設定要不要先改？

這一段主要是給 **Step 2 客製化** 使用，不是第一次跑主流程的必要步驟。

- 第一次操作時，可以先保留 `.env.example` 內建的預設值
- 如果你暫時不想做客製化，也不需要先自己改成別的產業
- 如果你把 `INDUSTRY` 和 `USECASE` 註解掉，之後跑到資料生成步驟時，腳本會改成互動式詢問你要輸入什麼
- 如果 `DATA_SIZE` 沒填，腳本會預設使用 `small`

換句話說，第一次接觸這個 workshop 時，最省事的做法就是：**先不要改這三個值，等你真的要做 Step 2 再改**。

!!! note "Azure 服務變數不需要手動抄寫"
    只要你是透過 `azd up` 建立環境，像是 `AZURE_AI_PROJECT_ENDPOINT`、`AZURE_AI_ENDPOINT`、`AZURE_OPENAI_ENDPOINT`、`AZURE_IMAGE_OPENAI_ENDPOINT`、`AZURE_PLAYWRIGHT_DATAPLANE_URI` 等值都會自動從 `.azure/<env>/.env` 載入

!!! note "PII demo 不再需要額外 Language key"
    `12_demo_pii_redaction.py` 現在可直接使用 `AZURE_AI_ENDPOINT` 加上 `DefaultAzureCredential`。只有在你刻意要用獨立 Language resource 時，才需要另外設定 `AZURE_LANGUAGE_ENDPOINT` / `AZURE_LANGUAGE_KEY`

!!! note "Browser Automation 的手動交接"
    `azd up` 會自動建立 Playwright Workspace，但 Browser Automation 仍需要你手動補完 Foundry project 中的 Browser Automation connection

### Browser Automation 最短手動 SOP

如果你要真正執行 `10_demo_browser_automation.py`，最少只需要補完以下手動步驟：

1. 到 Azure Portal 的 Playwright Workspace，進入 **Settings** > **Access Management**，產生一次性的 **Access token**
2. 在同一個 Workspace 的 **Overview** 頁面，複製 **Browser endpoint**（`wss://...`）
3. 到 Foundry project 的 **Build** > **Tools** > **Connect a tool** > **Browser Automation**
4. 將 **Browser endpoint** 貼到 *Playwright workspace region endpoint*，將 **Access token** 貼到 *Access token*
5. connection 建好後，把該工具頁面上的 **Project connection ID** 寫入專案根目錄 `.env`：

```env
AZURE_PLAYWRIGHT_CONNECTION_ID=/subscriptions/.../resourceGroups/.../providers/Microsoft.CognitiveServices/accounts/.../projects/.../connections/...
```

6. 執行：

```bash
python scripts/10_demo_browser_automation.py --strict
```

!!! note "真正會被腳本讀取的是 connection ID"
    Browser endpoint 與 Access token 是用來手動建立 Foundry connection 的中介資訊；腳本實際執行時讀取的是 `AZURE_PLAYWRIGHT_CONNECTION_ID`

!!! note "官網連結"
    [Browser Automation setup](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/browser-automation#set-up-browser-automation)
    [Manage Playwright workspaces](https://aka.ms/pww/docs/manage-workspaces)
    [Generate Playwright access token](https://aka.ms/pww/docs/manage-access-tokens)

!!! note "共用環境交接"
    如果這套環境是別人先幫你部署好的，請先拿到正確的 `FABRIC_WORKSPACE_ID` 與其他必要設定，再修改 `.env`

## 檢查點

繼續之前，請確認：

- [x] `azd up` 已成功完成
- [x] Python 環境已啟用
- [x] 相依套件已安裝
- [x] Fabric 工作區 ID 已設定

!!! success "準備就緒"
    請繼續至下一步實際看到成果

---

[← 建立 Fabric 工作區](02-setup-fabric.md) | [建置解決方案 →](04-run-scenario.md)
