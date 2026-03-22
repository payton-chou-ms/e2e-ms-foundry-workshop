# 腳本用途與執行順序

這一頁現在改成入口頁，方便把 script 說明拆成幾個較短的章節。

## 先看哪一頁

| 你的目標 | 建議先看哪一頁 |
|----------|----------------|
| 只想快速跑通 workshop | [快速建置與測試](05a-script-core-paths.md) |
| 想理解主流程的核心腳本 | [主流程腳本 01-08](05b-script-core-pipeline.md) |
| 想在 Foundry portal 內做 guided demo | [Microsoft Foundry 手動 Demo](04a-manual-experiments.md) |
| 想手動驗證 Fabric 資料物件 | [Microsoft Fabric 手動驗證](04b-fabric-manual-validation.md) |
| 想看選配 demo | [選配 demo 09-13](05c-script-optional-demos.md) |
| 要測 Browser Automation | [Browser Automation 補充設定](05d-browser-automation-setup.md) |
| 想看 multi-agent 與新版 Agent Framework 範例 | [Multi-agent 與進階範例](05e-script-advanced.md) |

## 最常用的兩條路

### Path 1: Foundry IQ only

```bash
python scripts/00_build_solution.py --foundry-only
python scripts/08_test_foundry_agent.py --foundry-only
```

如果你想把這條文件-only path 改成 Foundry-native agent 版本，請改跑：

```bash
python scripts/00_build_solution.py --foundry-iq
python scripts/08b_test_foundry_iq_agent.py
```

### Path 2: Foundry IQ + Fabric IQ

```bash
python scripts/00_build_solution.py --from 02
python scripts/08_test_foundry_agent.py
```

## 你可以怎麼使用這一組頁面

- 先從 [快速建置與測試](05a-script-core-paths.md) 確認你要走哪一條 path
- 如果你要理解主流程，再看 [主流程腳本 01-08](05b-script-core-pipeline.md)
- 如果你只是在補 demo，再直接看 [選配 demo 09-13](05c-script-optional-demos.md)
- 如果你要測 `10_demo_browser_automation.py`，只看 [Browser Automation 補充設定](05d-browser-automation-setup.md) 即可

---

[← Microsoft Fabric 手動驗證](04b-fabric-manual-validation.md) | [快速建置與測試 →](05a-script-core-paths.md)

---

[← 建置方案](04-run-scenario.md) | [為你的使用案例自訂 →](../02-customize/index.md)