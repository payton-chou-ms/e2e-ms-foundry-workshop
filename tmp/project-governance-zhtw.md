# 專案治理與關鍵決策（繁體中文）

## 目的

這份文件保留目前仍然有效的治理規則、教學方向與交付邊界，作為後續維護與交接的共同基準。

## 內容來源治理

### 唯一主要內容來源

- `workshop/docs/` 是所有正式使用者文件的唯一主要來源。
- root `site/` 與 `workshop/site/` 一律視為建置輸出，不作為編輯來源。
- `guides/` 只保留導向頁、review note 或補充說明，不再承擔第二套正式教學內容。

### tmp/ 的角色

- `tmp/` 只保留交接用的整理文件。
- `tmp/` 不再保留逐項任務工作單、一次性盤點稿、完成後即失效的中間紀錄。

## 教學架構決策

### Deep Dive 主軸

Deep dive 區段目前採用下列主軸組織技術敘事：

1. Foundry Model
2. Foundry Agent
3. Foundry Tool
4. 智慧接地層（Foundry IQ + Fabric IQ）
5. Foundry Control Plane
6. 多代理程式延伸

這個結構的目標，是先用五個核心主軸講清楚單代理程式 workshop 的主要技術敘事，再把多角色工作流放到第六個延伸主題中，避免高層導覽和實際頁面結構脫節。

### 教學優先順序

1. 先讓主流程可部署、可示範、可驗證
2. 再補齊可教學的技術解釋與導覽
3. 最後才處理進階展示能力與額外模型

### 教學方式

- 文件與腳本以最小可行示範為主
- 部署完成後，以 UI 與 portal 講解為主
- 文件中的流程要盡量對齊現有 repo 腳本與 IaC，而不是另起一套抽象架構

## 能力邊界

### 必要能力

以下能力屬於 workshop 主流程必要條件：

- `azd up` 可部署主流程所需 Azure 資源
- 至少一個可用的 orchestration model
- 至少一個可用的 embedding model
- 文件檢索主流程
- 結構化資料查詢主流程
- Orchestrator Agent 建立與基本測試流程

### 選配能力

以下能力屬於進階示範或補強內容，不得阻塞主流程：

- 額外模型部署
- agent trace
- publish to Teams / Microsoft 365 Copilot
- Content Understanding
- Browser Automation
- Web Search
- PII
- Image Generation

### 選配能力原則

- 若因權限、區域、配額、preview 條件或租戶政策無法啟用，應 `warning` 或 `skip`
- 單一選配能力失敗不得中斷主流程部署或驗證
- 文件中必須清楚標註前置條件與失敗時的行為

## 交付策略

### 文件與實作的承諾層級

- 主流程必要能力必須可執行、可測試
- 選配能力至少要有清楚文件、最小 demo 設計與明確 skip 條件
- 若某項選配能力已具備 demo 腳本，仍應視為 guarded execution，而非保證所有租戶都能跑通

### 語系策略

- 英文主文件先穩定
- 繁體中文內容在英文架構穩定後整批落地，並以 `Microsoft Foundry`、`Foundry project`、`Foundry Control Plane` 為正式對外用語
- 目前先以單源翻譯規範治理，不預先綁定雙語站台架構

## 實作與維護原則

### 腳本風格

新增腳本或補強既有腳本時，遵循以下慣例：

1. 以環境變數為主要設定來源
2. 單檔腳本單一責任
3. console output 清楚
4. warning 與 skip 明確可見

### 最佳努力策略

- 多模型與進階工具採最佳努力部署與 guarded execution
- `best-effort` 的意思是顯式允許某能力缺席，不是隱性吞掉真正的主流程錯誤

## 本輪已固化的結論

- `workshop/docs/` 已成為唯一正式內容來源
- Deep dive 已補齊 Foundry Agent、Foundry Tool、Control Plane 等關鍵教學缺口
- optional demos 已採獨立腳本與非阻塞策略
- 文件、IaC、腳本已對齊目前 Foundry / Azure SDK 的可行路徑

## Current State / Last Consolidation

### 本輪交付總結

本輪工作已完成下列幾類補強：

1. 治理與內容來源收斂
2. Deep dive 資訊架構補強
3. IaC 與 Foundry 腳本支援
4. 選配能力 demo 與 guarded execution
5. 首頁、部署敘事與教學文件對齊
6. 翻譯規範與交付規範整理

### 主要成果

#### 文件成果

- 補齊 `Foundry Model`、`Foundry Agent`、`Foundry Tool`、`Control Plane` 等 deep dive 內容
- 重寫 `03-understand` overview，讓 Deep dive 結構更完整
- 更新首頁與部署路徑敘事，使 workshop 主流程與 Foundry-only 路徑更清楚
- 將正式內容來源收斂到 `workshop/docs/`

#### IaC 與平台成果

- 補強 `infra/main.bicep` 與相關 module 輸出，讓 Control Plane 敘事有對應的實際資源與 output
- 導入較清楚的必要模型與選配模型策略
- 補上 optional model deployment 的 best-effort 概念與輸出摘要

#### 腳本成果

- 導入 `00_admin_prepare_demo.py` 作為公開 prepare 入口，並保留舊 build pipeline 作為內部實作
- 將 tool contract 集中於 `scripts/foundry_tool_contract.py`
- 增加 tracing、publish precheck 與多個 optional demos 的 guarded execution 行為
- 對齊較新的 Azure / Foundry SDK 類型與執行方式

### 選配能力結論

| 能力 | 目前定位 | 保留方式 | 原則 |
| --- | --- | --- | --- |
| Content Understanding | 選配 demo | 獨立腳本 | 不阻塞主流程 |
| Browser Automation | 選配 demo | 獨立腳本 | 缺 connection 時應 skip |
| Web Search | 選配 demo | 獨立腳本 | 不進主流程 tool loop |
| PII | 選配 demo | 獨立腳本 | 缺前提時應 skip |
| Image Generation | 選配 demo | 獨立腳本 | 受模型與區域可用性限制 |
| Agent trace | 選配支援 | env flag 控制 | tracing 失敗只 warning |
| Publish to Teams / M365 Copilot | 選配支援 | precheck + 文件 | 不阻塞主流程 |

### 關鍵實作落點

#### 腳本與模組

- `scripts/00_admin_prepare_demo.py`
- `scripts/07_create_foundry_agent.py`
- `scripts/08_test_foundry_agent.py`
- `scripts/09_demo_content_understanding.py`
- `scripts/10_demo_browser_automation.py`
- `scripts/11_demo_web_search.py`
- `scripts/12_demo_pii_redaction.py`
- `scripts/13_demo_image_generation.py`
- `scripts/foundry_trace.py`
- `scripts/foundry_tool_contract.py`

#### 文件與站台

- `workshop/docs/03-understand/index.md`
- `workshop/docs/03-understand/00-foundry-model.md`
- `workshop/docs/03-understand/02-foundry-agent.md`
- `workshop/docs/03-understand/03-foundry-tool.md`
- `workshop/docs/03-understand/04-control-plane.md`
- `README.md`
- `workshop/docs/index.md`
- `workshop/docs/01-deploy/index.md`

#### IaC

- `infra/main.bicep`
- `infra/main.parameters.json`
- `infra/modules/foundry.bicep`

### 驗證結果摘要

#### 主流程

已完成的驗證方向包含：

- Bicep 可編譯
- 主要 Python 腳本可通過基本語法編譯檢查
- Foundry-only 主流程可完成建置與最小驗證
- 文件、導覽與 deep dive 主軸已落到實際 repo 內容

#### optional demos

optional demos 的驗證原則不是「每個租戶都必須成功」，而是：

- 條件滿足時可做最小示範
- 條件不滿足時能清楚 `skip`
- 不把 preview、region 或 quota 風險擴散到主流程

### 不再保留的內容類型

以下內容已不再保留為獨立文件：

- 單一 task 的工作單與完成紀錄
- 一次性 gap analysis
- 一次性 docs quality scan
- 中間版 teaching plan
- smoke test 原始紀錄稿

這些資訊若仍重要，應吸收到本檔、`translation-standards-zhtw.md` 或其他仍保留的治理文件。

## 後續仍可追蹤的少量事項

### 文件微調

- Deep dive 頁面的 footer 導航順序仍可再做一次整體檢視與微調

### 翻譯工作

- 若啟動下一輪繁中落地，應直接依 `translation-standards-zhtw.md` 執行，不再拆回 task-by-task 筆記
