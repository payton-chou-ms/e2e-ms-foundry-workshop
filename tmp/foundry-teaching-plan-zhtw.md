# Foundry 教學主軸補強計劃（繁體中文）

## 目標

將目前以 `Foundry IQ + Fabric IQ` 為核心的 workshop，補強為可清楚對外說明下列五個主軸的教學內容：

1. Foundry Model
2. Foundry IQ
3. Foundry Agent
4. Foundry Tool
5. Control Plane

本計劃的重點不是重寫整個 workshop，而是補上目前 repo 已有實作、但尚未被文件清楚教學化的部分。

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
   - IaC 有部署 chat model 與 embedding model。
   - 但目前文件幾乎沒有說明這兩種 model 的角色差異、為何這樣選、如何被 agent 使用。

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
3. 這個 repo 目前使用哪些 model
4. chat model 與 embedding model 各自負責哪一段流程
5. model deployment 與 agent definition 的關係

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

主要參考來源：

- `scripts/07_create_foundry_agent.py`
- `scripts/08_test_foundry_agent.py`

### 3. Foundry Tool

建議檔案：

- `workshop/docs/03-understand/03-foundry-tool.md`

建議內容：

1. 什麼是 function tool
2. `search_documents` 與 `execute_sql` 的責任邊界
3. tool parameters schema 怎麼定義
4. tool call output 如何回填給 response loop
5. 為什麼這個 repo 用兩個 tool 就能示範複合查詢

主要參考來源：

- `scripts/07_create_foundry_agent.py`
- `scripts/08_test_foundry_agent.py`

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

### Phase 2：內容深化

目標：讓每一頁不只是名詞介紹，而是能回答客戶與內部技術同仁的問題。

工作項目：

1. 為每頁加入架構圖或流程圖
2. 補上 repo 中實際對應的程式位置
3. 加入常見問答與 talking points

### Phase 3：整體敘事對齊

目標：讓首頁、部署流程、PoC 示範、deep dive 的說法一致。

工作項目：

1. 更新首頁與 README 敘事
2. 調整 deploy 頁與 demo 頁，讓五主軸與操作流程對得上
3. 檢查是否有舊文案只提 IQ、不提 Foundry 平台構成

## 驗收標準

完成後應能達到以下結果：

1. 使用者能從網站導覽明確看到五個主軸。
2. 每個主軸至少有一頁可獨立閱讀的技術說明。
3. 每個主軸都能對應到 repo 中的實作檔案或 IaC 定義。
4. 文件能回答「這個 solution 的 model、agent、tool、IQ、control plane 各自是什麼」。
5. 首頁、deep dive、部署頁的說法一致，不再只有 `Foundry IQ + Fabric IQ` 的雙主軸敘事。

## 建議下一步

若要直接開始落地，建議依下列順序執行：

1. 先新增 `Control Plane` 頁面
2. 再新增 `Foundry Agent` 與 `Foundry Tool` 頁面
3. 最後補 `Foundry Model` 頁面
4. 完成後再統一調整 `03-understand/index.md` 與 `workshop/mkdocs.yml`

這樣可以先把最大缺口補起來，再整理整體敘事。