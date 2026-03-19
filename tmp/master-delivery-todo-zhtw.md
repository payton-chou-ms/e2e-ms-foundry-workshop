# 完整交付 To-Do List（程式、文件、翻譯、測試）

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

---

## T-00 專案對齊與決策紀錄

- 狀態：已完成
- 類型：治理 / 規格
- 平行處理：否
- 建議 Agent：Agent A 或 Agent C

### 內容

- 明確定義主流程必要能力
- 明確定義選配能力
- 明確定義繁中站台策略
- 明確定義本次是否要做到進階工具真的可跑

### 產出

- 一份決策記錄文件
  - `tmp/t-00-delivery-decisions-zhtw.md`

### 驗收

- 所有後續任務可明確判斷是否屬於必要或選配

---

## T-01 盤點現有實作與缺口

- 狀態：已完成
- 類型：分析
- 平行處理：是
- 建議 Agent：Agent A + Agent B + Agent C

### 內容

- 盤點 `infra/modules/foundry.bicep` 現有 control plane 定義
- 盤點 `scripts/07_create_foundry_agent.py`、`scripts/08_test_foundry_agent.py` 現有 agent / tool 流程
- 盤點 `workshop/docs/03-understand/` 現有文件缺口

### 產出

- 一份 gap analysis 清單
  - `tmp/t-01-gap-analysis-zhtw.md`

### 依賴

- T-00

---

## T-02 設計五主軸資訊架構

- 狀態：已完成
- 類型：文件架構
- 平行處理：可部分平行
- 建議 Agent：Agent C

### 內容

- 設計 `03-understand/` 新導覽順序
- 決定檔名與頁面命名
- 定義各頁互相引用關係

### 目標頁面

- `workshop/docs/03-understand/00-foundry-model.md`
- `workshop/docs/03-understand/01-foundry-iq.md`
- `workshop/docs/03-understand/02-foundry-agent.md`
- `workshop/docs/03-understand/03-foundry-tool.md`
- `workshop/docs/03-understand/02-fabric-iq.md`
- `workshop/docs/03-understand/04-control-plane.md`

### 依賴

- T-01

### 產出

- `tmp/t-02-information-architecture-zhtw.md`

---

## T-03 擴充 Bicep：多模型部署策略

- 狀態：未開始
- 類型：程式 / IaC
- 平行處理：可部分平行
- 建議 Agent：Agent A

### 內容

- 檢視 `infra/modules/foundry.bicep`
- 設計主流程模型與選配模型的參數化方式
- 支援最佳努力部署與失敗跳過策略
- 規劃成功部署模型清單輸出

### 涵蓋模型

- 主流程必要模型
  - 主要 orchestration model
  - embedding model
- 選配模型
  - `gpt-5.4`
  - `gpt-5.4-pro`
  - `gpt-5.3-Codex`
  - `claude-sonnet-4-6`
  - `claude-opus-4-6`
  - `model-router`
  - `gpt-image-1`（若要 image generation demo）

### 依賴

- T-00
- T-01

### 測試

- Bicep syntax / diagnostics
- 參數組合 smoke test
- 選配模型 unavailable 時可跳過

---

## T-04 擴充 Bicep：Control Plane 文件所需輸出

- 狀態：未開始
- 類型：程式 / IaC
- 平行處理：是
- 建議 Agent：Agent A

### 內容

- 確認 project、connections、RBAC、App Insights、Search、Storage 的輸出是否足夠支撐文件敘事
- 若不足，補上必要 output 或註解

### 依賴

- T-01

### 測試

- Bicep diagnostics
- azd output 檢查

---

## T-05 擴充 agent 程式：agent trace 支援

- 狀態：未開始
- 類型：程式
- 平行處理：可部分平行
- 建議 Agent：Agent B

### 內容

- 在 `scripts/07_create_foundry_agent.py` 或相關新腳本補上 trace 啟用策略
- 確認與 Application Insights 的關聯
- 若無權限或功能不可用，輸出 warning 並跳過

### 依賴

- T-01
- T-04

### 測試

- 基本 trace 啟用 smoke test
- trace unavailable 時不阻塞主流程

---

## T-06 擴充 agent 程式：publish to Teams / M365 Copilot 規劃

- 狀態：未開始
- 類型：程式 / 文件支援
- 平行處理：可部分平行
- 建議 Agent：Agent B

### 內容

- 研究是否需要新增腳本或只補文件與 pseudo flow
- 若真的實作，需提供 non-blocking 的 publish 流程
- 記錄 publish 後 identity / RBAC 差異

### 依賴

- T-00
- T-01

### 測試

- 若實作腳本，至少完成 dry-run 或 guarded execution smoke test

---

## T-07 擴充 tool 程式：主流程 tool 文件對齊

- 狀態：未開始
- 類型：程式 / 文件對齊
- 平行處理：是
- 建議 Agent：Agent B

### 內容

- 明確整理 `search_documents` 與 `execute_sql` 的 schema、責任邊界、回應 loop
- 視需要補註解、補 helper、補示例輸出

### 依賴

- T-01

### 測試

- 主流程 tool smoke test
- 文件示例與實際輸出一致性檢查

---

## T-08 評估延伸工具：Content Understanding

- 狀態：未開始
- 類型：研究 / 選配實作
- 平行處理：是
- 建議 Agent：Agent B

### 內容

- 確認最小 demo 方案
- 判斷要做文件示意、腳本示範、還是兩者都做
- 若不可用，定義 skip 條件

### 依賴

- T-00

### 測試

- 最小 demo 或 skip behavior 驗證

---

## T-09 評估延伸工具：Browser Automation

- 狀態：未開始
- 類型：研究 / 選配實作
- 平行處理：是
- 建議 Agent：Agent B

### 內容

- 盤點 Playwright / browser session 依賴
- 定義 trusted-site demo
- 定義無法建立時的 skip 機制

### 測試

- 最小 demo 或 skip behavior 驗證

---

## T-10 評估延伸工具：Web Search

- 狀態：未開始
- 類型：研究 / 選配實作
- 平行處理：是
- 建議 Agent：Agent B

### 內容

- 盤點可行工具接法
- 定義 demo 與 skip 條件

### 測試

- 最小 demo 或 skip behavior 驗證

---

## T-11 評估延伸工具：PII

- 狀態：未開始
- 類型：研究 / 選配實作
- 平行處理：是
- 建議 Agent：Agent B

### 內容

- 定義最小文字範例
- 定義偵測與遮罩 demo
- 定義不可用時的 fallback 或 skip 文案

### 測試

- 最小 demo 或 skip behavior 驗證

---

## T-12 評估延伸工具：Image Generation

- 狀態：未開始
- 類型：研究 / 選配實作
- 平行處理：是
- 建議 Agent：Agent B + Agent A

### 內容

- 確認 `gpt-image-1` 或等價能力的可部署性
- 若可用，定義最小示範腳本
- 若不可用，文件中標示選配並跳過

### 依賴

- T-03

### 測試

- 最小 demo 或 skip behavior 驗證

---

## T-13 撰寫英文頁：Foundry Model

- 狀態：未開始
- 類型：文件
- 平行處理：可部分平行
- 建議 Agent：Agent C

### 目標檔案

- `workshop/docs/03-understand/00-foundry-model.md`

### 內容

- chat / embedding model deployment
- 多模型策略
- 模型角色差異
- 主流程與選配模型
- 不可用時如何跳過

### 依賴

- T-02
- T-03

---

## T-14 撰寫英文頁：Foundry Agent

- 狀態：未開始
- 類型：文件
- 平行處理：可部分平行
- 建議 Agent：Agent C

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

- 狀態：未開始
- 類型：文件
- 平行處理：可部分平行
- 建議 Agent：Agent C

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

- 狀態：未開始
- 類型：文件
- 平行處理：可部分平行
- 建議 Agent：Agent C

### 目標檔案

- `workshop/docs/03-understand/04-control-plane.md`

### 內容

- AI Services account
- Foundry project
- model deployments
- project connections
- App Insights / Search / Storage
- RBAC
- control plane vs runtime path

### 依賴

- T-02
- T-04

---

## T-17 重寫英文頁：Deep Dive Overview

- 狀態：未開始
- 類型：文件
- 平行處理：否
- 建議 Agent：Agent C

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

- 狀態：未開始
- 類型：文件 / 設定
- 平行處理：否
- 建議 Agent：Agent C

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

- 狀態：未開始
- 類型：文件
- 平行處理：可部分平行
- 建議 Agent：Agent C

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

- 狀態：未開始
- 類型：文件資產
- 平行處理：是
- 建議 Agent：Agent C

### 內容

- Control Plane 圖
- model / agent / tool / IQ 關係圖
- 可選擇使用 Mermaid 或靜態圖資產

### 依賴

- T-02

---

## T-21 撰寫英文 FAQ / talking points 補強

- 狀態：未開始
- 類型：文件
- 平行處理：是
- 建議 Agent：Agent C

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

- 狀態：未開始
- 類型：測試
- 平行處理：否
- 建議 Agent：Agent E

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

- 狀態：未開始
- 類型：測試
- 平行處理：是
- 建議 Agent：Agent E

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

### 第二波可平行啟動

在 T-02 與各技術研究初步完成後，可平行進行：

- T-13 Foundry Model 頁
- T-14 Foundry Agent 頁
- T-15 Foundry Tool 頁
- T-16 Control Plane 頁
- T-21 FAQ / talking points

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

- T-17 重寫 `03-understand/index.md`
- T-18 更新 `workshop/mkdocs.yml`
- T-19 更新首頁與部署頁核心敘事
- T-24 / T-33 建站驗證
- T-34 最終 walkthrough 與驗收

## 最小可行落地順序（建議）

若要先求「最快有成果」，建議先做這條主線：

1. T-00
2. T-01
3. T-02
4. T-04
5. T-07
6. T-13
7. T-14
8. T-15
9. T-16
10. T-17
11. T-18
12. T-19
13. T-24

這樣可以先把英文的五主軸骨架與主流程敘事補齊。

之後再做：

14. T-03
15. T-05
16. T-06
17. T-08 ~ T-12
18. T-22
19. T-23
20. T-25 ~ T-33
21. T-34

## 備註

1. 若時間有限，可先只完成文件骨架與主流程 code/document alignment，不做所有選配工具的真實可執行 demo。
2. 若要用多個 Agent，最有效率的切法是：
   - 一個 Agent 專做 IaC / platform
   - 一個 Agent 專做 scripts / demo flow
   - 一個 Agent 專做英文文件
   - 一個 Agent 專做繁中翻譯
   - 一個 Agent 專做驗證與回歸檢查
3. 所有選配功能都應保留 skip 文案與 warning path，這是本次教學計劃的重要要求。