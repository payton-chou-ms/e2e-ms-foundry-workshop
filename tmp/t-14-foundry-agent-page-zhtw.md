# T-14 Foundry Agent 頁面完成紀錄

## 產出

- `workshop/docs/03-understand/02-foundry-agent.md`

## 完成內容

- 說明 `PromptAgentDefinition` 的三個核心輸入：`model`、`instructions`、`tools`
- 對齊 `scripts/07_create_foundry_agent.py` 的 instructions 組裝來源與 full / foundry-only mode
- 補上 create / get / test flow Mermaid 圖
- 說明 `scripts/foundry_trace.py` 的 tracing env flags 與 best-effort 原則
- 說明 `scripts/09_publish_foundry_agent.py` 的 guarded publish boundary 與 RBAC 影響

## 驗證

- Markdown diagnostics clean
- 已加入 `workshop/mkdocs.yml` 導覽
- `python3 -m mkdocs build --config-file /workspaces/nc-iq-workshop/workshop/mkdocs.yml` 可通過