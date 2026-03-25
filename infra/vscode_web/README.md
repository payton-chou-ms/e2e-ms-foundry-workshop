# VS Code for the Web - Microsoft Foundry Templates

我們已為你產生一個簡單的開發環境來部署這些範本。

Microsoft Foundry 擴充功能提供工具，協助你直接在 VS Code 中建構、測試與部署 AI 模型及 AI 應用程式。它提供簡化的操作方式，讓你不需要離開開發環境就能與模型、代理程式和執行緒互動。點選左側的 Microsoft Foundry 圖示以查看更多。

請依照以下操作說明開始！

你應該會看到一個終端視窗，其中已經 clone 了範本程式碼。

## 部署範本

你可以使用以下指令佈建與部署此範本：

```bash
azd up
```

依照部署腳本的指示操作並啟動應用程式。


如果你需要刪除部署並停止產生費用，請執行：

```bash
azd down
```

## 如果你不是走 `azd` 路徑

有些 VS Code Web 範本會直接提供 connection string 或既有 endpoint，而不是要求你先用 `azd up` 佈建環境。

這種情況下，請改依範本內提供的 `.env` 模板填入必要設定，例如：

- project connection string
- Foundry project endpoint
- 其他範本要求的認證或環境變數

換句話說：

- 如果範本提供的是完整基礎架構與部署流程，照 `azd up` / `azd down` 走
- 如果範本提供的是既有資源連線方式，優先依 `.env` 與 sample code 的說明設定，不必額外建立 `azd` 流程

## 繼續在本機桌面工作

你可以點選畫面左下角的「Continue On Desktop...」來繼續在 VS Code Desktop 上工作。請確保帶上 .env 檔案，步驟如下：

- 右鍵點選 .env 檔案
- 選取「Download」
- 將檔案從你的 Downloads 資料夾移動到本機 git repo 目錄
- 若使用 Windows，你需要用右鍵「Rename...」將檔案名稱改回 .env

## 更多範例

請參閱 [Azure AI Projects client library for Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/README.md) 以了解更多使用此 SDK 的資訊。

## 疑難排解

- 如果你透過 Foundry project 的端點初始化 client，請確認 `.env` 中設定的端點格式為 https://{your-foundry-resource-name}.services.ai.azure.com/api/projects/{your-foundry-project-name}
