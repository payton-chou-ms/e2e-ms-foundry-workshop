# 產生自訂資料

這一頁的目標不是檢查每一行 console log，而是幫你判斷「資料有沒有成功生成」以及「生成後我該看哪幾個地方」。

## 先決定你要改哪一層

如果你現在要自訂情境，先用下面這個簡單判斷：

1. **只想換產業 / use case**：不用改 script 原始碼，改輸入值就好
2. **想重新建整套 PoC**：跑 `00_admin_prepare_demo.py --mode full --clean`
3. **只想先看新資料長什麼樣子**：跑 `01_generate_sample_data.py`

## 你實際會動到哪些 script

大多數情況下，你只需要操作這兩支：

1. `scripts/00_admin_prepare_demo.py`
2. `scripts/01_generate_sample_data.py`

它們的分工很簡單：

| script | 什麼時候用 | 會做什麼 |
|--------|------------|-----------|
| `00_admin_prepare_demo.py` | 你要重建完整 PoC 或切換 prepare 模式 | 轉到對應 prepare 路徑，重跑資料、Fabric、Search、agent |
| `01_generate_sample_data.py` | 你只想先生成新的資料與文件 | 只產生新的 data folder，不重建後面資源 |

`00_admin_prepare_demo.py` 會把你提供的 `--industry`、`--usecase`、`--size` 往下傳給內部 build pipeline，所以第一次使用時，直接改公開入口的執行參數通常最省事。

## 執行 AI 產生器

在 `.env` 設定完成後，產生客戶專屬資料：

```bash
python scripts/00_admin_prepare_demo.py --mode full --clean
```

| 旗標 | 用途 |
|------|------|
| `--clean` | 重設 Fabric 產物（切換情境時必要） |

### 替代方式：內嵌參數

直接在命令列覆蓋 `.env` 的設定：

```bash
python scripts/00_admin_prepare_demo.py --mode full --clean \
  --industry "Insurance" \
  --usecase "Property insurance with claims processing and policy management"
```

### 如果你只想重跑資料生成

```bash
python scripts/01_generate_sample_data.py \
  --industry "Insurance" \
  --usecase "Property insurance with claims processing and policy management" \
  --size small
```

這種做法適合下面兩種情況：

1. 你想先看 AI 生成的資料品質
2. 你還沒決定要不要把這組資料正式建進 Fabric / Search / agent

### 如果你是第一次自訂，建議直接用哪個？

第一次使用時，建議直接用這個：

```bash
python scripts/00_admin_prepare_demo.py --mode full --clean \
  --industry "Your Industry" \
  --usecase "Your use case description" \
  --size small
```

因為這樣最不容易漏掉後面的步驟。

## 產生流程

!!! note "關於下面的輸出範例"
  下列區塊是腳本常見的實際 console 輸出範例
  訊息語言與細節可能會隨腳本版本略有不同，請以步驟順序與成功標記為準

第一次跑時，你可以只看三件事：

1. 有沒有成功生成 ontology、CSV、PDF 與 sample questions
2. 最後有沒有輸出一個新的 `data/...` 目錄
3. 後續測試用的 `sample_questions.txt` 是否存在

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

生成完成後，先做最實用的確認：到底生成了哪些檔案，以及後面可以拿什麼問題來測。

```bash
# 檢視產生的檔案
ls data/*/

# 讀取範例問題以供測試
cat data/*/config/sample_questions.txt
```

### 範例問題（保險案例）

你大致會看到三類問題。這一段最重要的價值，是幫你判斷生成結果有沒有同時涵蓋資料、文件和混合問法：

- 結構化資料問題：目前有多少件未結案理賠、這個月理賠總金額是多少、哪位 agent 管理最多保單
- 文件問題：房屋保險理賠流程是什麼、標準住宅保單涵蓋哪些內容、高風險物件的核保條件是什麼
- 混合問題：哪些未結案理賠快接近 SLA 截止時間、目前是否有理賠項目超出標準保單範圍

## 預期輸出

完整建置約需 5 分鐘。

讀這段輸出時，不需要逐行比對；你只要確認每個主要階段都有成功標記即可：

- AI 資料有生成
- Fabric workspace 有建立
- 文件有上傳到 Search
- Orchestrator Agent 有建立

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

### 我看到很多輸出，但不確定算不算成功

- 先看最後是否有新的 `data/<timestamp>_<scenario>/`
- 再看 `config/sample_questions.txt` 是否存在
- 如果你跑的是完整 build，再看最後是否有 `Build complete!` 類似成功訊息

---

[← 總覽](index.md) | [建置與測試 PoC →](03-demo.md)
