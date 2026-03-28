# 進階：維護者腳本對照

這一頁是維護者／講師用的進階參考頁。

學員如果只想知道要跑哪些命令，請優先看公開入口，不需要理解底下的 internal / pipeline 腳本。

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

如果你要除錯、拆解流程，或理解背後的 internal / pipeline 分工，再往下看維護者腳本對照。

## 維護者核心流程順序

```text
01 產生情境資料
02 建立 Fabric 項目
03 載入資料到 Fabric
04 產生 NL2SQL prompt
06 上傳文件到 Azure AI Search
07 建立 Foundry agent
08 測試 agent
```

平常不一定要手動逐支執行，因為新的公開 wrappers 會替你切到對應的 prepare / validate 路徑。這一段主要是給維護者理解底層組成。

## 維護者腳本對照

### `00_admin_prepare_demo.py`（legacy shim）

- 用途：目前的內部 prepare orchestration；對外已由新的 `admin_prepare_*` wrappers 包裝
- 什麼時候跑：你在除錯或維護舊路徑時

```bash
python scripts/00_admin_prepare_demo.py
python scripts/00_admin_prepare_demo.py --mode foundry-only
python scripts/00_admin_prepare_demo.py --mode foundry-iq
python scripts/00_admin_prepare_demo.py --mode full --from-step 02
python scripts/00_admin_prepare_demo.py --mode full --clean --industry "Insurance" --usecase "Property insurance with claims processing and policy management"
```

### `01_generate_sample_data.py`

- 用途：根據輸入情境產生新的 sample data
- 什麼時候跑：你在公開入口之外，直接做資料生成除錯時

```bash
python scripts/author_generate_custom_data.py
```

如果你要看 `--industry` / `--usecase` / `--size` 的完整自訂方式，請回 [產生自訂資料](../02-customize/02-generate.md)。

### `01_generate_sample_data_templates.py`

- 用途：用固定 template 產生內建情境資料
- 什麼時候跑：你想走 template-based 固定情境時

```bash
python scripts/01_generate_sample_data_templates.py --scenario retail --size small
```

### `02_create_fabric_items.py`

- 用途：在 Fabric 建立 Lakehouse、Ontology、DataBindings 和 relationships
- 什麼時候跑：你要使用完整的 Fabric IQ 路徑時

```bash
python scripts/02_create_fabric_items.py
python scripts/02_create_fabric_items.py --clean
```

### `03_load_fabric_data.py`

- 用途：把 CSV 載入 Lakehouse
- 什麼時候跑：`02` 完成之後

```bash
python scripts/03_load_fabric_data.py
```

### `04_generate_agent_prompt.py`

- 用途：產生 `schema_prompt.txt`
- 什麼時候跑：你要讓 agent 理解 schema 時

```bash
python scripts/04_generate_agent_prompt.py
python scripts/04_generate_agent_prompt.py --from-config
```

### `05_create_fabric_agent.py`（legacy shim）

- 用途：較早期的 Fabric Data Agent 路徑
- 什麼時候跑：一般學員通常不用跑，主要保留作為舊路徑參考

```bash
python scripts/05_create_fabric_agent.py
```

### `06_upload_to_search.py`

- 用途：把 PDF 文件切 chunk、做 embedding、上傳到 Azure AI Search
- 什麼時候跑：你要讓 agent 可以回答文件問題時

```bash
python scripts/06_upload_to_search.py
```

### `06b_upload_to_foundry_knowledge.py`

- 用途：建立或更新 Foundry IQ 路徑所需的 knowledge source、knowledge base 和 project connection
- 什麼時候跑：你要走 Foundry-native IQ agent 路徑時

```bash
python scripts/06b_upload_to_foundry_knowledge.py
```

### `07_create_foundry_agent.py`

- 用途：在 Foundry project 建立主 workshop agent
- 什麼時候跑：`04` 和 `06` 準備好之後

```bash
python scripts/07_create_foundry_agent.py
python scripts/07_create_foundry_agent.py --foundry-only
```

### `07b_create_foundry_iq_agent.py`

- 用途：在 Foundry project 建立使用 knowledge base MCP tool 的文件型 agent
- 什麼時候跑：`06b` 跑完之後，且你想在 Foundry 內直接示範文件 agent 時

```bash
python scripts/07b_create_foundry_iq_agent.py
```

### `08_test_foundry_agent.py`（legacy shim）

- 用途：舊版測試入口名稱；目前保留為 shim
- 什麼時候跑：你在維護舊筆記或比對 legacy 路徑時

```bash
python scripts/participant_validate_docs_data.py
python scripts/participant_validate_docs.py
```

### `08b_test_foundry_iq_agent.py`（legacy shim）

- 用途：舊版 Foundry IQ 測試入口名稱；目前保留為 shim
- 什麼時候跑：你在維護舊筆記或比對 legacy 路徑時

```bash
python scripts/participant_validate_foundry_iq.py
```

---

[← 腳本用途、快速路徑與執行順序](05-script-sequence.md) | [選配 demo 09-13 →](05c-script-optional-demos.md)