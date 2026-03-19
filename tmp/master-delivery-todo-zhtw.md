# 完整交付 To-Do List（程式、文件、翻譯、測試）

## Summary

### 進度總覽

| 類別 | 數量 | 任務 |
| --- | --- | --- |
| 已完成 | 35 | T-00 ~ T-34 |
| 未完成 | 0 | — |
| 後續新增 | 見下方 | T-35 |

### 已完成任務詳細紀錄

- 已完成任務的細節、產出與驗證，已移到：`tmp/master-delivery-completed-zhtw.md`

### 完整掃描後發現的後續改善項目

| Task | 主題 | 說明 |
| --- | --- | --- |
| T-35 | Deep Dive footer 連結導航順序微調 | 部分 Deep Dive 頁面的 footer 前後頁連結未完全按照六主軸順序排列（如 00-foundry-model 跳到 01-foundry-iq，但中間少了 Agent/Tool）。目前不影響功能，但可考慮統一。 |
| T-26 | 未開始 | T-25 | T-25 |
| T-27 | 未開始 | T-25 | T-25 |
| T-28 | 未開始 | T-25 | T-25 |
| T-29 | 未開始 | T-17, T-25 | T-25 |
| T-30 | 未開始 | T-25 | T-25 |
| T-31 | 未開始 | T-25 | T-25 |
| T-32 | 未開始 | T-26 ~ T-31 | T-26 ~ T-31 |
| T-33 | 未開始 | T-32 | T-32 |
| T-34 | 未開始 | 最終驗收任務 | 建議待 T-24 與 T-33 後執行 |

## 目的

這份文件整理目前 repo 若要依據下列兩份計劃完整落地所需的全部工作：

1. `tmp/foundry-teaching-plan-zhtw.md`
2. `tmp/translation-plan-zhtw.md`

目標不是只補單一頁文件，而是把：

- Foundry 教學主軸補強
- 程式與 IaC 支援
- 文件導覽與敘事重整
- 繁中翻譯
- 測試與驗證

全部拆成可執行、可排程、可平行處理的工作清單。

## 交付定義

完成後應至少達成：

1. `Deep dive` 可清楚呈現五主軸：
   - Foundry Model
   - Foundry IQ
   - Foundry Agent
   - Foundry Tool
   - Control Plane
2. 相關程式與 IaC 能支撐文件中承諾的最小 demo。
3. 必要能力與選配能力有清楚區分。
4. 所有使用者可見文件具備繁中版本或明確翻譯策略。
5. 建站、文件連結、主要腳本與關鍵流程至少完成一次驗證。

## 規劃原則

1. `workshop/docs/` 是唯一主要內容來源。
2. 先完成英文主流程與技術骨架，再做繁中全面落地。
3. 先保主流程可運作，再補選配能力。
4. 可選功能失敗時應 warning 並跳過，不阻塞 workshop 主流程。
5. 所有新功能、文件與測試，都要盡量沿用目前 repo 的腳本風格。

## 平行處理標記說明

| 標記 | 意義 |
| --- | --- |
| `否` | 必須等前置工作完成後才能安全開始 |
| `可部分平行` | 可先啟動研究或草稿，但合併前需等前置工作 |
| `是` | 幾乎可獨立進行，適合交給另一個 Agent |

## 建議 Agent 分工

| Agent 類型 | 建議負責 |
| --- | --- |
| Agent A: IaC / Platform | Bicep、RBAC、Connections、模型部署策略 |
| Agent B: App / Script | `scripts/` 中 agent、tool、trace、publish 相關程式 |
| Agent C: Docs / English | `workshop/docs/` 英文技術文件與導覽 |
| Agent D: Translation | 繁中翻譯、術語套用、review checklist |
| Agent E: QA / Validation | Build、腳本 smoke test、文件連結與導覽驗證 |

## 總體執行順序

### Phase 0: 對齊範圍與驗收

- 確認必要能力與選配能力邊界
- 確認本次要做到「文件說明」還是「程式可執行 demo」
- 確認繁中站台策略：單語覆蓋或雙語並存

### Phase 1: 平台與程式骨架

- 補 Control Plane、Model、Agent、Tool 所需程式與 IaC

### Phase 2: 英文文件補完

- 補四個新頁面與 Deep Dive 導覽重整

### Phase 3: 測試與技術驗證

- 驗證部署、建站、主要腳本、選配能力的 skip 行為

### Phase 4: 繁中翻譯

- 依既有 glossary 與 style guide 逐批翻譯

### Phase 5: 最終整體驗收

- 做一次完整 walkthrough、文檔檢查、站台檢查與 smoke test

## 完整 To-Do List

已完成任務的詳細內容已移至：`tmp/master-delivery-completed-zhtw.md`

---

## T-00 專案對齊與決策紀錄

- 狀態：已完成
- 類型：治理 / 規格
- 平行處理：否
- 建議 Agent：Agent A 或 Agent C
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-00-delivery-decisions-zhtw.md`
- 依賴：無

---

## T-01 盤點現有實作與缺口

- 狀態：已完成
- 類型：分析
- 平行處理：是
- 建議 Agent：Agent A + Agent B + Agent C
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-01-gap-analysis-zhtw.md`
- 依賴：T-00

---

## T-02 設計五主軸資訊架構

- 狀態：已完成
- 類型：文件架構
- 平行處理：可部分平行
- 建議 Agent：Agent C
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-02-information-architecture-zhtw.md`
- 依賴：T-01

---

## T-03 擴充 Bicep：多模型部署策略

- 狀態：已完成
- 類型：程式 / IaC
- 平行處理：可部分平行
- 建議 Agent：Agent A
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-03-multi-model-strategy-zhtw.md`
- 依賴：T-00, T-01

---

## T-04 擴充 Bicep：Control Plane 文件所需輸出

- 狀態：已完成
- 類型：程式 / IaC
- 平行處理：是
- 建議 Agent：Agent A
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`infra/main.bicep`, `infra/modules/foundry.bicep`
- 依賴：T-01

---

## T-05 擴充 agent 程式：agent trace 支援

- 狀態：已完成
- 類型：程式
- 平行處理：可部分平行
- 建議 Agent：Agent B
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-05-agent-tracing-zhtw.md`, `scripts/foundry_trace.py`, `scripts/07_create_foundry_agent.py`, `scripts/08_test_foundry_agent.py`, `scripts/requirements.txt`
- 依賴：T-01, T-04

---

## T-06 擴充 agent 程式：publish to Teams / M365 Copilot 規劃

- 狀態：已完成
- 類型：程式 / 文件支援
- 平行處理：可部分平行
- 建議 Agent：Agent B
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-06-publish-plan-zhtw.md`, `scripts/09_publish_foundry_agent.py`
- 依賴：T-00, T-01

---

## T-07 擴充 tool 程式：主流程 tool 文件對齊

- 狀態：已完成
- 類型：程式 / 文件對齊
- 平行處理：是
- 建議 Agent：Agent B
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-07-tool-contract-alignment-zhtw.md`, `scripts/foundry_tool_contract.py`
- 依賴：T-01

---

## T-08 評估延伸工具：Content Understanding

- 狀態：已完成
- 類型：研究 / 選配實作
- 平行處理：是
- 建議 Agent：Agent B
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-08-content-understanding-zhtw.md`, `scripts/09_demo_content_understanding.py`
- 依賴：T-00

---

## T-09 評估延伸工具：Browser Automation

- 狀態：已完成
- 類型：研究 / 選配實作
- 平行處理：是
- 建議 Agent：Agent B
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-09-browser-automation-zhtw.md`, `scripts/10_demo_browser_automation.py`
- 依賴：無

---

## T-10 評估延伸工具：Web Search

- 狀態：已完成
- 類型：研究 / 選配實作
- 平行處理：是
- 建議 Agent：Agent B
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-10-web-search-zhtw.md`, `scripts/11_demo_web_search.py`
- 依賴：無

---

## T-11 評估延伸工具：PII

- 狀態：已完成
- 類型：研究 / 選配實作
- 平行處理：是
- 建議 Agent：Agent B
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-11-pii-zhtw.md`, `scripts/12_demo_pii_redaction.py`, `scripts/requirements.txt`
- 依賴：無

---

## T-12 評估延伸工具：Image Generation

- 狀態：已完成
- 類型：研究 / 選配實作
- 平行處理：是
- 建議 Agent：Agent B + Agent A
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-12-image-generation-zhtw.md`, `scripts/13_demo_image_generation.py`, `scripts/optional_demo_utils.py`
- 依賴：T-03

---

## T-13 撰寫英文頁：Foundry Model

- 狀態：已完成
- 類型：文件
- 平行處理：可部分平行
- 建議 Agent：Agent C
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`workshop/docs/03-understand/00-foundry-model.md`
- 依賴：T-02, T-03

---

## T-14 撰寫英文頁：Foundry Agent

- 狀態：已完成
- 類型：文件
- 平行處理：可部分平行
- 建議 Agent：Agent C
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-14-foundry-agent-page-zhtw.md`, `workshop/docs/03-understand/02-foundry-agent.md`

### 目標檔案

- `workshop/docs/03-understand/02-foundry-agent.md`

### 內容

- PromptAgentDefinition
- instructions 組成
- tool selection
- create / get / test flow
- trace
- publish

### 依賴

- T-02
- T-05
- T-06

---

## T-15 撰寫英文頁：Foundry Tool

- 狀態：已完成
- 類型：文件
- 平行處理：可部分平行
- 建議 Agent：Agent C
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-15-foundry-tool-page-zhtw.md`, `workshop/docs/03-understand/03-foundry-tool.md`

### 目標檔案

- `workshop/docs/03-understand/03-foundry-tool.md`

### 內容

- function tool
- `search_documents`
- `execute_sql`
- tool schema
- tool execution loop
- 延伸工具能力分層

### 依賴

- T-02
- T-07
- T-08
- T-09
- T-10
- T-11
- T-12

---

## T-16 撰寫英文頁：Control Plane

- 狀態：已完成
- 類型：文件
- 平行處理：可部分平行
- 建議 Agent：Agent C
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`workshop/docs/03-understand/04-control-plane.md`
- 依賴：T-02, T-04

---

## T-17 重寫英文頁：Deep Dive Overview

- 狀態：已完成
- 類型：文件
- 平行處理：否
- 建議 Agent：Agent C
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-17-deep-dive-overview-zhtw.md`, `workshop/docs/03-understand/index.md`

### 目標檔案

- `workshop/docs/03-understand/index.md`

### 內容

- 改成五主軸導覽
- 補 `model -> agent -> tools -> IQ -> data sources` 關係
- 對齊新頁面連結

### 依賴

- T-13
- T-14
- T-15
- T-16

---

## T-18 更新 MkDocs 導覽

- 狀態：已完成
- 類型：文件 / 設定
- 平行處理：否
- 建議 Agent：Agent C
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-18-mkdocs-nav-update-zhtw.md`, `workshop/mkdocs.yml`

### 目標檔案

- `workshop/mkdocs.yml`

### 內容

- Deep dive 導覽加入新頁面
- 調整排序
- 對齊頁面標題

### 依賴

- T-17

---

## T-19 更新首頁與部署頁敘事

- 狀態：已完成
- 類型：文件
- 平行處理：可部分平行
- 建議 Agent：Agent C
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-19-homepage-deploy-narrative-zhtw.md`, `README.md`, `workshop/docs/index.md`, `workshop/docs/01-deploy/index.md`

### 目標檔案

- `README.md`
- `workshop/docs/index.md`
- `workshop/docs/01-deploy/index.md`

### 內容

- 從雙主軸 `Foundry IQ + Fabric IQ` 擴展為五主軸敘事
- 但保留目前 workshop 主流程的簡潔性

### 依賴

- T-17

---

## T-20 為新頁面補架構圖或 Mermaid 圖

- 狀態：已完成
- 類型：文件資產
- 平行處理：是
- 建議 Agent：Agent C
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`workshop/docs/03-understand/index.md`, `workshop/docs/03-understand/00-foundry-model.md`, `workshop/docs/03-understand/04-control-plane.md`
- 依賴：T-02

---

## T-21 撰寫英文 FAQ / talking points 補強

- 狀態：已完成
- 類型：文件
- 平行處理：是
- 建議 Agent：Agent C
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-21-faq-talking-points-zhtw.md`, `workshop/docs/03-understand/00-foundry-model.md`, `workshop/docs/03-understand/02-foundry-agent.md`, `workshop/docs/03-understand/03-foundry-tool.md`, `workshop/docs/03-understand/04-control-plane.md`

### 內容

- Foundry Model 常見問答
- Foundry Agent 常見問答
- Foundry Tool 常見問答
- Control Plane 常見問答

### 依賴

- T-13
- T-14
- T-15
- T-16

---

## T-22 主流程腳本 smoke test

- 狀態：已完成
- 類型：測試
- 平行處理：否
- 建議 Agent：Agent E
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-22-main-flow-smoke-test-zhtw.md`, `scripts/08_test_foundry_agent.py`

### 內容

- 驗證 `00_build_solution.py`
- 驗證 `07_create_foundry_agent.py`
- 驗證 `08_test_foundry_agent.py`
- 驗證既有 Foundry-only 路徑

### 依賴

- T-03
- T-05
- T-07

### 驗收

- 主流程可執行或至少在無雲端資源時給出正確錯誤 / guardrail

---

## T-23 選配能力 smoke test

- 狀態：已完成
- 類型：測試
- 平行處理：是
- 建議 Agent：Agent E
- 詳細紀錄：`tmp/master-delivery-completed-zhtw.md`
- 主要產出：`tmp/t-23-optional-extension-smoke-test-zhtw.md`

### 內容

- trace
- publish
- Content Understanding
- Browser Automation
- Web Search
- PII
- Image Generation

### 驗收

- 每個功能都能被歸類為：
  - 可執行
  - 不可用但可正確 skip

### 依賴

- T-05 ~ T-12

---

## T-24 建站驗證（英文）

- 狀態：未開始
- 類型：測試
- 平行處理：否
- 建議 Agent：Agent E

### 內容

- `mkdocs build --strict`
- 驗證 nav、頁面連結、錨點、admonition、表格

### 依賴

- T-18
- T-19

---

## T-25 開始繁中翻譯：首頁與導覽

- 狀態：未開始
- 類型：翻譯
- 平行處理：可部分平行
- 建議 Agent：Agent D

### 範圍

- `README.md`
- `workshop/README.md`
- `workshop/docs/index.md`
- `workshop/mkdocs.yml`

### 依賴

- T-19
- `tmp/translation-glossary-zhtw.md`
- `tmp/translation-style-guide-zhtw.md`

---

## T-26 繁中翻譯：Get Started

- 狀態：未開始
- 類型：翻譯
- 平行處理：是
- 建議 Agent：Agent D

### 範圍

- `workshop/docs/00-get-started/index.md`
- `workshop/docs/00-get-started/workshop-flow.md`

### 依賴

- T-25

---

## T-27 繁中翻譯：Deploy

- 狀態：未開始
- 類型：翻譯
- 平行處理：是
- 建議 Agent：Agent D

### 範圍

- `workshop/docs/01-deploy/index.md`
- `workshop/docs/01-deploy/00-admin-deploy-share.md`
- `workshop/docs/01-deploy/00-participant-run-validate.md`
- `workshop/docs/01-deploy/01-deploy-azure.md`
- `workshop/docs/01-deploy/02-setup-fabric.md`
- `workshop/docs/01-deploy/03-configure.md`
- `workshop/docs/01-deploy/04-run-scenario.md`

### 依賴

- T-25

---

## T-28 繁中翻譯：Customize

- 狀態：未開始
- 類型：翻譯
- 平行處理：是
- 建議 Agent：Agent D

### 範圍

- `workshop/docs/02-customize/index.md`
- `workshop/docs/02-customize/02-generate.md`
- `workshop/docs/02-customize/03-demo.md`

### 依賴

- T-25

---

## T-29 繁中翻譯：Understand

- 狀態：未開始
- 類型：翻譯
- 平行處理：可部分平行
- 建議 Agent：Agent D

### 範圍

- `workshop/docs/03-understand/index.md`
- `workshop/docs/03-understand/00-foundry-model.md`
- `workshop/docs/03-understand/01-foundry-iq.md`
- `workshop/docs/03-understand/02-foundry-agent.md`
- `workshop/docs/03-understand/03-foundry-tool.md`
- `workshop/docs/03-understand/02-fabric-iq.md`
- `workshop/docs/03-understand/04-control-plane.md`

### 依賴

- T-17
- T-25

---

## T-30 繁中翻譯：Cleanup

- 狀態：未開始
- 類型：翻譯
- 平行處理：是
- 建議 Agent：Agent D

### 範圍

- `workshop/docs/04-cleanup/index.md`
- `workshop/docs/04-cleanup/next-steps.md`

### 依賴

- T-25

---

## T-31 繁中翻譯：guides 與 VS Code Web 補充文件

- 狀態：未開始
- 類型：翻譯
- 平行處理：是
- 建議 Agent：Agent D

### 範圍

- `guides/deployment_guide.md`
- `infra/vscode_web/README.md`
- `infra/vscode_web/README-noazd.md`

### 依賴

- T-25

---

## T-32 繁中術語稽核與 reviewer checklist 驗證

- 狀態：未開始
- 類型：校對
- 平行處理：可部分平行
- 建議 Agent：Agent D + Agent E

### 內容

- 套用 `tmp/translation-reviewer-checklist-zhtw.md`
- 檢查 glossary 一致性
- 檢查中英混排與格式

### 依賴

- T-26 ~ T-31

---

## T-33 建站驗證（繁中）

- 狀態：未開始
- 類型：測試
- 平行處理：否
- 建議 Agent：Agent E

### 內容

- 重新執行 MkDocs build
- 驗證中文導覽是否正常
- 驗證翻譯後連結、錨點、表格與 admonition 是否正常

### 依賴

- T-32

---

## T-34 最終 walkthrough 與對外驗收

- 狀態：未開始
- 類型：驗收
- 平行處理：否
- 建議 Agent：Agent E + 人工 reviewer

### 內容

- 以講師視角跑一次整體敘事
- 以參與者視角跑一次整體敘事
- 確認首頁、deploy、deep dive、cleanup 說法一致
- 確認五主軸敘事已落地

### 驗收

- 符合 `tmp/foundry-teaching-plan-zhtw.md` 驗收標準
- 符合 `tmp/translation-plan-zhtw.md` 驗收標準

---

## 可平行處理建議

### 可立即平行啟動的工作群

#### 群組 A：平台與程式研究

- T-01
- T-03
- T-04
- T-07
- T-08
- T-09
- T-10
- T-11
- T-12

#### 群組 B：文件骨架設計

- T-02
- T-20

#### 群組 C：翻譯基礎治理

- 已完成：glossary / style guide / reviewer checklist

### 第二波可平行啟動（目前）

在 T-18 / T-19 完成後，目前最合理的平行工作是：

- T-24 建站驗證（英文）
- T-25 開始繁中翻譯：首頁與導覽

### 第三波可平行啟動

在英文頁面定稿後，可平行進行翻譯：

- T-26
- T-27
- T-28
- T-29
- T-30
- T-31

## 不建議平行的工作

以下工作強依賴前置結果，不建議同時多人直接改同一檔案：

- T-18 更新 `workshop/mkdocs.yml`
- T-19 更新首頁與部署頁核心敘事
- T-24 / T-33 建站驗證
- T-34 最終 walkthrough 與驗收

## 最小可行落地順序（建議）

若從目前進度往前推，建議先做這條主線：

1. T-24
2. T-25

這樣可以先完成英文站台驗證，並開始繁中入口內容落地。

之後再做：

3. T-26 ~ T-33
4. T-34

## 備註

1. 若時間有限，可先只完成文件骨架與主流程 code/document alignment，不做所有選配工具的真實可執行 demo。
2. 若要用多個 Agent，最有效率的切法是：
   - 一個 Agent 專做 IaC / platform
   - 一個 Agent 專做 scripts / demo flow
   - 一個 Agent 專做英文文件
   - 一個 Agent 專做繁中翻譯
   - 一個 Agent 專做驗證與回歸檢查
3. 所有選配功能都應保留 skip 文案與 warning path，這是本次教學計劃的重要要求。