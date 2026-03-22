# 建置解決方案

!!! info "兩條路徑都會使用"
       管理員使用本頁來驗證預設部署
       參與者使用本頁來執行或驗證已準備好的環境中的範例情境

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

建置：

```bash
python scripts/00_build_solution.py --foundry-only
```

測試：

```bash
python scripts/08_test_foundry_agent.py --foundry-only
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

建置：

```bash
python scripts/00_build_solution.py --from 02
```

測試：

```bash
python scripts/08_test_foundry_agent.py
```

## 選配 demo

`09` 到 `13` 都是選配 demo，不是主流程必要步驟。

如果你之後要測 Browser Automation，再回頭看 [Browser Automation 補充設定](05d-browser-automation-setup.md)。

## 檢查點

!!! success "方案已部署！"
       你現在至少擁有一個可運作的方案：

       - [x] Path 1：**Foundry IQ** 可回答文件問題
       - [x] Path 2：**Foundry IQ + Fabric IQ** 可同時回答文件與資料問題

    ---

[← 設定開發環境](03-configure.md) | [Microsoft Foundry / Fabric 手動實驗流程 →](04a-manual-experiments.md)
