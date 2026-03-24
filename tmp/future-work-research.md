# Future Work 研究筆記

此文件根據 `tmp/future-work.md` 的條目，對照目前 repo 結構，整理如果要把這些功能真正補進 workshop，可能需要動到哪些部分。

## 目前 repo 的可用基礎

這個 workshop 目前已經有幾個可以延伸的基礎：

- `scripts/07_create_foundry_agent.py` 與 `scripts/08_test_foundry_agent.py`：單一 Foundry Agent 的建立與測試流程。
- `scripts/14_create_multi_agent_workflow.py`、`scripts/15_test_multi_agent_workflow.py`、`multi_agent/workflow.yaml`：多代理工作流的延伸入口。
- `scripts/06_upload_to_search.py`：文件上傳與搜尋索引流程。
- `infra/` 與 `infra/modules/foundry.bicep`：目前的 Azure 資源部署骨架。
- `workshop/docs/`：正式文件入口，後續新增能力時需要補齊部署、操作與理解文件。

整體來看，這個 repo 已經適合往「安全性、評估、治理、企業整合」方向擴充，但目前主線仍以 Foundry Agent、Foundry IQ、Fabric IQ 為核心，尚未把這些 future work 做成正式流程。

## 1. add ai gateway integration

### 可能要補的部分

- `infra/modules/`：新增 API Gateway / APIM 的 Bicep 模組，例如 `api_gateway.bicep`。
- `infra/modules/foundry.bicep`：把 gateway 納入主部署流程，並串接 Foundry endpoint 或後端服務。
- `.env.example` 或對應環境設定：新增 gateway endpoint、credential、route 設定。
- `scripts/`：補一支用來設定 gateway route / policy / backend 的腳本。
- `workshop/docs/01-deploy/` 與 `workshop/docs/03-understand/`：補部署、流量治理、架構說明。

### 為什麼需要這些

目前 repo 是 Python client 直接呼叫 Foundry Agent 或相關服務，沒有中介層做：

- 流量治理
- 路由切換
- 金鑰與政策集中管理
- request / response policy 套用

如果要加 AI gateway，實際上是在目前腳本與模型端點之間多一層企業治理入口。

### 外部相依

- Azure API Management 或其他 API Gateway 服務
- 可能需要 Key Vault 管理機密
- 可能需要 App Insights / Monitor 做流量觀測

### 風險與問題

- 會增加 workshop 複雜度與成本
- 需要先定義 gateway 要代理哪些流量：只代理 agent endpoint，還是也代理 tool/backends
- 可能會影響回應延遲

## 2. add red team test

### 可能要補的部分

- `scripts/`：新增 red team 測試腳本，例如 `17_red_team_test.py`。
- `data/`：新增紅隊測試資料集，例如 prompt injection、jailbreak、data exfiltration、tool abuse 範例。
- `multi_agent/workflow.yaml`：若多代理流程也要驗證，需把紅隊情境納入工作流測試。
- `workshop/docs/03-understand/`：新增安全測試方法、案例分類與判讀方式。

### 為什麼需要這些

目前 repo 有功能測試，但缺少「惡意輸入」或「對抗式提示」驗證。若要把 workshop 往企業級 PoC 靠攏，至少需要：

- 一組固定 red team prompt dataset
- 一個可重複執行的測試腳本
- 一份結果摘要，讓參與者知道哪些攻擊目前會失敗、哪些還沒擋住

### 外部相依

- 最基本可先不依賴外部服務，直接用 curated dataset 測
- 若要更完整，可與 Content Safety 或 evaluator 串接

### 風險與問題

- 需要先定義 red team 範圍，不然會很容易失焦
- 如果只有 prompt 測試、沒有評分或分類，結果會不好比較

## 3. add evaluation

### 可能要補的部分

- `scripts/`：新增 evaluation 腳本，例如 `17_evaluate_agent.py` 或 `18_evaluation_run.py`。
- `data/`：新增 evaluation dataset，至少要有測試問題、預期答案、評分準則或 rubric。
- `multi_agent/`：若多代理流程也要評估，需要補 workflow 對應的測試集與指標。
- `workshop/docs/03-understand/`：說明評估指標、執行方式與結果判讀。

### 為什麼需要這些

目前 repo 的驗證比較偏手動互動測試。若要把能力做成可以重複驗證的 workshop 元件，evaluation 幾乎是必需品，因為它能回答：

- 回答是否 grounded
- 是否用對工具
- SQL 是否合理
- 文件與資料整合回答是否一致
- 多代理流程是否比單代理更好

### 可優先補的內容

- relevance / groundedness / faithfulness
- tool usage correctness
- SQL query safety / correctness
- 安全相關指標（後續可與 content safety 連動）

### 風險與問題

- 開放式問題很難只有單一正解
- 若沒有先定義資料集，evaluation 會流於展示而不易重複

## 4. add content safety

### 可能要補的部分

- `infra/modules/`：新增 Azure Content Safety 相關資源。
- `infra/modules/foundry.bicep`：把 safety 資源與主部署流程接起來。
- `scripts/`：新增共用 safety utility，例如 input/output 檢查模組。
- `scripts/07_create_foundry_agent.py`：若 Foundry Agent 建立流程支援 safety / RAI 設定，應納入建立邏輯。
- `scripts/08_test_foundry_agent.py`：補使用者輸入與 agent 輸出的 safety 檢查。
- `multi_agent/workflow.yaml`：針對多代理最終輸出或中間節點增加 safety gate。
- `workshop/docs/`：補政策、門檻、誤判處理方式。

### 為什麼需要這些

這個 repo 已經有一些治理與 guardrail 敘事，但還沒有把 content safety 真的做成主流程能力。若要提升 workshop 的實務感，這會是很合理的下一步，因為它可直接支撐：

- 惡意內容攔截
- 有害輸出過濾
- 與 red team / evaluation 的整合

### 可結合現有內容

- 既有 PII redaction demo 可以作為 safety 敘事的一部分
- 後續可把 content safety + PII + evaluation 串成同一條治理故事線

### 風險與問題

- 會有 false positive / false negative
- 需要決定是要做「教學示範版」還是「接近正式治理版」

## 5. agent365

### 目前最大問題：名稱有歧義

單看 `future-work.md`，`agent365` 可能有幾種意思：

1. 把 Foundry Agent 接到 Microsoft 365 / Teams / Copilot 生態
2. 讓 agent 能讀取 Microsoft 365 資料來源
3. 做成能在 365 工作場景使用的 agent 封裝

從 repo 主題與 workshop 敘事來看，**最合理的解讀**應該是：把目前的 Foundry Agent 能力往 Microsoft 365 或 Teams 場景延伸。

### 如果是「整合到 Microsoft 365 / Teams」

可能要補的部分：

- `scripts/`：新增發布或封裝腳本，例如 M365 / Teams deployment helper。
- `infra/`：補 Entra ID / app registration / 權限設定相關資源。
- 新增 Teams app manifest 或 Copilot 擴充相關描述檔。
- `workshop/docs/`：補企業整合、授權、治理與使用情境文件。

### 如果是「讀取 Microsoft 365 資料」

可能還要再補：

- Microsoft Graph 整合
- 郵件 / 文件 / Teams / Calendar 等資料存取權限
- 新的 tool contract 與資料治理規則

### 風險與問題

- 這一項目前最缺明確定義
- 一旦牽涉到 Microsoft 365 資料，就會立刻增加權限治理、租戶設定與合規難度
- 不適合在主 workshop 主線中太早加入，較像後續企業整合延伸題

## 6. hosted agent 整合研究

### 這裡的 hosted agent，建議怎麼解讀

在 Azure / Foundry 脈絡下，這裡比較合理的解讀不是 Azure DevOps hosted agent，而是：

- Azure AI Foundry Agent Service 的 hosted / managed agent 能力
- Agent Service 內建或託管的 tools，例如 file search、code interpreter、grounding 類型能力
- 以 Azure 代管方式承載 agent runtime、tool orchestration、observability 與治理

也就是說，這一項更接近「把目前 repo 的 workshop agent，往 Azure 原生託管 agent 能力整合」，而不是單純再多一個自建 orchestration layer。

### 可能要補的部分

- `scripts/07_create_foundry_agent.py`：擴充 agent 建立流程，讓它能選擇 hosted tools / managed tools。
- `scripts/08_test_foundry_agent.py`：新增 hosted tool 的驗證路徑，例如 file search、grounding、code interpreter 的測試案例。
- `scripts/14_create_multi_agent_workflow.py` 與 `multi_agent/workflow.yaml`：若多代理流程要採用 hosted agent / hosted tools，需要重新定義 agent node 與 tool wiring。
- `data/`：準備 file search / grounding / code interpreter 可重現的 sample data。
- `workshop/docs/01-deploy/`：補 hosted agent 版本的建置與驗證步驟。
- `workshop/docs/03-understand/`：補 hosted tools、managed tools、tool governance、tracing 與限制說明。

### 會牽涉到的能力面

- **File Search / Grounding**：把文件上傳、向量化、檢索接到 Agent Service 的 hosted tool 模式。
- **Code Interpreter**：讓 agent 能執行受控程式碼處理資料、產生分析結果。
- **Tracing / Observability**：若採用 hosted agent 路徑，應補對應的執行追蹤與失敗診斷方式。
- **Tool Governance**：需要定義哪些 tool 可以開、哪些情境要關、哪些資料可被 hosted tool 使用。

### 與目前 repo 的關係

目前 repo 已經有：

- Foundry Agent 建立與測試腳本
- Search / 文件 grounding 的概念主線
- 多代理延伸入口

所以 hosted agent integration 並不是從零開始，而是要把現有 workshop 的「自定義腳本與流程」重新對應成更接近 Azure 原生 Agent Service 的操作方式。這會讓 workshop 更貼近 Azure 官方示範與後續 sample code 生態。

### 外部相依

- Azure AI Foundry Agent Service
- Azure AI Search / vector store 能力
- 可能需要 Foundry project 內的額外權限與 project setup
- 若使用 code interpreter，還要確認其可用區域、成本與執行限制

### 風險與問題

- hosted tools 的可用性、區域、配額與價格可能與 workshop 環境不完全一致
- 若把太多 hosted capability 拉進主線，會讓 workshop 的最短路徑變複雜
- 需要先決定 hosted agent 是「主線替代方案」還是「進階延伸模組」
- 若和 `agent365` 同時推進，邊界容易混淆：前者偏 Azure agent runtime，後者偏企業應用接面

## 建議的實作順序

若目標是把這些功能逐步變成可教、可跑、可驗證的 workshop 延伸路徑，建議順序如下：

1. **content safety**
2. **evaluation**
3. **red team test**
4. **ai gateway integration**
5. **hosted agent integration**
6. **agent365**

### 順序理由

- `content safety` 先做，可建立最基本的治理故事線。
- `evaluation` 接著做，才能讓後面的安全與品質驗證可量化。
- `red team test` 放在 evaluation 後面，結果才容易比較與報告。
- `ai gateway integration` 比較偏架構治理，適合在安全與評估基礎成形後再加。
- `hosted agent integration` 放在 gateway 後面，能把 workshop 往 Azure 官方 agent service 能力靠攏，但不會太早破壞主線。
- `agent365` 最依賴清楚的產品定義與治理邊界，適合最後做。

## 建議拆分成哪些工作包

### 工作包 A：Safety Foundation

- 建 safety resource
- 定義 input/output 檢查流程
- 補文件與示例

### 工作包 B：Evaluation Foundation

- 建 evaluation dataset
- 補 batch evaluation script
- 定義報表格式

### 工作包 C：Adversarial Testing

- 建 red team dataset
- 建 red team runner
- 與 safety/evaluation 串接

### 工作包 D：Gateway Governance

- 部署 AI gateway / APIM
- 定義 policy、route、觀測方式
- 更新部署文件

### 工作包 E：Enterprise Surface

- 先把 hosted agent 與 enterprise integration 的邊界切開
- 先釐清 `agent365` 的實際目標
- 再決定是 Teams/M365 integration、Graph data access，或 Copilot extensibility

### 工作包 F：Hosted Agent Path

- 定義哪些 hosted tools 要納入 workshop
- 補 agent 建立 / 測試腳本
- 準備 sample data 與 demo path
- 補 tracing、限制與成本說明

## Azure 官方 Sample Code / 文件參考

以下連結可以直接作為下一步設計與實作時的參考來源，優先挑選 Microsoft Learn、Azure 官方 docs 與 Azure-Samples / microsoft-foundry repo。

### AI Gateway / APIM

- `AI gateway in Azure API Management`  
  https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities
- `Import an Azure OpenAI API as a REST API`  
  https://learn.microsoft.com/en-us/azure/api-management/azure-openai-api-from-specification
- `Import a Microsoft Foundry API`  
  https://learn.microsoft.com/en-us/azure/api-management/azure-ai-foundry-api
- `Azure-Samples/AI-Gateway`  
  https://github.com/Azure-Samples/AI-Gateway

這組資源可直接支撐 `add ai gateway integration`，特別適合參考：

- APIM fronting Azure OpenAI / Foundry 的導入方式
- token / quota / policy / routing / observability 設計
- AI gateway lab 與範例 policy

### Content Safety

- `Quickstart: Analyze text content with Azure AI Content Safety`  
  https://learn.microsoft.com/en-us/azure/ai-services/content-safety/quickstart-text?tabs=python
- `Azure AI Content Safety documentation`  
  https://learn.microsoft.com/en-us/azure/ai-services/content-safety/
- `Implement Azure AI Content Safety`  
  https://microsoftlearning.github.io/mslearn-ai-services/Instructions/Exercises/05-implement-content-safety.html
- `Azure-Samples/azureai-samples`  
  https://github.com/Azure-Samples/azureai-samples

這組資源可支撐 `add content safety`，特別是：

- Python / REST 的 moderation 呼叫方式
- 在 Foundry Guardrails + controls 介面中的操作概念
- 後續如何把 sample code 落回 workshop script

### Evaluation / Agent Evaluation

- `Resources for developing AI apps`  
  https://learn.microsoft.com/en-us/azure/developer/ai/resources-overview
- `microsoft-foundry/foundry-samples`  
  https://github.com/microsoft-foundry/foundry-samples
- `Build your code-first agent with Azure AI Foundry` resources  
  https://microsoft.github.io/build-your-first-agent-with-azure-ai-agent-service-workshop/resources/
- `Azure-Samples/azureai-samples`  
  https://github.com/Azure-Samples/azureai-samples

這組資源可支撐 `add evaluation` 與部分 `hosted agent` 路徑，特別適合拿來找：

- evaluation SDK 或 notebook 範例
- tracing / observability / code-first agent sample
- 可沿用的資料集格式與 sample app 結構

### Hosted Agent / Agent Service / Hosted Tools

- `Microsoft Foundry documentation`  
  https://learn.microsoft.com/en-us/azure/foundry/
- `Develop Python apps that use Foundry Tools`  
  https://learn.microsoft.com/en-us/azure/developer/python/azure-ai-for-python-developers
- `Azure-Samples/get-started-with-ai-agents`  
  https://github.com/Azure-Samples/get-started-with-ai-agents
- `Get started with AI agents` template page  
  https://azure.github.io/ai-app-templates/repo/azure-samples/get-started-with-ai-agents/
- `Lab 2: Grounding with Documents`  
  https://microsoft.github.io/build-your-first-agent-with-azure-ai-agent-service-workshop/lab-2-file_search/
- `Azure-Samples/ai-foundry-agents-samples`  
  https://github.com/Azure-Samples/ai-foundry-agents-samples

這組資源最適合支撐 `hosted agent integration`，因為它們直接對應：

- code-first agent 建立
- file search / grounding / vector store
- 內建或託管 tools 的接法
- 可部署 sample app 與 workshop lab

### 如何把這些 sample 套回本 repo

建議不是把 sample code 直接搬進來，而是先做一層 mapping：

1. 對照 sample 的目標能力
2. 對照本 repo 已有的 `scripts/`、`infra/`、`multi_agent/`、`workshop/docs/`
3. 決定哪些內容應該變成：
   - 新增 script
   - 新增 infra module
   - 新增 dataset
   - 新增 doc / lab
4. 最後再決定哪些 sample 值得最小化移植

## 結論

如果要完成 `tmp/future-work.md` 裡的功能，真正需要補的不只是「多幾支 script」，而是一整套對應的：

- Azure 資源
- 環境設定
- Python 腳本
- dataset
- workflow / policy
- 文件與教學敘事

其中最值得先做的是 `content safety + evaluation`。這兩個能力一旦建立，後續的 red team、gateway、hosted agent 與 enterprise integration 才有穩定的底座。

如果下一步要開始做 implementation planning，最有價值的切法會是：

- 先選 1-2 個 Azure 官方 sample 當參考基線
- 再把 `hosted agent integration` 與 `agent365` 拆開規劃
- 最後決定哪些能力是主 workshop 主線、哪些能力是進階延伸
