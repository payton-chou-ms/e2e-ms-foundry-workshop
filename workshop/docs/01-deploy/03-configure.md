# 設定開發環境

!!! info "兩條路徑都會使用"
    如果你是自己部署環境，本頁會幫你把環境接好。
    如果你拿到的是現成環境，本頁會幫你把本機 checkout 連接上去。

## Python 環境

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

=== "快速（建議）"

    ```bash
    pip install uv && uv pip install -r scripts/requirements.txt
    ```

=== "標準"

    ```bash
    pip install -r scripts/requirements.txt
    ```

=== "如果你也要本機建置文件站台"

    ```bash
    pip install -r scripts/requirements.txt -r workshop/requirements.txt
    ```

!!! note "目前沒有根目錄 requirements.txt"
    Workshop 腳本相依套件在 `scripts/requirements.txt`，MkDocs 站台相依套件在 `workshop/requirements.txt`。

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

!!! note "Azure 服務變數不需要手動抄寫"
    只要你是透過 `azd up` 建立環境，像是 `AZURE_AI_PROJECT_ENDPOINT`、`AZURE_AI_ENDPOINT`、`AZURE_OPENAI_ENDPOINT`、`AZURE_IMAGE_OPENAI_ENDPOINT`、`AZURE_PLAYWRIGHT_DATAPLANE_URI` 等值都會自動從 `.azure/<env>/.env` 載入。

!!! note "PII demo 不再需要額外 Language key"
    `12_demo_pii_redaction.py` 現在可直接使用 `AZURE_AI_ENDPOINT` 加上 `DefaultAzureCredential`。只有在你刻意要用獨立 Language resource 時，才需要另外設定 `AZURE_LANGUAGE_ENDPOINT` / `AZURE_LANGUAGE_KEY`。

!!! note "Browser Automation 的手動交接"
    Playwright Workspace 現在會隨部署自動建立，但你仍需要在 Azure Portal 產生 Playwright access token，並在 Foundry project 中建立 Browser Automation connection，`10_demo_browser_automation.py` 才會真正執行。

### Browser Automation 最短手動 SOP

如果你要真正執行 `10_demo_browser_automation.py`，最少只需要補完以下手動步驟：

1. 在 Azure Portal 開啟 `azd up` 建立出的 Playwright Workspace。
2. 產生一次性的 Playwright access token，先把它暫時記下來。
3. 在同一個 Foundry project 中建立 `Browser Automation` connection，使用剛剛的 Playwright Workspace 與 token。
4. 把該 connection 的資源 ID 寫入專案根目錄 `.env`：

```env
AZURE_PLAYWRIGHT_CONNECTION_ID=/subscriptions/.../resourceGroups/.../providers/Microsoft.CognitiveServices/accounts/.../projects/.../connections/...
```

5. 執行：

```bash
python scripts/10_demo_browser_automation.py --strict
```

!!! note "真正會被腳本讀取的是 connection ID"
    `AZURE_PLAYWRIGHT_WS_ENDPOINT` 與 Playwright access token 是用來手動建立 Foundry connection 的中介資訊；腳本實際執行時讀取的是 `AZURE_PLAYWRIGHT_CONNECTION_ID`。

!!! note "共用環境交接"
    如果這套環境是別人先幫你部署好的，請先拿到正確的 `FABRIC_WORKSPACE_ID` 與其他必要設定，再修改 `.env`。

## 檢查點

繼續之前，請確認：

- [x] `azd up` 已成功完成
- [x] Python 環境已啟用
- [x] 相依套件已安裝
- [x] Fabric 工作區 ID 已設定

!!! success "準備就緒"
    請繼續至下一步實際看到成果。

---

[← 建立 Fabric 工作區](02-setup-fabric.md) | [建置解決方案 →](04-run-scenario.md)
