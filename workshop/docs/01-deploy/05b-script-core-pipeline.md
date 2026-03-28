# 進階：維護者腳本對照

這一頁是維護者／講師用的進階參考頁。

學員如果只想知道要跑哪些命令，請優先看公開入口，不需要理解底下的 internal / pipeline 腳本。

目前的定位如下：`01`、`04`、`06`、`06a`、`06b`、`07`、`07b` 保留為維護者入口，方便拆解流程與除錯；`00`、`08`、`08b` 則是 Deprecated shim，只保留給舊筆記和相容性路徑。

附錄資料路徑專用腳本已移到 [附錄中的資料腳本對照](../05-appendix/05-maintainer-data-scripts.md)。

## 建議優先使用的公開入口

```bash
python scripts/admin_prepare_shared_demo.py
python scripts/admin_prepare_docs_demo.py
python scripts/admin_prepare_foundry_iq_demo.py
python scripts/admin_prepare_docs_data_demo.py

python scripts/participant_validate_docs.py
python scripts/participant_validate_foundry_iq.py
python scripts/participant_validate_docs_data.py

python scripts/author_generate_custom_data.py
python scripts/author_rebuild_custom_poc.py --industry "Insurance" --usecase "Property insurance with claims processing and policy management"
```

`admin_prepare_shared_demo.py` 預設會附帶 `--skip-fabric`，也就是只準備共享示範所需的 Foundry 主線；若維護者真的要連附錄資料路徑一起建立，請顯式加上 `--with-fabric`。

如果你要除錯、拆解流程，或理解背後的 internal / pipeline 分工，再往下看維護者腳本對照。

## 維護者核心流程順序

```text
01 產生情境資料
04 產生 schema prompt
06a 上傳情境來源資產到 Blob
06 上傳文件到 Azure AI Search
06b 建立 Foundry IQ knowledge
07 建立 Foundry agent
08 測試 agent
```

平常不一定要手動逐支執行，因為新的公開 wrappers 會替你切到對應的 prepare / validate 路徑。這一段主要是給維護者理解底層組成。

## 維護者腳本對照

### `00_admin_prepare_demo.py`（Deprecated shim）

- 用途：舊版 prepare 入口名稱；實際上只是轉呼叫 `internal/prepare_demo.py`
- 什麼時候跑：你在除錯或維護舊路徑時

```bash
python scripts/00_admin_prepare_demo.py
python scripts/00_admin_prepare_demo.py --mode foundry-only
python scripts/00_admin_prepare_demo.py --mode foundry-iq
python scripts/00_admin_prepare_demo.py --mode full --from-step 02
python scripts/00_admin_prepare_demo.py --mode full --clean --industry "Insurance" --usecase "Property insurance with claims processing and policy management"
```

一般情況請改用：`admin_prepare_shared_demo.py`、`admin_prepare_docs_demo.py`、`admin_prepare_foundry_iq_demo.py` 或 `admin_prepare_docs_data_demo.py`。

### `01_generate_sample_data.py`（維護者入口）

- 用途：根據輸入情境產生新的 sample data
- 什麼時候跑：你在公開入口之外，直接做資料生成除錯時

```bash
python scripts/01_generate_sample_data.py --industry "Insurance" --usecase "Property insurance with claims processing and policy management"
python scripts/01_generate_sample_data.py

# 平常作者入口
python scripts/author_generate_custom_data.py
```

如果你要看 `--industry` / `--usecase` / `--size` 的完整自訂方式，請回 [產生自訂資料](../02-customize/02-generate.md)。

### `01_generate_sample_data_templates.py`

- 用途：用固定 template 產生內建情境資料
- 什麼時候跑：你想走 template-based 固定情境時

```bash
python scripts/01_generate_sample_data_templates.py --scenario retail --size small
```

### `04_generate_agent_prompt.py`（維護者入口）

- 用途：產生 `schema_prompt.txt`
- 什麼時候跑：你要讓 agent 理解 schema 時

```bash
python scripts/04_generate_agent_prompt.py
python scripts/04_generate_agent_prompt.py --from-config
```

### `06_upload_to_search.py`（維護者入口）

- 用途：把 PDF 文件切 chunk、做 embedding、上傳到 Azure AI Search
- 什麼時候跑：你要讓 agent 可以回答文件問題時

```bash
python scripts/06_upload_to_search.py
```

### `06a_upload_scenario_assets_to_blob.py`（維護者入口）

- 用途：把情境來源文件、表格與中介產物上傳到對應的 Blob container
- 什麼時候跑：你要準備 blob-based 素材、測試知識來源附件，或維護情境資產時

```bash
python scripts/06a_upload_scenario_assets_to_blob.py --scenario default
python scripts/06a_upload_scenario_assets_to_blob.py --data-folder data/default
```

### `06b_upload_to_foundry_knowledge.py`（維護者入口）

- 用途：建立或更新 Foundry IQ 路徑所需的 knowledge source、knowledge base 和 project connection
- 什麼時候跑：你要走 Foundry-native IQ agent 路徑時

```bash
python scripts/06b_upload_to_foundry_knowledge.py
```

### `07_create_foundry_agent.py`（維護者入口）

- 用途：在 Foundry project 建立主 workshop agent
- 什麼時候跑：`04` 和 `06` 準備好之後

```bash
python scripts/07_create_foundry_agent.py
python scripts/07_create_foundry_agent.py --foundry-only
```

### `07b_create_foundry_iq_agent.py`（維護者入口）

- 用途：在 Foundry project 建立使用 knowledge base MCP tool 的文件型 agent
- 什麼時候跑：`06b` 跑完之後，且你想在 Foundry 內直接示範文件 agent 時

```bash
python scripts/07b_create_foundry_iq_agent.py
```

### `08_test_foundry_agent.py`（Deprecated shim）

- 用途：舊版測試入口名稱；目前只保留相容性轉呼叫
- 什麼時候跑：你在維護舊筆記或比對 legacy 路徑時

```bash
python scripts/08_test_foundry_agent.py
python scripts/08_test_foundry_agent.py --foundry-only

# 一般請改用公開入口
python scripts/participant_validate_docs_data.py
python scripts/participant_validate_docs.py
```

### `08b_test_foundry_iq_agent.py`（Deprecated shim）

- 用途：舊版 Foundry IQ 測試入口名稱；目前只保留相容性轉呼叫
- 什麼時候跑：你在維護舊筆記或比對 legacy 路徑時

```bash
python scripts/08b_test_foundry_iq_agent.py

# 一般請改用公開入口
python scripts/participant_validate_foundry_iq.py
```

---

[← 腳本用途、快速路徑與執行順序](05-script-sequence.md) | [選配 demo 09-13 →](05c-script-optional-demos.md)