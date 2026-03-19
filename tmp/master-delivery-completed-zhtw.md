# 已完成任務詳細紀錄

## 用途

這份文件集中保存已完成任務的細節、產出與驗證結果。

主清單 `tmp/master-delivery-todo-zhtw.md` 只保留：

- 任務摘要
- 依賴關係
- 排程與下一步判讀

## 已完成任務清單

| Task | 主題 | 主要產出 |
| --- | --- | --- |
| T-00 | 專案對齊與決策紀錄 | `tmp/t-00-delivery-decisions-zhtw.md` |
| T-01 | 現況與缺口盤點 | `tmp/t-01-gap-analysis-zhtw.md` |
| T-02 | 五主軸資訊架構 | `tmp/t-02-information-architecture-zhtw.md` |
| T-03 | 多模型部署策略 | `tmp/t-03-multi-model-strategy-zhtw.md` |
| T-04 | Control Plane 輸出補齊 | `infra/main.bicep`、`infra/modules/foundry.bicep` |
| T-05 | Agent trace 支援 | `tmp/t-05-agent-tracing-zhtw.md`、`scripts/foundry_trace.py` |
| T-06 | Publish 規劃 | `tmp/t-06-publish-plan-zhtw.md`、`scripts/09_publish_foundry_agent.py` |
| T-07 | Tool contract 對齊 | `tmp/t-07-tool-contract-alignment-zhtw.md`、`scripts/foundry_tool_contract.py` |
| T-08 | Content Understanding 評估 | `tmp/t-08-content-understanding-zhtw.md`、`scripts/09_demo_content_understanding.py` |
| T-09 | Browser Automation 評估 | `tmp/t-09-browser-automation-zhtw.md`、`scripts/10_demo_browser_automation.py` |
| T-10 | Web Search 評估 | `tmp/t-10-web-search-zhtw.md`、`scripts/11_demo_web_search.py` |
| T-11 | PII 評估 | `tmp/t-11-pii-zhtw.md`、`scripts/12_demo_pii_redaction.py` |
| T-12 | Image Generation 評估 | `tmp/t-12-image-generation-zhtw.md`、`scripts/13_demo_image_generation.py` |
| T-13 | Foundry Model 頁 | `workshop/docs/03-understand/00-foundry-model.md` |
| T-14 | Foundry Agent 頁 | `workshop/docs/03-understand/02-foundry-agent.md` |
| T-15 | Foundry Tool 頁 | `workshop/docs/03-understand/03-foundry-tool.md` |
| T-16 | Control Plane 頁 | `workshop/docs/03-understand/04-control-plane.md` |
| T-17 | Deep Dive Overview 重寫 | `workshop/docs/03-understand/index.md` |
| T-18 | MkDocs 導覽更新 | `workshop/mkdocs.yml` |
| T-19 | 首頁與部署頁敘事更新 | `README.md`、`workshop/docs/index.md`、`workshop/docs/01-deploy/index.md` |
| T-20 | Mermaid 圖補齊 | `workshop/docs/03-understand/index.md`、`workshop/docs/03-understand/00-foundry-model.md`、`workshop/docs/03-understand/04-control-plane.md` |
| T-21 | FAQ / talking points 補強 | `workshop/docs/03-understand/00-foundry-model.md`、`workshop/docs/03-understand/02-foundry-agent.md`、`workshop/docs/03-understand/03-foundry-tool.md`、`workshop/docs/03-understand/04-control-plane.md` |
| T-22 | 主流程 smoke test | `tmp/t-22-main-flow-smoke-test-zhtw.md`、`scripts/08_test_foundry_agent.py` |
| T-23 | 選配能力 smoke test | `tmp/t-23-optional-extension-smoke-test-zhtw.md` |

---

## T-00 專案對齊與決策紀錄

- 狀態：已完成
- 類型：治理 / 規格
- 主要產出：`tmp/t-00-delivery-decisions-zhtw.md`

完成內容：

- 明確定義主流程必要能力
- 明確定義選配能力
- 明確定義繁中站台策略
- 明確定義本次是否要做到進階工具真的可跑

驗收結果：

- 後續任務可明確區分必要與選配
- 英文主線先行、繁中後補的執行順序已固定

---

## T-01 盤點現有實作與缺口

- 狀態：已完成
- 類型：分析
- 主要產出：`tmp/t-01-gap-analysis-zhtw.md`

完成內容：

- 盤點 `infra/modules/foundry.bicep` 現有 control plane 定義
- 盤點 `scripts/07_create_foundry_agent.py`、`scripts/08_test_foundry_agent.py` 現有 agent / tool 流程
- 盤點 `workshop/docs/03-understand/` 現有文件缺口

驗收結果：

- 已確認 `Foundry IQ`、`Fabric IQ` 有基礎內容
- 已確認 `Foundry Model`、`Foundry Agent`、`Foundry Tool`、`Control Plane` 仍需補強

---

## T-02 設計五主軸資訊架構

- 狀態：已完成
- 類型：文件架構
- 主要產出：`tmp/t-02-information-architecture-zhtw.md`

完成內容：

- 設計 `03-understand/` 新導覽順序
- 決定檔名與頁面命名
- 定義各頁互相引用關係

目標頁面：

- `workshop/docs/03-understand/00-foundry-model.md`
- `workshop/docs/03-understand/01-foundry-iq.md`
- `workshop/docs/03-understand/02-foundry-agent.md`
- `workshop/docs/03-understand/03-foundry-tool.md`
- `workshop/docs/03-understand/02-fabric-iq.md`
- `workshop/docs/03-understand/04-control-plane.md`

---

## T-03 擴充 Bicep：多模型部署策略

- 狀態：已完成
- 類型：程式 / IaC
- 主要產出：`tmp/t-03-multi-model-strategy-zhtw.md`

完成內容：

- 為 `infra/modules/foundry.bicep` 新增型別化 `optionalModelDeployments`
- 區分必要模型與選配模型
- 補上部署摘要輸出與 enabled / skipped 清單輸出
- 清理 `infra/main.parameters.json` 的失效參數漂移

驗證結果：

- `infra/modules/foundry.bicep` diagnostics clean
- `az bicep build --file infra/main.bicep` 可編譯
- 已明確記錄目前 best-effort 僅代表顯式 enable / disable，不代表 continue-on-error

---

## T-04 擴充 Bicep：Control Plane 文件所需輸出

- 狀態：已完成
- 類型：程式 / IaC
- 主要產出：`infra/main.bicep`、`infra/modules/foundry.bicep`

完成內容：

- 補齊 AI Services / Project / Search / Storage / App Insights / Log Analytics 相關 output
- 補齊 connection name / resource id / principal id 等可供文件敘事使用的輸出
- 讓後續 `Control Plane` 頁面可直接引用實際 IaC 輸出命名

驗證結果：

- Bicep diagnostics 可通過
- `azd` 可讀取更完整的 deployment outputs

---

## T-06 擴充 agent 程式：publish to Teams / M365 Copilot 規劃

- 狀態：已完成
- 類型：程式 / 文件支援
- 主要產出：`tmp/t-06-publish-plan-zhtw.md`、`scripts/09_publish_foundry_agent.py`

完成內容：

- 明確決定第一階段不做完整 publish automation
- 新增 guarded precheck helper script
- 記錄 publish 後 identity / RBAC 差異與 UI 導向流程

驗收結果：

- 缺少 publish 前提時可 warning 並 skip，不阻塞主流程
- 已保留後續擴成第二階段自動化的空間

---

## T-08 評估延伸工具：Content Understanding

- 狀態：已完成
- 類型：研究 / 選配實作
- 主要產出：`tmp/t-08-content-understanding-zhtw.md`、`scripts/09_demo_content_understanding.py`

完成內容：

- 決定採用「獨立腳本示範 + 文件說明」模式
- 定義最小 demo、先決條件與 skip 條件
- 明確不把 Content Understanding 併入主流程 tool loop

驗收結果：

- 可透過獨立腳本做最小示範
- 不可用時可清楚 skip，不影響 workshop 主流程

---

## T-05 擴充 agent 程式：agent trace 支援

- 狀態：已完成
- 類型：程式
- 主要產出：`tmp/t-05-agent-tracing-zhtw.md`、`scripts/foundry_trace.py`

完成內容：

- 新增可重用 trace helper
- `07_create_foundry_agent.py` 與 `08_test_foundry_agent.py` 接上 best-effort tracing
- 透過 env flag 控制是否啟用 tracing / content tracing / trace context propagation
- tracing 失敗時只 warning，不阻塞主流程

驗收結果：

- 相關 Python 檔案 diagnostics clean
- `python3 -m py_compile` 可通過

---

## T-07 擴充 tool 程式：主流程 tool 文件對齊

- 狀態：已完成
- 類型：程式 / 文件對齊
- 主要產出：`tmp/t-07-tool-contract-alignment-zhtw.md`、`scripts/foundry_tool_contract.py`

完成內容：

- 為 tool contract 新增結構化 rows 與 response loop helper
- 保持 schema、責任邊界、instruction block 的單一來源
- 為後續 `Foundry Tool` 頁面鋪路

驗收結果：

- contract 結構集中於同一模組
- 相關 Python 檔案 diagnostics clean

---

## T-09 評估延伸工具：Browser Automation

- 狀態：已完成
- 類型：研究 / 選配實作
- 主要產出：`tmp/t-09-browser-automation-zhtw.md`、`scripts/10_demo_browser_automation.py`

完成內容：

- 依官方 preview tool 類型建立最小 demo
- 將 demo 限制在 trusted Microsoft Learn page
- 缺少 SDK / connection / 功能可用性時直接 skip

驗收結果：

- Python diagnostics clean
- 可做獨立 demo，不進入主流程 tool loop

---

## T-10 評估延伸工具：Web Search

- 狀態：已完成
- 類型：研究 / 選配實作
- 主要產出：`tmp/t-10-web-search-zhtw.md`、`scripts/11_demo_web_search.py`

完成內容：

- 依官方 `WebSearchTool` 類型建立最小 demo
- 支援 citation 輸出與 clean-up temporary agent version
- 功能不可用時直接 skip

驗收結果：

- Python diagnostics clean
- 已與 public web search 路徑對齊

---

## T-11 評估延伸工具：PII

- 狀態：已完成
- 類型：研究 / 選配實作
- 主要產出：`tmp/t-11-pii-zhtw.md`、`scripts/12_demo_pii_redaction.py`

完成內容：

- 採用 Azure Language PII detection 做最小 redaction demo
- 定義範例文字、entity 輸出與 redacted text 輸出
- 缺 endpoint / key / SDK 時直接 skip

驗收結果：

- Python diagnostics clean
- 已與 optional governance demo 定位一致

---

## T-12 評估延伸工具：Image Generation

- 狀態：已完成
- 類型：研究 / 選配實作
- 主要產出：`tmp/t-12-image-generation-zhtw.md`、`scripts/13_demo_image_generation.py`

完成內容：

- 採用 Azure OpenAI image generation REST API 做最小 demo
- 支援從 env outputs 解析 image deployment
- 找不到 optional model deployment 時直接 skip

驗收結果：

- Python diagnostics clean
- 與 T-03 optional deployment strategy 對齊

---

## T-13 撰寫英文頁：Foundry Model

- 狀態：已完成
- 類型：文件
- 主要產出：`workshop/docs/03-understand/00-foundry-model.md`

完成內容：

- 說明 required vs optional models
- 說明多模型部署策略與 explicit enable / skip 邏輯
- 補上 model deployment Mermaid 圖

驗收結果：

- Markdown diagnostics clean
- 已加入 workshop nav

---

## T-14 撰寫英文頁：Foundry Agent

- 狀態：已完成
- 類型：文件
- 主要產出：`tmp/t-14-foundry-agent-page-zhtw.md`、`workshop/docs/03-understand/02-foundry-agent.md`

完成內容：

- 說明 `PromptAgentDefinition` 的 model / instructions / tools 三要素
- 對齊 `07_create_foundry_agent.py` 與 `08_test_foundry_agent.py` 的 create / get / test flow
- 補上 tracing env flags、best-effort 原則與 publish boundary 說明
- 補上 agent orchestration Mermaid 圖

驗收結果：

- Markdown diagnostics clean
- 已加入 workshop nav
- `mkdocs build` 可通過

---

## T-15 撰寫英文頁：Foundry Tool

- 狀態：已完成
- 類型：文件
- 主要產出：`tmp/t-15-foundry-tool-page-zhtw.md`、`workshop/docs/03-understand/03-foundry-tool.md`

完成內容：

- 對齊 canonical tool contract 與 main runtime execution loop
- 說明 `execute_sql` / `search_documents` schema 與責任邊界
- 說明 optional demos 為 layered extensions，不直接混入主流程 tool contract
- 補上 function-call sequence Mermaid 圖

驗收結果：

- Markdown diagnostics clean
- 已加入 workshop nav
- `mkdocs build` 可通過

---

## T-16 撰寫英文頁：Control Plane

- 狀態：已完成
- 類型：文件
- 主要產出：`workshop/docs/03-understand/04-control-plane.md`

完成內容：

- 說明 AI Services account、Foundry project、connections、Search、Storage、App Insights、RBAC
- 區分 control plane 與 runtime path
- 補上 resource topology Mermaid 圖

驗收結果：

- Markdown diagnostics clean
- 已加入 workshop nav

---

## T-17 重寫英文頁：Deep Dive Overview

- 狀態：已完成
- 類型：文件
- 主要產出：`tmp/t-17-deep-dive-overview-zhtw.md`、`workshop/docs/03-understand/index.md`

完成內容：

- 將 overview 重寫為五主軸導覽
- 補上 `control plane -> model -> agent -> tool -> IQ -> data sources` 關係圖
- 新增頁面對照與 customer-question routing 區塊
- 對齊 Foundry Model / Agent / Tool / IQ / Control Plane 的連結

驗收結果：

- Markdown diagnostics clean
- `mkdocs build` 可通過

---

## T-18 更新 MkDocs 導覽

- 狀態：已完成
- 類型：文件 / 設定
- 主要產出：`tmp/t-18-mkdocs-nav-update-zhtw.md`、`workshop/mkdocs.yml`

完成內容：

- 將 Deep Dive 導覽順序調整為與五主軸敘事更一致
- 將 `Foundry Agent`、`Foundry Tool` 放到 `Foundry IQ` 之前
- 保持 nav 標題與頁面標題一致

驗收結果：

- YAML diagnostics clean
- `mkdocs build` 可通過

---

## T-19 更新首頁與部署頁敘事

- 狀態：已完成
- 類型：文件
- 主要產出：`tmp/t-19-homepage-deploy-narrative-zhtw.md`、`README.md`、`workshop/docs/index.md`、`workshop/docs/01-deploy/index.md`

完成內容：

- 將入口文件從雙主軸敘事擴展為「主流程簡潔 + 五主軸架構」的雙層說法
- 在 `README.md` 補上五主軸架構與主流程 / 技術深談分層
- 在 overview 與 deploy 頁補上 main path vs five-axis architecture 的說明
- 保持 workshop 執行路徑仍以單一 agent、兩個 core tools、兩條 grounding path 為主

驗收結果：

- Markdown diagnostics clean
- `mkdocs build` 可通過

---

## T-20 為新頁面補架構圖或 Mermaid 圖

- 狀態：已完成
- 類型：文件資產
- 主要產出：`workshop/docs/03-understand/index.md`、`workshop/docs/03-understand/00-foundry-model.md`、`workshop/docs/03-understand/04-control-plane.md`

完成內容：

- 補上 overview Mermaid 圖
- 補上 model deployment Mermaid 圖
- 補上 control plane / runtime Mermaid 圖

驗收結果：

- Markdown diagnostics clean
- Deep dive 導覽已可直接連到新圖與新頁面

---

## T-21 撰寫英文 FAQ / talking points 補強

- 狀態：已完成
- 類型：文件
- 主要產出：`tmp/t-21-faq-talking-points-zhtw.md`、`workshop/docs/03-understand/00-foundry-model.md`、`workshop/docs/03-understand/02-foundry-agent.md`、`workshop/docs/03-understand/03-foundry-tool.md`、`workshop/docs/03-understand/04-control-plane.md`

完成內容：

- 為 Foundry Model、Foundry Agent、Foundry Tool、Control Plane 四頁補上 FAQ 區塊
- 保留並強化每頁可直接口述的 talking points
- 讓頁面同時支援技術深談與 customer-facing 解說

驗收結果：

- Markdown diagnostics clean
- `mkdocs build` 可通過

---

## T-22 主流程腳本 smoke test

- 狀態：已完成
- 類型：測試
- 主要產出：`tmp/t-22-main-flow-smoke-test-zhtw.md`、`scripts/08_test_foundry_agent.py`

完成內容：

- 驗證 `00_build_solution.py --only 07-search --dry-run` 可正確組裝 pipeline
- 驗證 `07_create_foundry_agent.py` 在 full / foundry-only 都會對缺少 `AZURE_AI_PROJECT_ENDPOINT` 給出正確 guardrail
- 驗證 `08_test_foundry_agent.py` 在 full / foundry-only 都會對缺少 `AZURE_AI_PROJECT_ENDPOINT` 給出正確 guardrail
- 修正 full mode 先被 `pyodbc` 缺件短路的問題，改為 lazy import 與 SQL-time failure

驗收結果：

- 主流程在無雲端資源的目前環境下會給出正確錯誤，不會被本機 ODBC 缺件誤導
- `scripts/08_test_foundry_agent.py` diagnostics clean
- `python3 -m py_compile /workspaces/nc-iq-workshop/scripts/08_test_foundry_agent.py` 可通過

---

## T-23 選配能力 smoke test

- 狀態：已完成
- 類型：測試
- 主要產出：`tmp/t-23-optional-extension-smoke-test-zhtw.md`

完成內容：

- 以 `py_compile` 驗證 tracing helper、publish helper、Content Understanding、Browser Automation、Web Search、PII、Image Generation 腳本語法
- 執行各腳本並分類為可執行或正確 skip
- 確認目前環境下所有不可用功能都會明確輸出 `SKIP:` 或 guarded precheck 訊息

驗收結果：

- 選配腳本未出現未處理例外造成的直接崩潰
- Publish / Content Understanding / Browser Automation / Web Search / PII / Image Generation 均正確落在 guarded skip 路徑