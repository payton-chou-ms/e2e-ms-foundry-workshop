# 使用 Solution Accelerators 更快建構方案 – Foundry IQ + Fabric IQ（Workshop）

建構可同時結合**非結構化文件知識**與**結構化企業資料**的 AI 代理程式，同時保留一條清楚的路徑，讓你能說明這個 PoC 背後更完整的五主軸技術架構。

## 這個機會點

組織的重要知識通常分散在文件（PDF、政策文件、操作手冊）與結構化系統（資料庫、資料倉儲）中。透過 AI 串接這些來源，使用者就能在單一對話介面中取得整合後的答案。

## 方案內容

這個實作練習會建立一個智慧代理程式，具備以下能力：

- **部署必要模型**，供對話與向量嵌入使用，並將選配延伸模型獨立管理
- **建立提示詞代理程式**，在 Azure AI Foundry 中協調 grounded reasoning
- **定義嚴格的 tool contract**，以明確 guardrail 執行 SQL 與文件檢索
- **從文件建立 knowledge base**，透過 agentic retrieval（plan、iterate、reflect）取得答案
- **定義商業本體（business ontology）**，理解實體、關聯與規則
- **結合兩者**，回答更複雜的商業問題

## 五主軸架構

這個 workshop 的執行路徑維持簡潔，但技術敘事現在已經擴展成五個主軸：

| Axis | Why it exists |
|------|---------------|
| **Foundry Model** | 區分必要的 chat + embedding 部署與選配延伸模型 |
| **Foundry Agent** | 在 Foundry project 中儲存並重用 prompt agent 定義 |
| **Foundry Tool** | 用嚴格的 SQL + 文件 tool contract 約束 function call |
| **Foundry IQ + Fabric IQ** | 讓答案 grounded 到企業文件與商業資料 |
| **Control Plane** | 提供支撐 runtime 的 Azure 資源、connections、RBAC 與 observability |

主 workshop 路徑仍聚焦在兩個對使用者最可見的能力：

1. 透過 Foundry IQ 進行文件 grounding
2. 透過 Fabric IQ 進行結構化資料 grounding

其他主軸則用來說明這個體驗是如何被建構與治理的。

---

## 快速開始

### 先決條件

- 具備 Contributor 權限的 Azure subscription
- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- [Python 3.10+](https://www.python.org/downloads/)
- Microsoft Fabric 工作區（供 Fabric IQ 功能使用）

### 你將建立的內容

| Component | Technology | Description |
|-----------|------------|-------------|
| Model deployments | Azure AI Services / Foundry | 必要的 chat + embedding 部署，以及選配延伸模型 |
| AI Agent | Azure AI Foundry | 協調工具並產生回應 |
| Tool contract | Azure AI Foundry + local runtime | 以明確 guardrail 執行 SQL 與文件檢索 |
| Knowledge Base | Foundry IQ | 對文件做 agentic retrieval |
| Business Ontology | Fabric IQ | 實體、關聯與 NL→SQL |
| Sample Data | AI-Generated | 針對任意產業與使用案例產生客製資料 |

### 開啟 Lab


[![Open in GitHub Codespaces](https://img.shields.io/badge/GitHub-Codespaces-blue?logo=github)](https://codespaces.new/nchandhi/nc-iq-workshop)
[![Open in VS Code](https://img.shields.io/badge/VS%20Code-Dev%20Containers-blue?logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/nchandhi/nc-iq-workshop)
[![Open in VS Code Web](https://img.shields.io/badge/VS%20Code-Open%20in%20Web-blue?logo=visualstudiocode)](https://vscode.dev/azure/?vscode-azure-exp=foundry&agentPayload=eyJiYXNlVXJsIjogImh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9uY2hhbmRoaS9uYy1pcS13b3Jrc2hvcC9tYWluL2luZnJhL3ZzY29kZV93ZWIiLCAiaW5kZXhVcmwiOiAiL2luZGV4Lmpzb24iLCAidmFyaWFibGVzIjogeyJhZ2VudElkIjogIiIsICJjb25uZWN0aW9uU3RyaW5nIjogIiIsICJ0aHJlYWRJZCI6ICIiLCAidXNlck1lc3NhZ2UiOiAiIiwgInBsYXlncm91bmROYW1lIjogIiIsICJsb2NhdGlvbiI6ICIiLCAic3Vic2NyaXB0aW9uSWQiOiAiIiwgInJlc291cmNlSWQiOiAiIiwgInByb2plY3RSZXNvdXJjZUlkIjogIiIsICJlbmRwb2ludCI6ICIifSwgImNvZGVSb3V0ZSI6IFsiYWktcHJvamVjdHMtc2RrIiwgInB5dGhvbiIsICJkZWZhdWx0LWF6dXJlLWF1dGgiLCAiZW5kcG9pbnQiXX0=)

---

## Lab 模組

### 01 設定

#### 部署基礎架構

```bash
# 登入 Azure
azd auth login

# 部署所有資源（AI Services、AI Search、Storage）
azd up
```

這會部署：
- Azure AI Services (Foundry) with GPT-4o-mini and text-embedding-3-large
- Optional Content Understanding defaults: gpt-4.1-mini and text-embedding-3-large
- Azure AI Search (Basic tier with semantic search)
- Azure Storage Account
- Application Insights

所有 Azure endpoint 都會自動儲存到 `.azure/<env>/.env`，並由腳本讀取。

#### Python 環境

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# 安裝相依套件（擇一）
pip install uv && uv pip install -r requirements.txt  # 快速（建議）
pip install -r requirements.txt                        # 標準方式
```

#### 設定環境

執行 `azd up` 後，Azure service endpoint 會自動從 azd 環境載入。

請只在專案根目錄的 `.env` 中設定**專案專屬設定**：

```env
# --- Microsoft Fabric（必要） ---
FABRIC_WORKSPACE_ID=your-workspace-id
SOLUTION_NAME=myproject

# --- AI 資料產生 ---
INDUSTRY=Logistics
USECASE=Fleet management with delivery tracking
DATA_SIZE=small
```

**產業與使用案例範例組合：**

| Industry | Use Case |
|----------|----------|
| Telecommunications | Network operations and service management |
| Retail | Inventory management with sales analytics |
| Manufacturing | Production line tracking with quality control |
| Insurance | Claims processing and policy management |
| Finance | Transaction monitoring and fraud detection |
| Energy | Grid monitoring and outage response |
| Education | Student enrollment and course management |
| Hospitality | Hotel reservations and guest services |
| Logistics | Fleet management with delivery tracking |
| Real Estate | Property listings and lease management |

> **注意**：Azure endpoint（例如 `AZURE_AI_PROJECT_ENDPOINT`、`AZURE_AI_SEARCH_ENDPOINT`）會自動從 azd 環境讀取，不需要手動複製。

---

### 02 執行流程

使用單一命令執行完整 pipeline：

```bash
python scripts/00_build_solution.py
```

此命令會自動：
1. **產生範例資料** - 由 AI 依你的產業建立表格、PDF 與問題
2. **設定 Fabric** - 建立 Lakehouse 與語意本體
3. **載入資料** - 上傳 CSV 並建立 Delta table
4. **產生提示詞** - 建立最佳化的 NL2SQL 結構描述提示詞
5. **索引文件** - 將 PDF 上傳至 Azure AI Search
6. **建立代理程式** - 建立含 SQL + Search 的協調代理程式

**Pipeline 選項：**
- `--clean` - 在切換情境時重設 Fabric 產生物
- `--foundry-only` - 完全跳過 Fabric，只使用 AI Search（不需要 Fabric 授權）
- `--foundry-only` 也會先自動設定 Content Understanding defaults，讓 `09_demo_content_understanding.py` 可直接執行
- `--from 03` - 從指定步驟開始
- `--only 06` - 只執行單一步驟
- `--skip 05` - 跳過指定步驟

---

### 03 測試代理程式

執行互動式測試，同時驗證 Foundry IQ 與 Fabric IQ：

```bash
python scripts/08_test_foundry_agent.py
```

可先嘗試這幾種類型的問題：

| Type | Example | Data Source |
|------|---------|-------------|
| SQL | "How many orders last month?" | Fabric（結構化） |
| Document | "What is our return policy?" | Search（非結構化） |
| Combined | "Which drivers violate the hours policy?" | 兩者皆用 |

## 為什麼這個 workshop 能從 demo 延伸到架構對話

這個 workshop 在 runtime 層刻意維持簡潔：

- 一個 prompt agent
- 兩個 core tools
- 兩條 grounding path

但當客戶開始追問它是怎麼運作時，repo 現在也提供了一條清楚的技術展開路徑：

1. **Model**：部署了哪些模型
2. **Agent**：協調流程如何被儲存與重用
3. **Tool**：function call 如何被約束
4. **IQ**：答案如何 grounded 到文件與資料
5. **Control Plane**：Azure 資源與權限如何支撐整個 demo

這讓你可以在維持 PoC 容易執行的前提下，仍有能力回答更深入的技術問題。

### 選配能力 Demo：Content Understanding

可對產生出來的 workshop PDF 之一執行最小型的獨立 Content Understanding demo：

```bash
python scripts/09_demo_content_understanding.py
```

這個 demo 會對本機 PDF 使用 `prebuilt-documentSearch`。如果環境中尚未設定這個選配能力，腳本會印出明確的 `SKIP:` 訊息，而不是阻塞主 workshop 流程。

### 選配能力 Demo：目前驗證狀態

目前 repo 中的選配 demo 已調整為以下行為：

- `09_demo_content_understanding.py`：可用，會自動使用已部署的 Content Understanding defaults
- `10_demo_browser_automation.py`：SDK 相容性已修正；若未建立 Browser Automation / Playwright connection，會乾淨地 `SKIP:`
- `11_demo_web_search.py`：可用，已對齊目前 `azure-ai-projects` SDK 類型名稱
- `12_demo_pii_redaction.py`：可用，支援 `DefaultAzureCredential` 與 `AZURE_AI_ENDPOINT`，不再強制要求 `AZURE_LANGUAGE_KEY`
- `13_demo_image_generation.py`：已支援 AAD 驗證，但 East US 目前沒有可部署的可用 image model；若沒有 image deployment 會乾淨地 `SKIP:`

---

### 04 清理

完成後請刪除 Azure 資源：

```bash
azd down
```

---

## 專案結構

```
nc-iq-workshop/
├── .devcontainer/          # GitHub Codespaces config
├── .env.example            # Configuration template
├── azure.yaml              # azd configuration
├── infra/                  # Bicep infrastructure
│   ├── main.bicep
│   └── modules/
│       └── foundry.bicep
├── scripts/
│   ├── 00_build_solution.py    # Full pipeline orchestrator
│   ├── 01_generate_sample_data.py   # AI data generation
│   ├── 02_create_fabric_items.py  # Create Fabric items
│   ├── 03_load_fabric_data.py  # Load data to Fabric
│   ├── 04_generate_agent_prompt.py # Agent prompt generation
│   ├── foundry_tool_contract.py # Shared tool contract definitions
│   ├── foundry_trace.py         # Optional tracing bootstrap
│   ├── optional_demo_utils.py   # Shared helpers for optional demos
│   ├── 06_upload_to_search.py  # Document indexing
│   ├── 07_create_foundry_agent.py   # Create Foundry agent
│   ├── 08_test_foundry_agent.py     # Interactive testing
│   ├── 09_demo_content_understanding.py  # Optional Content Understanding demo
│   ├── 10_demo_browser_automation.py     # Optional browser automation demo
│   ├── 11_demo_web_search.py             # Optional web grounding demo
│   ├── 12_demo_pii_redaction.py          # Optional PII redaction demo
│   ├── 13_demo_image_generation.py       # Optional image generation demo
│   ├── 14_create_multi_agent_workflow.py # Declarative multi-agent creator
│   ├── 15_test_multi_agent_workflow.py   # Declarative multi-agent runner
│   └── foundry_multi_agent_runtime.py    # Shared multi-agent runtime helpers
├── multi_agent/            # Declarative multi-agent extension config
└── data/                   # Generated sample data
```

---

## 預估成本

| Resource | SKU | Est. Monthly Cost |
|----------|-----|-------------------|
| Azure AI Services | S0 | ~$0 (pay per token) |
| Azure AI Search | Basic | ~$70 |
| Storage Account | Standard LRS | ~$1 |
| Application Insights | Pay-per-use | ~$2 |

**總計**：約 `$75/月`，另加 token 使用成本

---

## 疑難排解

| Issue | Solution |
|-------|----------|
| "FABRIC_WORKSPACE_ID not set" | 從 Fabric 入口網站 URL 取得 ID |
| "Role assignment failed" | 在 `azd up` 後等待 2 分鐘再重試 |
| "Model deployment not found" | 檢查 `.env` 中的 `MODEL_DEPLOYMENT` |

---

## 授權

MIT
