# 腳本用途與執行順序

## 概要

如果你是學員，先記住這四點就夠了：

- 大多數情況下，你**不需要手動把 `scripts/00` 到 `scripts/15` 全部跑一遍**
- 標準 workshop 最常用的是 `00_build_solution.py` 和 `08_test_foundry_agent.py`
- `09` 到 `13` 是選配 demo，要用到再跑
- `14` 到 `15` 是 multi-agent 延伸，不是基本 workshop 必跑步驟

最短主流程通常是：

```bash
python scripts/00_build_solution.py --from 02
python scripts/08_test_foundry_agent.py
```

如果你只有 Azure、沒有 Fabric，請改用：

```bash
python scripts/00_build_solution.py --foundry-only
python scripts/08_test_foundry_agent.py --foundry-only
```

## 先用這張表判斷你要看哪幾支

| 你的目標 | 你通常需要的腳本 |
|----------|------------------|
| 跑通標準 workshop | `00`、`08` |
| 從頭理解主流程 | `01`、`02`、`03`、`04`、`06`、`07`、`08` |
| 驗證選配能力 | `09`、`10`、`11`、`12`、`13` |
| 看多代理程式延伸 | `14`、`15` |

## 主流程順序

標準 workshop 的主流程可以理解成下面這一條：

```text
01 產生情境資料
02 建立 Fabric 項目
03 載入資料到 Fabric
04 產生 NL2SQL prompt
06 上傳文件到 Azure AI Search
07 建立 Foundry agent
08 測試 agent
```

平常你不一定要手動逐支執行，因為 `00_build_solution.py` 會幫你把前面的建置步驟串起來。

## 每一支 script 是做什麼、什麼時候跑、怎麼跑

### `00_build_solution.py`

**它是做什麼的**

- 這是主流程總控腳本
- 它會依照你指定的模式，依序執行主要建置步驟

**什麼時候跑**

- 你要快速把 workshop 建起來時
- 你不想手動逐支執行 `01` 到 `07` 時

**怎麼跑**

```bash
python scripts/00_build_solution.py --from 02
```

常見變體：

```bash
python scripts/00_build_solution.py
python scripts/00_build_solution.py --foundry-only
python scripts/00_build_solution.py --clean
python scripts/00_build_solution.py --from 04
```

### `01_generate_sample_data.py`

**它是做什麼的**

- 根據你的產業與 use case 產生一套新的 sample data
- 會產生 CSV、PDF、ontology config 和示範問題

**什麼時候跑**

- 你要換新的產業或新的 use case
- 你想從頭重做情境資料

**怎麼跑**

```bash
python scripts/01_generate_sample_data.py
python scripts/01_generate_sample_data.py --industry "Telecommunications" --usecase "Network outage tracking"
```

### `01_generate_sample_data_templates.py`

**它是做什麼的**

- 用固定 template 產生內建情境資料

**什麼時候跑**

- 你想走 template-based 的固定情境
- 一般學員通常不用先跑這支

**怎麼跑**

```bash
python scripts/01_generate_sample_data_templates.py --scenario retail --size small
```

### `02_create_fabric_items.py`

**它是做什麼的**

- 在 Fabric 建立 Lakehouse、Ontology、DataBindings 和 relationships
- 這一步還不會把資料真正載入進去

**什麼時候跑**

- 你要使用完整的 Fabric IQ 路徑時
- `01` 已經產生好資料之後

**怎麼跑**

```bash
python scripts/02_create_fabric_items.py
python scripts/02_create_fabric_items.py --clean
```

### `03_load_fabric_data.py`

**它是做什麼的**

- 把 CSV 上傳進 Lakehouse，載入成可查詢的資料表

**什麼時候跑**

- `02` 已經建立好 Fabric 項目之後

**怎麼跑**

```bash
python scripts/03_load_fabric_data.py
```

### `04_generate_agent_prompt.py`

**它是做什麼的**

- 根據 ontology/schema 產生給 agent 使用的 `schema_prompt.txt`

**什麼時候跑**

- 你要讓 agent 能正確理解資料表與欄位時

**怎麼跑**

```bash
python scripts/04_generate_agent_prompt.py
python scripts/04_generate_agent_prompt.py --from-config
```

### `05_create_fabric_agent.py`

**它是做什麼的**

- 這是較早期的 Fabric Data Agent 路徑

**什麼時候跑**

- 一般學員通常**不用跑**
- 它現在主要保留作為舊路徑參考

**怎麼跑**

```bash
python scripts/05_create_fabric_agent.py
```

### `06_upload_to_search.py`

**它是做什麼的**

- 把 PDF 文件切 chunk、做 embedding、上傳到 Azure AI Search

**什麼時候跑**

- 你要讓 agent 可以回答文件型問題時

**怎麼跑**

```bash
python scripts/06_upload_to_search.py
```

### `07_create_foundry_agent.py`

**它是做什麼的**

- 在 Foundry project 建立主 workshop agent
- 完整模式會有 SQL + Search 兩個工具
- `--foundry-only` 只會建立 Search-only agent

**什麼時候跑**

- `04` 和 `06` 已準備好之後
- 完整模式下，通常也代表 `02`、`03` 已完成

**怎麼跑**

```bash
python scripts/07_create_foundry_agent.py
python scripts/07_create_foundry_agent.py --foundry-only
```

### `08_test_foundry_agent.py`

**它是做什麼的**

- 測試你剛建立好的 agent
- 這也是你最常用來 demo 的互動式腳本

**什麼時候跑**

- `07` 跑完之後

**怎麼跑**

```bash
python scripts/08_test_foundry_agent.py
python scripts/08_test_foundry_agent.py --foundry-only
```

## 選配 demo：09 到 13

這些都不是主流程必跑步驟。只有在你要示範額外能力時才需要。

### `09_demo_content_understanding.py`

**用途**：示範 Content Understanding 對本機 PDF 的分析。

```bash
python scripts/09_demo_content_understanding.py
python scripts/09_demo_content_understanding.py --strict
```

### `09_publish_foundry_agent.py`

**用途**：做 publish 前檢查，確認 agent、Azure CLI、Bot Service provider 等前置條件。

```bash
python scripts/09_publish_foundry_agent.py
python scripts/09_publish_foundry_agent.py --teams
```

### `10_demo_browser_automation.py`

**用途**：示範 Browser Automation tool。

```bash
python scripts/10_demo_browser_automation.py
python scripts/10_demo_browser_automation.py --strict
```

### `11_demo_web_search.py`

**用途**：示範 Web Search tool。

```bash
python scripts/11_demo_web_search.py
python scripts/11_demo_web_search.py --strict
```

### `12_demo_pii_redaction.py`

**用途**：示範 PII detection 和 redaction。

```bash
python scripts/12_demo_pii_redaction.py
python scripts/12_demo_pii_redaction.py --strict
```

### `13_demo_image_generation.py`

**用途**：示範 image generation。

```bash
python scripts/13_demo_image_generation.py
python scripts/13_demo_image_generation.py --strict
```

## Multi-agent 延伸：14 到 15

這兩支不是基本 workshop 必跑步驟。它們是給你在主流程跑通之後，往 multi-agent workflow 延伸用的。

### `14_create_multi_agent_workflow.py`

**用途**：依照 `multi_agent/workflow.yaml` 建立多角色 agents。

```bash
python scripts/14_create_multi_agent_workflow.py
python scripts/14_create_multi_agent_workflow.py --scenario policy_gap_analysis
```

### `15_test_multi_agent_workflow.py`

**用途**：執行 multi-agent workflow。

```bash
python scripts/15_test_multi_agent_workflow.py --scenario policy_gap_analysis
python scripts/15_test_multi_agent_workflow.py --scenario exception_triage --question "We saw an unusual spike in escalations. What policy applies and what does the data suggest?"
```

### 最新 Agent Framework 小範例

如果你想把上面的 multi-agent 概念，對照到新版 Microsoft Agent Framework API，可以直接看 `scripts/16_agent_framework_workflow_example.py`。這支是幫你理解新版寫法的最小範例，不是本 repo 目前 workshop 主流程的正式實作。

建議先固定目前常見的 preview 版本：

```bash
pip install --pre "agent-framework-core==1.0.0rc3" "agent-framework-azure-ai==1.0.0rc3"
```

如果你之後要把 workflow 包成 HTTP 服務，再另外補裝 hosting adapter：

```bash
pip install --pre "azure-ai-agentserver-core==1.0.0b16" "azure-ai-agentserver-agentframework==1.0.0b16"
```

執行方式：

```bash
python scripts/16_agent_framework_workflow_example.py
python scripts/16_agent_framework_workflow_example.py --question "Summarize the policy risk and next step."
```

這支腳本示範兩個 agents 串成一條 workflow，再把 workflow 包成一個 agent 來執行。它也刻意用新版較常見的 `WorkflowBuilder(start_executor=...)` 寫法。

你可以把它對照成這個 workshop 的縮小版心智模型：

- `policy-researcher` 類似先產出 `policy_findings` 或 `data_findings`
- `answer-synthesizer` 類似最後整理成 `final_answer`
- `WorkflowBuilder(start_executor=...)` 則是新版 API 比較常見的 workflow 起手式

## 學員最常用的兩條路

### 路徑 A：標準 workshop

```bash
python scripts/00_build_solution.py --from 02
python scripts/08_test_foundry_agent.py
```

### 路徑 B：只有 Foundry，沒有 Fabric

```bash
python scripts/00_build_solution.py --foundry-only
python scripts/08_test_foundry_agent.py --foundry-only
```

## 如果你想手動逐步跑主流程

```bash
python scripts/01_generate_sample_data.py
python scripts/02_create_fabric_items.py
python scripts/03_load_fabric_data.py
python scripts/04_generate_agent_prompt.py
python scripts/06_upload_to_search.py
python scripts/07_create_foundry_agent.py
python scripts/08_test_foundry_agent.py
```

## 你可以怎麼使用這一頁

- 先看概要，判斷自己是不是只需要 `00` 和 `08`
- 如果某一步失敗，再回來查那支 script 的用途與執行命令
- 如果你要加 demo，再看 `09` 到 `13`
- 如果你要看進階延伸，再看 `14` 到 `15`

---

[← 建置方案](04-run-scenario.md) | [為你的使用案例自訂 →](../02-customize/index.md)