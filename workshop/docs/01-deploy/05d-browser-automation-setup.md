# Browser Automation 補充設定

只有在你真的要測 `10_demo_browser_automation.py` 時，才需要做這一頁。

## 你要做的事

1. 到 Azure Portal 的 Playwright Workspace 建立 Access token
2. 複製 Browser endpoint
3. 到 Microsoft Foundry project 建立 Browser Automation connection
4. 把 connection ID 寫入 `.env` 的 `AZURE_PLAYWRIGHT_CONNECTION_ID`

## 手動設定步驟

### Step 1. 在 Azure Portal 找到 Playwright Workspace

- 開啟 Azure Portal：<https://portal.azure.com/>
- 找到這次部署建立的 Playwright Workspace
- 如果 `.azure/<env>/.env` 裡的 `AZURE_PLAYWRIGHT_STATUS=failed`，通常代表這次部署碰到 quota 上限；這種情況先清理 subscription 內不用的 Playwright Workspace，或直接略過這個 demo
- 進入 `Settings > Access Management`
- 產生 Access token
- 回到 `Overview` 複製 Browser endpoint，格式通常是 `wss://...`

### Step 2. 在 Microsoft Foundry 建立 connection

- 開啟 Microsoft Foundry：<https://ai.azure.com/>
- 進入這次 workshop 使用的 project
- 到 `Build > Tools > Connect a tool > Browser Automation`
- 貼上 Browser endpoint 和 Access token

### Step 3. 回填 `.env`

connection 建好後，把 Project connection ID 寫入專案根目錄 `.env` 的 `AZURE_PLAYWRIGHT_CONNECTION_ID`

## 相關官方說明

- Browser Automation setup: <https://learn.microsoft.com/azure/foundry/agents/how-to/tools/browser-automation#set-up-browser-automation>
- Manage authentication for Playwright Workspaces: <https://learn.microsoft.com/azure/app-testing/playwright-workspaces/how-to-manage-authentication>
- Manage workspace access tokens: <https://learn.microsoft.com/azure/app-testing/playwright-workspaces/how-to-manage-access-tokens>

---

[← 延伸示範與快貼範例](05c-script-optional-demos.md) | [Multi-agent 與進階範例 →](05e-script-advanced.md)