# Workshop 文件敘事審稿清單（2026-03-20）

## 範圍

本清單合併兩輪 narrative review，重點只看文件敘事是否準確反映目前 repository、IaC 與腳本行為，不包含 build / link 層級問題。

涵蓋區域：

- `workshop/docs/01-deploy/*`
- `workshop/docs/03-understand/*`

## 結論摘要

本次敘事審稿確認的主要問題可分成四類：

1. 可直接執行的 setup 指令寫錯
2. 將目前 workshop 的實作敘述成更完整的產品能力
3. 文件與實際 tool / IaC contract 脫節
4. 頁面內容本身有重複或結構損壞

## 完整 findings

### N-01 Setup 頁安裝指令指向不存在的 requirements 檔

- 嚴重度：高
- 檔案：`workshop/docs/01-deploy/03-configure.md`

問題：

- 文件要求使用者安裝 `requirements.txt`
- repository 根目錄沒有這個檔案
- 目前實際存在的是 `scripts/requirements.txt` 與 `workshop/requirements.txt`

影響：

- 使用者依照文件操作，會在最前面的環境設定階段直接失敗

### N-02 Foundry IQ 頁把目前流程講成 Foundry 原生 agentic retrieval

- 嚴重度：高
- 檔案：`workshop/docs/03-understand/01-foundry-iq.md`

問題：

- 文件把目前 workshop 描述成 Azure AI Foundry 的「統一知識層」與「代理式檢索」
- 但 repo 目前的主路徑是：文件上傳到 Azure AI Search，agent 透過本機 runtime 的 `search_documents` 工具做檢索

影響：

- 會讓讀者誤解本 workshop 已經示範 Foundry 原生 agentic retrieval 能力

### N-03 Fabric IQ 頁把目前流程講成 ontology-driven 平台能力

- 嚴重度：高
- 檔案：`workshop/docs/03-understand/02-fabric-iq.md`

問題：

- 文件將主路徑描述為 ontology / business rules / actions 驅動的語意平台
- 目前實作主路徑其實是：用 `ontology_config.json` 與 `schema_prompt.txt` 補充情境與資料表脈絡，再由 agent 透過 `execute_sql` 產生唯讀 T-SQL 並由本機 runtime 執行
- 頁面中的 SQL 範例還使用 `LIMIT`，和目前工具指令中的 T-SQL 規則不一致

影響：

- 會讓讀者誤認 repo 已經展示更完整的 Fabric semantic / ontology 產品能力

### N-04 Foundry Tool 頁仍記載 `search_documents.top`

- 嚴重度：中
- 檔案：`workshop/docs/03-understand/03-foundry-tool.md`

問題：

- 文件說 `search_documents` schema 有 `query` 與 `top`
- 但目前 canonical tool contract 已經只保留 `query`

影響：

- 文件宣稱自己是單一事實來源，卻和實際 strict schema 不一致

### N-05 Deep Dive 首頁延續了 Foundry IQ / Fabric IQ 的過度產品化敘事

- 嚴重度：中
- 檔案：`workshop/docs/03-understand/index.md`

問題：

- 首頁把 Foundry IQ 寫成「代理式擷取」
- 把 Fabric IQ 寫成「本體驅動的 NL→SQL」
- 客戶對話區也延續相同說法

影響：

- 即使細頁修正，高層導讀仍會先把讀者帶到過度產品化的理解

### N-06 Foundry Model 頁的選用模型範例格式與 Bicep 實際型別不一致

- 嚴重度：中
- 檔案：`workshop/docs/03-understand/00-foundry-model.md`

問題：

- 文件範例使用 `deploymentName`
- 實際 Bicep 型別使用 `name`
- 實際型別還要求 `modelFormat`

影響：

- 讀者如果依文件準備 `optionalModelDeployments` 參數，會得到錯誤結構

### N-07 Control Plane 頁把 project connections 講成主執行路徑

- 嚴重度：中
- 檔案：`workshop/docs/03-understand/04-control-plane.md`

問題：

- 文件將 Azure AI Search / Browser Automation / Bing reference connections 描述為主要 connection 模式
- 目前主路徑中，Search 與 Fabric 主要仍由本機 runtime 直接呼叫
- Browser Automation 確實依賴手動建立的 Foundry connection
- Web Search demo 則是直接使用內建 web search tool，不是本頁暗示的 Bing project connection 主路徑

影響：

- 讀者會高估 project connections 在目前 workshop 主流程中的角色

### N-08 Multi-Agent 頁被接上第二份重複版本

- 嚴重度：中
- 檔案：`workshop/docs/03-understand/05-multi-agent-extension.md`

問題：

- 頁面後半段被拼接進第二份版本
- 兩份版本內容相近但不完全相同

影響：

- 直接損害頁面可讀性與可信度

## 建議修正順序

1. 先修可執行指令與 contract 類問題：N-01、N-04、N-06
2. 再修高層產品敘事漂移：N-02、N-03、N-05、N-07
3. 最後清掉頁面結構損壞：N-08

## 修正原則

- 文件只描述 repo 目前真的有的能力
- 若是「可延伸方向」或「平台可做到的能力」，必須明確標示為後續延伸，而不是目前主路徑
- 高層總覽頁的說法必須和細頁與腳本一致