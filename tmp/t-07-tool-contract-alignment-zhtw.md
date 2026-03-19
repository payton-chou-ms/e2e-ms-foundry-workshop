# T-07 主流程 Tool 文件對齊

## 目的

降低 `search_documents` / `execute_sql` 在腳本、文件與示例間的 drift。

## 實作內容

- 延伸 `scripts/foundry_tool_contract.py`
- 新增 `TOOL_CONTRACT_ROWS`
- 新增 `get_response_loop_lines()`
- 新增 `get_tool_contract_rows()`
- 保留原有 `build_*_tool()` 與 instruction builder，讓 create/test 腳本仍從同一個模組取用定義

## 目前效果

- tool schema、責任邊界、response loop 已集中在單一模組
- `workshop/docs/02-customize/03-demo.md` 既有內容已與目前 contract 對齊
- 後續 `Foundry Tool` 頁可以直接引用同一份結構化資料

## 驗證

- `get_errors`：無錯誤
- `python3 -m py_compile`：可通過

## 結論

T-07 目前已達到「主流程 tool 文件對齊」的最低可維護狀態，後續只需在 T-15 文件頁再做敘事化整理。