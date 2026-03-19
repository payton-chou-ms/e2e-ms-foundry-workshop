# Foundry 教學主軸補強計劃（繁體中文）

## 目標

將目前以 `Foundry IQ + Fabric IQ` 為核心的 workshop，補強為可清楚對外說明下列五個主軸的教學內容：

1. Foundry Model
2. Foundry IQ
3. Foundry Agent
4. Foundry Tool
5. Control Plane

本計劃的重點不是重寫整個 workshop，而是補上目前 repo 已有實作、但尚未被文件清楚教學化的部分。

## 教學原則

本次補強以「教學目標優先」為原則，不追求一次把所有 Foundry 能力做成完整產品化流程。

### 核心原則

1. 以簡單扼要的部署與 demo 為主
   - 文件重點是讓講師可在短時間內完成設定、跑通最小示範、再進入 UI 手動講解。

2. 流程與 sample 盡量貼近現有 repo 的程式邏輯與寫法
   - 優先沿用目前 `00_build_solution.py`、`07_create_foundry_agent.py`、`08_test_foundry_agent.py` 的敘事方式。
   - 新增能力時，文件中的 sample flow 與 pseudo code 也要維持類似風格，避免突然切成另一套框架或完全不同的架構。

3. 採用非阻塞部署策略
   - 若某些模型、tool、connection、publish 或 trace 功能因權限、區域、SKU、preview 限制或租戶政策無法啟用，直接跳過並繼續後續步驟。
   - 不讓單一可選能力卡住整體 workshop 的部署與 demo 流程。

4. 部署完成後，以 UI 講解為主
   - 文件只需把最小可用能力部署完成。
   - 講師可在 Azure portal、Foundry portal、Application Insights、Agents UI 中手動帶看設定與結果。

### 非阻塞部署原則

所有新增能力均應明確標註為以下兩類之一：

1. 必要能力
   - 不具備時，無法完成 workshop 主流程。

2. 選配能力
   - 不具備時，僅影響進階 demo。
   - 若部署失敗，記錄 warning 並繼續。

本次新增的多模型部署、部分 Foundry tools、agent trace、publish to Teams，原則上都應視為「選配能力」，除非後續明確決定要把它們提升為主流程必要條件。

## 現況判斷

### 已覆蓋

1. `Foundry IQ`
   - 已有獨立 deep dive 頁面。
   - 已能說明 agentic retrieval、知識庫與文件檢索。

2. `Fabric IQ`
   - 已有獨立 deep dive 頁面。
   - 已能說明 ontology、NL to SQL 與資料查詢流程。

### 部分覆蓋

1. `Foundry Agent`
   - 文件中有提到 orchestrator agent。
   - 程式中已有 agent create / get / test 實作。
   - 但尚未形成獨立教學單元。

### 明顯缺口

1. `Foundry Model`
   - IaC 目前只明確呈現基本 chat model 與 embedding model 的部署概念。
   - 但目前文件幾乎沒有說明多模型策略、模型能力差異、為何這樣選、如何被 agent 與 tool 使用。

2. `Foundry Tool`
   - 程式中已有 `search_documents` 與 `execute_sql` 的 function tool。
   - 但目前文件沒有一頁明確解釋 tool schema、tool selection、tool execution loop。

3. `Control Plane`
   - Bicep 已定義 AI Services、Project、Connections、RBAC、App Insights。
   - 但文件目前幾乎只講「執行 `azd up` 會部署資源」，沒有說清楚平台控制層的結構與責任分工。

## 優先順序

### 第一優先

1. `Control Plane`
   - 這是目前最大缺口。
   - 它是串起 model、agent、tool、IQ 的基礎骨架。
   - 若沒有這一層，學員會知道功能有跑起來，但不知道 Foundry 平台是怎麼組成的。

### 第二優先

1. `Foundry Agent`
2. `Foundry Tool`

原因：

- 這兩塊是 workshop 真正的示範核心。
- 使用者最後看到的「智能體如何決策並查資料」就落在 agent 與 tool 的交互。

### 第三優先

1. `Foundry Model`

原因：

- 這塊重要，但它比較像能力來源與平台基礎設定。
- 若前兩層還沒講清楚，單講 model 對受眾的價值感會比較弱。

## 建議資訊架構調整

目前 `Deep dive` 章節只有：

1. Foundry IQ
2. Fabric IQ

建議改為五主軸結構，至少在導覽層級上顯式呈現：

1. Overview
2. Foundry Model
3. Foundry IQ
4. Foundry Agent
5. Foundry Tool
6. Fabric IQ
7. Control Plane

若不想一次擴太多頁，也可採兩階段做法：

### 階段一：先補 4 頁

1. Foundry Model
2. Foundry Agent
3. Foundry Tool
4. Control Plane

### 階段二：再重寫 `03-understand/index.md`

把現有 overview 改成五主軸導讀頁，清楚說明它們之間的關係。

## 建議新增文件

### 1. Foundry Model

建議檔案：

- `workshop/docs/03-understand/00-foundry-model.md`

建議內容：

1. 什麼是 chat model deployment
2. 什麼是 embedding model deployment
3. 為什麼 workshop 要採多模型部署而不是只放單一模型
4. chat model、reasoning model、coding model、router model、image model、embedding model 在解決方案中的角色差異
5. model deployment 與 agent definition 的關係
6. 缺少權限、區域不支援或配額不足時，如何跳過個別模型部署而不阻塞整體流程

### Foundry Model 部署清單

建議把以下模型列為教學上的「目標部署清單」：

1. `gpt-5.4`
2. `gpt-5.4-pro`
3. `gpt-5.3-Codex`
4. `claude-sonnet-4-6`
5. `claude-opus-4-6`
6. `model-router`

另保留現有或必要的基礎模型：

1. `text-embedding-*` 系列作為向量化與檢索基礎
2. 若需 image generation，另補 `gpt-image-1`

### Foundry Model 教學策略

文件不應要求所有環境都成功部署上述所有模型，而應採「最佳努力 + 失敗即跳過」模式。

建議寫法：

1. 先部署 workshop 主流程必需模型
   - 例如：一個主要 chat / orchestration model
   - 一個 embedding model

2. 再依序嘗試部署進階模型
   - `gpt-5.4`
   - `gpt-5.4-pro`
   - `gpt-5.3-Codex`
   - `claude-sonnet-4-6`
   - `claude-opus-4-6`
   - `model-router`

3. 若遇到任一情況，直接跳過並記錄 warning
   - 權限不足
   - 該 subscription / region 無配額
   - 模型在該租戶不可用
   - API / SKU / preview 條件不成立

4. 最後輸出「已成功部署模型清單」供講師於 UI 手動展示

### Foundry Model 簡單差異與比較

文件應提供一個簡單對照表，重點不是做完整 benchmark，而是讓講師能快速說明用途差異。

建議比較維度：

1. 主要用途
2. 適合的 demo 場景
3. 預期成本 / 延遲取向
4. 是否適合當 orchestration 預設模型
5. 是否建議作為進階展示模型

建議敘事方向：

1. `gpt-5.4`
   - 通用主力模型
   - 適合做 agent orchestration、工具調用、綜合問答

2. `gpt-5.4-pro`
   - 較高階推理或高品質回答展示
   - 適合講師在 UI 中示範同題不同模型品質差異

3. `gpt-5.3-Codex`
   - 偏向程式、規則、結構化輸出或開發導向情境
   - 適合示範 code-related 或 workflow-related 任務，不建議當通用主模型唯一選項

4. `claude-sonnet-4-6`
   - 中高階通用模型
   - 適合與 GPT 系列做跨模型比較，作為 alternate orchestration choice

5. `claude-opus-4-6`
   - 偏高品質、高成本、高階展示模型
   - 適合做「品質優先」展示，不建議當所有 demo 的預設基線

6. `model-router`
   - 偏路由與彈性選模能力展示
   - 適合拿來說明 control plane / model strategy，而不是當唯一 demo 主角

### Foundry Model 驗收方向

1. 主流程至少有一個可用的 orchestration model 與一個 embedding model
2. 其餘模型採可用即展示、不可用即跳過
3. 文件必須清楚標註「跳過不影響 workshop 主流程」

主要參考來源：

- `infra/modules/foundry.bicep`
- `scripts/07_create_foundry_agent.py`

### 2. Foundry Agent

建議檔案：

- `workshop/docs/03-understand/02-foundry-agent.md`

建議內容：

1. 什麼是 orchestrator agent
2. 什麼是 `PromptAgentDefinition`
3. agent instructions 如何組成
4. agent 如何判斷該用哪個 tool
5. agent create、get、test 的基本流程
6. 如何啟用與查看 agent trace
7. 如何把 agent publish 成可分享的 application
8. 如何延伸到 Teams / Microsoft 365 Copilot 發佈

### Foundry Agent 必要補強

文件需把下列兩個能力納入 agent 教學範圍：

1. `agent trace`
   - 說明 trace、span、tool call、latency、input/output 在教學中的觀察重點
   - 說明 tracing 會把資料寫到 Application Insights
   - 強調 trace 是教學與除錯用途，不必在 workshop 內做複雜自訂 instrumentation

2. `publish to Teams`
   - 說明 agent 在 project 中開發完成後，可 publish 成 Agent Application
   - 說明 publish 後有穩定 endpoint、獨立 identity、獨立 RBAC scope
   - 說明可延伸發布到 Microsoft 365 Copilot 與 Teams
   - 說明 publish 後 identity 改變，原本可用的工具權限可能需要重新指派

### Foundry Agent 教學策略

1. 主流程只要求完成 agent create 與本地 / script 測試
2. trace 視為進階但高價值 demo
3. publish to Teams 視為延伸展示，不應阻塞 workshop 主流程
4. 若缺少 `Azure AI Project Manager` 或相關 RBAC，直接跳過 publish 步驟並記錄為選配能力未啟用

### Foundry Agent Demo 建議

建議示範順序：

1. 建立 agent
2. 執行既有對話測試流程
3. 在 Foundry UI 檢視 trace 與 tool calls
4. 若權限允許，再示範 publish 與 Teams / M365 Copilot 發布入口

主要參考來源：

- `scripts/07_create_foundry_agent.py`
- `scripts/08_test_foundry_agent.py`
- Agent tracing 與 publish 相關 Microsoft Learn 文件

### 3. Foundry Tool

建議檔案：

- `workshop/docs/03-understand/03-foundry-tool.md`

建議內容：

1. 什麼是 function tool
2. `search_documents` 與 `execute_sql` 的責任邊界
3. tool parameters schema 怎麼定義
4. tool call output 如何回填給 response loop
5. 為什麼這個 repo 用兩個 tool 就能示範複合查詢

### Foundry Tool 補強範圍

除現有 `search_documents` 與 `execute_sql` 之外，文件需納入以下能力的教學規劃：

1. `Content Understanding`
2. `Browser Automation`
3. `Web Search`
4. `PII`
5. `Image Generation`

### 各工具的教學定位

1. `Content Understanding`
   - 用途：把文件、圖片、影音等內容轉成可用於後續 agent 流程的結構化結果
   - 教學重點：使用 prebuilt analyzer 做最小示範即可
   - 部署策略：若 Foundry 資源與預設模型連線未完成，直接跳過，不阻塞主流程

2. `Browser Automation`
   - 用途：讓 agent 在受控瀏覽器工作區中進行網站操作
   - 教學重點：示範 sandboxed browser session、tool call 與 trace 檢視
   - 依賴：Playwright workspace 與 project connection
   - 風險：屬 preview，且具安全風險，應僅用 trusted site 做 demo
   - 部署策略：若 Playwright workspace、token 或 connection 無法建立，直接跳過

3. `Web Search`
   - 用途：補足模型知識截止點，做即時公網查詢與來源引用
   - 教學重點：優先採用最簡單的 Web Search 模式
   - 部署策略：若租戶政策禁用或工具不可用，直接跳過，不影響既有 Foundry IQ / Fabric IQ demo

4. `PII`
   - 用途：偵測與遮罩文本中的個資
   - 教學重點：用最小文本範例示範偵測、類別、confidence、redaction policy
   - 部署策略：若 Language / Foundry 資源或 portal 體驗受限，改成 UI 示範或直接跳過

5. `Image Generation`
   - 用途：讓 agent 可產生圖片輸出，補足多模態展示
   - 依賴：除了 orchestrator model 外，需同專案內另有 `gpt-image-1`
   - 教學重點：最小示範即可，例如依 prompt 產圖並在 UI 檢查 tool call
   - 部署策略：若 `gpt-image-1` 無法部署，則整段 image generation 直接標為選配並跳過

### Foundry Tool 教學策略

文件應把工具分成兩層：

1. 主流程工具
   - `search_documents`
   - `execute_sql`

2. 延伸展示工具
   - `Content Understanding`
   - `Browser Automation`
   - `Web Search`
   - `PII`
   - `Image Generation`

這樣可維持目前 workshop 的核心流程不變，同時把更多 Foundry tool capability 納入教學範圍。

### Foundry Tool Demo 設計原則

1. 每個工具都只做一個最小可用 demo
2. sample 流程需長得像目前腳本流程
   - 初始化 client
   - 建立 / 宣告 tool
   - 建立 agent definition
   - 發送最小 request
   - 顯示 tool result
3. 不把所有工具硬塞進同一個 agent demo
4. 以「主 agent + 若干獨立工具示範 agent」的形式最清楚

主要參考來源：

- `scripts/07_create_foundry_agent.py`
- `scripts/08_test_foundry_agent.py`
- Content Understanding、Browser Automation、Web Search、PII、Image Generation 相關 Microsoft Learn 文件

### 4. Control Plane

建議檔案：

- `workshop/docs/03-understand/04-control-plane.md`

建議內容：

1. AI Services account 的角色
2. Foundry project 的角色
3. model deployments 的角色
4. project connections 的角色
5. App Insights 與 Search 如何掛到 project
6. RBAC 為什麼是這個 workshop 能運作的前提
7. control plane 與 runtime path 的差異

主要參考來源：

- `infra/modules/foundry.bicep`
- `workshop/docs/01-deploy/01-deploy-azure.md`

## 建議新增實作原則

為了讓後續文件與程式補強不偏離現有 repo 風格，建議把下列原則寫進計劃：

### 1. 腳本風格一致

新增部署或 demo 腳本時，優先沿用目前 repo 的模式：

1. 用環境變數做主要設定來源
2. 用單檔腳本呈現單一責任
3. 用清楚的 console output 顯示目前步驟
4. 有 warning 就顯示，但不要把選配能力失敗升級成整體流程失敗

### 2. 部署順序一致

建議新能力的文件敘事仍沿用「先 deploy，再 create，再 test，再看 UI」：

1. Deploy infrastructure / connections
2. Create or configure model / tool / agent
3. Run minimal demo
4. Go to UI for manual walkthrough

### 3. 選配能力不得卡住主流程

以下能力預設列為選配：

1. 額外模型部署
2. Browser Automation
3. Web Search
4. PII
5. Image Generation
6. Agent trace
7. Publish to Teams / M365 Copilot

只要主流程的 document search、data query、orchestrator agent 仍可運作，就算 workshop 可成功完成。

## 建議同步更新文件

### 1. Deep dive 首頁

檔案：

- `workshop/docs/03-understand/index.md`

要做的事：

1. 把現有 architecture overview 改成五主軸導覽
2. 加入一張顯示 `model -> agent -> tools -> IQ -> data sources` 關係的圖
3. 明確說明 `Fabric IQ` 是資料語義層，`Foundry IQ` 是知識擷取層
4. 明確說明 `Control Plane` 是平台設定與治理層

### 2. MkDocs 導覽

檔案：

- `workshop/mkdocs.yml`

要做的事：

1. 在 `Deep dive` 下加入新頁面
2. 重新排序導覽，讓五主軸出現得更清楚

### 3. 首頁與部署頁文案

建議補強檔案：

- `README.md`
- `workshop/docs/index.md`
- `workshop/docs/01-deploy/index.md`

要做的事：

1. 把目前的敘事從「Foundry IQ + Fabric IQ」調整成「五主軸架構」
2. 避免讓讀者誤以為 Foundry 只有 IQ 功能，沒有 model、agent、tool、control plane 的平台層次

## 執行分期

### Phase 1：文件骨架

目標：先把主軸補齊，讓導覽可見。

工作項目：

1. 新增 4 個 Markdown 頁面
2. 更新 `workshop/mkdocs.yml`
3. 更新 `03-understand/index.md`
4. 在 Foundry Model、Foundry Tool、Foundry Agent 三頁中明確標示必要能力與選配能力

### Phase 2：內容深化

目標：讓每一頁不只是名詞介紹，而是能回答客戶與內部技術同仁的問題。

工作項目：

1. 為每頁加入架構圖或流程圖
2. 補上 repo 中實際對應的程式位置
3. 加入常見問答與 talking points
4. 加入「若部署失敗則跳過」的範例流程與 warning 文案
5. 補上多模型差異與工具適用場景比較表

### Phase 3：整體敘事對齊

目標：讓首頁、部署流程、PoC 示範、deep dive 的說法一致。

工作項目：

1. 更新首頁與 README 敘事
2. 調整 deploy 頁與 demo 頁，讓五主軸與操作流程對得上
3. 檢查是否有舊文案只提 IQ、不提 Foundry 平台構成
4. 確保所有新增 demo 都維持與既有腳本相近的寫法與輸出風格

## 驗收標準

完成後應能達到以下結果：

1. 使用者能從網站導覽明確看到五個主軸。
2. 每個主軸至少有一頁可獨立閱讀的技術說明。
3. 每個主軸都能對應到 repo 中的實作檔案或 IaC 定義。
4. 文件能回答「這個 solution 的 model、agent、tool、IQ、control plane 各自是什麼」。
5. 首頁、deep dive、部署頁的說法一致，不再只有 `Foundry IQ + Fabric IQ` 的雙主軸敘事。
6. 文件已清楚區分必要能力與選配能力。
7. 文件已明確說明：若某些模型或進階工具缺少權限、區域支援或配額，應直接跳過，不阻塞部署流程。
8. 多模型部署、進階 tool、trace、publish 的 demo 敘事與現有 repo 程式風格一致。

## 建議下一步

若要直接開始落地，建議依下列順序執行：

1. 先新增 `Control Plane` 頁面
2. 再新增 `Foundry Agent` 與 `Foundry Tool` 頁面
3. 最後補 `Foundry Model` 頁面
4. 完成後再統一調整 `03-understand/index.md` 與 `workshop/mkdocs.yml`

這樣可以先把最大缺口補起來，再整理整體敘事。

## 本次追加需求摘要

為避免後續落地時遺漏，本次使用者追加的要求應明確視為計劃輸入條件：

1. `Foundry Model`
   - 補上多模型部署規劃：
     - `gpt-5.4`
     - `gpt-5.4-pro`
     - `gpt-5.3-Codex`
     - `claude-sonnet-4-6`
     - `claude-opus-4-6`
     - `model-router`
   - 補上簡單差異與比較
   - 若缺權限或部署條件不足，直接跳過

2. `Foundry Tool`
   - 補上 `Content Understanding`
   - 補上 `Browser Automation`
   - 補上 `Web Search`
   - 補上 `PII`
   - 補上 `Image Generation`

3. `Foundry Agent`
   - 補上 `agent trace`
   - 補上 `publish to Teams`

4. 全部內容都要以教學目標為主
   - 部署與 demo 要簡單扼要
   - sample flow 要接近現有程式邏輯、寫法與風格
   - 部署完成後主要由講師在 UI 手動帶看