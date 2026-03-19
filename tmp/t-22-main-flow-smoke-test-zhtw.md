# T-22 主流程 smoke test 紀錄

## 驗證範圍

- `scripts/00_build_solution.py`
- `scripts/07_create_foundry_agent.py`
- `scripts/08_test_foundry_agent.py`
- foundry-only 路徑

## 執行結果

### 1. `00_build_solution.py`

執行：

```bash
python3 /workspaces/nc-iq-workshop/scripts/00_build_solution.py --only 07-search --dry-run
```

結果：

- 可正確組裝 pipeline
- 會列出 `Create Foundry Agent (Search Only)` 步驟
- `--dry-run` 可正常退出，不進入互動流程

### 2. `07_create_foundry_agent.py`

執行：

```bash
python3 /workspaces/nc-iq-workshop/scripts/07_create_foundry_agent.py --foundry-only
python3 /workspaces/nc-iq-workshop/scripts/07_create_foundry_agent.py
```

結果：

- 在目前環境缺少 `AZURE_AI_PROJECT_ENDPOINT` 時，兩條路徑都回傳相同明確 guardrail：
  - `ERROR: AZURE_AI_PROJECT_ENDPOINT not set`
  - `Run 'azd up' to deploy Azure resources`

### 3. `08_test_foundry_agent.py`

執行：

```bash
printf 'quit\n' | python3 /workspaces/nc-iq-workshop/scripts/08_test_foundry_agent.py --foundry-only
printf 'quit\n' | python3 /workspaces/nc-iq-workshop/scripts/08_test_foundry_agent.py
```

結果：

- foundry-only 路徑可正確在 startup guardrail 停下，訊息與 `07` 對齊
- full mode 原本會先被 `pyodbc` / ODBC runtime 缺失短路，無法到達環境 guardrail
- 已修正 `scripts/08_test_foundry_agent.py`：將 `pyodbc` 改為 optional import，只有實際執行 SQL tool 時才回傳 SQL error
- 修正後 full mode 也會先回到一致的 `AZURE_AI_PROJECT_ENDPOINT` guardrail

## 結論

- 在沒有雲端資源的目前環境下，主流程腳本符合驗收條件：
  - 可執行的部分可執行
  - 不可繼續時會給出正確 guardrail
- 另修補一個本機依賴問題，避免 ODBC 缺件在 full mode 啟動時造成誤導性失敗