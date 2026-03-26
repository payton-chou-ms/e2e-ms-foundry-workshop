# 為你的使用案例自訂

這一節的目標，是把前面跑通的 workshop 主流程，快速換成更貼近你情境的資料、文件和測試問題。

!!! info "何時使用本節"
    請在完成 [管理員部署](../01-deploy/00-admin-deploy-share.md) 或 [參與者執行與驗證](../01-deploy/00-participant-run-validate.md) 之後再開始

!!! example "想直接用現成情境示範"
    如果你不想先從零設計產業資料，可以直接使用現成 manual demo：

    - [零售手動 demo](04-retail-manual-demo.md)：示範多 agent workflow、incident routing 與 image prompt 驗證
    - [合約關鍵字審閱手動 demo](05-contract-keyword-review-manual-demo.md)：示範 Azure Content Understanding 中間產物、規則清單與 reviewer 審閱流程

## 你需要提供的輸入

只需提供兩個輸入：

| 輸入 | 說明 | 範例 |
|------|------|------|
| **產業** | 業務領域或垂直產業 | 電信、零售、製造、金融、能源 |
| **使用案例** | 方案要協助處理的事項 | "理賠處理與保單管理" |

!!! tip "盡量描述詳細"
    你提供的使用案例說明越詳細，產生的內容就越貼合你的情境。例如：

    - ✓ "含理賠處理、保單管理與保障範圍查核的產物保險"
    - ✗ "保險相關事務"

## script 方面實際要改什麼

先記住一句就好：**大多數情況下，你不需要改 Python script 內容，只需要改輸入值與執行命令。**

| 你要改什麼 | 怎麼改 |
|------------|--------|
| 產業 / use case / 資料量 | 改 `.env`，或在命令列傳 `--industry`、`--usecase`、`--size` |
| 重跑整套流程 | 執行公開 prepare 入口 |
| 只先看新資料 | 只跑 `01_generate_sample_data.py` |

如果你只是要把 workshop 換成另一個產業情境，通常**不用修改**這些 script 原始碼：

- `scripts/00_admin_prepare_demo.py`
- `scripts/01_generate_sample_data.py`
- `scripts/02_create_fabric_items.py`
- `scripts/03_load_fabric_data.py`
- `scripts/07_create_foundry_agent.py`

## 先記住兩種最常用的改法

### 改法 A：重跑整套流程

如果你要把整個 PoC 換成新的產業與使用案例，最簡單的方式是直接重跑完整 build：

```bash
python scripts/00_admin_prepare_demo.py --mode full --clean \
    --industry "Insurance" \
    --usecase "Property insurance with claims processing and policy management" \
    --size small
```

這是最建議第一次使用者採用的方式，因為它會一路重跑：

1. 資料生成
2. Fabric 產物建立與載入
3. prompt 生成
4. Search 上傳
5. agent 建立

!!! note "固定範例資產"
    本頁下方各個產業 tab 都對應到 `data/static_examples/<scenario>/`。
    這一段是共用說明，不需要在每個 tab 裡再重新理解一次。

### 改法 B：只重跑資料生成

如果你只是想先看新的資料、文件和 sample questions 長什麼樣子，可以只跑：

```bash
python scripts/01_generate_sample_data.py \
    --industry "Insurance" \
    --usecase "Property insurance with claims processing and policy management" \
    --size small
```

這樣只會先產生新的 `data/<timestamp>_<scenario>/`，不會自動重建後面的 Fabric / Search / agent。

## 什麼情況下才需要真的改 script

只有在你要改「生成邏輯」本身時，才需要碰 script 原始碼。例如：

1. 想改資料表 schema 的生成方式
2. 想改 sample questions 的格式或分類
3. 想改 PDF 文件的內容結構
4. 想改 orchestrator agent 的 instructions 或 tool contract

如果你只是換產業或 use case，先不要改 script，先改輸入值就好。

## 會產生什麼內容

如果你是第一次做自訂，先把下面四種輸出看成四個用途就好：

- 文件：讓 agent 可以回答政策、流程和 FAQ 類問題
- 資料：讓 agent 可以回答查詢、統計和比較類問題
- Ontology：幫助 agent 理解資料之間的關係
- 範例問題：讓你有一組可以立刻測的題目

| 元件 | 產生的內容 |
|------|-----------|
| **文件** | 針對你的產業的政策、程序、FAQ |
| **資料** | 具有產業適當實體的真實 CSV 檔案 |
| **本體（Ontology）** | 用於 NL→SQL 的商業規則與關係 |
| **範例問題** | 用來測試方案的問題集 |

!!! note "固定範例資產"
    為了讓每個 tab 都對應到實際可查看的檔案，這份 workshop 材料提供固定樣本資產於 `data/static_examples/<scenario>/`
    每個固定樣本資料夾也都包含 `config/sample_questions.txt`，可直接對應該 tab 的問題集

## 範例轉換

你可以把下面這些情境當成「自訂之後大概會長什麼樣子」的快速參考。第一次看時，不需要逐欄比較；只要觀察每個產業都同時有資料、文件和問題集即可。

=== "電信"

    **輸入：** "含停機追蹤與障礙單管理的網路營運"

    **固定範例路徑：** `data/static_examples/telecommunications/`（含 `config/sample_questions.txt`）

    | 產生項目 | 說明 |
    |----------|------|
    | `network_outages.csv` | 停機事件、持續時間、影響程度 |
    | `trouble_tickets.csv` | 連結到停機事件的支援工單 |
    | `outage_management_policies.pdf` | 回應程序與 SLA |
    | `customer_service_policies.pdf` | 客戶通知指引 |

    **範例問題：**

    - "Which outage events exceeded our maximum duration policy?"
    - "What is the escalation procedure for high-impact outages?"
    - "Which open trouble tickets are linked to outages still under monitoring?"
    - "How many affected customers were involved in high-impact fiber outages?"
    - "When must customer updates be issued during a major outage?"

=== "零售"

    **輸入：** "含季節性庫存與退貨的時尚電子商務"

    **固定範例路徑：** `data/static_examples/retail/`（含 `config/sample_questions.txt`）

    | 產生項目 | 說明 |
    |----------|------|
    | `products.csv` | SKU、類別、季節系列 |
    | `orders.csv` | 客戶訂單與狀態 |
    | `return_policy.pdf` | 退貨與換貨指引 |
    | `shipping_guide.pdf` | 配送選項與時程 |

    **範例問題：**

    - "What is the return policy for discounted electronics?"
    - "Which spring products are already below their reorder point?"
    - "Which orders were returned after delivery?"
    - "Do any products in the spring catalog need immediate replenishment?"
    - "When do orders qualify for free standard shipping?"

=== "製造"

    **輸入：** "含品質控管與供應商的汽車零件"

    **固定範例路徑：** `data/static_examples/manufacturing/`（含 `config/sample_questions.txt`）

    | 產生項目 | 說明 |
    |----------|------|
    | `equipment.csv` | 機器、維護排程 |
    | `suppliers.csv` | 供應商關係、前置時間 |
    | `quality_standards.pdf` | QC 程序與門檻 |
    | `maintenance_guide.pdf` | 設備維護規範 |

    **範例問題：**

    - "Which machines are overdue for preventive maintenance?"
    - "What are the QC thresholds for critical automotive components?"
    - "Which suppliers have the longest lead times for key components?"
    - "Which production equipment is near or past its maintenance due date?"
    - "When must a supplier corrective action request be issued?"

=== "保險"

    **輸入：** "含理賠與保單管理的產物保險"

    **固定範例路徑：** `data/static_examples/insurance/`（含 `config/sample_questions.txt`）

    | 產生項目 | 說明 |
    |----------|------|
    | `policies.csv` | 保單明細、保障範圍、保費 |
    | `claims.csv` | 理賠狀態、金額、日期 |
    | `claims_process.pdf` | 理賠申請與處理流程 |
    | `coverage_guide.pdf` | 保單保障範圍說明 |

    **範例問題：**

    - "Which open claims are approaching their SLA deadline?"
    - "What does the standard homeowners policy cover?"
    - "Which claims require supervisor review within 48 hours?"
    - "Which policy types have the highest coverage limits?"
    - "What is the escalation path for catastrophic loss claims?"

=== "金融"

    **輸入：** "含貸款與合規的區域銀行"

    **固定範例路徑：** `data/static_examples/finance/`（含 `config/sample_questions.txt`）

    | 產生項目 | 說明 |
    |----------|------|
    | `accounts.csv` | 客戶帳戶、餘額 |
    | `loans.csv` | 貸款申請、狀態 |
    | `lending_policy.pdf` | 核准標準與利率 |
    | `compliance_guide.pdf` | 法規要求 |

    **範例問題：**

    - "Which loan applications currently meet our approval conditions?"
    - "What are the compliance requirements for large transactions?"
    - "Which applications still need senior credit review?"
    - "Which business accounts need a beneficial ownership refresh?"
    - "What risk score threshold requires manual underwriting?"

=== "能源"

    **輸入：** "含電網監控與停電回應的電力公用事業"

    **固定範例路徑：** `data/static_examples/energy/`（含 `config/sample_questions.txt`）

    | 產生項目 | 說明 |
    |----------|------|
    | `substations.csv` | 電網基礎設施、容量水位 |
    | `outages.csv` | 停電事件、影響區域、復電時間 |
    | `safety_protocols.pdf` | 現場人員安全程序 |
    | `emergency_response.pdf` | 停電升級與通知 |

    **範例問題：**

    - "Which substations are operating above 80 percent load?"
    - "What is the restoration priority for critical facilities?"
    - "Which outages should trigger regional command activation?"
    - "Which sites support critical facilities and are nearing capacity?"
    - "What safety checks are required before switching work begins?"

=== "教育"

    **輸入：** "含選課管理與課程排程的大學"

    **固定範例路徑：** `data/static_examples/education/`（含 `config/sample_questions.txt`）

    | 產生項目 | 說明 |
    |----------|------|
    | `students.csv` | 學生記錄、選課狀態 |
    | `courses.csv` | 課程目錄、排程、容量 |
    | `enrollment_policies.pdf` | 選課規則與截止日期 |
    | `academic_handbook.pdf` | 學術標準與程序 |

    **範例問題：**

    - "Which courses are at risk of under-enrollment?"
    - "What are the prerequisites for advanced engineering courses?"
    - "Which students are requesting or carrying overload credit loads?"
    - "Which courses are already at full capacity?"
    - "When can students add courses during the term?"

=== "旅宿"

    **輸入：** "含訂房與賓客服務的連鎖飯店"

    **固定範例路徑：** `data/static_examples/hospitality/`（含 `config/sample_questions.txt`）

    | 產生項目 | 說明 |
    |----------|------|
    | `reservations.csv` | 訂房記錄、房型、賓客資訊 |
    | `rooms.csv` | 房間庫存、狀態、設施 |
    | `guest_policies.pdf` | 入住/退房、取消規定 |
    | `service_standards.pdf` | 賓客體驗指引 |

    **範例問題：**

    - "Which arriving guests require priority room readiness?"
    - "What is the policy for late checkout?"
    - "Which rooms need housekeeping attention before same-day arrivals?"
    - "Which reservations are marked as VIP arrivals?"
    - "When do same-day cancellations incur a room charge?"

=== "物流"

    **輸入：** "含配送追蹤與駕駛合規的車隊管理"

    **固定範例路徑：** `data/static_examples/logistics/`（含 `config/sample_questions.txt`）

    | 產生項目 | 說明 |
    |----------|------|
    | `vehicles.csv` | 車隊清冊、維修狀態 |
    | `deliveries.csv` | 貨物、路線、配送狀態 |
    | `driver_policies.pdf` | 工時規定、安全要求 |
    | `routing_guidelines.pdf` | 路線最佳化程序 |

    **範例問題：**

    - 「哪些司機已接近每週駕駛時數上限？」
    - 「配送延遲超過 60 分鐘時，政策要求是什麼？」
    - 「哪些車輛因為檢查狀態而不能派車？」
    - 「哪些配送目前已延遲或有風險？」
    - 「路線延誤時，什麼情況下必須通知客戶？」

!!! tip "越具體越好"
    AI 會根據你的描述產生適當的實體名稱、真實的資料關係、產業專屬文件，以及相關的範例問題

---

[← 建置解決方案](../01-deploy/04-run-scenario.md) | [產生與建置 →](02-generate.md)
