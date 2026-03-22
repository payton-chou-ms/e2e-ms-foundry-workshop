# Microsoft Foundry / Fabric 手動實驗流程

這一頁給「已經跑過腳本，但想回到 portal 直接觀察」的人使用。

你可以把它理解成兩條平行路徑：

- **Foundry 路徑**：看 agent、model、tool、playground、trace
- **Fabric 路徑**：看 workspace、lakehouse、tables、SQL endpoint、ontology

如果你想先在 Foundry portal 中看到一個比較原生的文件問答 agent，可以先跑：

```bash
python scripts/06b_upload_to_foundry_knowledge.py
python scripts/07b_create_foundry_iq_agent.py
python scripts/08b_test_foundry_iq_agent.py
```

這條路會使用 Foundry-native File Search，不會走目前 `07_create_foundry_agent.py` 那條本機 function tool runtime。

如果你只是想確認 script 有沒有成功，不需要每個畫面都點完。先照下面的「最短檢查路徑」做即可。

!!! note "UI 名稱可能有小幅變動"
	 Microsoft Foundry 和 Microsoft Fabric 的 portal 介面更新頻率高。
	 如果你看到的按鈕名稱和本頁有一點差異，通常先找相同層級的頁面即可，例如 `Build`、`Agents`、`Tools`、`Models + endpoints`、`SQL analytics endpoint`。

## 最短檢查路徑

如果你只有 5 到 10 分鐘，建議只做下面幾件事：

1. 到 Microsoft Foundry 開啟這次部署用的 **project**
2. 到 **Build** > **Agents** 找到 workshop agent，確認 instructions 與 tools 存在
3. 在 **Agents playground** 手動問一題文件問題，確認 agent 可回應
4. 到 Microsoft Fabric 開啟你的 workspace
5. 找到 `*_lakehouse_*`，確認 **Tables** 底下真的有資料表
6. 切到 **SQL analytics endpoint**，用預覽或查詢確認表格有資料

## Path 1: 在 Microsoft Foundry 手動做實驗

Portal URL:

- Microsoft Foundry: <https://ai.azure.com/>
- Azure Portal: <https://portal.azure.com/>

### 這條路徑適合做什麼

- 確認 project、models、agents 和 tools 都已建立
- 手動測 prompt，不用重跑 script
- 檢查 Search / Browser Automation 等 connection 是否存在
- 從 playground 直接看 thread logs、tool calls、evaluations

### Step 0. 先知道你要找哪個 project

如果你是自己部署的，通常可以從下面幾個來源找回正確 project：

1. 專案根目錄 `.azure/<env>/.env` 的 `AZURE_AI_PROJECT_NAME`
2. Azure Portal 資源群組中的 Foundry project 名稱
3. `AZURE_AI_PROJECT_ENDPOINT`

如果你是使用別人分享的環境，先向管理員確認你該進哪一個 Foundry project。

### Step 1. 開啟 Foundry project

1. 開啟 <https://ai.azure.com/>
2. 使用和部署環境相同的 Azure 帳號登入
3. 如果首頁先看到資源或 project 清單，選擇這次 workshop 使用的 **project**
4. 進入 project 後，先停 10 秒看左側導覽，確認至少看得到下列群組：
	- **Build**
	- **Agents** 或 **Build > Agents**
	- **Tools**
	- **Models + endpoints**

### Step 2. 確認模型部署是否存在

這一步的目的，是先分清楚「主 Foundry 模型」和「獨立 image OpenAI resource」。

1. 在左側進入 **Models + endpoints**
2. 查看 chat 與 embedding 相關 deployment 是否存在
3. 如有看到 `gpt-4.1-mini`，代表選配文字模型也有建立
4. 不要把這一頁當成 image model 的唯一檢查點

!!! note "`gpt-image-1.5` 的位置和主模型不同"
	 這個 repo 的 image generation 預設走獨立 Azure OpenAI resource，不一定出現在主 Foundry project 的同一份模型清單裡。
	 你如果要驗證 image demo，應優先檢查 `.azure/<env>/.env` 裡的 `AZURE_IMAGE_OPENAI_ENDPOINT` 與 `AZURE_IMAGE_MODEL_DEPLOYMENT`，或回 Azure Portal 看獨立的 image OpenAI resource。

### Step 3. 到 Agents 頁面檢查 workshop agent

1. 在左側進入 **Build** > **Agents**
2. 找這次 workshop 建立的 agent
3. 點進 agent 後，依序檢查：
	- **Name** 是否合理
	- **Instructions** 是否已填入
	- **Model** 是否綁到正確 deployment
	- **Tools** 區塊是否看得到工具設定

如果你是走主流程，這裡最重要的不是外觀，而是 agent 已存在且能打開設定頁。

### Step 4. 用 Agents playground 手動測一題

1. 在 agent 詳細頁面選 **Try in playground**，或直接開 **Agents playground**
2. 在輸入框先測一題文件型問題，例如：

```text
這個 workshop 的主要目標是什麼？
```

3. 再測一題偏結構化的問題，例如：

```text
這個方案除了文件問答，還能結合哪一類企業資料？
```

4. 觀察回答時，重點看三件事：
	- 有沒有正常產出答案
	- 回答是否像是 grounded 在 workshop 文件內容
	- 若有 tool call 顯示，是否能看出 agent 有使用搜尋或其他工具

### Step 5. 回看 instructions 和 tools

如果你想知道 agent 為什麼這樣回答，回到 agent 設定頁，重點檢查這幾塊：

1. **Instructions**
	- 看系統提示是否描述了文件問答、Fabric 查詢、工具使用規則
2. **Tools**
	- 確認是否有 workshop 使用的 tool 或相應連線
3. **Knowledge** 或相似區塊
	- 如果 portal 中有顯示，可順手確認是否已掛上相關知識來源

這一步最適合拿來對照 [05-script-sequence.md](05-script-sequence.md) 裡的腳本用途，而不是單純「看畫面」。

### Step 6. 檢查專案連線與 Browser Automation 狀態

這一步只是在 portal 裡確認「能不能用」，不是要求你現在就把所有 demo 都手動跑完。

1. 在 project 中進入 **Build** > **Tools**
2. 查看是否已有 Azure AI Search、Browser Automation 或其他工具連線
3. 如果你只是跑主流程，看到 Search 相關資源已存在即可
4. 如果你要驗證 Browser Automation：
	- 選 **Connect a tool**
	- 在 **Configured** 或相近頁籤找 **Browser Automation**
	- 確認是否已建立 connection
	- 若未建立，代表目前仍停留在「Playwright Workspace 已建立，但 Foundry connection 尚未補」的狀態

如果你真的要補 Browser Automation，請回頭看 [05d-browser-automation-setup.md](05d-browser-automation-setup.md)。

### Step 7. 從 playground 看 thread logs、runs、tool calls

這一步最適合拿來做「為什麼這題回答成這樣」的觀察。

1. 回到 **Agents playground**
2. 找到剛剛測過的對話 thread
3. 選 **Thread logs**
4. 依序看：
	- thread 基本資訊
	- run 狀態
	- step 順序
	- tool call 與其輸入輸出
	- 最後回覆內容

如果畫面右上角看得到 **Metrics** 或 evaluation 設定：

1. 先確認目前有沒有勾選 evaluator
2. 如有勾選，再送一次測試問題
3. 回頭看該次對話是否出現 AI quality 或 risk and safety 類型的評估結果

!!! note "不是每個環境都一定要開 evaluation"
	 這個 workshop 的主線不是靠 playground evaluation 才能成立。
	 如果你只是要驗證 agent 能不能工作，先看 thread logs 和 tool calls 就夠了。

### Step 8. 用 Azure Portal 交叉確認底層資源

當 Foundry portal 顯示正常，但你仍想確認底層 Azure 資源時，再做這一步。

1. 開啟 <https://portal.azure.com/>
2. 進入這次部署的 resource group
3. 確認至少有：
	- Microsoft Foundry
	- Foundry project
	- Azure AI Search
	- Storage Account
	- Application Insights
	- Playwright Workspace
4. 如果你要追 image demo，再額外找獨立的 image OpenAI resource

## Path 2: 在 Microsoft Fabric 手動做實驗

Portal URL:

- Microsoft Fabric: <https://app.fabric.microsoft.com/>

### 這條路徑適合做什麼

- 確認 Lakehouse、Ontology 和表格是否真的建立成功
- 直接在 UI 看資料是否載入
- 用 SQL analytics endpoint 做最簡單的人工驗證
- 對照腳本輸出的 `fabric_ids.json` 和 portal 裡的實際 item

### Step 0. 先知道你要找哪些 Fabric item

這個 repo 的 Fabric 物件命名不是隨機的。

`02_create_fabric_items.py` 會建立：

- `lakehouse_name = <solution_name>_lakehouse_<suffix>`
- `ontology_name = <solution_name>_ontology_<suffix>`

而且它會把結果寫到資料資料夾下的 `config/fabric_ids.json`。

如果你不知道這次要找哪個 lakehouse 或 ontology，先去看：

1. `DATA_FOLDER/config/fabric_ids.json`
2. 其中的 `lakehouse_name`
3. 其中的 `ontology_name`
4. 其中的 `solution_name`

### Step 1. 開啟 Fabric workspace

1. 開啟 <https://app.fabric.microsoft.com/>
2. 使用和 workshop 相同的帳號登入
3. 左側進入 **Workspaces**
4. 開啟 `.env` 中 `FABRIC_WORKSPACE_ID` 對應的 workspace
5. 進入 workspace 後，先確認你看得到 item 清單，而不是權限不足的畫面

### Step 2. 找到這次腳本建立的 Lakehouse

1. 在 workspace item 清單中搜尋 `lakehouse`
2. 找名稱像 `<solution_name>_lakehouse_<suffix>` 的項目
3. 點進該 **Lakehouse**
4. 進入後，先檢查左側或主畫面的 **Tables**、**Files** 區塊是否存在

如果完全找不到 lakehouse，通常表示：

1. `02_create_fabric_items.py` 沒成功完成
2. 你開錯 workspace
3. 你現在看的 suffix 不是這次最後一次建立的那組

### Step 3. 確認 CSV 是否真的進到 Lakehouse Files

這一步是在對照 `03_load_fabric_data.py` 的上傳行為。

1. 在 Lakehouse 畫面切到 **Files**
2. 找 CSV 檔，檔名通常會和資料表名稱一致，例如 `customers.csv`、`orders.csv` 或其他情境資料表
3. 如果你看得到檔案，代表檔案至少已上傳到 OneLake 對應路徑

### Step 4. 確認 Tables 底下真的有 Delta tables

這一步是在對照 `03_load_fabric_data.py` 的 table load 行為。

1. 在同一個 Lakehouse 畫面切到 **Tables**
2. 確認 `ontology_config.json` 中列出的每張表都有出現
3. 任選一張表打開預覽
4. 看前幾列資料是否合理

如果你看得到 CSV，但 **Tables** 沒資料，通常代表檔案有上傳成功，但「載入為 Delta table」那一步沒有完成。

### Step 5. 切到 SQL analytics endpoint 做最簡單驗證

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

### Step 6. 檢查 semantic model

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

### Step 7. 找到 Ontology 並確認結構

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

### Step 8. 用 Fabric 視角驗證 agent 之後會問的問題

這一步不是要你在 portal 重建 agent，而是用人工方式驗證「agent 應該能從資料裡回答什麼」。

建議手動檢查三類問題：

1. **總量 / 聚合**
	- 例如總客戶數、總訂單數、總營收
2. **排行 / 分群**
	- 例如前 5 大產品、前 5 個區域
3. **關聯 / join 類型**
	- 例如客戶與訂單、門市與交易、設備與事件之間的關聯

做法：

1. 先在 ontology 看 relationship 是否存在
2. 再到 SQL analytics endpoint 用簡單 SQL 驗證資料真的能 join 起來
3. 最後再回 agent 測試同一題，看回答是否和你人工驗證結果一致

## Script 路徑和 Portal 操作對照表

| Script / 成果 | 你在 portal 應該去哪裡看 | 你要確認什麼 |
|---------------|--------------------------|----------------|
| `azd up` | Azure Portal resource group | Foundry、Search、Storage、App Insights、Playwright Workspace 都存在 |
| `07_create_foundry_agent.py` | Foundry `Build > Agents` | workshop agent 已建立，可打開設定頁 |
| `08_test_foundry_agent.py` | Foundry `Agents playground` | 能手動問答，必要時看 thread logs |
| `10_demo_browser_automation.py` | Foundry `Build > Tools` | Browser Automation connection 是否已建立 |
| `13_demo_image_generation.py` | Azure Portal 或 env 輸出 | image OpenAI resource 與 deployment 是否存在 |
| `02_create_fabric_items.py` | Fabric workspace | `*_lakehouse_*` 與 `*_ontology_*` 是否出現 |
| `03_load_fabric_data.py` | Fabric Lakehouse `Files` / `Tables` | CSV 已上傳，表格已載入 |
| `04_generate_agent_prompt.py` | 本機檔案，不在 portal | 主要看 `schema_prompt.txt` 是否產生 |

## 什麼情況下建議你優先看 portal，而不是重跑 script

1. 你只想確認資源是否存在
2. 你懷疑 tool / connection 沒掛上
3. 你想看 agent 實際做了哪些 tool calls
4. 你想驗證 Fabric 裡的資料與 relationships 是否合理

## Portal URL

- Microsoft Foundry: <https://ai.azure.com/>
- Azure Portal: <https://portal.azure.com/>
- Microsoft Fabric: <https://app.fabric.microsoft.com/>

---

[← 建置方案](04-run-scenario.md) | [腳本用途與執行順序總覽 →](05-script-sequence.md)