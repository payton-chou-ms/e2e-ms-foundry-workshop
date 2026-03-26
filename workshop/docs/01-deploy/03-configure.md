# 設定開發環境

!!! info "兩條路徑都會使用"
    不論你是自己部署 Azure 環境，還是使用別人已經部署好的環境
    這一頁都會幫你完成本機端的開發環境和 `.env` 設定

## Python 環境

!!! note "如果你使用 Dev Container 或 Codespaces"
    這份 workshop 的 Dev Container 會在建立環境時自動安裝根目錄 `requirements.txt`
    如果你是用 Dev Container 或 Codespaces 開啟專案，通常可以直接跳過下面的安裝步驟
    只有在你是本機 Python 環境、或想重新安裝相依套件時，才需要手動執行

!!! note "統一使用專案根目錄 `.venv`"
    本 repo 的 Python 環境統一放在專案根目錄 `.venv`
    下列指令也都預設從專案根目錄執行

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

```bash
pip install -r requirements.txt
```

### 驗證設定

```bash
python -c "import azure.ai.projects; print('Ready!')"
```

## 設定 Fabric

只有在你要執行 Fabric IQ 相關內容時，才需要做這一段。

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

# --- Active Scenario (preferred) ---
SCENARIO_KEY=default

# --- Data Folder (backward-compatible fallback) ---
DATA_FOLDER=data/default
```

如果你是第一次跑 workshop，建議先填 `FABRIC_WORKSPACE_ID` 和 `SCENARIO_KEY`，其他資料產生設定先保留 `.env.example` 的預設值即可。

!!! note "跳過 Browser Automation 部署"
    `.env` 不控制 `azd up` 是否建立 Playwright Workspace。
    如果你想在這次部署先跳過 Browser Automation，請在執行 `azd up` 前先跑：

    ```bash
    azd env set AZURE_DEPLOY_BROWSER_AUTOMATION false
    ```

    之後若要重新啟用，再改成 `true` 並重新部署即可。

### AI 資料產生設定要不要先改？

第一次跑 workshop 時，這一段可以先不要改。

- 先保留 `.env.example` 的預設值即可
- 如果你之後要自訂產業與 use case，統一到 [產生自訂資料](../02-customize/02-generate.md) 操作
- `DATA_SIZE` 沒填時，預設會用 `small`

!!! note "Azure 服務變數不需要手動抄寫"
    透過 `azd up` 建立的 Azure 服務變數，會自動從 `.azure/<env>/.env` 載入

!!! note "PII demo 不再需要額外 Language key"
    `12_demo_pii_redaction.py` 直接用 `AZURE_AI_ENDPOINT` 和 `DefaultAzureCredential` 即可

!!! note "Browser Automation 的手動交接"
    `azd up` 會自動建立 Playwright Workspace，但 Browser Automation 還需要你手動建立 Foundry connection。
    等你真的要測 `10_demo_browser_automation.py` 時，再看 [Browser Automation 補充設定](05d-browser-automation-setup.md) 即可。

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

[← 參與者執行與驗證](00-participant-run-validate.md) | [建置與驗證解決方案 →](04-run-scenario.md)
