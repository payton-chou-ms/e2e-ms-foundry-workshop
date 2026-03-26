# Microsoft Fabric 手動驗證

這一頁專門用來驗證結構化資料與 Fabric 物件是否已正確建立。

如果你現在要做的是 Foundry portal demo，請先看 [Microsoft Foundry 手動 Demo](04a-manual-experiments.md)。

## 這一頁適合做什麼

- 確認 Lakehouse、Ontology 和表格是否真的建立成功
- 直接在 UI 看資料是否載入
- 用 SQL analytics endpoint 做最簡單的人工驗證
- 對照腳本輸出的 `fabric_ids.json` 和 portal 裡的實際 item

Portal URL:

- Microsoft Fabric: <https://app.fabric.microsoft.com/>

## Step 0. 先知道你要找哪些 Fabric item

這個 repo 的 Fabric 物件命名不是隨機的。

`02_create_fabric_items.py` 會建立：

- `lakehouse_name = <solution_name>-lakehouse-<suffix>`
- `ontology_name = <solution_name>-ontology-<suffix>`

而且它會把結果寫到資料資料夾下的 `config/fabric_ids.json`。

如果你不知道這次要找哪個 lakehouse 或 ontology，先去看：

1. `DATA_FOLDER/config/fabric_ids.json`
2. 其中的 `lakehouse_name`
3. 其中的 `ontology_name`
4. 其中的 `solution_name`

## Step 1. 開啟 Fabric workspace

1. 開啟 <https://app.fabric.microsoft.com/>
2. 使用和 workshop 相同的帳號登入
3. 左側進入 **Workspaces**
4. 如果你知道 workspace 名稱，就直接從清單中打開
5. 如果你只有 `FABRIC_WORKSPACE_ID`，可以用下面這種 URL 形式開啟：

```text
https://app.fabric.microsoft.com/groups/<workspace-id>/...
```

6. 進入 workspace 後，先確認你看得到 item 清單，而不是權限不足的畫面

## Step 2. 找到這次腳本建立的 Lakehouse

1. 在 workspace item 清單中搜尋 `lakehouse`
2. 找名稱像 `<solution_name>-lakehouse-<suffix>` 的項目
3. 點進該 **Lakehouse**
4. 進入後，先檢查左側或主畫面的 **Tables**、**Files** 區塊是否存在

如果完全找不到 lakehouse，通常表示：

1. `02_create_fabric_items.py` 沒成功完成
2. 你開錯 workspace
3. 你現在看的 suffix 不是這次最後一次建立的那組

## Step 3. 確認 CSV 是否真的進到 Lakehouse Files

這一步是在對照 `03_load_fabric_data.py` 的上傳行為。

1. 在 Lakehouse 畫面切到 **Files**
2. 找 CSV 檔，檔名通常會和資料表名稱一致，例如 `customers.csv`、`orders.csv` 或其他情境資料表
3. 如果你看得到檔案，代表檔案至少已上傳到 OneLake 對應路徑

## Step 4. 確認 Tables 底下真的有 Delta tables

這一步是在對照 `03_load_fabric_data.py` 的 table load 行為。

1. 在同一個 Lakehouse 畫面切到 **Tables**
2. 確認 `ontology_config.json` 中列出的每張表都有出現
3. 任選一張表打開預覽
4. 看前幾列資料是否合理

如果你看得到 CSV，但 **Tables** 沒資料，通常代表檔案有上傳成功，但「載入為 Delta table」那一步沒有完成。

## Step 5. 切到 SQL analytics endpoint 做最簡單驗證

這一步最接近 agent 之後執行 SQL 查詢時看到的資料面。

1. 在 lakehouse 畫面右上方或上方功能列，從 **Lakehouse** 下拉切到 **SQL analytics endpoint**
2. 等 schema 和 tables 載入
3. 如果一開始沒看到表，按一次 **Refresh**
4. 在表格清單裡展開 `dbo` 或預設 schema
5. 任選一張表，先用預覽確認有資料
6. 如果畫面支援查詢編輯器，再跑最小查詢，例如：

```sql
SELECT TOP 10 *
FROM <table_name>
```

你只需要確認「查得到資料」，不需要在這一步驗證所有商業邏輯。

## Step 6. 檢查 semantic model

如果你想從報表或 Direct Lake 視角確認資料結構，可以再做這一步。

1. 保持在 **SQL analytics endpoint** 或 lakehouse 頁面
2. 找 **New semantic model** 或相近按鈕
3. 檢查 workspace 中是否已存在預設 semantic model
4. 如需手動建立：

- 選 **New semantic model**
- 輸入名稱
- 勾選要納入的 tables
- 選 **Confirm**

這不是 workshop 主流程必要步驟，但很適合用來跟業務同仁展示「同一組 Lakehouse tables 之後也能接報表層」。

## Step 7. 找到 Ontology 並確認結構

這一步是在對照 `02_create_fabric_items.py` 建 ontology 與 relationships 的行為。

1. 回到 workspace item 清單
2. 搜尋 `ontology`
3. 找名稱像 `<solution_name>_ontology_<suffix>` 的項目
4. 點開後，檢查：

- entity types 是否存在
- properties 是否對應各表欄位
- relationships 是否出現
- data bindings 是否綁到正確的 lakehouse tables

如果 ontology item 存在但內容不完整，優先懷疑：

1. `ontology_config.json` 內容本身缺欄位或 relationships
2. `02_create_fabric_items.py` 在建立 bindings 或 relationships 時中途中斷

## Step 8. 用 Fabric 視角驗證 agent 之後會問的問題

這一步不是要你在 portal 重建 agent，而是用人工方式驗證「agent 應該能從資料裡回答什麼」。

建議手動檢查三類問題：

1. **總量 / 聚合**
2. **排行 / 分群**
3. **關聯 / join 類型**

做法：

1. 先在 ontology 看 relationship 是否存在
2. 再到 SQL analytics endpoint 用簡單 SQL 驗證資料真的能 join 起來
3. 最後再回 agent 測試同一題，看回答是否和你人工驗證結果一致

## Script 路徑和 Portal 操作對照表

| Script / 成果 | 你在 portal 應該去哪裡看 | 你要確認什麼 |
|---------------|--------------------------|----------------|
| `02_create_fabric_items.py` | Fabric workspace | `*_lakehouse_*` 與 `*_ontology_*` 是否出現 |
| `03_load_fabric_data.py` | Fabric Lakehouse `Files` / `Tables` | CSV 已上傳，表格已載入 |
| `04_generate_agent_prompt.py` | 本機檔案，不在 portal | 主要看 `schema_prompt.txt` 是否產生 |

## Portal URL

- Microsoft Fabric: <https://app.fabric.microsoft.com/>

---

[← Microsoft Foundry 手動 Demo](04a-manual-experiments.md) | [腳本用途與執行順序總覽 →](05-script-sequence.md)