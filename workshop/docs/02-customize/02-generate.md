# 產生自訂資料

## 執行 AI 產生器

在 `.env` 設定完成後，產生客戶專屬資料：

```bash
python scripts/00_build_solution.py --clean
```

| 旗標 | 用途 |
|------|------|
| `--clean` | 重設 Fabric 產物（切換情境時必要） |

### 替代方式：內嵌參數

直接在命令列覆蓋 `.env` 的設定：

```bash
python scripts/00_build_solution.py --clean \
  --industry "Insurance" \
  --usecase "Property insurance with claims processing and policy management"
```

## 產生流程

!!! note "關於下面的輸出範例"
  下列區塊是腳本常見的實際 console 輸出範例
  訊息語言與細節可能會隨腳本版本略有不同，請以步驟順序與成功標記為準

```
============================================================
Generating Custom Data with AI
============================================================

Industry: Insurance
Use Case: Property insurance with claims processing and policy management

[1/4] Generating ontology configuration...
  → Analyzing use case for entities and relationships
  → Created: Policies, Claims, Customers, Agents
  → Defined: 6 relationships, 4 business rules
  ✓ ontology_config.json

[2/4] Generating structured data (CSV)...
  → policies.csv (16 rows) — Policy details, coverage, premiums
  → claims.csv (40 rows) — Claim status, amounts, dates
  → customers.csv (20 rows) — Policyholder information
  → agents.csv (8 rows) — Agent assignments
  ✓ 4 CSV files generated

[3/4] Generating documents (PDF)...
  → claims_process.pdf — How to file and process claims
  → coverage_guide.pdf — Policy coverage explanations
  → underwriting_policy.pdf — Risk assessment guidelines
  ✓ 3 documents generated

[4/4] 產生示範問題...
  → 15 題涵蓋資料、文件與混合情境的示範問題
  ✓ sample_questions.txt

============================================================
Data generated: data/20260202_143022_insurance/
============================================================
```

## 檢視產生的內容

確認產生了什麼：

```bash
# 檢視產生的檔案
ls data/*/

# 讀取範例問題以供測試
cat data/*/config/sample_questions.txt
```

### 範例問題（保險案例）

你大致會看到三類問題：

- 結構化資料問題：目前有多少件未結案理賠、這個月理賠總金額是多少、哪位 agent 管理最多保單
- 文件問題：房屋保險理賠流程是什麼、標準住宅保單涵蓋哪些內容、高風險物件的核保條件是什麼
- 混合問題：哪些未結案理賠快接近 SLA 截止時間、目前是否有理賠項目超出標準保單範圍

## 預期輸出

完整建置約需 5 分鐘：

```
============================================================
Building Solution: Insurance
============================================================

[01a/07] Generating AI data...
  ✓ Ontology, CSVs, PDFs, and questions generated

[02/07] Setting up Fabric workspace...
  ✓ Cleaned previous artifacts
  ✓ Lakehouse: iqworkshop_lakehouse
  ✓ Warehouse: iqworkshop_warehouse

[03/07] Loading data into Fabric...
  ✓ policies.csv → 16 rows
  ✓ claims.csv → 40 rows
  ✓ customers.csv → 20 rows
  ✓ agents.csv → 8 rows

[04/07] Generating NL2SQL prompt...
  ✓ Schema prompt created for insurance domain

[05/07] Creating Fabric Data Agent...
  ✓ Agent: fabric-agent-insurance

[06/07] Uploading documents to AI Search...
  ✓ 3 documents → 24 chunks indexed

[07/07] Creating Orchestrator Agent...
  ✓ Agent: insurance-multi-agent

============================================================
Build complete! Ready for customer PoC.
============================================================
```

## 疑難排解

### AI 產生逾時

- 檢查你的網路連線
- 嘗試使用 `--size small` 加快產生速度
- 確認 Azure AI Services 配額

### --clean 時出現 Fabric 錯誤

- 確認 `FABRIC_WORKSPACE_ID` 正確
- 確認你對工作區具備可建立與清理 Fabric 產物的權限
- 等待一分鐘後重試（Fabric 操作可能較慢）

---

[← 總覽](index.md) | [建置與測試 PoC →](03-demo.md)
