# 參與者執行與驗證

當 Azure 和 Fabric 環境已經為你準備好時，請走這條路徑。

## 這條路徑適合誰

- 已拿到現成環境的學員
- 只需要登入、設定本機環境、跑驗證的學員
- 想先確認 agent 可用，再回頭看部署細節的學員

如果你還不確定自己需不需要 Azure 部署權限，先看 [部署總覽中的 Azure 權限對照](index.md#azure-permissions)。

## 開始前 checklist

先確認你已經從管理員或講師拿到下面資訊。

- [ ] 指定要使用的 Azure 帳號或租用戶
- [ ] 已準備好的 Azure 資源存取權
- [ ] 已準備好的 Fabric 工作區存取權
- [ ] 正確的 `FABRIC_WORKSPACE_ID`
- [ ] 要使用的 `SCENARIO_KEY`，若沒有特別指定就用 `default`
- [ ] 如果是自訂或臨時資料集，再另外確認 `DATA_FOLDER`
- [ ] 這套環境目前是「已完成範例建置」還是「只完成部署，尚未建置資料與 agent」
- [ ] 你這次要驗證的是哪一條 path：`Foundry IQ only` 或 `Foundry IQ + Fabric IQ`

如果上面有任何一項拿不到，先不要往下做。

## 環境快速檢查

### 1. 確認登入身分正確

- [ ] 你已登入正確的 Azure 帳號
- [ ] 你看到的是預期的租用戶與訂用帳戶

可先執行：

```bash
az account show --query "{tenantId:tenantId, subscription:name, user:user.name}" -o table
```

如果你還沒登入，可先執行：

```bash
az login
```

官方文件：

- Azure CLI 互動式登入：<https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively?view=azure-cli-latest>
- Azure CLI `az account` 指令：<https://learn.microsoft.com/cli/azure/account?view=azure-cli-latest>

### 2. 確認 Fabric 工作區可開啟

- [ ] 你可以在瀏覽器開啟目標 Fabric 工作區
- [ ] 工作區 URL 中的 workspace ID 與你拿到的 `FABRIC_WORKSPACE_ID` 一致

如果你沒有 Fabric 工作區，或不確定自己的租用戶是否可使用 Fabric，先看官方說明：

- Microsoft Fabric 入口網站：<https://app.fabric.microsoft.com/>
- Microsoft Fabric 試用與工作區說明：<https://learn.microsoft.com/fabric/get-started/fabric-trial>

### 3. 確認本機設定完成

請依照 [設定開發環境](03-configure.md) 操作，至少完成下面幾項。

- [ ] 已建立並啟用 Python 環境
- [ ] 已安裝相依套件
- [ ] 已從 `.env.example` 建立 `.env`
- [ ] `.env` 內已填入正確的 `FABRIC_WORKSPACE_ID`
- [ ] `.env` 內已填入正確的 `SCENARIO_KEY`

最小 `.env` 範例：

```env
FABRIC_WORKSPACE_ID=<admin-shared-workspace-id>
SCENARIO_KEY=default
DATA_FOLDER=data/default
```

你也可以先快速確認 `.env` 是否存在，且至少包含這兩個值：

```bash
grep -E '^(FABRIC_WORKSPACE_ID|SCENARIO_KEY|DATA_FOLDER)=' .env
```

### 4. 確認本機 Python 與 SDK 可用

- [ ] Python 環境可正常匯入必要套件
- [ ] 你知道自己目前用的是哪個 Python

可先執行：

```bash
python --version
which python
python -c "import azure.ai.projects; print('Ready!')"
```

如果你還沒建立虛擬環境，可參考官方文件：

- Python `venv` 官方文件：<https://docs.python.org/3/library/venv.html>

### 5. 確認 Azure 與 workshop 設定已成功載入

- [ ] Azure 相關變數已從 `.azure/<env>/.env` 或其他方式載入
- [ ] workshop 的 `.env` 已成功載入

如果你不確定目前 shell 內是不是有值，可先執行：

```bash
python -c "from scripts.load_env import load_all_env; load_all_env(); import os; print('AZURE_AI_PROJECT_ENDPOINT=', 'set' if os.getenv('AZURE_AI_PROJECT_ENDPOINT') else 'missing'); print('AZURE_AI_SEARCH_ENDPOINT=', 'set' if os.getenv('AZURE_AI_SEARCH_ENDPOINT') else 'missing'); print('FABRIC_WORKSPACE_ID=', 'set' if os.getenv('FABRIC_WORKSPACE_ID') else 'missing'); print('SCENARIO_KEY=', os.getenv('SCENARIO_KEY', 'missing')); print('DATA_FOLDER=', os.getenv('DATA_FOLDER', 'missing'))"
```

## 選擇你的 path

請先用最簡單的方式判斷。

### Path 1: Foundry IQ only

適合你只想先確認文件搜尋與回答流程。

你通常應該已經具備：

- [ ] 正確的 Azure 登入身分
- [ ] `AZURE_AI_PROJECT_ENDPOINT` 已可用
- [ ] `AZURE_AI_SEARCH_ENDPOINT` 已可用
- [ ] `SCENARIO_KEY` 已設定

這條路徑不要求你先驗證 Fabric 資料查詢。

### Path 2: Foundry IQ + Fabric IQ

適合你要同時確認文件問答和資料問答。

你通常應該已經具備：

- [ ] Path 1 的所有條件都已成立
- [ ] `FABRIC_WORKSPACE_ID` 正確
- [ ] 你能開啟對應的 Fabric 工作區
- [ ] 共享環境裡已存在可供查詢的 Fabric 項目與資料

## 最小驗證流程

先判斷你接手的是哪一種環境。

| 目前狀態 | 你要做的事 |
|------|----------|
| **已完成預設建置** | 直接執行測試腳本 |
| **只完成部署，尚未建置** | 先執行建置，再執行測試 |

### Path 1 checklist: Foundry IQ only

如果這次只要確認文件搜尋與回答流程正常，請照下面順序做。

- [ ] 確認 `AZURE_AI_PROJECT_ENDPOINT` 已載入
- [ ] 確認 `AZURE_AI_SEARCH_ENDPOINT` 已載入
- [ ] 確認 `DATA_FOLDER` 指向正確資料夾
- [ ] 如果環境尚未建置，執行 search-only 建置
- [ ] 執行 search-only 測試

建置：

```bash
python scripts/00_build_solution.py --foundry-only
```

測試：

```bash
python scripts/08_test_foundry_agent.py --foundry-only
```

你可以用下面問題做最小驗證：

- [ ] 詢問一個文件內容問題，確認 agent 能從文件回答

### Path 2 checklist: Foundry IQ + Fabric IQ

如果這次要確認文件與 Fabric 資料都可用，請照下面順序做。

- [ ] 確認共享環境已有 Fabric 工作區與資料
- [ ] 確認 `FABRIC_WORKSPACE_ID` 已載入
- [ ] 確認你能開啟對應的 Fabric workspace
- [ ] 如果環境尚未建置，執行完整路徑建置
- [ ] 執行完整測試

如果你想先檢查工作區裡是否已有 workshop 建立的 Fabric 項目，可執行：

```bash
python scripts/check_fabric_items.py
```

這支腳本會用你目前的 Azure CLI 登入身分，列出對應 workspace 中符合 prefix 的 lakehouse 與 ontology。

建置：

```bash
python scripts/00_build_solution.py --from 02
```

測試：

```bash
python scripts/08_test_foundry_agent.py
```

你可以用下面問題做最小驗證：

- [ ] 詢問一個文件內容問題
- [ ] 詢問一個資料問題
- [ ] 詢問一個需要同時結合文件與資料的問題

完整流程可參考 [建置解決方案](04-run-scenario.md)。

## 驗證完成的判斷標準

至少確認下面幾項。

- [ ] 測試腳本可以正常啟動
- [ ] Path 1 時，agent 能回答至少一個文件問題
- [ ] Path 2 時，agent 能回答至少一個資料問題
- [ ] Path 2 時，agent 能回答至少一個同時結合文件與資料的問題

如果測試一開始就失敗，先回頭檢查：

- `AZURE_AI_PROJECT_ENDPOINT` 是否已由 `.azure/<env>/.env` 或其他方式載入
- `AZURE_AI_SEARCH_ENDPOINT` 是否已正確載入
- `FABRIC_WORKSPACE_ID` 是否正確
- `DATA_FOLDER` 是否指向正確資料夾
- 你目前登入的 Azure 身分是否就是管理員指定的身分

如果你是 Path 2，另外再檢查：

- 你是否真的能開啟指定的 Fabric workspace
- workspace 中是否已有管理員準備好的 lakehouse / ontology / data agent

## 這條路徑不涵蓋的內容

- 從零開始佈建 Azure 資源
- 從零開始建立 Fabric 工作區
- 授予其他使用者 Azure RBAC
- 將環境分享給額外的參與者

這些工作請改走 [管理員部署](00-admin-deploy-share.md)

## 驗證後的下一步

範例情境正常運作後，請繼續至 [為你的使用案例自訂](../02-customize/index.md)。

---

[← 建立 Fabric 工作區](02-setup-fabric.md) | [設定開發環境 →](03-configure.md)
