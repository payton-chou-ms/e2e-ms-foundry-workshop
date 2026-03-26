# 腳本用途、快速路徑與執行順序

這一頁同時負責兩件事：

1. 先給你最常用的快速建置與測試命令
2. 再把其餘 script 說明頁導向到正確位置

如果你現在只想知道該跑哪兩個命令，先看下面的快速路徑即可。

## 最常用的兩條路

### Path 1: Foundry IQ only

適合先做文件問答，不接 Fabric。

這條 path 有兩種變體：

- **本機 workshop runtime**：

```bash
python scripts/00_admin_prepare_demo.py --mode foundry-only
python scripts/08_test_foundry_agent.py --foundry-only
```

- **Foundry-native IQ Agent**：

```bash
python scripts/00_admin_prepare_demo.py --mode foundry-iq
python scripts/08b_test_foundry_iq_agent.py
```

### Path 2: Foundry IQ + Fabric IQ

適合同時做文件問答和資料問答。

```bash
python scripts/00_admin_prepare_demo.py --mode full --from-step 02
python scripts/08_test_foundry_agent.py
```

## 先看哪一頁

| 你的目標 | 建議先看哪一頁 |
|----------|----------------|
| 想理解主流程的核心腳本 | [主流程腳本 01-08](05b-script-core-pipeline.md) |
| 想在 Foundry portal 內做 guided demo | [Microsoft Foundry 手動 Demo](04a-manual-experiments.md) |
| 想手動驗證 Fabric 資料物件 | [Microsoft Fabric 手動驗證](04b-fabric-manual-validation.md) |
| 想看選配 demo | [選配 demo 09-13](05c-script-optional-demos.md) |
| 要測 Browser Automation | [Browser Automation 補充設定](05d-browser-automation-setup.md) |
| 想看 multi-agent 與新版 Agent Framework 範例 | [Multi-agent 與進階範例](05e-script-advanced.md) |

## 你可以怎麼使用這一組頁面

- 如果你要理解主流程，再看 [主流程腳本 01-08](05b-script-core-pipeline.md)
- 如果你只是在補 demo，再直接看 [選配 demo 09-13](05c-script-optional-demos.md)
- 如果你要測 `10_demo_browser_automation.py`，只看 [Browser Automation 補充設定](05d-browser-automation-setup.md) 即可

---

[← 建置與驗證解決方案](04-run-scenario.md) | [為你的使用案例自訂 →](../02-customize/index.md)