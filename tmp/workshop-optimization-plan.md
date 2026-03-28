# Workshop 腳本重整計畫

> 掃描範圍：`scripts/`、`tests/`、`README.md`、`workshop/docs/`、`data/*/README.md`
> 更新日期：2026-03-28
> 目的：把 `00` 到 `08b` 的工程編號流程，重整成學員可理解的公開入口 + 維護者可管理的內部 pipeline

---

## 問題定義

目前正式文件已經接近角色導向：

1. 管理員部署
2. 參與者驗證
3. 客製情境

但 `scripts/` 仍然以 `00` 到 `08b` 的工程步驟編號暴露主流程，造成三個問題：

1. 學員看到的是 pipeline 編號，不是學習任務。
2. 正式文件與腳本目錄使用兩套不同的心智模型。
3. 維護者雖然需要細粒度 pipeline，但學員不應該先理解它們。

核心判斷：目前真正需要重整的不是 Azure / Fabric 流程本身，而是 CLI surface 和腳本資訊架構。

---

## 設計目標

1. 學員只需要理解角色與任務，不需要理解 `00` 到 `08b`。
2. 正式文件只教公開入口，不把內部 pipeline 當主線。
3. 維護者仍保有可拆解、可除錯的細粒度腳本。
4. 舊指令在過渡期內仍可執行，避免 workshop 筆記與環境說明一次全部失效。

---

## 目標資訊架構

### 使用者可見層

學員與講師主要只碰這幾類入口：

1. `prepare`
2. `validate`
3. `customize`
4. `advanced`

### 建議目錄模型

長期目標結構如下：

```text
scripts/
  admin_prepare_shared_demo.py
  admin_prepare_docs_demo.py
  admin_prepare_foundry_iq_demo.py
  admin_prepare_docs_data_demo.py

  participant_validate_docs.py
  participant_validate_docs_data.py
  participant_validate_foundry_iq.py

  author_generate_custom_data.py
  author_rebuild_custom_poc.py

  pipelines/
	 agents/
	 fabric/
	 search/
	 data/

  internal/
	 preload_scenarios.py
	 build_solution.py

  legacy/
	 create_fabric_data_agent.py

  shared/
	 load_env.py
	 scenario_utils.py
	 credential_utils.py
	 foundry_trace.py
	 foundry_tool_contract.py
```

第一階段不會一次搬完所有檔案，而是先建立新的公開入口，並保留既有實作。

---

## 公開入口命名

### 管理員入口

1. `admin_prepare_shared_demo.py`
	說明：準備共享 workshop 環境
2. `admin_prepare_docs_demo.py`
	說明：準備文件問答示範
3. `admin_prepare_foundry_iq_demo.py`
	說明：準備 Foundry-native IQ 示範
4. `admin_prepare_docs_data_demo.py`
	說明：準備文件 + 資料整合示範

### 參與者入口

1. `participant_validate_docs.py`
	說明：驗證文件問答路徑
2. `participant_validate_docs_data.py`
	說明：驗證文件 + 資料問答路徑
3. `participant_validate_foundry_iq.py`
	說明：驗證 Foundry-native IQ agent

### 作者入口

1. `author_generate_custom_data.py`
	說明：只產生客製資料
2. `author_rebuild_custom_poc.py`
	說明：重建整套自訂 PoC

---

## 現有腳本對應

| 現有腳本 | 目標定位 |
|---|---|
| `00_admin_prepare_demo.py` | 內部 prepare orchestration；外部由新的 `admin_prepare_*` wrappers 取代 |
| `00_admin_preload_scenarios.py` | `internal/` |
| `00_build_solution.py` | `internal/` |
| `01_generate_sample_data.py` | `author_generate_custom_data.py` 對應的實作 |
| `01_generate_sample_data_templates.py` | `pipelines/data/` 或 `legacy/` |
| `02_create_fabric_items.py` | `pipelines/fabric/` |
| `03_load_fabric_data.py` | `pipelines/fabric/` |
| `04_generate_agent_prompt.py` | `pipelines/fabric/` |
| `05_create_fabric_agent.py` | `legacy/` |
| `06_upload_to_search.py` | `pipelines/search/` |
| `06a_upload_scenario_assets_to_blob.py` | `pipelines/search/` |
| `06b_upload_to_foundry_knowledge.py` | `pipelines/search/` |
| `07_create_foundry_agent.py` | `pipelines/agents/` |
| `07b_create_foundry_iq_agent.py` | `pipelines/agents/` |
| `08_test_foundry_agent.py` | `pipelines/agents/` |
| `08b_test_foundry_iq_agent.py` | `pipelines/agents/` |

---

## 過渡策略

### 原則

1. 先新增新入口，再重整內部實作。
2. 舊腳本保留一段相容期。
3. 正式文件立刻改教新入口。
4. 內部 pipeline 與 legacy 路徑只在進階文件中出現。

### 相容層

舊腳本在過渡期應該：

1. 仍可執行
2. 明確告知新的公開入口名稱
3. 將既有 exit code 行為維持不變

---

## 分階段實作

### Phase 1：公開入口落地

目標：先建立新的 CLI surface，不搬核心邏輯。

範圍：

1. 新增公開 wrapper 腳本
2. 新增 wrapper 測試
3. 更新主要文件中的主線命令
4. 更新暫存計畫與待辦文件

不在這一階段：

1. 不搬移 `pipelines/`
2. 不改既有核心腳本內部邏輯
3. 不一次清掉所有舊命名

### Phase 2：搬移內部實作

目標：把 agent / fabric / search / data 的實作腳本收進 `pipelines/`。

### Phase 3：建立 deprecation shim

目標：把舊命名正式降級為相容層，避免學員再把 legacy script 當成主入口。

目前狀態：

1. `00_admin_prepare_demo.py`、`00_admin_preload_scenarios.py`、`00_build_solution.py`、`08_test_foundry_agent.py`、`08b_test_foundry_iq_agent.py` 已改成 shim。
2. shim 會保留可執行性，並提示新的公開入口。
3. 主線 docs 已大致切到新入口。

剩餘重點：

1. 清掉 `data/*/README.md`、`tmp/*.md`、註解文字中的舊主線命名。
2. 決定是否要把更多 `01`~`07b` root scripts 也逐步 shim 化，或保留為維護者入口。
3. 統一 `internal/` 檔案內的 deprecation 文案，避免再導向舊的 `00_admin_prepare_demo.py`。

### Phase 4：文件封板與站點重建

目標：把文件、站內搜尋、與教學語言全面封板到新入口模型。

剩餘重點：

1. 將 learner-facing 文件中的「01-08 主流程」語言進一步降到進階／維護者頁。
2. 把 `05b-script-core-pipeline.md` 明確改成 advanced / maintainer reference，而不是半主線頁。
3. 重建 `workshop/site/`，確認站內搜尋結果與產生頁面不再優先曝光舊命名。
4. 做最後 smoke check：抽查新公開入口、舊 shim、以及主要頁面的命令一致性。

---

## 驗收標準

1. 學員不需要理解 `00` 到 `08b` 就能跑主線。
2. `README.md` 與 deploy 主線頁面優先使用新入口名稱。
3. 進階頁面才解釋 pipeline 腳本。
4. 舊命令在過渡期仍能用。
5. 文件與 CLI 講的是同一套角色語言。

---

## 目前實作決策

目前已完成 Phase 1 主體、Phase 2 主體，以及 Phase 3 的核心 shim 工作。

接下來應把重點放在：

1. Phase 3 收尾：清理非主線引用與內部 deprecation 文案。
2. Phase 4 封板：把文件與產出網站正式對齊新入口。

---

## 暫不處理

1. 不修改 Azure / Fabric 佈署語意
2. 不一次更動所有 `scripts/` 檔案位置
3. 不在本輪重建所有 generated site 內容
4. 不把 `guides/` 重新變成第二份正式教學來源
