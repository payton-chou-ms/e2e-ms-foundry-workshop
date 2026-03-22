# 建置解決方案

!!! info "兩條路徑都會使用"
       管理員使用本頁來驗證預設部署
       參與者使用本頁來執行或驗證已準備好的環境中的範例情境

## 執行完整流程

如果你想先看「每一支 script 是做什麼、什麼時候該跑、要怎麼跑」，請先看 [腳本用途與執行順序](05-script-sequence.md)。

這個命令的意思是：

- 使用專案內已經附好的預設資料集 `data/default`
- 從 pipeline 的 **步驟 02** 開始往後執行
- 一路做到建立 Foundry agent 為止

也就是說，它**不會重新產生範例資料**，而是直接接手後面的建置流程。

```text
01 產生範例資料        ← 這一步會跳過
02 建立 Fabric 項目    ← 從這裡開始
03 載入資料到 Fabric
04 產生 NL2SQL 提示詞
05 建立 Fabric 資料代理程式
06 上傳文件到 Azure AI Search
07 建立協調代理程式
```

一個命令即可完成上述建置：

```bash
python scripts/00_build_solution.py --from 02
```

### 為什麼是 `--from 02`

`scripts/00_build_solution.py` 的完整預設流程其實是從 `01` 到 `07`。

但在這個 workshop 的預設部署路徑裡，`data/default` 已經存在，所以不需要每次都重跑資料生成。文件這裡用 `--from 02`，是要讓你：

- 跳過耗時較長的資料生成步驟
- 直接把現成的預設資料載入 Fabric
- 建好後續 prompt、Fabric agent、Search 索引與 Foundry agent

### 什麼情況適合用這個命令

適合：

- 你在跑專案內建的預設情境
- `data/default` 已存在，且你不打算重做資料內容
- 你只是要把預設 workshop 環境建好或驗證一次

不適合：

- 你要產生新的產業 / use case 資料
- 你剛修改過 `INDUSTRY`、`USECASE` 或資料生成設定
- 你想從頭完整重跑含資料生成的全流程

如果你要從頭連資料一起重建，請改用：

```bash
python scripts/00_build_solution.py
```

這會從步驟 `01` 開始，先產生新的範例資料，再往後完成整條 pipeline。

如果環境已經完全為你準備好，而且範例建置已成功執行過，你可能只需要本頁稍後的測試步驟。

下面這張表，就是 `--from 02` 這個命令實際會執行的步驟：

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

       這會先自動設定 Content Understanding defaults，接著跳過 Fabric 設定步驟（02-05），只在 Microsoft Foundry 中建立代理程式

       `--foundry-only` 的目前步驟如下：

       | 步驟 | 執行內容 | 時間 |
       |------|----------|------|
       | cu-defaults | 設定 Content Understanding defaults | ~5s |
       | 01 | 產生範例資料 | ~2min |
       | 06 | 上傳文件到 Azure AI Search | ~1min |
       | 07-search | 建立 Search-only Foundry agent | ~10s |

## 選配 demo 先怎麼理解

如果你是第一次接觸這個 workshop，這一段可以先簡單記住：

- `09` 到 `13` 都是**額外示範**，不是主流程必要步驟
- 主流程先跑通就好，不需要第一次就把這些都測完
- 如果某個選配 demo 還沒準備好，腳本通常會顯示 `SKIP:`，不會把主流程卡住

目前最容易理解的方式是：

- `09_demo_content_understanding.py`：額外示範文件理解
- `10_demo_browser_automation.py`：額外示範瀏覽器自動化
- `11_demo_web_search.py`：額外示範網頁搜尋
- `12_demo_pii_redaction.py`：額外示範 PII 遮蔽
- `13_demo_image_generation.py`：額外示範影像生成

其中只有 Browser Automation 需要額外手動補一段 connection 設定。若沒有設定好 `AZURE_PLAYWRIGHT_CONNECTION_ID`，腳本會直接 `SKIP:`，這是正常行為。

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
輸入 `quit` 離開，輸入 `help` 查看示範問題

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

[← 設定開發環境](03-configure.md) | [腳本用途與執行順序 →](05-script-sequence.md)
