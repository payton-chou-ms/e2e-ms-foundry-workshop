# T-05 Agent Trace 支援

## 目的

為 `scripts/07_create_foundry_agent.py` 與 `scripts/08_test_foundry_agent.py` 補上可選的 tracing 支援，但不能讓 observability 設定反過來阻塞 workshop 主流程。

## 實作內容

- 新增 `scripts/foundry_trace.py`
- 使用 `azure-ai-projects` + OpenTelemetry + Azure Monitor 的 best-effort 啟用流程
- 透過環境變數控制是否啟用 tracing
- 若無 Application Insights connection string、preview instrumentation 失敗、或套件未安裝，僅輸出 warning
- 在 create agent、get agent、create conversation、responses.create、tool execution 周圍補 span

## 環境變數

- `ENABLE_FOUNDRY_TRACING=true`
- `ENABLE_FOUNDRY_CONTENT_TRACING=true`
- `ENABLE_TRACE_CONTEXT_PROPAGATION=true`
- `APPLICATIONINSIGHTS_CONNECTION_STRING=...`
- `OTEL_SERVICE_NAME=...`

## 驗證

- `get_errors`：相關 Python 檔案無錯誤
- `python3 -m py_compile`：可通過

## 結論

- tracing 現在是顯式 opt-in
- 無法啟用時不影響 `07` / `08` 主流程
- 已可支撐後續 `Foundry Agent` 文件頁面對 trace 的說明