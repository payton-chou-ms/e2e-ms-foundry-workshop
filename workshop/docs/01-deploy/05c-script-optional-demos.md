# 選配 demo 09-13

這些都不是主流程必要步驟。只有在你要示範額外能力時才需要。

如果某支 script 印出 `SKIP:`，通常代表這個選配能力在目前環境還沒配置好。這不影響主 workshop 路徑，可以先略過。

### `09_demo_content_understanding.py`

示範什麼：把本機 PDF 丟給 Azure Content Understanding，看看它怎麼轉成可讀的文件內容。

```bash
python scripts/09_demo_content_understanding.py
```

### `09_publish_foundry_agent.py`

示範什麼：先檢查 Foundry agent 能不能進入 publish 流程，並列出後面的手動步驟。

```bash
python scripts/09_publish_foundry_agent.py
python scripts/09_publish_foundry_agent.py --teams
```

### `10_demo_browser_automation.py`

示範什麼：讓 Foundry agent 開一個受信任的 Microsoft Learn 頁面，讀取頁面內容後回報結果。

```bash
python scripts/10_demo_browser_automation.py
```

如果你要真的測這支 script，先看 [Browser Automation 補充設定](05d-browser-automation-setup.md)。

### `11_demo_web_search.py`

示範什麼：讓 Foundry agent 用 Web Search tool 查公開網站資訊，並附上引用來源。

```bash
python scripts/11_demo_web_search.py
```

### `12_demo_pii_redaction.py`

示範什麼：把一小段含個資的文字送進 Azure Language，看看它怎麼偵測並遮罩 PII。

```bash
python scripts/12_demo_pii_redaction.py
```

### `13_demo_image_generation.py`

示範什麼：呼叫 image generation API，產生一張示範圖片並存到本機。

```bash
python scripts/13_demo_image_generation.py
```

---

[← 主流程腳本 01-08](05b-script-core-pipeline.md) | [Browser Automation 補充設定 →](05d-browser-automation-setup.md)