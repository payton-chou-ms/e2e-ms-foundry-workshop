# 建置解決方案

!!! info "兩條路徑都會使用"
       管理員使用本頁來驗證預設部署。
       參與者使用本頁來執行或驗證已準備好的環境中的範例情境。

## 執行完整流程

一個命令即可建置方案，包括資料處理與代理程式建立：

```bash
python scripts/00_build_solution.py --from 02
```

如果環境已經完全為你準備好，而且範例建置已成功執行過，你可能只需要本頁稍後的測試步驟。

這使用 `data/default` 資料夾並執行所有設定步驟：

| 步驟 | 執行內容 | 時間 |
|------|----------|------|
| 02 | 設定 Fabric 工作區 | ~30s |
| 03 | 載入資料到 Fabric | ~1min |
| 04 | 產生 NL2SQL 提示詞 | ~5s |
| 05 | 建立 Fabric 資料代理程式 | ~30s |
| 06 | 上傳文件到 Azure AI Search | ~1min |
| 07a | 建立協調代理程式 | ~10s |

!!! tip "沒有 Fabric 授權？"
    如果你沒有 Microsoft Fabric 的存取權，仍然可以只使用 Azure 服務執行 workshop：

    ```bash
    python scripts/00_build_solution.py --foundry-only
    ```

       這會先自動設定 Content Understanding defaults，接著跳過 Fabric 設定步驟（02-05），只在 Microsoft Foundry 中建立代理程式。

       `--foundry-only` 的目前步驟如下：

       | 步驟 | 執行內容 | 時間 |
       |------|----------|------|
       | cu-defaults | 設定 Content Understanding defaults | ~5s |
       | 01 | 產生範例資料 | ~2min |
       | 06 | 上傳文件到 Azure AI Search | ~1min |
       | 07-search | 建立 Search-only Foundry agent | ~10s |

## 選配 demo 驗證狀態

部署完成後，可額外驗證以下獨立 demo：

| 腳本 | 目前狀態 | 備註 |
|------|----------|------|
| `09_demo_content_understanding.py` | 可用 | 依賴已部署的 CU defaults |
| `10_demo_browser_automation.py` | 條件式可用 | `azd up` 會自動建立 Playwright Workspace，但仍需先在 Portal 產生 Playwright access token 並建立 Browser Automation connection |
| `11_demo_web_search.py` | 可用 | 已對齊新版 SDK 類型 |
| `12_demo_pii_redaction.py` | 可用 | 支援 AAD，不需額外 Language key |
| `13_demo_image_generation.py` | 可用 | `azd up` 會自動建立獨立 image resource，腳本預設讀取 `AZURE_IMAGE_OPENAI_ENDPOINT` 與 `AZURE_IMAGE_MODEL_DEPLOYMENT` |

### Browser Automation 手動收尾

`10_demo_browser_automation.py` 的最短手動收尾如下：

1. 在 Portal 的 Playwright Workspace 產生 access token。
2. 在 Foundry project 建立 Browser Automation connection。
3. 將 connection resource ID 填入 `.env` 的 `AZURE_PLAYWRIGHT_CONNECTION_ID`。
4. 執行 `python scripts/10_demo_browser_automation.py --strict`。

如果沒有 `AZURE_PLAYWRIGHT_CONNECTION_ID`，腳本會直接 `SKIP:`，這是預期行為。

## 預期輸出

```
> [02] Create Fabric Items... [OK]
> [03] Load Data into Fabric... [OK]
> [04] Generate Agent Prompt... [OK]
> [05] Create Fabric Data Agent... [OK]
> [06] Upload to AI Search... [OK]
> [07] Create Foundry Agent... [OK]

------------------------------------------------------------
[OK] Pipeline completed successfully!

Next: python scripts/08_test_foundry_agent.py

```

## 測試代理程式

```bash
python scripts/08_test_foundry_agent.py
```

### 範例對話

```
============================================================
Orchestrator Agent Chat
============================================================
Type 'quit' to exit, 'help' for sample questions

------------------------------------------------------------

You: How many outages occurred last month?

Agent: Based on the database, there were 16 network outages recorded
       in January 2024.

You: What are the policies for notifying customers of outages?

Agent: According to our Customer Service Policies document:

       - Customers must be notified within 15 minutes of confirmed outage
       - Use SMS, email, and app notifications for affected customers
       - Provide estimated restoration time when available
       - Send updates every 30 minutes during extended outages

       [Source: customer_service_policies.pdf]

You: Which outages exceeded the maximum duration defined in our policy?

Agent: Let me check the outage data against our policy thresholds...

       Based on a 4-hour (240 minute) maximum duration policy, these
       outages exceeded the threshold:

       | Outage ID | Duration (min) | Impact Level |
       |-----------|----------------|--------------|
       | OUT011    | 472            | Medium       |
       | OUT004    | 446            | Low          |
       | OUT007    | 445            | Low          |
       | OUT005    | 417            | Medium       |
       | OUT003    | 411            | Low          |

       5 outages exceeded the policy maximum duration.

You: quit
```

## 檢查點

!!! success "方案已部署！"
    你現在擁有一個可運作的方案：

    - [x] **Fabric IQ** 回答資料問題
    - [x] **Foundry IQ** 擷取文件知識
    - [x] **協調代理程式** 結合兩個來源

    ---

[← 設定開發環境](03-configure.md) | [為你的使用案例自訂 →](../02-customize/index.md)
