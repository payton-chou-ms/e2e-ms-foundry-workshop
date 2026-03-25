# Fabric 詳細設定

這一頁不是教你再建立一次 workspace，而是把管理員部署時真正要確認的 Fabric 設定集中整理在一起。

如果你只需要一個最短路徑，先看 [建立 Fabric 工作區](../02-setup-fabric.md)。
如果你要把環境整理成可分享、可重複使用的 workshop 環境，這一頁才是你真正要對照的檢查清單。

!!! info "主要適用對象"
	本頁主要供管理員部署與環境維護者使用。
	若你只是參與者，通常只需要確認自己能開啟既有 workspace，並拿到正確的 `FABRIC_WORKSPACE_ID`。

## 先看最小必要條件

| 設定項 | 為什麼需要 | 你要在哪裡確認 |
|--------|------------|----------------|
| Workspace 已綁定 Fabric 容量 | 沒有 Fabric 容量就無法走完整 Fabric IQ 路徑 | Workspace `Settings` → `License info` |
| 你的登入身分可存取該 workspace | 腳本會用目前 Azure CLI 身分呼叫 Fabric API 與 OneLake | Workspace access + `az account show` |
| Workspace 可使用 Ontology | `02_create_fabric_items.py` 會建立 ontology；若功能不可用會直接失敗 | 建立流程是否出現 `FeatureNotAvailable` |
| 已記錄正確的 Workspace ID | `.env`、後續建置與分享都靠這個值定位 workspace | Workspace URL `/groups/<workspace-id>/...` |
| `.env` 已填 `FABRIC_WORKSPACE_ID` | 主流程腳本都會先檢查這個變數 | 專案根目錄 `.env` |
| 已決定要分享給哪些人或群組 | 後續學員是否能看見 lakehouse / ontology 取決於 workspace access | Workspace access |

## Portal 內要先確認的三件事

### 1. License info 顯示的是 Fabric 容量

1. 開啟目標 workspace
2. 進入 `Settings`
3. 查看 `License info`
4. 確認這個 workspace 不是一般 Power BI 共用狀態，而是真的綁在 Fabric 容量上

如果這一步不成立，完整的 `Foundry IQ + Fabric IQ` 路徑就不應該繼續往下做。

### 2. 你的管理身分和執行身分都在 workspace access 裡

這個 repo 的 Fabric 腳本不是用 portal session 執行，而是用 `AzureCliCredential()` 取得目前本機登入者的 token，再呼叫：

- `https://api.fabric.microsoft.com/v1/...`
- `https://onelake.dfs.fabric.microsoft.com/...`

所以真正需要對得上的，不只是瀏覽器裡看得到 workspace，而是：

- 你在本機 `az login` 使用的身分
- 你在 Fabric workspace access 裡授權的身分或群組

如果這兩者不一致，常見結果就是：

- Fabric API `403`
- 看得到 workspace，但腳本抓不到 item
- OneLake 上傳或 table load 失敗

### 3. 先把 Workspace ID 抄好

這個 workshop 不會替你自動猜 workspace。

請直接從 workspace URL 取值：

- `https://app.fabric.microsoft.com/groups/<workspace-id>/...`
- 把 `<workspace-id>` 存成 `FABRIC_WORKSPACE_ID`

## 本機設定要怎麼對起來

專案根目錄 `.env` 最少要有：

```env
FABRIC_WORKSPACE_ID=<your-workspace-id>
DATA_FOLDER=data/default
```

你可以用下面兩個指令先做最小確認：

```bash
az account show --query "{tenantId:tenantId, user:user.name}" -o table
grep -E '^(FABRIC_WORKSPACE_ID|DATA_FOLDER)=' .env
```

這兩個檢查分別在回答兩件事：

- 你現在本機到底是用哪個 Entra 身分在跑腳本
- 這個 repo 會把資料建到哪個 workspace、哪個 data folder

## 這個 workshop 會用到哪些 Fabric 設定

把腳本串起來看，你會更容易知道為什麼前面的設定不能少。

| 腳本 | 會碰到的 Fabric 行為 | 依賴哪些設定 |
|------|----------------------|----------------|
| `02_create_fabric_items.py` | 建立 lakehouse 與 ontology，並把結果寫到 `config/fabric_ids.json` | Workspace ID、Fabric API 權限、Ontology 可用性 |
| `03_load_fabric_data.py` | 把 CSV 上傳到 OneLake，再載入成 Delta tables | Workspace access、OneLake 存取、正確的 lakehouse 資訊 |
| `check_fabric_items.py` | 檢查現有 lakehouse / ontology 是否存在 | Workspace ID、CLI 身分有權讀取 workspace |
| `08_test_foundry_agent.py` | 讀取 lakehouse metadata，讓 agent 可以執行唯讀 SQL | 前面已成功建 item，且目前身分可讀取 |

所以這裡所謂的「Fabric 設定」，實際上至少包含四件事：

1. 目標 workspace 是對的
2. 執行腳本的身分是對的
3. workspace 具備完整 Fabric 能力
4. ontology / lakehouse 建立後能被後續腳本接續使用

## 建議你分享給學員的 Fabric 資訊

如果你要把這套環境交給下一位使用者，建議至少一起交付下面這些值：

- Workspace 名稱與 URL
- `FABRIC_WORKSPACE_ID`
- 預期使用的租用戶或登入帳號
- 目前環境是「已完成建置」還是「只完成部署」
- 是否允許學員重跑 Fabric 建置流程，或只能做驗證

這樣下一位使用者在看 [參與者執行並驗證](../00-participant-run-validate.md) 時，才不需要反覆回頭猜目前環境狀態。

## 常見失敗與你該先查什麼

### `FeatureNotAvailable`

代表這個 workspace 雖然可能已綁 Fabric 容量，但目前還不能用本 workshop 需要的 ontology 功能。

先做這些事：

- 確認你用的是正確 tenant 下的 workspace
- 確認不是拿到只有一般容量設定、但未開通對應功能的 workspace
- 如果當下只需要跑 workshop，先改走 `--foundry-only`

### `FABRIC_WORKSPACE_ID` 未設定或設錯

這會直接讓 `02_create_fabric_items.py`、`03_load_fabric_data.py`、`08_test_foundry_agent.py` 這類腳本在前面就停止。

先做這些事：

- 檢查 `.env`
- 重新對照 workspace URL
- 確認不是把別人的 workspace ID 貼進來

### Fabric API / OneLake `403`

通常不是腳本壞掉，而是執行身分沒有對到 workspace access。

先做這些事：

- `az account show` 確認本機目前登入帳號
- 確認該帳號或其所屬群組已加進 workspace access
- 重新登入 Azure CLI 後再重試

### Workspace 裡找不到 lakehouse 或 ontology

常見原因只有兩種：

- 其實還沒跑建立流程
- 之前已切換 suffix 或 solution prefix，現在看的不是同一組 item

如果你只是想快速盤點目前環境，可執行：

```bash
python scripts/check_fabric_items.py
```

如果 item 已存在，但你還想逐步對照 portal 內容，請直接看 [Microsoft Fabric 手動驗證](../04b-fabric-manual-validation.md)。

## 官方文件

- Fabric workspace roles: <https://learn.microsoft.com/fabric/fundamentals/roles-workspaces>
- Give users access to Fabric workspaces: <https://learn.microsoft.com/fabric/fundamentals/give-access-workspaces>
- Microsoft Fabric trial: <https://learn.microsoft.com/fabric/get-started/fabric-trial>

---

[← 建立 Fabric 工作區](../02-setup-fabric.md) | [Microsoft Fabric 手動驗證 →](../04b-fabric-manual-validation.md)