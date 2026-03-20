# Workshop 流程

## Step 1：部署方案

請先從以下兩條路徑中擇一開始：

| Route | Use this when | Primary page |
|-------|---------------|--------------|
| **Admin deploy and share** | 你想自己把整套 Azure 與 Fabric 環境準備完成 | [管理員部署並分享](../01-deploy/00-admin-deploy-share.md) |
| **Participant run and validate** | 你已拿到現成環境，只需要執行範例情境與驗證代理程式 | [參與者執行並驗證](../01-deploy/00-participant-run-validate.md) |

這兩條路徑最終都會收斂到相同的範例情境與驗證步驟。

完整部署路徑包含：

- 部署 **Microsoft Foundry control plane** 與支援 Azure 資源，包括 AI Services / project、模型部署、AI Search、Storage、Application Insights，以及選配的 image OpenAI 與 Playwright Workspace
- 設定 **Microsoft Fabric** 連線
- 設定開發環境
- 讓代理程式對範例資料實際運作
- 約需 15 分鐘

## Step 2：依使用案例自訂

為**每個使用案例**產生客製資料：

| Customer Industry | Use Case Example | Sample Questions |
|-------------------|------------------|------------------|
| Telecommunications | Network outages + service policies | "Which outages exceeded our SLA threshold?" |
| Manufacturing | Equipment data + maintenance docs | "Which machines are overdue for maintenance per our schedule?" |
| Retail | Product catalog + return policies | "What's our return policy for electronics over $500?" |
| Finance | Account data + lending policies | "Which loan applications meet our approval criteria?" |
| Insurance | Claims data + policy documents | "What's the status of claims filed this week vs our SLA?" |
| Energy | Grid monitoring + safety protocols | "Which substations are operating above 80% capacity?" |
| **Customer X** | **客戶自己的資料 + 客戶自己的文件** | **客戶最在意的問題** |

!!! tip "PoC 前準備"
    在 PoC 前先執行 Step 2。輸入產業與簡短的使用案例描述後，AI 會依照你的情境產生更貼近實際的範例資料、文件與測試問題。

!!! note "單一文件來源"
    請以 `workshop/docs/` 底下的頁面作為目前有效的操作說明。
    `guides/` 與 PDF 輸出屬於發佈產生物，內容可能較精簡。

## Step 3：Deep dive

請用這一段來補齊你對技術細節的理解：

- **Fabric IQ**：本體如何把商業問題轉換成 SQL
- **Foundry IQ**：agentic retrieval 如何 plan、iterate 與 reflect
- **Orchestrator Agent**：代理程式如何決定要查詢哪個來源

---

[← 快速開始](index.md) | [部署方案 →](../01-deploy/index.md)
