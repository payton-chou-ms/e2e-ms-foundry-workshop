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
| Workspace 已綁定 Fabric 容量 | 沒有 Fabric 容量就無法走完整 Fabric IQ 路徑 | Workspace settings → `Workspace type` |
| 你的登入身分可存取該 workspace | 腳本會用目前 Azure CLI 身分呼叫 Fabric API 與 OneLake | Workspace access + `az account show` |
| Workspace 可使用 Ontology | `02_create_fabric_items.py` 會建立 ontology；若功能不可用會直接失敗 | 建立流程是否出現 `FeatureNotAvailable` |
| 已記錄正確的 Workspace ID | `.env`、後續建置與分享都靠這個值定位 workspace | Workspace URL `/groups/<workspace-id>/...` |
| `.env` 已填 `FABRIC_WORKSPACE_ID` | 主流程腳本都會先檢查這個變數 | 專案根目錄 `.env` |
| 已決定要分享給哪些人或群組 | 後續學員是否能看見 lakehouse / ontology 取決於 workspace access | Workspace access |

## Portal 內要先確認的三件事

### 1. 在 Workspace type 確認目前是 Fabric workspace

1. 開啟目標 workspace (如果沒有就新建一個)
2. 開啟 workspace settings
3. 找到 `Workspace type`
4. 確認目前顯示的是 Fabric workspace type，而不是 Shared / Power BI 類型
5. 如有 `Edit`，展開後確認這個 workspace 目前綁定到正確的 Fabric capacity

如果這一步不成立，完整的 `Foundry IQ + Fabric IQ` 路徑就不應該繼續往下做。

如果你在 workspace 裡看不到這個選項，通常代表你目前不是 workspace admin，或 UI 權限不足。這時請改用下列其中一條管理員路徑確認：

- Fabric Admin portal → `Workspaces` → 找到目標 workspace → `Reassign workspace`
- Fabric Admin portal → `Capacity settings` → 目標 capacity → `Workspaces assigned to this capacity`

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
| `participant_validate_docs_data.py` | 讀取 lakehouse metadata，讓 agent 可以執行唯讀 SQL | 前面已成功建 item，且目前身分可讀取 |

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

| 錯誤 | 更可能的原因 | 先查什麼 |
|------|--------------|----------|
| `FeatureNotAvailable` | workspace 尚未具備 ontology 相關能力 | tenant、workspace 類型、capacity 是否正確 |
| `InvalidInput` / `DisplayName is Invalid for ArtifactType` | 多半不是名字本身，而是 workspace type / capacity / 功能可用性不對 | `Workspace type`、capacity 綁定、是否真的能建立 Lakehouse |
| `FABRIC_WORKSPACE_ID` 未設定或設錯 | `.env` 與實際 workspace 不一致 | `.env`、workspace URL |
| Fabric API / OneLake `403` | 執行身分沒有對到 workspace access | `az account show`、workspace access |
| 找不到 lakehouse 或 ontology | 還沒建立成功，或看的不是同一組 suffix | `check_fabric_items.py`、目前 solution prefix |

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