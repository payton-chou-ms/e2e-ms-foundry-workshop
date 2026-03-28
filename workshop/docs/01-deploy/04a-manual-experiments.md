# Microsoft Foundry Live Tour

這一頁只保留 live tour 需要的最小內容。

目的很單純：回到 Microsoft Foundry portal，快速帶大家看這次 workshop 已經建好的 project、agent、knowledge、tools 和 model。

如果你現在要驗證的是 Lakehouse、tables、ontology 或 SQL endpoint，請改看附錄中的 [資料手動驗證](../05-appendix/03-manual-validation.md)。

## Live tour 前先確認

先確認你打開的是這次剛建好的環境，而不是其他舊 project。

- `.azure/<env>/.env` 裡的 `AZURE_AI_PROJECT_NAME`
- `.azure/<env>/.env` 裡的 `AZURE_AI_PROJECT_ENDPOINT`
- `data/default/config/sample_questions.txt` 或目前 scenario 的 `config/sample_questions.txt`

如果你是跑 [建置與驗證解決方案](04-run-scenario.md) 的 Path 1A，就看 workshop runtime agent。

如果你是跑 Path 1B，就看 Foundry-native IQ agent。

## Live tour 最短路徑

### 1. 進入正確的 Foundry project

開啟 Microsoft Foundry，找到這次部署使用的 project。

Portal URL:

- Microsoft Foundry: <https://ai.azure.com/>

### 2. 到 Build 看 agent

進入 **Build > Agents**，打開這次建立的 agent。

現場只要簡單指出下面幾件事即可：

- 這個 agent 就是剛才腳本建立出來的主要資產
- instructions 已存在
- model deployment 已綁定
- knowledge / tools 已掛上

### 3. 到 Knowledge 看文件來源

進入 **Build > Knowledge**，確認目前掛上的知識來源。

這裡 live tour 只要說明一件事：文件問答能力就是從這裡來的。

### 4. 到 Tools 看外部能力

進入 **Build > Tools** 或對應的 connections 畫面，快速帶過目前 agent 可用的工具。

如果這次沒有做選配 demo，就不用展開細節。

### 5. 用一題 sample question 做最小展示

從 `sample_questions.txt` 挑一題文件問題，示範 agent 可以直接回答。

這一步只要證明「agent 可以用」，不用在這頁展開完整測試流程。

### 6. 最後到 Operate 看資產平面

進入 **Operate > Assets**，用 solution name、scenario name 或 agent name 搜尋一次。

這一步的重點只有一個：讓大家知道 Foundry 不只是聊天介面，還有完整的資產管理視角。

## Live tour 只講這三件事

- **Discover**：知道 Foundry 是模型、agent 和工具的入口即可，不展開
- **Build**：這次 live tour 的主角，重點看 agent、knowledge、tools、models
- **Operate**：最後用 Assets 搜尋收尾，帶出管理與治理視角

## 不要在這一頁展開的內容

- 不在這一頁細講附錄資料物件
- 不在這一頁逐項介紹 Foundry 全部功能
- 不在這一頁重跑完整測試腳本

如果你接下來要驗證資料物件，請改看附錄中的 [資料手動驗證](../05-appendix/03-manual-validation.md)。

---

[← 建置與驗證解決方案](04-run-scenario.md) | [附錄中的資料手動驗證 →](../05-appendix/03-manual-validation.md)