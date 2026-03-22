# Microsoft Foundry 手動 Demo

這一頁是給「剛完成部署，現在要回到 Microsoft Foundry portal 確認這次到底建立了哪些資源」的人使用。

請先把這一頁當成部署完成後的 summary 頁，而不是完整產品導覽。目標很單純：

1. 先找出這次部署完成後產生的 Foundry project 和相關資產
2. 確認 agent、knowledge、tools、models 都真的存在
3. 再從這些已建立的資產出發，開始認識 Discover / Build / Operate

這裡不再混講 Fabric。Fabric 的資料物件驗證請看 [Microsoft Fabric 手動驗證](04b-fabric-manual-validation.md)。

## 先找出這次剛部署完的資源

在開始前，先確認你打開的是這次部署出來的資源，而不是其他專案或舊環境。

### 先看這幾個地方

如果你是照 [建置方案](04-run-scenario.md) 跑完，先回頭確認：

- `.azure/<env>/.env` 裡的 `AZURE_AI_PROJECT_NAME`
- `.azure/<env>/.env` 裡的 `AZURE_AI_PROJECT_ENDPOINT`
- `data/default/config/sample_questions.txt` 或你自訂 scenario 對應的 `config/sample_questions.txt`

如果你走的是自訂 use case，也請同步確認你現在使用的是哪一組：

- `documents`
- `tables`
- `sample_questions.txt`

### 你在 portal 中應該先找到什麼

進入 Foundry 之後，先不要急著到處點。請先確認下面幾類資產：

1. 這次部署用的 Foundry project
2. 這次建立的 agent
3. 這次掛上的 knowledge 或知識來源
4. 這次使用的 model deployment
5. 這次配置的 tools 或 connections

## 這頁怎麼讀

建議照下面順序操作：

1. 先找到這次部署完的 project 與資產
2. 再用 **Build** 確認主要資產都存在
3. 最後再回頭看 **Discover** 與 **Operate**，理解它們在整個平台中的位置

如果你只是第一次操作，不需要把每個功能都點完。先把「這次部署產生了哪些東西」看清楚即可。

!!! note "UI 名稱可能有小幅變動"
	 Foundry portal 更新很快。
	 如果你的畫面名稱和本頁不同，請先找對應層級，例如 `Discover`、`Build`、`Operate`、`Agents`、`Knowledge`、`Guardrails`。

## 最短檢查路徑

1. 開啟正確的 Foundry project
2. 在 **Build > Agents** 打開 workshop agent 或 Foundry IQ agent
3. 在 **Build > Knowledge** 或相關區塊確認文件知識來源
4. 在 **Build > Tools** 確認已配置的工具或連線
5. 在 **Build > Models** 確認這次使用的部署
6. 在 **Operate** 搜尋這個 solution name 相關資產，打開資產詳細頁

如果你需要驗證 Lakehouse、tables、SQL endpoint 或 ontology，請改去 [Microsoft Fabric 手動驗證](04b-fabric-manual-validation.md)。

## 先知道你要找哪個 project

如果你是自己部署的，通常可以從下面幾個來源找回正確 project：

1. 專案根目錄 `.azure/<env>/.env` 的 `AZURE_AI_PROJECT_NAME`
2. Azure Portal resource group 中的 Foundry project 名稱
3. `AZURE_AI_PROJECT_ENDPOINT`

如果你是使用別人分享的環境，先向管理員確認你該進哪一個 project。

Portal URL:

- Microsoft Foundry: <https://ai.azure.com/>
- Azure Portal: <https://portal.azure.com/>

參考：

- [Microsoft Foundry portal 官方說明](https://learn.microsoft.com/azure/foundry/what-is-foundry#foundry-portal)
- [新版 Foundry portal 功能位置對照](https://learn.microsoft.com/azure/foundry/how-to/navigate-from-classic#navigate-the-portal)

## Discover

先把 Discover 當成入口頁。這一區的重點不是把所有能力都看完，而是先建立基本概念：目前這個平台有哪些模型、工具和模板入口，哪些和你現在的 scenario 有關。

參考：

- [Foundry portal 功能狀態與 Discover / Build / Operate 導覽](https://learn.microsoft.com/azure/foundry/concepts/general-availability#feature-readiness-at-ga)
- [What is Microsoft Foundry](https://learn.microsoft.com/azure/foundry/what-is-foundry)

### Browse the catalog

在 catalog 這裡，你不用把每一個項目都看完。比較好的做法是先知道 Foundry 有哪些大類能力，然後回頭對照這個 workshop 實際用到哪些。

在這個 workshop 中，catalog 比較適合當成導覽起點，但不用停在產品瀏覽層太久。重點是把它對回目前 scenario 的已部署資產，例如：

- 這次 PoC 主要使用的模型類型
- 這次使用的 agent 類型
- 這次有沒有額外用到 image、browser automation 或 evaluation 能力

如果你走的是自訂 use case，也請記得：

- 文件與資料都已經換成該 use case 的內容
- catalog 裡看到的是平台能力，實際操作仍要回到你現在的 scenario 資產

官方文件：

- [What is Microsoft Foundry](https://learn.microsoft.com/azure/foundry/what-is-foundry)

### Models

在 Discover 看 models 時，重點不是把所有模型都點過一輪，而是確認你現在這個 scenario 實際用到哪些部署：

1. chat model
2. embedding model
3. 選配的 image model 或其他專用模型

- Foundry IQ 主要依賴 chat 與 embedding 模型
- 如果是自訂 use case，模型可能不變，但 documents / tables / sample questions 已經換掉

官方文件：

- [Microsoft Foundry Models overview](https://learn.microsoft.com/azure/foundry/concepts/foundry-models-overview)

### Tools

在 Discover 看 tools 時，重點是先知道 Foundry 支援哪些工具型態，然後立刻對回 workshop 已配置的工具或連線。

這個 workshop 最常對應的是：

- 文件相關能力
- Search 相關能力
- 選配的 Browser Automation

如果你現在只是在驗證主流程，就不用把每種 tool 都展開。只要先確認目前這個 use case 實際有掛哪些工具即可。

官方文件：

- [Foundry Agent Service tool catalog](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)

### Solution templates

這裡可以補充一個平台視角：Foundry 不只是單一 agent playground，也有模板化建構路徑。

但在這個 workshop 裡，不建議把 solution templates 當成主線。比較適合的理解方式是：

- solution templates 是平台入口
- 本 workshop 是已經準備好的 end-to-end solution accelerator
- 現在看的，是這個 accelerator 建好的實際資產，而不是從 template 重新建立一次

官方文件：

- [Foundry portal 功能狀態與 Discover 區說明](https://learn.microsoft.com/azure/foundry/concepts/general-availability#feature-readiness-at-ga)

## Build

Build 是這一頁最重要的區域。你在這裡看到的，不是抽象功能，而是這次 workshop 已經建好的 agent、knowledge、tools、模型配置和治理能力。

### Agents

這是 04a 最核心的區塊。

先在 **Build > Agents** 確認兩種可能路徑：

1. 主流程 workshop agent
2. Foundry-native 文件問答 agent

對應腳本：

- `07_create_foundry_agent.py`
- `07b_create_foundry_iq_agent.py`

打開 agent 時，重點檢查：

1. agent 名稱是否對應現在的 solution / scenario
2. instructions 是否不是空的
3. model 是否綁到正確 deployment
4. tools / knowledge 是否已掛上

如果你走的是自訂 use case，這裡最值得確認的是：

- agent 外觀可能相似
- 但 instructions、documents、knowledge 與 sample questions 已經換成你的 use case

官方文件：

- [Build agents in Foundry](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)

### Models

在 Build 看 models，重點是從「可用模型」切到「目前 build 出來實際綁定的模型」。

- 主流程 agent 綁的是哪個 chat deployment
- 文件知識路徑需要哪個 embedding deployment
- 如果有 image 功能，模型在另一個資源中，不一定全都顯示在同一視角

官方文件：

- [Microsoft Foundry Models overview](https://learn.microsoft.com/azure/foundry/concepts/foundry-models-overview)

### Fine-tune

這個 workshop 主流程不依賴 fine-tune。

所以這裡不用深挖，只要先知道：

- Fine-tune 是平台能力之一
- 這個 solution accelerator 的主線是 retrieval + tools + enterprise data integration
- 如果未來某個 use case 要做風格或分類器微調，才是下一階段議題

官方文件：

- [Fine-tuning considerations in Foundry](https://learn.microsoft.com/azure/foundry/openai/concepts/fine-tuning-considerations)

### Tools

這裡要看的不是「有沒有 tool 這個功能」，而是「目前這個 scenario 的 agent 掛了哪些 tool / connection」。

對這個 workshop，最常見的觀察點是：

1. Search 或知識檢索相關設定
2. Browser Automation 是否已建立 connection
3. 其他選配功能是否有額外工具資產

如果你現在看的是企業 use case，這裡可以直接對照：

- tools 決定 agent 可以怎麼接外部能力
- documents 與 tables 決定 agent 能回答什麼內容

官方文件：

- [Foundry Agent Service tool catalog](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)

### Knowledge

這裡是最適合確認「use case 已經套用」的地方。

請重點確認：

1. 現在掛上的 knowledge 是否對應你當前的 documents
2. 名稱是否對應目前 scenario 或 solution
3. 如果你走的是 Foundry IQ 路徑，是否能看到 knowledge base 或相近知識來源配置

如果你走的是自訂 use case，建議直接確認：

- 這裡不是示意資料
- 這裡掛的是你剛剛生成或建置的那套 use case 文件

官方文件：

- [Foundry IQ overview](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)
- [Connect a Foundry IQ knowledge base to Agent Service](https://learn.microsoft.com/azure/foundry/agents/how-to/foundry-iq-connect)

### Data

Build 裡看到 Data 時，請把它當成 Foundry 視角的資料入口，不要在這一頁深挖 Fabric 細節。

這一頁只需要說明：

- 這個 workshop 會結合文件與企業資料
- 資料的實際物件驗證請看 [Microsoft Fabric 手動驗證](04b-fabric-manual-validation.md)
- 如果你現在只是先確認 Foundry portal 裡的資產，這裡知道有資料面就夠了

官方文件：

- [Foundry architecture: projects and project assets](https://learn.microsoft.com/azure/foundry/concepts/architecture#how-resources-relate-in-foundry)

### Evaluation

這裡適合用來理解「怎麼評估 agent 品質」，但第一次操作不需要展開完整評估流程。

先知道下面三點即可：

1. Foundry 有 evaluation 能力
2. 你可以對 agent 的回答做 quality / safety / task-level 檢查
3. 這個 workshop 主流程不要求先把 evaluation 設好才算成功

如果你有時間，再用 sample question 補一題，說明 evaluation 可以如何接到當前 scenario。

官方文件：

- [Evaluate generative AI applications in Foundry](https://learn.microsoft.com/azure/foundry/how-to/evaluate-generative-ai-app)

### Guardrails

Guardrails 比較適合放在後面理解，當作治理與風險控制的延伸。

先把它理解成：

- 這個 workshop 先示範怎麼把 documents 與 enterprise data 接上 agent
- guardrails 則是把回答邊界、風險控制與生產治理補齊

第一次操作不需要把所有 policy 都設完，但可以先知道這一層在 Foundry 裡的位置。

官方文件：

- [Guardrails and controls overview](https://learn.microsoft.com/azure/foundry/guardrails/guardrails-overview)
- [How to configure guardrails in Foundry](https://learn.microsoft.com/azure/foundry/guardrails/how-to-create-guardrails)

## Operate

Operate 適合放在最後看。前面是確認這個 use case 有沒有建好，這一段則是確認這些資產能不能被管理、搜尋、治理和追蹤。

參考：

- [Foundry Control Plane overview](https://learn.microsoft.com/azure/foundry/control-plane/overview)
- [Operate / Assets / Compliance / Quota / Admin 功能總覽](https://learn.microsoft.com/azure/foundry/control-plane/overview#key-features)

### Assets

這裡適合回答「這個 solution 現在到底建立了哪些東西」。

建議你用 solution name、scenario name 或 agent name 當搜尋關鍵字，快速找到：

- agent
- knowledge
- tool / connection
- model deployment 關聯資產

官方文件：

- [Manage agents in Foundry Control Plane](https://learn.microsoft.com/azure/foundry/control-plane/how-to-manage-agents)
- [Assets pane in Foundry Control Plane](https://learn.microsoft.com/azure/foundry/control-plane/overview#key-features)

### Compliance

這裡不是 workshop 主流程的必跑區，但很適合用來理解平台不只是 build agent，也包含治理與合規視角。

官方文件：

- [Manage compliance and security in Microsoft Foundry](https://learn.microsoft.com/azure/foundry/control-plane/how-to-manage-compliance-security)

### Quota

Quota 很適合拿來理解「這個 PoC 如果往正式環境走，容量與限制在哪裡」。

你不一定要現場逐項解釋，只需要指出：

- model deployment 有容量限制
- 某些能力可能受 quota 或區域可用性影響
- 這些都屬於 operate / admin 階段要關注的問題

官方文件：

- [Quota pane overview](https://learn.microsoft.com/azure/foundry/control-plane/overview#key-features)
- [Azure OpenAI in Foundry quotas and limits](https://learn.microsoft.com/azure/foundry/openai/quotas-limits#regional-quota-capacity-limits)

### Admin

Admin 主要對應多人共用、權限管理和正式化之後的管理面。

如果你想知道管理員要做哪些事，可以對照 [管理員部署並分享](00-admin-deploy-share.md)。

官方文件：

- [Admin pane overview](https://learn.microsoft.com/azure/foundry/control-plane/overview#key-features)

### Search and filter assets

這一段很適合直接實際操作一次：

1. 用 solution name 搜尋
2. 用 asset type 篩選
3. 找出 agent、knowledge、tool 或其他相關資產

這樣比只看單一頁面更容易理解 Foundry 不是只有聊天介面，而是完整資產平面。

官方文件：

- [Assets pane in Foundry Control Plane](https://learn.microsoft.com/azure/foundry/control-plane/overview#key-features)
- [Manage agents in Foundry Control Plane](https://learn.microsoft.com/azure/foundry/control-plane/how-to-manage-agents)

### View asset details and lineage

如果你想理解「這個 agent 後面連了什麼」，lineage 是很好的檢查方式。

重點可以放在：

1. 這個 agent 綁了哪個 model
2. 這個 agent 用了哪些 knowledge / tools
3. 這些資產如何回到目前的 use case 或 scenario

對 workshop 而言，這一步最能把 Discover、Build、Operate 三塊串起來。

官方文件：

- [Foundry Control Plane overview](https://learn.microsoft.com/azure/foundry/control-plane/overview)
- [Assets pane in Foundry Control Plane](https://learn.microsoft.com/azure/foundry/control-plane/overview#key-features)

## 什麼時候要跳去看 Fabric

如果你接下來想確認的是資料物件本身，而不是 Foundry portal 裡的 agent 和資產，這時就不要繼續留在 04a：

1. 想確認 lakehouse / ontology 是否存在
2. 想驗證 tables 是否真的載入
3. 想在 SQL analytics endpoint 手動查詢
4. 想從資料角度驗證 agent 之後會回答什麼

這些請直接改看 [Microsoft Fabric 手動驗證](04b-fabric-manual-validation.md)。

## Portal URL

- Microsoft Foundry: <https://ai.azure.com/>
- Azure Portal: <https://portal.azure.com/>

---

[← 建置方案](04-run-scenario.md) | [Microsoft Fabric 手動驗證 →](04b-fabric-manual-validation.md)