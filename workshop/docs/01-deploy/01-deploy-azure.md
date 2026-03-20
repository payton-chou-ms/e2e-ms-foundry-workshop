# 部署基礎架構

!!! info "主要適用對象"
    本頁主要供**管理員部署與分享**路徑使用。
    如果已有人為你準備好環境，請從 [參與者執行與驗證](00-participant-run-validate.md) 開始。

## 複製 Repository

```bash
git clone https://github.com/nchandhi/nc-iq-workshop.git
cd nc-iq-workshop
```

## 登入 Azure

```bash
azd auth login
```

這會開啟瀏覽器進行驗證。

!!! warning "部署權限"
    本 repository 會在部署過程中建立 Azure 角色指派。
    如果 `azd up` 在 RBAC 建立時失敗，請確認你的身分可以在目標範圍內建立角色指派。

## 部署資源

```bash
azd up
```

依照提示選擇你的環境名稱、訂用帳戶與位置等。

這個部署現在除了主要 chat + embedding 模型外，也會一併建立 Content Understanding 所需的延伸模型部署：

- `gpt-4.1-mini`
- `text-embedding-3-large`

此外，部署流程也會自動建立兩個選配能力所需的控制平面資源：

- 一個專用的 image-capable Azure OpenAI resource，用於 `13_demo_image_generation.py`
- 一個 Playwright Workspace，用於 `10_demo_browser_automation.py`

!!! warning "請等待完成"
    部署大約需要 7-8 分鐘。請在看到成功訊息之後再繼續操作。

## 驗證部署

在 [Azure Portal](https://portal.azure.com/) 中確認你的資源群組包含所有資源：

- Microsoft Foundry
- Azure AI Search
- Storage Account
- Application Insights

## 環境變數

部署完成後，Azure 端點會自動儲存到 `.azure/<env>/.env`，並由腳本自動載入。

!!! note "無需手動設定"
    你不需要手動設定 Azure 連線字串。腳本會自動從 azd 環境讀取。

!!! note "Browser Automation 的最後一段仍需手動"
    `azd up` 現在會自動建立 Playwright Workspace，但 Browser Automation 仍需要你在 Azure Portal 產生一次性的 Playwright access token，並在 Foundry project 中建立 Browser Automation connection。

!!! note "Image Generation 已納入正式部署流程"
    `azd up` 現在會自動建立獨立的 image-capable Azure OpenAI resource，並把 `AZURE_IMAGE_OPENAI_ENDPOINT` / `AZURE_IMAGE_MODEL_DEPLOYMENT` 寫入 azd 環境輸出。

---

[← 管理員部署與分享](00-admin-deploy-share.md) | [建立 Fabric 工作區 →](02-setup-fabric.md)
