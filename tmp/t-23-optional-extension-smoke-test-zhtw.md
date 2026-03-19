# T-23 選配能力 smoke test 紀錄

## 驗證範圍

- trace helper
- publish helper
- Content Understanding
- Browser Automation
- Web Search
- PII redaction
- Image Generation

## 靜態驗證

執行：

```bash
python3 -m py_compile \
  /workspaces/nc-iq-workshop/scripts/foundry_trace.py \
  /workspaces/nc-iq-workshop/scripts/optional_demo_utils.py \
  /workspaces/nc-iq-workshop/scripts/09_publish_foundry_agent.py \
  /workspaces/nc-iq-workshop/scripts/09_demo_content_understanding.py \
  /workspaces/nc-iq-workshop/scripts/10_demo_browser_automation.py \
  /workspaces/nc-iq-workshop/scripts/11_demo_web_search.py \
  /workspaces/nc-iq-workshop/scripts/12_demo_pii_redaction.py \
  /workspaces/nc-iq-workshop/scripts/13_demo_image_generation.py
```

結果：

- 全數可通過語法編譯

## 執行分類結果

| 功能 | 腳本 | 分類 | 實際結果 |
|------|------|------|----------|
| Publish precheck | `09_publish_foundry_agent.py` | 正確 skip | 缺 `AZURE_AI_PROJECT_ENDPOINT` 時輸出 `[SKIP] Publish flow left for manual UI steps` |
| Content Understanding | `09_demo_content_understanding.py` | 正確 skip | 缺 `azure-ai-contentunderstanding` 套件時輸出 `SKIP:` |
| Browser Automation | `10_demo_browser_automation.py` | 正確 skip | 目前安裝的 `azure-ai-projects` 不含 preview types，輸出 `SKIP:` |
| Web Search | `11_demo_web_search.py` | 正確 skip | 目前安裝的 `azure-ai-projects` 不含 Web Search types，輸出 `SKIP:` |
| PII redaction | `12_demo_pii_redaction.py` | 正確 skip | 缺 `azure-ai-textanalytics` 套件時輸出 `SKIP:` |
| Image Generation | `13_demo_image_generation.py` | 正確 skip | 缺 Azure OpenAI endpoint/key 時輸出 `SKIP:` |

## Trace helper 補充

- `scripts/foundry_trace.py` 已通過 `py_compile`
- tracing 能力已由 T-22 主流程 smoke test 間接驗證為 best-effort，不會在目前缺環境設定時成為主流程 blocker

## 結論

- 每個選配功能都能被歸類為：
  - 可執行前先通過靜態驗證
  - 或在缺條件時明確 `SKIP:`
- 目前環境沒有任何一支選配腳本因未處理的例外而直接崩潰