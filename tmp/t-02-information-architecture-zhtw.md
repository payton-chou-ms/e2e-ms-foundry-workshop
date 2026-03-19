# T-02 五主軸資訊架構草案

## 目的

定義 workshop 在 `Deep dive` 區段的資訊架構，讓後續新增文件、導覽、翻譯與測試都依同一套頁面結構進行。

## 設計目標

1. 使用者能從導覽直接看到 Foundry 平台的完整構成。
2. 每個主軸至少有一個可獨立閱讀的頁面。
3. 主流程與選配能力的分界要能在頁面結構中被清楚標示。
4. 新頁面需能對應到 repo 中現有腳本或 IaC。

## 建議導覽結構

### 現況

`Deep dive` 目前只有：

1. Overview
2. Foundry IQ: Documents
3. Fabric IQ: Data

### 建議改版後

1. Overview
2. Foundry Model
3. Foundry IQ
4. Foundry Agent
5. Foundry Tool
6. Fabric IQ
7. Control Plane

## 建議檔案結構

### 保留

- `workshop/docs/03-understand/index.md`
- `workshop/docs/03-understand/01-foundry-iq.md`
- `workshop/docs/03-understand/02-fabric-iq.md`

### 新增

- `workshop/docs/03-understand/00-foundry-model.md`
- `workshop/docs/03-understand/02-foundry-agent.md`
- `workshop/docs/03-understand/03-foundry-tool.md`
- `workshop/docs/03-understand/04-control-plane.md`

## 各頁定位

### Overview

用途：

- 五主軸導讀頁
- 用一張圖說清楚 `model -> agent -> tools -> IQ -> data sources`
- 說明哪些是必要能力、哪些是選配能力

主要讀者：

- 講師
- 技術 seller
- 首次進入 deep dive 的客戶技術方

### Foundry Model

用途：

- 說明 model deployment 與用途差異
- 說明主流程模型與選配模型
- 說明多模型部署與 guarded strategy

主要讀者：

- 對模型選擇與平台策略有疑問的人

### Foundry IQ

用途：

- 延續目前文件
- 專注文件檢索、agentic retrieval 與知識庫敘事

### Foundry Agent

用途：

- 說明 orchestrator agent
- 說明 agent instructions、tool selection、trace、publish

### Foundry Tool

用途：

- 說明主流程 function tools
- 區分主流程工具與延伸展示工具

### Fabric IQ

用途：

- 延續目前文件
- 專注 ontology、NL to SQL 與資料查詢敘事

### Control Plane

用途：

- 說明平台設定與治理層
- 說明 AI Services、project、connections、RBAC、App Insights、Search、Storage 的關係

## 頁面互相引用建議

### Overview 應連到

- Foundry Model
- Foundry IQ
- Foundry Agent
- Foundry Tool
- Fabric IQ
- Control Plane

### Foundry Model 應連到

- Foundry Agent
- Control Plane

### Foundry Agent 應連到

- Foundry Tool
- Control Plane
- Foundry IQ
- Fabric IQ

### Foundry Tool 應連到

- Foundry Agent
- Foundry IQ
- Fabric IQ

### Control Plane 應連到

- Deploy Azure resources
- Foundry Model
- Foundry Agent

## 導覽命名建議

在 `workshop/mkdocs.yml` 建議使用：

- `Overview`
- `Foundry Model`
- `Foundry IQ: Documents`
- `Foundry Agent`
- `Foundry Tool`
- `Fabric IQ: Data`
- `Control Plane`

這樣能保留既有 `Foundry IQ` / `Fabric IQ` 命名習慣，同時把其餘三個主軸補齊。

## 導覽排序理由

### 建議排序

1. 先從 Overview 建立全貌
2. 再看 Model，理解能力來源
3. 再看 Foundry IQ 與 Fabric IQ，理解兩大知識來源
4. 再看 Agent 與 Tool，理解運作機制
5. 最後看 Control Plane，理解平台治理層

### 替代排序

若希望更貼近 runtime path，可改成：

1. Overview
2. Foundry Model
3. Foundry Agent
4. Foundry Tool
5. Foundry IQ
6. Fabric IQ
7. Control Plane

目前建議先保留 Foundry IQ / Fabric IQ 的可見性，避免既有 workshop 使用者找不到原本熟悉的內容。

## 與程式 / IaC 的映射

| 主軸 | 主要對應 |
| --- | --- |
| Foundry Model | `infra/modules/foundry.bicep` |
| Foundry IQ | `workshop/docs/03-understand/01-foundry-iq.md`, `scripts/06_upload_to_search.py` |
| Foundry Agent | `scripts/07_create_foundry_agent.py`, `scripts/08_test_foundry_agent.py` |
| Foundry Tool | `scripts/07_create_foundry_agent.py`, `scripts/08_test_foundry_agent.py` |
| Fabric IQ | `workshop/docs/03-understand/02-fabric-iq.md`, `scripts/02_create_fabric_items.py`, `scripts/03_load_fabric_data.py` |
| Control Plane | `infra/modules/foundry.bicep`, `workshop/docs/01-deploy/01-deploy-azure.md` |

## 本階段不處理事項

這份資訊架構只定義頁面與關係，不處理：

- 實際頁面全文內容
- 多模型 Bicep 實作
- trace / publish 程式實作
- 延伸工具實作
- 繁中翻譯內容

## 建議下一步

根據這份架構，後續應接續：

1. 新增 `Foundry Model`、`Foundry Agent`、`Foundry Tool`、`Control Plane` 四頁
2. 重寫 `workshop/docs/03-understand/index.md`
3. 更新 `workshop/mkdocs.yml` 中 `Deep dive` 導覽