# Workshop 腳本重整實作順序

> 對應文件：`tmp/workshop-optimization-plan.md`
> 這份檔案只保留可執行順序，不重複設計說明。
> 更新日期：2026-03-28

---

## Phase 1：公開入口落地

### 1. 建立 wrapper 測試

- [x] 新增 `tests/test_public_entrypoints.py`
- [x] 驗證新入口在實作前會失敗

### 2. 建立公開入口 helper

- [x] 新增 `scripts/entrypoint_runner.py`
- [x] 提供共用 command-building 與 subprocess delegation

### 3. 建立管理員入口

- [x] 新增 `scripts/admin_prepare_shared_demo.py`
- [x] 新增 `scripts/admin_prepare_docs_demo.py`
- [x] 新增 `scripts/admin_prepare_foundry_iq_demo.py`
- [x] 新增 `scripts/admin_prepare_docs_data_demo.py`

### 4. 建立參與者入口

- [x] 新增 `scripts/participant_validate_docs.py`
- [x] 新增 `scripts/participant_validate_docs_data.py`
- [x] 新增 `scripts/participant_validate_foundry_iq.py`

### 5. 建立作者入口

- [x] 新增 `scripts/author_generate_custom_data.py`
- [x] 新增 `scripts/author_rebuild_custom_poc.py`

### 6. 更新主線文件命令

- [x] 更新 `workshop/docs/01-deploy/00-admin-deploy-share.md`
- [x] 更新 `workshop/docs/01-deploy/00-participant-run-validate.md`
- [x] 更新 `workshop/docs/01-deploy/04-run-scenario.md`
- [x] 更新 `workshop/docs/01-deploy/05-script-sequence.md`
- [x] 更新 `workshop/docs/01-deploy/05b-script-core-pipeline.md`
- [x] 更新 `workshop/docs/02-customize/02-generate.md`

### 7. 驗證

- [x] 跑 `python -m unittest tests/test_public_entrypoints.py`
- [x] 跑既有 smoke tests，避免影響現有 CLI 測試

---

## Phase 2：搬移內部 pipeline

### 1. 建立內部分類資料夾

- [x] 建立 `scripts/pipelines/agents/`
- [x] 建立 `scripts/pipelines/fabric/`
- [x] 建立 `scripts/pipelines/search/`
- [x] 建立 `scripts/pipelines/data/`
- [x] 建立 `scripts/internal/`
- [x] 建立 `scripts/legacy/`
- [x] 建立 `scripts/shared/`

### 2. 搬移通用模組

- [x] 搬移 `load_env.py`
- [x] 搬移 `scenario_utils.py`
- [x] 搬移 `credential_utils.py`
- [x] 搬移 `foundry_trace.py`
- [x] 搬移 `foundry_tool_contract.py`

### 3. 搬移 pipeline 腳本

- [x] 搬移 fabric 相關腳本
- [x] 搬移 search 相關腳本
- [x] 搬移 agent 相關腳本
- [x] 搬移 data generation 相關腳本

### 4. 修正 imports 與相依輸出

- [x] 修正 `scripts/` 內 import 路徑
- [x] 修正錯誤訊息中的下一步腳本名稱
- [x] 修正 summary 輸出的命令建議

---

## Phase 3：舊命名相容層

### 1. 建立 deprecation shim

- [x] 讓舊腳本名稱只做轉呼叫
- [x] 加上明確的新版入口提示

### 2. 更新非主線引用

- [x] 更新 `data/*/README.md`（已掃描，現階段無需變更）
- [x] 更新 `tmp/*.md`
- [x] 更新註解檔中的舊腳本說明

### 3. Phase 3 收尾

- [x] 統一 `internal/*.py` 的 deprecation 文案，避免再導向 `00_admin_prepare_demo.py`
- [x] 決定 `01`~`07b` root scripts 的最終定位：保留 `01`、`02`、`03`、`04`、`06`、`06a`、`06b`、`07`、`07b` 作為維護者入口；`05` 維持 legacy shim
- [x] 抽查 `README.md`、`guides/`、`ref/` 是否仍把 legacy script 當主線入口

---

## Phase 4：封板

### 1. 清理主線教學語言

- [x] 不再以「01-08」描述 learner-facing 主流程
- [x] 將 `05b` 明確改成 advanced / maintainer reference

### 2. 重建網站輸出

- [x] 重新產生 `workshop/site/`
- [x] 檢查站內搜尋結果是否仍以舊命名為主

### 3. 最終驗證

- [x] 跑 focused tests（`tests.test_public_entrypoints` + `tests.test_legacy_script_shims`）
- [x] 抽查新公開入口：`admin_prepare_*`、`participant_validate_*`、`author_*`
- [x] 抽查舊 shim：`00_admin_prepare_demo.py`、`00_build_solution.py`、`08_test_foundry_agent.py`、`08b_test_foundry_iq_agent.py`
- [x] 抽查主要 learner-facing 文件頁面與站內搜尋結果