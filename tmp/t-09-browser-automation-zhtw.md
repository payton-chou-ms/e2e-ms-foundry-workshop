# T-09 Browser Automation 評估

## 決策

採用「獨立 demo 腳本 + 明確 trusted-site 限制 + 缺前置時 skip」模式，不併入主 workshop tool loop。

## 主要產出

- `scripts/10_demo_browser_automation.py`

## Demo 邊界

- 僅示範 Microsoft Learn trusted page
- prompt 明確禁止登入、填表、提交資料、離開信任網域
- 需要 Browser Automation project connection ID 才會執行

## 依賴

- Foundry project endpoint
- Playwright workspace 對應的 project connection ID
- 支援 `BrowserAutomationPreviewTool` 的 SDK 版本

## Skip 條件

- SDK 無 preview 類型
- 未設定 Browser Automation connection ID
- 執行時功能尚未在環境中可用

## 結論

這個能力適合作為 optional extension demo，但因為安全風險高，不應進入預設主流程。