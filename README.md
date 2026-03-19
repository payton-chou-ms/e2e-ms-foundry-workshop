# Build faster with Solution Accelerators – Foundry IQ + Fabric IQ (Workshop)

Build AI agents that combine **unstructured document knowledge** with **structured enterprise data** while giving you a clear path to explain the broader five-axis architecture behind the demo.

## The Opportunity

Organizations have valuable knowledge spread across documents (PDFs, policies, manuals) and structured systems (databases, data warehouses). By connecting these sources through AI, users can get unified answers from a single conversational interface.

## The Solution

This lab enables an intelligent agent that:

- **Deploys the required models** for chat and embeddings, with optional extension models kept separate
- **Creates a prompt agent** that orchestrates grounded reasoning in Azure AI Foundry
- **Defines a strict tool contract** for SQL and document retrieval with explicit guardrails
- **Creates knowledge bases** from documents with agentic retrieval (plan, iterate, reflect)
- **Defines business ontology** to understand entities, relationships, and rules
- **Combines both** to answer complex business questions

## The five-axis architecture

The workshop runtime stays simple, but the technical story now spans five axes:

| Axis | Why it exists |
|------|---------------|
| **Foundry Model** | Separates required chat + embedding deployments from optional extensions |
| **Foundry Agent** | Stores and reuses the prompt agent definition in the Foundry project |
| **Foundry Tool** | Constrains function calls with a strict SQL + document tool contract |
| **Foundry IQ + Fabric IQ** | Grounds answers in enterprise documents and business data |
| **Control Plane** | Provides the Azure resources, connections, RBAC, and observability that support the runtime |

The main workshop path still focuses on two user-visible capabilities:

1. document grounding through Foundry IQ
2. structured-data grounding through Fabric IQ

The extra axes explain how that experience is built and governed.

---

## Get Started

### Prerequisites

- Azure subscription with Contributor access
- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- [Python 3.10+](https://www.python.org/downloads/)
- Microsoft Fabric workspace (for Fabric IQ features)

### What You'll Build

| Component | Technology | Description |
|-----------|------------|-------------|
| Model deployments | Azure AI Services / Foundry | Required chat + embedding deployments, plus optional extensions |
| AI Agent | Azure AI Foundry | Orchestrates tools and generates responses |
| Tool contract | Azure AI Foundry + local runtime | Executes SQL and document retrieval with explicit guardrails |
| Knowledge Base | Foundry IQ | Agentic retrieval over documents |
| Business Ontology | Fabric IQ | Entities, relationships, and NL→SQL |
| Sample Data | AI-Generated | Custom data for any industry/use case |

### Open the Lab


[![Open in GitHub Codespaces](https://img.shields.io/badge/GitHub-Codespaces-blue?logo=github)](https://codespaces.new/nchandhi/nc-iq-workshop)
[![Open in VS Code](https://img.shields.io/badge/VS%20Code-Dev%20Containers-blue?logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/nchandhi/nc-iq-workshop)
[![Open in VS Code Web](https://img.shields.io/badge/VS%20Code-Open%20in%20Web-blue?logo=visualstudiocode)](https://vscode.dev/azure/?vscode-azure-exp=foundry&agentPayload=eyJiYXNlVXJsIjogImh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9uY2hhbmRoaS9uYy1pcS13b3Jrc2hvcC9tYWluL2luZnJhL3ZzY29kZV93ZWIiLCAiaW5kZXhVcmwiOiAiL2luZGV4Lmpzb24iLCAidmFyaWFibGVzIjogeyJhZ2VudElkIjogIiIsICJjb25uZWN0aW9uU3RyaW5nIjogIiIsICJ0aHJlYWRJZCI6ICIiLCAidXNlck1lc3NhZ2UiOiAiIiwgInBsYXlncm91bmROYW1lIjogIiIsICJsb2NhdGlvbiI6ICIiLCAic3Vic2NyaXB0aW9uSWQiOiAiIiwgInJlc291cmNlSWQiOiAiIiwgInByb2plY3RSZXNvdXJjZUlkIjogIiIsICJlbmRwb2ludCI6ICIifSwgImNvZGVSb3V0ZSI6IFsiYWktcHJvamVjdHMtc2RrIiwgInB5dGhvbiIsICJkZWZhdWx0LWF6dXJlLWF1dGgiLCAiZW5kcG9pbnQiXX0=)

---

## Lab Modules

### 01 Setup

#### Deploy Infrastructure

```bash
# Login to Azure
azd auth login

# Deploy all resources (AI Services, AI Search, Storage)
azd up
```

This deploys:
- Azure AI Services (Foundry) with GPT-4o-mini and text-embedding-3-large
- Azure AI Search (Basic tier with semantic search)
- Azure Storage Account
- Application Insights

All Azure endpoints are automatically saved to `.azure/<env>/.env` and loaded by the scripts.

#### Python Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Install dependencies (choose one)
pip install uv && uv pip install -r requirements.txt  # Fast (recommended)
pip install -r requirements.txt                        # Standard
```

#### Configure Environment

After `azd up`, Azure service endpoints are automatically available from the azd environment.

Edit `.env` in the project root for **project-specific settings only**:

```env
# --- Microsoft Fabric (required) ---
FABRIC_WORKSPACE_ID=your-workspace-id
SOLUTION_NAME=myproject

# --- AI Data Generation ---
INDUSTRY=Logistics
USECASE=Fleet management with delivery tracking
DATA_SIZE=small
```

**Sample Industry-UseCase Combinations:**

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

> **Note**: Azure endpoints (`AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_SEARCH_ENDPOINT`, etc.) are read automatically from the azd environment. No need to copy them manually!

---

### 02 Run the Pipeline

Run the complete pipeline with a single command:

```bash
python scripts/00_build_solution.py
```

This automatically:
1. **Generates sample data** - AI creates tables, PDFs, and questions for your industry
2. **Sets up Fabric** - Creates lakehouse and semantic ontology
3. **Loads data** - Uploads CSVs and creates Delta tables
4. **Generates prompts** - Creates optimized NL2SQL schema prompt
5. **Indexes documents** - Uploads PDFs to Azure AI Search
6. **Creates agent** - Builds Orchestrator Agent with SQL + Search

**Pipeline Options:**
- `--clean` - Reset Fabric artifacts when switching scenarios
- `--foundry-only` - Skip Fabric entirely, use AI Search only (no Fabric license required)
- `--from 03` - Start from a specific step
- `--only 06` - Run only one step
- `--skip 05` - Skip a specific step

---

### 03 Test the Agent

Run interactive tests combining both Foundry IQ and Fabric IQ:

```bash
python scripts/08_test_foundry_agent.py
```

Try these question types:

| Type | Example | Data Source |
|------|---------|-------------|
| SQL | "How many orders last month?" | Fabric (structured) |
| Document | "What is our return policy?" | Search (unstructured) |
| Combined | "Which drivers violate the hours policy?" | Both |

## Why this workshop scales from demo to architecture conversation

The workshop is intentionally simple at runtime:

- one prompt agent
- two core tools
- two grounding paths

But when the customer asks how it works, the repo now gives you a clear technical progression:

1. **Model**: what gets deployed
2. **Agent**: how orchestration is stored and reused
3. **Tool**: how function calls are constrained
4. **IQ**: how answers are grounded in documents and data
5. **Control Plane**: how Azure resources and permissions support the demo

That lets you keep the initial PoC easy to run without losing the ability to answer deeper technical questions.

### Optional Capability Demo: Content Understanding

Run the smallest standalone Content Understanding demo against one of the generated workshop PDFs:

```bash
python scripts/09_demo_content_understanding.py
```

This demo uses `prebuilt-documentSearch` on a local PDF. If the optional capability is not configured in the environment, the script prints a visible `SKIP:` message instead of blocking the main workshop flow.

---

### 04 Cleanup

Delete Azure resources when done:

```bash
azd down
```

---

## Project Structure

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
│   ├── 06_upload_to_search.py  # Document indexing
│   ├── 07_create_foundry_agent.py   # Create Foundry agent
│   ├── 08_test_foundry_agent.py     # Interactive testing
│   └── 09_demo_content_understanding.py  # Optional Content Understanding demo
└── data/                   # Generated sample data
```

---

## Estimated Costs

| Resource | SKU | Est. Monthly Cost |
|----------|-----|-------------------|
| Azure AI Services | S0 | ~$0 (pay per token) |
| Azure AI Search | Basic | ~$70 |
| Storage Account | Standard LRS | ~$1 |
| Application Insights | Pay-per-use | ~$2 |

**Total**: ~$75/month + token usage

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "FABRIC_WORKSPACE_ID not set" | Get ID from Fabric portal URL |
| "Role assignment failed" | Wait 2 min after `azd up`, retry |
| "Model deployment not found" | Check MODEL_DEPLOYMENT in `.env` |

---

## License

MIT
