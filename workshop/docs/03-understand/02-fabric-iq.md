# Fabric IQ：資料智慧

## 什麼是 Fabric IQ？

Fabric IQ 是一個語意智慧平台，將 AI 代理程式連接到商業資料。它透過**本體**來理解資料的含義，超越了簡單的資料庫查詢。

## 什麼是本體？

本體是一種語意模型，幫助 AI 理解您的業務：

| 元件 | 用途 | 範例 |
|------|------|------|
| **實體** | 業務物件 | 故障、工單、區域 |
| **關係** | 實體之間的連結方式 | 工單 → 關聯至 → 故障 |
| **規則** | 業務邏輯 | 「重大故障 = customerImpact > 1000」 |
| **動作** | 可查詢的操作 | GetOutagesByRegion、GetTicketResolutionTime |

## NL→SQL 的運作方式

```
User: "Which outages had the most customer impact last month?"

┌─────────────────────────────────────────────────────────────┐
│  Step 1: UNDERSTAND                                         │
│  Agent interprets intent using ontology:                    │
│  • "outages" → NetworkOutages entity                        │
│  • "customer impact" → customersAffected column              │
│  • "last month" → date filter                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: TRANSLATE                                          │
│  Generate SQL from semantic understanding:                  │
│                                                             │
│  SELECT outageId, region, customersAffected, duration       │
│  FROM network_outages                                       │
│  WHERE outageDate >= DATEADD(month, -1, GETDATE())          │
│  ORDER BY customersAffected DESC                            │
│  LIMIT 10                                                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: EXECUTE & EXPLAIN                                  │
│  Run against Fabric, format response:                       │
│                                                             │
│  "Here are the outages with highest customer impact:        │
│   1. OUT-1042 (Northeast) - 15,234 customers                │
│   2. OUT-1089 (West) - 12,891 customers                     │
│   3. OUT-1056 (South) - 8,445 customers"                    │
└─────────────────────────────────────────────────────────────┘
```

## 為什麼本體很重要

### 沒有本體：脆弱的關鍵字比對

```
User: "Show me our best customers"
System: ??? (what makes a customer "best"?)
```

### 有本體：業務理解

```yaml
# Ontology defines:
rules:
  - name: "Premium Customer"
    definition: "totalSpend > 10000 AND orderCount > 5"
  - name: "Best Customer"
    definition: "Premium Customer with healthScore > 80"
```

```
User: "Show me our best customers"
Agent: Uses "Best Customer" rule → Correct SQL → Meaningful results
```

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

## 客戶對話要點

| 問題 | 回應 |
|------|------|
| 「為什麼不直接讓使用者寫 SQL？」 | 「大多數使用者不會寫 SQL。即使會寫的人也未必了解結構描述。自然語言讓任何人都能查詢資料。」 |
| 「如何處理模糊的術語？」 | 「本體定義了業務術語。『重大故障』、『高影響』、『逾期工單』都有您的業務所控制的精確定義。」 |
| 「效能如何？」 | 「查詢在 Microsoft Fabric 的最佳化引擎上執行。NL→SQL 轉換只發生一次，之後就是標準的 SQL 執行。」 |

## 技術細節

### Microsoft Fabric 架構

```
┌─────────────────────────────────────────────────────────────┐
│                    Microsoft Fabric                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Lakehouse   │ →  │  Warehouse   │ →  │  Semantic    │  │
│  │  (Raw Data)  │    │  (SQL Tables)│    │  Model       │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                ↓            │
│                                          ┌──────────┐       │
│                                          │ Fabric IQ│       │
│                                          │ Ontology │       │
│                                          └──────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### 本體設定

```json
{
  "entities": [
    {
      "name": "NetworkOutages",
      "table": "network_outages",
      "key": "outageId",
      "attributes": ["region", "outageType", "customersAffected", "duration"]
    }
  ],
  "relationships": [
    {
      "name": "related_to_outage",
      "from": "TroubleTickets",
      "to": "NetworkOutages",
      "type": "many-to-one"
    }
  ],
  "businessRules": [
    {
      "name": "CriticalOutage",
      "entity": "NetworkOutages",
      "condition": "customersAffected > 1000"
    }
  ]
}
```

---

[← Foundry IQ：文件](01-foundry-iq.md) | [清理 →](../04-cleanup/index.md)
