# T-06 交付結果：publish to Teams / Microsoft 365 Copilot 規劃

## 任務目標

完成 `T-06 擴充 agent 程式：publish to Teams / M365 Copilot 規劃`，並決定這個 repo 在第一階段應該：

1. 只補文件與 pseudo flow
2. 補一支 guarded script
3. 或直接做完整自動化 publish

## 結論

本 repo 在第一階段 **不建議直接做完整自動化 publish to Teams / Microsoft 365 Copilot**。

建議採用下列策略：

1. **保留 UI 為主的正式 publish 流程**
   - 符合目前 workshop 的教學目標。
   - 講師可在 Foundry UI 中手動帶看 publish、Agent Application、Teams / Microsoft 365 Copilot 設定。

2. **補一支 guarded precheck / helper script**
   - 用來檢查最基本的 publish 前提是否成立。
   - 若條件不足，輸出 warning 並跳過，不阻塞 workshop 主流程。

3. **文件中補齊 publish identity / RBAC 差異與操作順序**
   - 這是目前缺口中最有價值的部分。

## 為什麼不建議先做完整自動化

### 1. Teams / Microsoft 365 Copilot publish 流程本身偏 UI 導向

根據官方文件，完整流程至少包含：

1. 先把 agent publish 成 Agent Application
2. 再從 Foundry UI 進一步 publish 到 Teams / Microsoft 365 Copilot
3. 填寫 metadata
4. 建立或選擇 Azure Bot Service
5. 選擇 Individual 或 Organization scope
6. 視 scope 進一步經過分享或 admin approval

這些步驟中有相當一部分最適合透過 UI 操作與講解，而不是先寫成硬自動化腳本。

### 2. 權限依賴多，且不是目前主流程必要能力

官方文件涉及的前提包含：

1. `Azure AI Project Manager` 角色，用於 publish agent
2. `Azure AI User` 角色，用於呼叫 published agent
3. `Microsoft.BotService` provider 已註冊
4. 可建立 Azure Bot Service
5. 若是 Organization scope，需 Microsoft 365 admin approval

這些條件在 workshop 環境不一定都成立，因此應維持選配能力定位。

### 3. Published agent identity 會改變

這是最重要的風險點。

agent 在 project 裡開發與測試時，使用的是 project 的 shared agent identity。

一旦 publish 成 Agent Application：

1. 會得到新的 agent identity
2. 會得到新的 RBAC scope
3. 先前 project identity 可存取的下游資源，不會自動轉移給 published identity

因此，若直接把 publish 自動化而沒有同步處理 RBAC，很容易出現：

- 在 Foundry project 內測試正常
- publish 後 tool call 全部授權失敗

## 第一階段建議交付

### A. 補 guarded helper script

建議新增：

- `scripts/09_publish_foundry_agent.py`

用途：

1. 讀取目前環境與 agent 設定
2. 檢查 agent 是否存在
3. 檢查 Azure CLI 是否登入
4. 檢查 `Microsoft.BotService` provider 註冊狀態
5. 輸出 UI publish 的建議下一步
6. 條件不足時 warning 並跳過

這支腳本 **不承諾完整自動 publish**，而是用來支援教學與前置檢查。

### B. 文件中補 pseudo flow

文件應把 publish 拆成兩段：

1. `Publish as Agent Application`
2. `Publish to Teams / Microsoft 365 Copilot`

並清楚說明：

1. 哪些步驟適合腳本
2. 哪些步驟保留給 UI
3. 哪些權限與 provider 缺失時要直接跳過

## 建議實作邊界

### 第一階段要做

1. agent existence precheck
2. Azure login / subscription / provider 狀態提示
3. UI publish next steps 輸出
4. publish 後 identity / RBAC 差異說明
5. non-blocking skip 行為

### 第一階段不要承諾

1. 自動建立 Agent Application + deployment 的完整管理 API 流程
2. 自動完成 Teams / Microsoft 365 Copilot metadata packaging
3. 自動完成 Organization scope approval
4. 自動修補 publish 後的所有 RBAC

## 建議 publish 流程

### Step 1：確認 agent 已存在且已測試

最低要求：

1. `07_create_foundry_agent.py` 已成功建立 agent
2. `08_test_foundry_agent.py` 已完成基本對話測試
3. 若 agent 使用 tool，先在 project 內確認 tool call 正常

### Step 2：先 publish 成 Agent Application

建議透過 Foundry UI 執行。

原因：

1. 對 workshop 講師最直覺
2. UI 比較容易解釋 application、deployment、stable endpoint
3. 比較符合「部署後在 UI 手動教大家如何查看」的需求

### Step 3：確認 publish 後的新 identity

這一步文件必須強調：

1. publish 後不是沿用 project shared identity
2. 下游資源權限需重新檢查

### Step 4：若需要，再進一步 publish 到 Teams / Microsoft 365 Copilot

同樣建議透過 UI 執行。

原因：

1. 需要填 metadata
2. 需要建立或選擇 Azure Bot Service
3. 可能涉及 scope 選擇與 admin approval

## publish 後需要重新檢查的權限

至少要重新檢查下列 Azure 資源是否授權給新的 Agent Application identity：

1. Azure AI Search
   - 若 agent 需要查詢索引或使用 search 相關工具

2. Storage Account
   - 若 agent 需要存取 blob / file 資料

3. 其他 project connection 對應資源
   - 例如後續若接入 Browser Automation、其他 tool connection

4. 任何使用 managed identity 驗證的下游資源

## 與目前 repo 的關係

目前 repo：

1. 已有 agent create / test
2. 已有 project connection 與基本 RBAC
3. 尚無 publish 相關腳本
4. 尚無 publish 後 identity 轉換與 RBAC 補授權流程

因此 T-06 的正確方向不是直接補一大段完整 publish 自動化，而是：

1. 先補 guarded precheck 腳本
2. 補文件與 pseudo flow
3. 把完整 Teams / M365 publish 視為 UI 教學與後續進階任務

## 推薦腳本行為

建議 `scripts/09_publish_foundry_agent.py` 採以下設計：

1. 預設為非阻塞
   - 缺前提時輸出 warning 後結束
   - 預設 exit code 應可維持成功結束，避免卡住整體 pipeline

2. 輸出清楚 checkpoint
   - 找到 agent
   - 找到 project endpoint
   - Azure CLI 是否登入
   - `Microsoft.BotService` 是否已註冊

3. 不直接替使用者做高風險 publish
   - 只做 precheck 與 next-step guidance

4. 保持現有 repo 風格
   - 環境變數驅動
   - 單檔腳本
   - 清楚 console output

## 後續若要擴成第二階段

若未來要做更深的 publish 自動化，建議拆成兩個後續任務：

### 階段二-A：Agent Application 管理 API 自動化

可能範圍：

1. 建立 application
2. 建立 managed deployment
3. 驗證 deployment state

### 階段二-B：Teams / Microsoft 365 Copilot 發布支援

可能範圍：

1. metadata 準備
2. package 檢查
3. UI 教學腳本化輔助

但這部分仍不建議在第一階段就納入必要能力。

## 驗收結果

T-06 完成標準建議定義為：

1. 已做出明確實作決策
   - 第一階段不做完整 publish automation

2. 已補一支 guarded helper script
   - 可做 precheck
   - 可輸出下一步 publish 指引
   - 缺條件時可 warning 並跳過

3. 已記錄 publish 後 identity / RBAC 差異

4. 已保留後續擴充空間
   - 若未來需要，可再把 Agent Application 管理 API 自動化獨立成下一個 task