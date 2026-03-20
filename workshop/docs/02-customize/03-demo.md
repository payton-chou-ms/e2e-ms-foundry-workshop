# 建置與測試（客戶 PoC）

## 測試你的方案

產生完成後，測試代理程式：

```bash
python scripts/08_test_foundry_agent.py
```

## 使用產生的範例問題

每個情境都會在資料夾中產生可直接使用的範例問題：

```bash
# 檢視你的情境的範例問題
cat data/default/config/sample_questions.txt
```

檔案包含三類問題：

| 分類 | 來源 | 範例 |
|------|------|------|
| **結構化資料問題** | Fabric IQ（資料） | "How many open claims do we have?" |
| **非結構化資料問題** | Foundry IQ（文件） | "What's our process for filing a property claim?" |
| **組合式問題** | 兩個來源 | "Which claims are approaching our SLA deadline based on our process guidelines?" |

!!! tip "先使用這些問題"
    產生的問題是針對你的情境的資料與文件量身打造的。請先使用這些問題，再自行即興發問

## 目前的工具合約

Workshop 代理程式使用一個小型、明確的工具合約。讓你的 demo 問題落在這些邊界內，行為會更可預測。

| 工具 | 用於 | 不要用於 | 輸入結構描述 | 結果格式 |
|------|------|----------|------------|----------|
| **execute_sql** | 在 Fabric 表格中做計數、加總、趨勢、排名、join 與記錄查詢 | 政策、程序、敘事性說明，或任何寫入操作 | `sql_query: string` | 含列數的 Markdown 表格 |
| **search_documents** | 政策、程序、FAQ、指引，以及其他非結構化文件內容 | 計算或大範圍表格掃描 | `query: string`, `top?: integer` | 含來源、標題與頁數的引用段落 |

在 `--foundry-only` 模式下，代理程式只註冊 `search_documents`。

### 回應迴圈

當你執行 `python scripts/08_test_foundry_agent.py` 時，執行時會依照以下迴圈：

1. 模型檢視問題，決定是否需要 `execute_sql`、`search_documents`，或兩者皆需
2. 本機腳本執行每個被請求的工具，並列印預覽讓你看到發生了什麼
3. 原始工具輸出以 `function_call_output` 傳回模型
4. 模型從工具結果合成最終答案

### 範例輸出

```text
[SQL Tool] Executing query:
    SELECT TOP 5 claim_id, status
    FROM claims

| claim_id | status |
|---|---|
| CLM-1001 | Open |
| CLM-1002 | Pending |

(2 rows returned)
```

```text
[Search Tool] Searching for: outage communication policy (top=3)...

--- Result 1 ---
Source: outage-policy.pdf (Page 2)
Title: Outage Management Policy
Content: Customers must be notified within 15 minutes of a confirmed outage...
```

## 測試技巧

### 先從結構化資料問題開始

展示自然語言查詢結構化資料的能力：

```
"How many [entities] do we have?"
"What's the total [metric] for [time period]?"
"Show me the top 5 [entities] by [metric]"
```

### 接著是非結構化資料問題

展示智慧文件擷取：

```
"What's our policy on [topic]?"
"How do we handle [process]?"
"What are the requirements for [action]?"
```

### 最後是組合式問題

這是「驚艷」時刻：同時需要兩個來源的問題：

```
"Based on our [policy], which [entities] need attention?"
"Are we meeting our [documented SLA] according to the data?"
"Which [items] don't comply with our [policy/guidelines]?"
```

## 準備你的測試腳本

在客戶會議之前，準備 5-7 個問題：

| # | 問題類型 | 範例 |
|---|----------|------|
| 1 | 結構化資料 | "How many open claims do we have?" |
| 2 | 結構化資料 | "What's the total value of claims filed this month?" |
| 3 | 結構化資料 | "Which agents have the most policies?" |
| 4 | 非結構化資料 | "What's our process for filing a property claim?" |
| 5 | 非結構化資料 | "What does our standard homeowner policy cover?" |
| 6 | **組合式** | "Which open claims are approaching our SLA deadline based on our process guidelines?" |
| 7 | **組合式** | "Do any current claims involve coverage types not in our standard policy?" |

!!! tip "讓客戶自己提問"
    在你準備好的問題之後，讓客戶提出自己的問題。這能展示方案可以處理真實情境，而不只是照稿演出

## 檢查點

!!! success "客戶 PoC 已就緒"
    你的自訂 PoC 應該：

    - [x] 準確回答結構化資料問題
    - [x] 擷取相關的非結構化文件內容
    - [x] 結合來源回答複雜問題
    - [x] 使用產業適當的用語

    **下一步：** 閱讀 [深入解析](../03-understand/index.md) 以準備回答技術問題

## 快速參考：替另一個產業使用案例重新產生

```bash
# 修改 .env 中新客戶的產業與使用案例，然後：
python scripts/00_build_solution.py --clean

# 或內嵌：
python scripts/00_build_solution.py --clean \
  --industry "New Industry" \
  --usecase "New use case description"
```

---

[← 產生與建置](02-generate.md) | [深入解析 →](../03-understand/index.md)
