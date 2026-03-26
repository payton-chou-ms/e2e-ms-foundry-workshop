# 參與者執行與驗證

當 Azure 和 Fabric 環境已經為你準備好時，請走這條路徑。

## 這條路徑適合誰

- 已拿到現成環境的學員
- 只需要登入、設定本機環境、跑驗證的學員
- 想先確認 agent 可用，再回頭看部署細節的學員

如果你還不確定自己需不需要 Azure 部署權限，先看 [部署總覽中的 Azure 權限對照](index.md#azure-permissions)。

## 開始前先確認

| 項目 | 至少要拿到什麼 |
|------|----------------|
| Azure 登入資訊 | 指定帳號或租用戶 |
| Azure 存取權 | 已準備好的既有資源存取 |
| Fabric 存取權 | 已準備好的 workspace 存取 |
| Workspace 設定 | 正確的 `FABRIC_WORKSPACE_ID` |
| Scenario 設定 | `SCENARIO_KEY`，若沒有特別指定就用 `default` |
| 資料夾設定 | 若是自訂資料集，另外確認 `DATA_FOLDER` |
| 環境狀態 | 已完成建置，或只完成部署尚未建置 |

如果上面任一項拿不到，先停在這裡，不要往下跑。

## 最短檢查

開始前只要先確認這四件事：

- 你已登入正確的 Azure 帳號
- 你能開啟對應的 Fabric workspace
- `.env` 內的 `FABRIC_WORKSPACE_ID` 與 `SCENARIO_KEY` 正確
- Python 與必要 SDK 可正常使用

??? note "更多檢查指令"
	```bash
	az account show --query "{tenantId:tenantId, subscription:name, user:user.name}" -o table
	grep -E '^(FABRIC_WORKSPACE_ID|SCENARIO_KEY|DATA_FOLDER)=' .env
	python --version
	python -c "import azure.ai.projects; print('Ready!')"
	python -c "from scripts.load_env import load_all_env; load_all_env(); import os; print('AZURE_AI_PROJECT_ENDPOINT=', 'set' if os.getenv('AZURE_AI_PROJECT_ENDPOINT') else 'missing'); print('AZURE_AI_SEARCH_ENDPOINT=', 'set' if os.getenv('AZURE_AI_SEARCH_ENDPOINT') else 'missing'); print('FABRIC_WORKSPACE_ID=', 'set' if os.getenv('FABRIC_WORKSPACE_ID') else 'missing'); print('SCENARIO_KEY=', os.getenv('SCENARIO_KEY', 'missing')); print('DATA_FOLDER=', os.getenv('DATA_FOLDER', 'missing'))"
	```

## 先判斷你要驗證哪一條路徑

| Path | 什麼時候用 | 最小前提 |
|------|------------|----------|
| `Foundry IQ only` | 只想先確認文件搜尋與回答流程 | `AZURE_AI_PROJECT_ENDPOINT`、`AZURE_AI_SEARCH_ENDPOINT`、正確的 `SCENARIO_KEY` |
| `Foundry IQ + Fabric IQ` | 要同時確認文件問答和資料問答 | Path 1 的所有條件，加上正確的 `FABRIC_WORKSPACE_ID` 與可用的 Fabric workspace |

## 最小驗證流程

### Path 1：Foundry IQ only

如果環境已建好，直接測試：

```bash
python scripts/08_test_foundry_agent.py --foundry-only
```

如果環境還沒建好，先建置再測：

```bash
python scripts/00_admin_prepare_demo.py --mode foundry-only
python scripts/08_test_foundry_agent.py --foundry-only
```

成功時，你至少應該能問出一題文件問題，並看到 agent 從文件內容回答。

### Path 2：Foundry IQ + Fabric IQ

如果環境已建好，直接測試：

```bash
python scripts/08_test_foundry_agent.py
```

如果環境還沒建好，先建置再測：

```bash
python scripts/00_admin_prepare_demo.py --mode full --from-step 02
python scripts/08_test_foundry_agent.py
```

如果你想先檢查 Fabric item 是否存在，可先執行：

```bash
python scripts/check_fabric_items.py
```

成功時，你至少應該能問出：

- 一題文件問題
- 一題資料問題
- 一題同時結合文件與資料的問題

## 失敗時先回頭查哪裡

先檢查：

- `AZURE_AI_PROJECT_ENDPOINT` 是否已載入
- `AZURE_AI_SEARCH_ENDPOINT` 是否已載入
- `FABRIC_WORKSPACE_ID` 是否正確
- `DATA_FOLDER` 是否指向正確資料夾
- 你目前登入的 Azure 身分是否就是管理員指定的身分

如果你走的是 Path 2，再另外檢查：

- 你是否真的能開啟指定的 Fabric workspace
- workspace 中是否已有管理員準備好的 lakehouse / ontology / data agent

## 何時算完成

- [ ] 測試腳本可以正常啟動
- [ ] Path 1 時，agent 能回答至少一個文件問題
- [ ] Path 2 時，agent 能回答至少一個資料問題
- [ ] Path 2 時，agent 能回答至少一個同時結合文件與資料的問題

完整流程可參考 [建置解決方案](04-run-scenario.md)。

## 這條路徑不涵蓋的內容

- 從零開始佈建 Azure 資源
- 從零開始建立 Fabric 工作區
- 授予其他使用者 Azure RBAC
- 將環境分享給額外的參與者

這些工作請改走 [管理員部署](00-admin-deploy-share.md)。

驗證完成後，請繼續到 [為你的使用案例自訂](../02-customize/index.md)。

---

[← 建立 Fabric 工作區](02-setup-fabric.md) | [設定開發環境 →](03-configure.md)
