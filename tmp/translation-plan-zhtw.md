# 文件翻譯計劃（繁體中文）

## 目標

將此 repo 中面向使用者的文件翻譯為繁體中文（zh-TW），並保留技術正確性、操作可行性與站台導覽一致性。

## 前提

翻譯應以 `workshop/docs/` 為唯一內容來源。

- `workshop/site/` 與 root `site/` 是產生物，不翻譯。
- `guides/` 以發佈產物、審閱文件或導向頁為主，不應再維護第二份完整教學內容。
- 若 PDF 需要中文版本，應在網站原始文件完成後再決定如何重新產出，不應直接把 PDF 當翻譯來源。

## 建議工作拆分

建議拆成 **12 個 work items**。這種拆法比逐檔案建立工作單更容易排期，也比較不會漏掉術語整理、校對與網站驗證。

## 範圍

包含：

1. 根目錄說明文件
2. `guides/` 底下仍保留為文字頁面的導向文件或說明文件
3. `workshop/docs/` 底下的 MkDocs 原始文件
4. `workshop/mkdocs.yml` 內會顯示給使用者看的站台導覽與文案
5. `infra/vscode_web/` 底下的補充說明文件

不包含：

1. `workshop/site/` 這類產生出的靜態網站內容
2. PDF 成品
3. CI workflow 與非使用者導向設定檔（除非決定連註解與說明一併在地化）

## 規模概估

- 主要 Markdown 原始文件：約 20 份
- 約 7,305 words
- 約 1,764 lines

實際工作量的重點不只在翻譯文字，還包括：

1. Azure / Fabric / Foundry 術語一致性
2. CLI 指令、環境變數、路徑與程式碼區塊不可誤翻
3. 表格、步驟、連結、錨點與導覽標題需同步驗證

## Work Items

### WI-01 建立翻譯規則與術語表

內容：

1. 定義繁中用語風格
2. 建立專有名詞對照表
3. 決定哪些術語保留英文，哪些翻譯

重點術語示例：

- Azure AI Foundry
- Foundry IQ
- Fabric IQ
- ontology
- workspace
- deployment
- lakehouse
- semantic search
- embeddings
- agent

產出：

1. 翻譯原則
2. 術語表 glossary

### WI-02 翻譯根目錄總覽文件

檔案：

- `/README.md`

內容：

1. 專案介紹
2. 快速開始
3. 成本估算
4. 疑難排解

### WI-03 翻譯部署指南

檔案：

- `/guides/deployment_guide.md`（若保留為導向頁，工作量會很小）

內容：

1. 導向說明
2. 官方網站入口連結
3. 來源說明

### WI-04 翻譯 Workshop 首頁與站台導覽

檔案：

- `/workshop/README.md`
- `/workshop/docs/index.md`
- `/workshop/mkdocs.yml`

內容：

1. 站台首頁文案
2. 導覽列名稱
3. 站台標題與描述

### WI-05 翻譯 Get Started 章節

檔案：

- `/workshop/docs/00-get-started/index.md`
- `/workshop/docs/00-get-started/workshop-flow.md`

內容：

1. 先決條件
2. Workshop 流程說明
3. 操作入口與啟動方式

### WI-06 翻譯 Deploy 章節

檔案：

- `/workshop/docs/01-deploy/index.md`
- `/workshop/docs/01-deploy/00-admin-deploy-share.md`
- `/workshop/docs/01-deploy/00-participant-run-validate.md`
- `/workshop/docs/01-deploy/01-deploy-azure.md`
- `/workshop/docs/01-deploy/02-setup-fabric.md`
- `/workshop/docs/01-deploy/03-configure.md`
- `/workshop/docs/01-deploy/04-run-scenario.md`

內容：

1. Admin deploy and share 路徑
2. Participant run and validate 路徑
3. Azure 資源部署
4. Fabric 設定
5. 開發環境設定
6. 執行情境與建置流程

### WI-07 翻譯 Customize 章節

檔案：

- `/workshop/docs/02-customize/index.md`
- `/workshop/docs/02-customize/02-generate.md`
- `/workshop/docs/02-customize/03-demo.md`

內容：

1. 自訂使用案例
2. 資料與提示產生流程
3. PoC 示範與驗證

### WI-08 翻譯 Understand 章節

檔案：

- `/workshop/docs/03-understand/index.md`
- `/workshop/docs/03-understand/01-foundry-iq.md`
- `/workshop/docs/03-understand/02-fabric-iq.md`

內容：

1. Foundry IQ 說明
2. Fabric IQ 說明
3. 架構與能力理解

### WI-09 翻譯 Cleanup 章節

檔案：

- `/workshop/docs/04-cleanup/index.md`
- `/workshop/docs/04-cleanup/next-steps.md`

內容：

1. 清理資源
2. 後續建議

### WI-10 翻譯 VS Code Web 補充文件

檔案：

- `/infra/vscode_web/README.md`
- `/infra/vscode_web/README-noazd.md`

內容：

1. Web 版使用說明
2. 非 azd 流程補充

### WI-11 技術校對與一致性檢查

檢查項目：

1. 術語是否一致
2. 指令與程式碼區塊是否保持原樣
3. 環境變數、檔名、路徑是否未被誤翻
4. 表格與清單格式是否完整
5. 中英混排與標點是否一致

### WI-12 站台驗證與重新產出

檢查項目：

1. MkDocs 導覽是否正常
2. 連結、標題、錨點是否正確
3. 繁中頁面是否正常顯示
4. 是否需要重新產生 PDF 或靜態站台

## 如果改用逐檔案管理

如果要用比較細的管理方式，也可以改成每份文件一個 work item，再加上：

1. 術語表與翻譯規範
2. 全站校對
3. 建站驗證

這種拆法大約會是 **22 到 24 個 work items**。

## 建議執行順序

1. 先完成 WI-01，避免後續術語不一致
2. 再處理首頁、README、Deploy 類文件，先把兩條主要使用路徑翻完
3. 接著翻譯 Customize / Understand / Cleanup
4. 最後進行技術校對與站台驗證

## 建議驗收標準

1. 所有使用者可見文件均有繁體中文版
2. 所有命令、程式碼區塊、環境變數名稱保持正確
3. 站台導覽與文件標題一致
4. 無失效連結
5. 專有名詞用法前後一致

## 建議備註

若後續要正式執行翻譯，建議另外建立：

1. `translation-glossary-zhtw.md`
2. `translation-style-guide-zhtw.md`
3. 每章節翻譯完成後的 reviewer checklist

另外建議在翻譯開始前先確認：

1. 是否保留 `guides/` 下的導向文件為中英雙語或僅英文
2. 中文站台是否要直接覆蓋現有英文站台，或改成雙語導覽
3. PDF 是否要等網站繁中版完成後再統一產出