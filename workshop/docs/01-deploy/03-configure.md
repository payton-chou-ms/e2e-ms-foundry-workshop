# 設定開發環境

!!! info "兩條路徑都會使用"
    管理員使用本頁來準備可分享的環境。
    參與者使用本頁來將本機 checkout 連接到已準備好的環境。

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
    pip install uv && uv pip install -r requirements.txt
    ```

=== "標準"

    ```bash
    pip install -r requirements.txt
    ```

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
    只要你是透過 `azd up` 建立環境，像是 `AZURE_AI_PROJECT_ENDPOINT`、`AZURE_AI_ENDPOINT`、`AZURE_OPENAI_ENDPOINT` 等值都會自動從 `.azure/<env>/.env` 載入。

!!! note "PII demo 不再需要額外 Language key"
    `12_demo_pii_redaction.py` 現在可直接使用 `AZURE_AI_ENDPOINT` 加上 `DefaultAzureCredential`。只有在你刻意要用獨立 Language resource 時，才需要另外設定 `AZURE_LANGUAGE_ENDPOINT` / `AZURE_LANGUAGE_KEY`。

!!! note "共用環境交接"
    如果管理員已為你預先部署環境，請先向管理員要到正確的 `FABRIC_WORKSPACE_ID` 與其他必要設定，再修改 `.env`。

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
