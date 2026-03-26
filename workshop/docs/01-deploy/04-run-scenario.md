# 建置與驗證解決方案

!!! info "兩條路徑都會使用"
       管理員使用本頁來驗證預設部署
       本頁一律假設：目前**還沒有預載資料與 Agent**

如果你接手的是**管理員已經預載好的共享環境**，請改看 [參與者執行與驗證](00-participant-run-validate.md)。

## 超速使用（略過說明，只留下最短指令；如果要看差異再往下看）

以下都以 `default` 這個預設 scenario 為前提

#### Path 1A: Foundry IQ only

```bash
python scripts/00_admin_prepare_demo.py --mode foundry-only
python scripts/08_test_foundry_agent.py --foundry-only
```

#### Path 1B: Foundry-native IQ Agent

```bash
python scripts/00_admin_prepare_demo.py --mode foundry-iq
python scripts/08b_test_foundry_iq_agent.py
```

#### Path 2: Foundry IQ + Fabric IQ

```bash
python scripts/00_admin_prepare_demo.py --mode full --from-step 02
python scripts/08_test_foundry_agent.py
```

## 執行完整流程

如果你想看每一支 script 的用途，再看 [腳本用途與執行順序](05-script-sequence.md)。

這一頁先只保留兩條主流程。

!!! tip "如果要換情境"
       請直接到 [產生自訂資料](../02-customize/02-generate.md) 看完整做法。
       本頁只保留預設情境的建置與驗證。

### Path 1: Foundry IQ only

適合先做文件問答，不接 Fabric。

預設 use case 使用 `data/default` 這套資料。

- 文件 source：`data/default/documents`
- sample question：`data/default/config/sample_questions.txt` 裡的 `DOCUMENT QUESTIONS`

這條 path 其實有兩種 prepare 模式，差別只在文件問答能力建立的位置：

- **search-only 版本**：走 search-only prepare 路徑，後面用 `08_test_foundry_agent.py --foundry-only` 驗證
- **Foundry-native 版本**：走 knowledge base + MCP prepare 路徑，後面用 `08b_test_foundry_iq_agent.py` 驗證

#### Path 1A: 本機 workshop runtime

先建置：

```bash
python scripts/00_admin_prepare_demo.py --mode foundry-only
```

再測試：

```bash
python scripts/08_test_foundry_agent.py --foundry-only
```

#### Path 1B: Foundry-native IQ Agent

這條變體仍然使用 `data/default` 的文件資料，但 prepare 不是走 search-only 路徑，而是改走 Foundry knowledge base + MCP tool 這條路。

- 主要差異：會建立 Foundry knowledge base、project connection，以及 Foundry-native IQ agent

先建置：

```bash
python scripts/00_admin_prepare_demo.py --mode foundry-iq
```

再測試：

```bash
python scripts/08b_test_foundry_iq_agent.py
```

### Path 2: Foundry IQ + Fabric IQ

適合同時做文件問答和資料問答。

同樣使用 `data/default` 這套預設資料。

- 文件 source：`data/default/documents`
- 資料表 source：`data/default/tables`
- sample question：`data/default/config/sample_questions.txt`
       - `DOCUMENT QUESTIONS` 可用來測 Foundry IQ
       - `SQL QUESTIONS` 可用來測 Fabric IQ
       - `COMBINED INSIGHT QUESTIONS` 可用來測整合問答

先建置：

```bash
python scripts/00_admin_prepare_demo.py --mode full --from-step 02
```

再測試：

```bash
python scripts/08_test_foundry_agent.py
```

## 選配 demo

`09` 到 `13` 都是選配 demo，不是主流程必要步驟。

如果你之後要測 Browser Automation，再回頭看 [Browser Automation 補充設定](05d-browser-automation-setup.md)。

## 檢查點

!!! success "方案已可執行！"
       你現在至少擁有一個可運作的方案：

       - [x] Path 1：**Foundry IQ** 可回答文件問題
       - [x] Path 1B：如果你選 Foundry-native 變體，也可在 Foundry 內用 knowledge base 回答文件問題
       - [x] Path 2：**Foundry IQ + Fabric IQ** 可同時回答文件與資料問題

    ---

[← 設定開發環境](03-configure.md) | [Microsoft Foundry 手動 Demo →](04a-manual-experiments.md)
