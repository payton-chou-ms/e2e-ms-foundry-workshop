# T-01 現況與缺口分析

## 目的

盤點目前 repo 在 Foundry 教學五主軸、程式實作、IaC 支撐與文件敘事上的現況，作為後續 T-03 之後實作工作的基準。

## 分析範圍

- IaC：`infra/modules/foundry.bicep`
- Agent 相關腳本：`scripts/07_create_foundry_agent.py`、`scripts/08_test_foundry_agent.py`
- Deep dive 文件：`workshop/docs/03-understand/`
- 站台導覽：`workshop/mkdocs.yml`

## 現況摘要

### 1. Foundry IQ

現況：已覆蓋良好。

證據：

- `workshop/docs/03-understand/01-foundry-iq.md`

已具備：

- agentic retrieval 概念
- knowledge base / document intelligence 敘事
- customer talking points
- technical details

缺口：

- 與 Foundry Agent、Foundry Tool、Control Plane 的關係仍未在導覽層明確銜接。

### 2. Fabric IQ

現況：已覆蓋良好。

證據：

- `workshop/docs/03-understand/02-fabric-iq.md`

已具備：

- ontology 概念
- NL to SQL 流程
- combined intelligence 敘事
- customer talking points

缺口：

- 與 Foundry Agent、Foundry Tool、Control Plane 的關聯仍未在總覽頁說清楚。

### 3. Foundry Agent

現況：部分覆蓋。

證據：

- `workshop/docs/03-understand/index.md` 有 `Orchestrator Agent` 但非獨立頁面
- `scripts/07_create_foundry_agent.py` 已建立 agent
- `scripts/08_test_foundry_agent.py` 已提供互動式測試

已具備：

- PromptAgentDefinition 建立流程
- function tools 綁定
- full mode / foundry-only mode
- 基本測試流程

缺口：

- 沒有獨立頁面說明 agent lifecycle
- 沒有 trace 教學
- 沒有 publish 教學
- 沒有把 agent 與 control plane / project / connection / model 關係明確教學化

### 4. Foundry Tool

現況：程式有、文件不足。

證據：

- `scripts/07_create_foundry_agent.py` 中已有 `search_documents` 與 `execute_sql`

已具備：

- 兩個主流程 function tool
- tool schema 與描述
- SQL / document query 的責任分工

缺口：

- 沒有獨立頁面解釋 tool schema 與 selection 邏輯
- 沒有說明 tool execution loop
- 沒有整理主流程工具與選配工具的分層
- 尚未納入 Content Understanding、Browser Automation、Web Search、PII、Image Generation 的教學定位

### 5. Foundry Model

現況：IaC 有基礎模型部署，但文件近乎空白。

證據：

- `infra/modules/foundry.bicep` 目前有 chat model deployment
- `infra/modules/foundry.bicep` 目前有 embedding model deployment

已具備：

- 一個 chat model deployment
- 一個 embedding model deployment

缺口：

- 沒有多模型策略
- 沒有模型比較表
- 沒有主流程模型 vs 選配模型的治理說明
- 沒有 skip / warning 策略文件

### 6. Control Plane

現況：IaC 有實作，文件明顯不足。

證據：

- `infra/modules/foundry.bicep` 已定義：
  - AI Services
  - Project
  - Search
  - Storage
  - App Insights
  - Connections
  - RBAC

已具備：

- Azure AI Foundry project 基礎控制層資源
- Search / Storage / App Insights connections
- managed identity 與 role assignments

缺口：

- 沒有獨立文件說明控制層與 runtime path 的差異
- 沒有說清楚 project、deployment、connection、RBAC 的責任分工
- 沒有把 Application Insights 放進教學敘事

## 導覽與敘事缺口

### Deep dive 導覽現況

目前 `Deep dive` 僅包含：

- Overview
- Foundry IQ: Documents
- Fabric IQ: Data

缺口：

- 缺 Foundry Model
- 缺 Foundry Agent
- 缺 Foundry Tool
- 缺 Control Plane

### 首頁與 Deep Dive 敘事現況

目前整體仍以 `Foundry IQ + Fabric IQ` 的雙主軸為主。

缺口：

- 對外無法清楚說明 Foundry 平台層次
- 容易讓讀者以為 Foundry 只有 IQ，而不是 model / agent / tool / project / connection / RBAC 的完整平台

## 權限與部署現況

### 已知強項

- Azure 資源可由 `azd up` 部署
- Agent 與工具主流程已有 working baseline

### 已知風險

- IaC 會建立 role assignments，部署前提高於單純 Contributor
- 選配能力很可能受權限、區域、SKU、preview 條件限制
- trace / publish / 進階工具未保證可在所有環境成功啟用

## 缺口優先級

### P1

1. Control Plane 文件
2. Foundry Agent 文件
3. Foundry Tool 文件

### P2

1. Foundry Model 文件
2. Deep dive 導覽與首頁敘事重整

### P3

1. 選配工具與多模型的最小 demo / guarded execution
2. 繁中翻譯全面落地

## 建議後續接續任務

根據這份 gap analysis，下一批最合理的後續工作是：

1. T-02 五主軸資訊架構草案
2. T-04 Control Plane 所需輸出與文件敘事盤點
3. T-07 主流程 tool 文件對齊
4. T-13 ~ T-16 新增英文頁面