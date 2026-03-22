# Fabric IQ：資料智慧

## 概要

Fabric IQ 這一頁講的是「自然語言問題怎麼變成資料查詢」。

在這個工作坊裡，agent 會先理解情境與資料表結構，再透過 `execute_sql` 產生唯讀 SQL，最後由本機 runtime 到 Fabric Lakehouse SQL analytics endpoint 查資料。

## 這頁要學什麼

看完這頁，你應該知道：

- agent 怎麼知道可以查哪些資料表
- 自然語言問題怎麼被轉成 SQL
- 為什麼這個流程是唯讀而且可控的

## 目前實際會用到哪些資料脈絡？

目前主路徑真正會進入 agent 指令或 runtime 的資訊包括：

| 元件 | 用途 | 範例 |
|------|------|------|
| **情境設定** | 告訴 agent 業務領域、資料表與關係 | 故障、工單、區域 |
| **schema prompt** | 提供資料表欄位與 join 線索 | `outages`、`tickets`、`customers` |
| **SQL guardrails** | 限制只允許唯讀查詢 | `SELECT`、`WITH`、拒絕 DDL / write |
| **Lakehouse SQL endpoint** | 查詢真正執行的位置 | Fabric Lakehouse |

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

## 為什麼這條路徑重要

因為很多企業問題需要的是數字、排名、比較、趨勢，這些答案通常來自資料表，而不是文件。

這個工作坊展示的是一條容易理解的路徑：

1. 先用情境設定和 schema 把問題說清楚
2. 再產生唯讀 SQL
3. 最後到 Fabric 查出結果

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

## 先記住這三件事

1. 使用者不需要自己寫 SQL，agent 會在受控範圍內代為生成唯讀查詢
2. scenario config 和 schema prompt 會幫助 agent 縮小資料語意上的歧義
3. 這一頁的重點不是平台神奇自動化，而是自然語言如何被轉成可執行查詢

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

## 你應該記住的重點

Fabric IQ 的價值不是「自動幫你做所有資料治理」，而是讓 agent 能在受控範圍內，把自然語言問題轉成可執行的查詢。

## 官方延伸閱讀

- [What is the SQL analytics endpoint for a lakehouse?](https://learn.microsoft.com/fabric/data-engineering/lakehouse-sql-analytics-endpoint)
- [What is a lakehouse in Microsoft Fabric?](https://learn.microsoft.com/fabric/data-engineering/lakehouse-overview#lakehouse-sql-analytics-endpoint)
- [Better together: the lakehouse and warehouse](https://learn.microsoft.com/fabric/data-warehouse/get-started-lakehouse-sql-analytics-endpoint)

---

[← Foundry IQ：文件](01-foundry-iq.md) | [清理 →](../04-cleanup/index.md)
