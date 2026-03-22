# 選配 demo 09-13

這些都不是主流程必要步驟。只有在你要示範額外能力時才需要。

### `09_demo_content_understanding.py`

用途：示範 Content Understanding 對本機 PDF 的分析。

```bash
python scripts/09_demo_content_understanding.py
python scripts/09_demo_content_understanding.py --strict
```

### `09_publish_foundry_agent.py`

用途：做 publish 前檢查，確認 agent、Azure CLI、Bot Service provider 等前置條件。

```bash
python scripts/09_publish_foundry_agent.py
python scripts/09_publish_foundry_agent.py --teams
```

### `10_demo_browser_automation.py`

用途：示範 Browser Automation tool。

```bash
python scripts/10_demo_browser_automation.py
python scripts/10_demo_browser_automation.py --strict
```

如果你要真的測這支 script，先看 [Browser Automation 補充設定](05d-browser-automation-setup.md)。

### `11_demo_web_search.py`

用途：示範 Web Search tool。

```bash
python scripts/11_demo_web_search.py
python scripts/11_demo_web_search.py --strict
```

### `12_demo_pii_redaction.py`

用途：示範 PII detection 和 redaction。

```bash
python scripts/12_demo_pii_redaction.py
python scripts/12_demo_pii_redaction.py --strict
```

### `13_demo_image_generation.py`

用途：示範 image generation。

```bash
python scripts/13_demo_image_generation.py
python scripts/13_demo_image_generation.py --strict
```

---

[← 主流程腳本 01-08](05b-script-core-pipeline.md) | [Browser Automation 補充設定 →](05d-browser-automation-setup.md)