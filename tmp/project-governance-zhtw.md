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
2. Foundry IQ
3. Foundry Agent
4. Foundry Tool
5. Fabric IQ
6. Control Plane

這個結構的目標是把原本偏向 `Foundry IQ + Fabric IQ` 的展示，補齊成可完整講解 Foundry 平台能力與控制面的教學路徑。

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
- 繁體中文內容在英文架構穩定後整批落地
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

## 後續仍可追蹤的少量事項

### 文件微調

- Deep dive 頁面的 footer 導航順序仍可再做一次整體檢視與微調

### 翻譯工作

- 若啟動下一輪繁中落地，應直接依 `translation-standards-zhtw.md` 執行，不再拆回 task-by-task 筆記
