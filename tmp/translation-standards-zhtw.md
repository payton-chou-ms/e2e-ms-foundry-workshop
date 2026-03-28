# 文件翻譯標準（繁體中文）

## 目的

這份文件整合翻譯計畫、術語表、寫作規範與 reviewer checklist，作為本 repo 後續所有繁體中文在地化工作的單一標準來源。

## 適用範圍

包含：

1. `README.md`
2. `guides/` 中仍保留為文字頁面的導向或補充文件
3. `workshop/docs/` 下的 MkDocs 原始文件
4. `workshop/mkdocs.yml` 中會直接顯示給使用者的文案
5. `infra/vscode_web/` 的使用者導向說明文件

不包含：

1. `workshop/site/`、root `site/` 等建置輸出
2. PDF 成品
3. CI workflow 與非使用者導向設定檔

## 來源與範圍原則

- 翻譯一律以 `workshop/docs/` 為唯一主要內容來源
- 不可把 PDF、產生出的站台內容或暫存輸出當作翻譯來源
- 檔名不翻，翻的是頁面內容、站台標題與導覽顯示文案

## 建議翻譯工作流

1. 先確認英文原文已穩定
2. 依本文件術語與風格規則翻譯
3. 用 reviewer checklist 做技術與格式校對
4. 驗證 MkDocs 導覽、連結、錨點與格式
5. 若需交付整批繁中內容，再評估是否產生 PDF 或其他發佈物

## 建議翻譯順序

1. 先完成規則與 glossary
2. 再翻首頁、README 與 Deploy 主路徑
3. 接著翻 Customize / Understand / Cleanup
4. 最後做全站校對與建站驗證

## 翻譯核心原則

1. 先保技術正確，再追求語句流暢
2. 不為了中文通順而改動命令、路徑、參數與程式碼
3. 保持與英文原文相同的操作順序與資訊層級
4. 標題、導覽與章節命名需彼此一致
5. 同一術語在全站只使用一種主要譯法，避免混用

## 不可翻譯項目

以下內容必須保持原文：

1. CLI 指令與參數
2. code block 全文
3. 環境變數名稱
4. 檔名、資料夾名稱、路徑
5. JSON / YAML key
6. API 與 SDK 符號名稱
7. URL 與連結目標

示例：

- `azd up`
- `python scripts/admin_prepare_docs_data_demo.py`
- `FABRIC_WORKSPACE_ID`
- `workshop/docs/01-deploy/04-run-scenario.md`
- `DefaultAzureCredential`

## 可翻譯項目

以下內容應翻譯：

1. 章節標題
2. 一般敘述句
3. 表格中的說明欄位
4. admonition 標題與內容
5. MkDocs 導覽列文字

## 優先術語表

| 英文 | 建議繁中 | 使用規則 |
| --- | --- | --- |
| Azure | Azure | 產品名稱不翻 |
| Microsoft Foundry | Microsoft Foundry | 本 repo 的正式平台名稱統一使用此寫法 |
| Foundry project | Foundry project | 專案邊界名稱不翻 |
| Foundry Control Plane | Foundry Control Plane | 控制面名稱不翻 |
| Microsoft Fabric | Microsoft Fabric | 產品正式名稱不翻 |
| Foundry IQ | Foundry IQ | 功能名稱不翻 |
| Fabric IQ | Fabric IQ | 功能名稱不翻 |
| Azure AI Search | Azure AI Search | 產品正式名稱不翻 |
| Azure AI Services | Azure AI Services | 產品正式名稱不翻 |
| Application Insights | Application Insights | 產品正式名稱不翻 |
| VS Code | VS Code | 產品名稱不翻 |
| Azure Developer CLI | Azure Developer CLI | 首次可寫 Azure Developer CLI（azd） |
| ontology | 本體 | 首次可寫 本體（ontology） |
| workspace | 工作區 | 一般敘述用；若是 UI 名稱可保留 Workspace |
| deployment / deploy | 部署 | 文件敘述翻譯，CLI 指令不翻 |
| participant | 參與者 | workshop 角色用語 |
| admin | 管理員 | 視上下文補前綴 |
| lakehouse | Lakehouse | 專有概念保留英文 |
| warehouse | Warehouse | 專有概念保留英文 |
| semantic search | 語意搜尋 | 技術概念可翻 |
| embeddings | 向量嵌入 | 首次可寫 向量嵌入（embeddings） |
| vector index | 向量索引 | 技術概念可翻 |
| agent | 代理程式 | 一般敘述用；產品功能名稱可保留 Agent |
| orchestrator agent | 協調代理程式 | 首次可寫 協調代理程式（Orchestrator Agent） |
| data agent | 資料代理程式 | 首次可寫 資料代理程式（Data Agent） |
| prompt | 提示詞 | 若語境偏 Prompt Engineering 可保留 prompt |
| schema | 結構描述 | 可依上下文簡化為 schema |
| sample scenario | 範例情境 | 文件固定用法 |
| use case | 使用案例 | 文件固定用法 |
| troubleshooting | 疑難排解 | 標題固定用法 |
| cleanup | 清理 | 標題可譯為 清理 或 清理資源 |
| source of truth | 唯一內容來源 | 文件治理用語 |
| generated artifact | 產生物 | 也可依語境寫 建置產物 |

補充規則：

- 本 repo 不再使用 `Azure AI Foundry` 作為對外正式名稱
- 若文件同時提到平台、專案與控制面，請分別使用 `Microsoft Foundry`、`Foundry project`、`Foundry Control Plane`

## 常見混用提醒

| 不建議混用 | 建議統一 |
| --- | --- |
| 工作空間 / 工作區 | 工作區 |
| 語義搜尋 / 語意搜尋 | 語意搜尋 |
| 部署 / 佈署 | 部署 |
| 代理 / 代理人 / agent | 預設用 代理程式，必要時保留 Agent |

## 寫作風格規則

### 語氣

- 使用專業、清楚、直接的繁體中文
- 避免口語化、行銷化、過度熱情的措辭
- 優先寫成可執行的說明，不寫模糊描述

### 句型

- 步驟用短句
- 複雜概念先給一句總結，再補細節
- 表格欄位名稱保持短而清楚

### 人稱

- 優先使用中性描述
- 例如「請執行以下指令」「確認你已具備下列權限」

## Markdown 與格式保留規則

翻譯時必須保留：

1. 標題層級
2. 清單層級
3. 表格欄數與格式
4. 連結目標
5. admonition 語法
6. tabbed block 與 code fence 語法

不得因翻譯而破壞：

- `!!! note`
- `=== "Windows"`
- 表格分隔線
- 相對路徑連結

## 中英混排規則

1. 產品名保留英文時，周邊敘述用中文
2. 程式碼與中文之間保留自然空白
3. 中文標點為主，但 code、路徑、環境變數周邊不要插入不必要全形符號

示例：

- 請先執行 `azd auth login`。
- 確認 `FABRIC_WORKSPACE_ID` 已設定。

## 導覽與標題規則

- 導覽名稱可翻譯，但需與頁面標題對齊
- 若頁面標題保留英文，導覽應保持一致
- 翻譯 `mkdocs.yml` 時，不可只改導覽而不檢查對應頁面標題

## Reviewer Checklist

### 1. 術語一致性

- [ ] 已依本文件使用術語
- [ ] 沒有出現同詞多譯
- [ ] 產品正式名稱保持一致

### 2. 技術正確性

- [ ] 所有指令與參數保持原樣
- [ ] 所有環境變數名稱保持原樣
- [ ] 所有檔名、資料夾名、路徑保持原樣
- [ ] 所有 API / SDK / 類別名稱保持原樣

### 3. Markdown 與格式

- [ ] 標題層級正確
- [ ] 清單層級正確
- [ ] 表格欄位完整
- [ ] code block 未被破壞
- [ ] admonition 與 tabbed blocks 語法正常

### 4. 導覽與連結

- [ ] 頁面標題與導覽名稱一致
- [ ] 相對連結未失效
- [ ] 錨點與交叉引用仍可正確使用

### 5. 中文品質

- [ ] 中文語句自然且清楚
- [ ] 中英混排一致
- [ ] 標點用法一致
- [ ] 沒有過度直譯或不自然說法

## 完成定義

一篇文件可視為翻譯完成，至少要同時滿足：

1. 術語符合本文件
2. 指令、路徑、環境變數保持正確
3. Markdown 格式未破壞
4. 與相鄰頁面的導覽名稱一致
5. reviewer checklist 可勾選通過
