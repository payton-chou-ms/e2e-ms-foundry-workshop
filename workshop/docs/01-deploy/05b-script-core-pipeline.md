# 主流程腳本 01-08

這一頁整理主流程最常碰到的 script。

## 主流程順序

```text
01 產生情境資料
02 建立 Fabric 項目
03 載入資料到 Fabric
04 產生 NL2SQL prompt
06 上傳文件到 Azure AI Search
07 建立 Foundry agent
08 測試 agent
```

平常不一定要手動逐支執行，因為 `00_build_solution.py` 會幫你串起主要步驟。

## 主流程腳本對照

### `00_build_solution.py`

- 用途：主流程總控腳本
- 什麼時候跑：你想快速把 workshop 建起來時

```bash
python scripts/00_build_solution.py --from 02
python scripts/00_build_solution.py --foundry-only
python scripts/00_build_solution.py --clean
python scripts/00_build_solution.py --from 04
```

### `01_generate_sample_data.py`

- 用途：根據產業與 use case 產生新的 sample data
- 什麼時候跑：你要換新的情境資料時

```bash
python scripts/01_generate_sample_data.py
python scripts/01_generate_sample_data.py --industry "Telecommunications" --usecase "Network outage tracking"
```

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

### `05_create_fabric_agent.py`

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

### `07_create_foundry_agent.py`

- 用途：在 Foundry project 建立主 workshop agent
- 什麼時候跑：`04` 和 `06` 準備好之後

```bash
python scripts/07_create_foundry_agent.py
python scripts/07_create_foundry_agent.py --foundry-only
```

### `08_test_foundry_agent.py`

- 用途：測試已建立好的 agent
- 什麼時候跑：`07` 跑完之後

```bash
python scripts/08_test_foundry_agent.py
python scripts/08_test_foundry_agent.py --foundry-only
```

---

[← 快速建置與測試](05a-script-core-paths.md) | [選配 demo 09-13 →](05c-script-optional-demos.md)