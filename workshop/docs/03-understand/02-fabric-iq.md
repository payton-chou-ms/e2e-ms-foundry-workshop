# Fabric IQ：資料智慧

## 概要

Fabric IQ 這一頁講的是「自然語言問題怎麼變成資料查詢」，但要先從 Fabric 官網的一個關鍵概念開始：

- **Lakehouse** 是 Fabric 裡同時服務資料工程與分析的資料底座
- **SQL analytics endpoint** 是每個 lakehouse 自動帶出的唯讀 T-SQL 查詢面

這個 workshop 並不是直接對資料檔案做即興處理，而是利用這個唯讀 SQL 面，把 agent 產生的 SQL 安全地落到 Fabric 上。

在這個工作坊裡，agent 會先理解情境與資料表結構，再透過 `execute_sql` 產生唯讀 SQL，最後由本機 runtime 到 Fabric Lakehouse SQL analytics endpoint 查資料。

## 這頁要學什麼

看完這頁，你應該知道：

- Fabric 官網對 lakehouse 與 SQL analytics endpoint 的重點是什麼
- agent 怎麼知道可以查哪些資料表
- 自然語言問題怎麼被轉成 SQL
- 為什麼這個流程是唯讀、可控，而且適合教學

## 先記住五件事

1. **Lakehouse 把資料湖和資料倉儲常見能力放在同一個資料底座。**
2. **每個 lakehouse 都會自動有一個 SQL analytics endpoint，不需要另外建立。**
3. **SQL analytics endpoint 是唯讀的 T-SQL 查詢面，不是資料寫入面。**
4. **只有 Delta tables 會出現在這個 SQL 查詢面。**
5. **這個 workshop 的 Fabric IQ，本質上是「NL → read-only SQL → lakehouse SQL endpoint」。**

## 官網重點：Lakehouse 在 Fabric 裡是什麼

官方文件把 lakehouse 定位為一種把 data lake 的彈性和 data warehouse 的查詢能力結合在一起的 Fabric item。

最值得先記住的不是所有功能，而是這三件事：

- 一份資料可以同時被 Spark 與 SQL 使用
- 資料主要以 Delta Lake 形式管理
- Lakehouse 同時服務資料工程、分析與 BI 場景

用最簡單的方式講：

- 資料工程師可以用 Spark / notebook 處理資料
- 分析或報表路徑可以用 SQL 讀取整理好的表

這正是這個 workshop 想利用的分工。

## 官網重點：SQL analytics endpoint 到底是什麼

官方文件對 SQL analytics endpoint 的定義很清楚：它是 **lakehouse 上自動提供的唯讀 T-SQL query surface**。

這意味著幾件很重要的事：

| 官網重點 | 對 workshop 的意義 |
|----------|--------------------|
| 每個 lakehouse 建立時會自動有 SQL analytics endpoint | 不需要再額外建一個獨立 SQL 服務 |
| 這個 endpoint 對 Delta tables 提供唯讀 T-SQL | 很適合讓 agent 查數字、做排名、做聚合 |
| 背後使用和 Fabric Warehouse 相同的 SQL engine | 讀取速度與互動方式對分析場景很友善 |
| 寫入或更新資料不走這條路 | 這讓主流程更容易控制風險 |

這也是為什麼這份 workshop 把 SQL 工具嚴格限定成唯讀查詢，而不是讓 agent 自由產生任意 SQL。

## 官網重點：Lakehouse 和 Warehouse 的關係

官方文件也特別強調，lakehouse 和 warehouse 不是互斥，而是可以互補。

最實用的理解方式是：

- **Lakehouse**：適合 Spark、資料工程、混合型資料、medallion 架構
- **Warehouse**：適合 SQL-first、BI、維度建模、進一步資料服務化

而 SQL analytics endpoint 則是兩者之間很實用的橋：

- 它讓你可以用 T-SQL 直接查 lakehouse 裡整理好的 Delta tables
- 又不需要先把這批資料複製成另一份倉儲資料

對這個 workshop 來說，重點不是教你設計完整 warehouse，而是讓 agent 可以對整理好的 lakehouse 表做安全查詢。

## 目前實際會用到哪些資料脈絡？

目前主路徑真正會進入 agent 指令或 runtime 的資訊包括：

| 元件 | 用途 | 範例 |
|------|------|------|
| **情境設定** | 告訴 agent 業務領域、資料表與關係 | 故障、工單、區域 |
| **schema prompt** | 提供資料表欄位與 join 線索 | `outages`、`tickets`、`customers` |
| **SQL guardrails** | 限制只允許唯讀查詢 | `SELECT`、`WITH`、拒絕 DDL / write |
| **Lakehouse SQL endpoint** | 查詢真正執行的位置 | Fabric Lakehouse |

也就是說，這個 workshop 不是把 agent 直接丟去「猜資料庫怎麼長」。它先把資料語意和查詢邊界準備好，再讓 agent 在那個範圍內做 NL→SQL。

## NL→SQL 的運作方式

```
User: "Which outages had the most customer impact last month?"

┌─────────────────────────────────────────────────────────────┐
│  Step 1: GROUND                                              │
│  Agent reads scenario context and schema guidance           │
│  • Which tables are available?                              │
│  • Which joins are allowed?                                 │
│  • What business question is being asked?                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: TRANSLATE                                          │
│  Generate read-only T-SQL from grounded context:            │
│                                                             │
│  SELECT TOP 10 outage_id, region, customers_affected        │
│  FROM network_outages                                       │
│  WHERE outage_date >= DATEADD(month, -1, GETDATE())         │
│  ORDER BY customers_affected DESC                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: EXECUTE & EXPLAIN                                  │
│  Local runtime validates SQL, runs it against Fabric,       │
│  and formats rows for the model:                            │
│                                                             │
│  "Here are the outages with highest customer impact:        │
│   1. OUT-1042 (Northeast) - 15,234 customers                │
│   2. OUT-1089 (West) - 12,891 customers                     │
│   3. OUT-1056 (South) - 8,445 customers"                    │
└─────────────────────────────────────────────────────────────┘
```

這條路徑其實正好對應到 Fabric 官網描述的使用方式：

- 整理好的 Delta tables 放在 lakehouse
- SQL analytics endpoint 提供唯讀查詢面
- 上層應用程式用 T-SQL 查資料

這個 workshop 多做的一步，是把上層應用程式換成一個會做工具選擇與 SQL 生成的 agent。

## 為什麼這條路徑重要

因為很多企業問題需要的是數字、排名、比較、趨勢，這些答案通常來自資料表，而不是文件。

這個工作坊展示的是一條容易理解的路徑：

1. 先用情境設定和 schema 把問題說清楚
2. 再產生唯讀 SQL
3. 最後到 Fabric 查出結果

而且這條路徑有一個很重要的官網優勢：SQL analytics endpoint 是自動存在、唯讀、且面向 Delta tables 的。對教學和 PoC 來說，這比讓 agent 直接碰更寬鬆的資料平面安全得多。

## 結合智慧的力量

| 問題類型 | 來源 | 範例 |
|---------|------|------|
| **政策/流程** | Foundry IQ（文件） | 「我們的故障通知政策是什麼？」 |
| **指標/數字** | Fabric IQ（資料） | 「我們的平均解決時間是多少？」 |
| **綜合** | 兩者 | 「我們是否達到 SLA 目標？」 |

### 綜合範例

```
User: "Are we meeting our ticket resolution SLA?"

Agent thinking:
1. First, I need the SLA targets (documents)
   → Search Foundry IQ → "Critical: 4 hours, High: 8 hours, Medium: 24 hours"

2. Then, I need actual performance (data)
   → Query Fabric IQ → "Avg critical: 3.2 hrs, High: 7.1 hrs, Medium: 18.5 hrs"

3. Compare and respond:
   "Yes, we're meeting all SLA targets. Critical tickets average
   3.2 hours (target: 4 hours), High priority averages 7.1 hours
   (target: 8 hours), and Medium averages 18.5 hours (target: 24 hours)."
```

這也是為什麼這頁不能單獨看成「SQL 自動生成」。真正有價值的是：

- 文件提供規則、門檻、SLA、流程
- Fabric 資料提供實際數字與記錄
- agent 把兩者接起來

## 官網重點：這條查詢面能做什麼、不能做什麼

官方文件明確指出，SQL analytics endpoint 的特性是：

- 可以用 T-SQL 查詢 Delta tables
- 可以建立 views、functions、stored procedures 等 SQL 物件
- 可以做報表與分析查詢
- **不能**透過這條面去 insert、update、delete 資料

對這個 workshop 來說，最重要的是最後一點。因為這正好支撐了目前的 guardrail 設計：

- 只允許 `SELECT` 或 `WITH`
- 禁止 `INSERT`、`UPDATE`、`DELETE`、`DROP`、`ALTER` 等寫入或 DDL 行為

換句話說，這不是臨時寫死的限制，而是和 Fabric 官方對 SQL analytics endpoint 的定位一致。

## 先記住這四件事

1. 使用者不需要自己寫 SQL，agent 會在受控範圍內代為生成唯讀查詢
2. scenario config 和 schema prompt 會幫助 agent 縮小資料語意上的歧義
3. Lakehouse SQL analytics endpoint 是這條路徑真正落地執行 SQL 的地方
4. 這一頁的重點不是平台神奇自動化，而是自然語言如何被轉成可執行查詢

## 技術細節

### 目前 workshop 的資料路徑

```
┌─────────────────────────────────────────────────────────────┐
│                    Microsoft Fabric                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Lakehouse   │ →  │ SQL endpoint │ ←  │ Local runtime│  │
│  │  tables      │    │  (read-only) │    │ execute_sql  │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                ↑            │
│                                          ┌──────────┐       │
│                                          │ Foundry  │       │
│                                          │ agent    │       │
│                                          └──────────┘       │
└─────────────────────────────────────────────────────────────┘
```

更精確地說，這條路徑在 repo 內是這樣實作的：

- `02_create_fabric_items.py` 建立 lakehouse 與 ontology
- `03_load_fabric_data.py` 把 CSV 載入 lakehouse tables
- `07_create_foundry_agent.py` 把 schema / relationships / SQL 規則寫進 agent instructions
- `08_test_foundry_agent.py` 讀取 lakehouse metadata，取得 SQL analytics endpoint，執行唯讀 SQL

### 用來接地 SQL 的設定來源

```json
{
  "tables": {
    "network_outages": {
      "columns": ["outage_id", "region", "customers_affected", "duration_minutes"]
    }
  },
  "relationships": [
    {
      "from": "TroubleTickets",
      "to": "NetworkOutages",
      "fromKey": "outage_id",
      "toKey": "outage_id"
    }
  ]
}
```

這裡最重要的不是 JSON 格式本身，而是它提供了三種 agent 最需要的資訊：

- 有哪些表
- 可以用哪些欄位
- 哪些 join path 是合理的

沒有這些資訊，模型即使會寫 SQL，也很容易寫出語意錯誤或 join 錯誤的查詢。

## 官網重點：自動 metadata sync 為什麼重要

Fabric 官方文件提到，lakehouse 的 SQL analytics endpoint 會自動偵測 Delta table 的變化並同步 SQL metadata，沒有額外 import 或手動 sync 步驟。

這點對 workshop 的意義是：

- 你不需要先維護另一份 SQL schema
- 只要資料真的已經以 Delta table 形式進到 lakehouse
- SQL endpoint 就能把它暴露成可查詢的 SQL table

這也是為什麼這個 workshop 要先完成「載入到 lakehouse tables」，而不是只把 CSV 丟在隨便一個檔案夾裡。

## 你應該記住的重點

Fabric IQ 的價值不是「自動幫你做所有資料治理」，而是把 Fabric 官網提供的 lakehouse + read-only SQL surface，變成一條對 agent 友善、對教學可驗證的 NL→SQL 路徑。

## 官方延伸閱讀

- [What is the SQL analytics endpoint for a lakehouse?](https://learn.microsoft.com/fabric/data-engineering/lakehouse-sql-analytics-endpoint)
- [What is a lakehouse in Microsoft Fabric?](https://learn.microsoft.com/fabric/data-engineering/lakehouse-overview#lakehouse-sql-analytics-endpoint)
- [Better together: the lakehouse and warehouse](https://learn.microsoft.com/fabric/data-warehouse/get-started-lakehouse-sql-analytics-endpoint)

---

[← Foundry IQ：文件](01-foundry-iq.md) | [清理 →](../04-cleanup/index.md)
