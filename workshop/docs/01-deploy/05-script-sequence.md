# 腳本用途、快速路徑與執行順序

這一頁同時負責兩件事：

1. 先給你最常用的快速建置與測試命令
2. 再把其餘 script 說明頁導向到正確位置

如果你現在只想知道該跑哪兩個命令，先看下面的快速路徑即可。

## 最常用的兩條路

### Path 1: Foundry IQ only

適合先做文件問答，不接資料附錄。

這條 path 有兩種變體：

- **本機 workshop runtime**：

```bash
python scripts/admin_prepare_docs_demo.py
python scripts/participant_validate_docs.py
```

- **Foundry-native IQ Agent**：

```bash
python scripts/admin_prepare_foundry_iq_demo.py
python scripts/participant_validate_foundry_iq.py
```

### 資料路徑留到附錄

如果你之後要把主線擴充成文件 + 資料整合問答，再回到 [附錄延伸](../05-appendix/index.md)。

## 先看哪一頁

| 你的目標 | 建議先看哪一頁 |
|----------|----------------|
| 想理解維護者用的底層腳本對照 | [進階：維護者腳本對照](05b-script-core-pipeline.md) |
| 想在 Foundry portal 內做 guided demo | [Microsoft Foundry Live Tour](04a-manual-experiments.md) |
| 想手動驗證資料物件 | [附錄中的資料手動驗證](../05-appendix/03-manual-validation.md) |
| 想看選配 demo | [選配 demo 09-13](05c-script-optional-demos.md) |
| 要測 Browser Automation | [Browser Automation 補充設定](05d-browser-automation-setup.md) |
| 想看 multi-agent 與新版 Agent Framework 範例 | [Multi-agent 與進階範例](05e-script-advanced.md) |

## 你可以怎麼使用這一組頁面

- 如果你要理解底層 internal / pipeline 分工，再看 [進階：維護者腳本對照](05b-script-core-pipeline.md)
- 如果你只是在補 demo，再直接看 [選配 demo 09-13](05c-script-optional-demos.md)
- 如果你要測 `10_demo_browser_automation.py`，只看 [Browser Automation 補充設定](05d-browser-automation-setup.md) 即可

補充：`05b` 裡列出的主線維護者入口以 `01`、`04`、`06`、`06a`、`06b`、`07`、`07b` 為主；資料附錄專用腳本另收在附錄頁。

如果你現在只是要先完成 Foundry 線，Path 1 就夠了；資料整合路徑與手動驗證都留到附錄再做。

---

[← 建置與驗證解決方案](04-run-scenario.md) | [為你的使用案例自訂 →](../02-customize/index.md)