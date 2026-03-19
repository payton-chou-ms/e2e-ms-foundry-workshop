# T-15 Foundry Tool 頁面完成紀錄

## 產出

- `workshop/docs/03-understand/03-foundry-tool.md`

## 完成內容

- 對齊 `scripts/foundry_tool_contract.py` 的 canonical tool contract
- 說明 `execute_sql` / `search_documents` 的責任邊界與 strict schema
- 說明 `scripts/08_test_foundry_agent.py` 的 tool execution loop
- 明確描述 optional demos 為 layered extensions，而非直接併入主流程 tool loop
- 補上 function-call execution Mermaid 圖

## 驗證

- Markdown diagnostics clean
- 已加入 `workshop/mkdocs.yml` 導覽
- `python3 -m mkdocs build --config-file /workspaces/nc-iq-workshop/workshop/mkdocs.yml` 可通過