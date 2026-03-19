# T-00 決策紀錄（Foundry 教學補強與翻譯專案）

## 目的

這份文件記錄目前專案在進入實作前必須先固定下來的決策，避免後續程式、文件、翻譯與測試方向不一致。

## 決策摘要

### D-01 `workshop/docs/` 是唯一主要內容來源

決策：

- 所有使用者導向的正式內容，以 `workshop/docs/` 為唯一主要來源。
- `workshop/site/` 與 root `site/` 都視為建置輸出，不作為編輯來源。
- `guides/` 只保留 review note、導向頁與補充說明，不再承擔第二套正式教學內容。

原因：

- 已移除 PDF 生成腳本與 PDF 產物。
- 先前 PDF 與網站內容已證實有分叉與過時問題。

### D-02 本次交付目標以英文主文件完整為先，繁中翻譯為第二階段

決策：

- 先補齊英文教學骨架、導覽與必要技術支撐。
- 繁中翻譯在英文骨架穩定後再進行整批落地。

原因：

- 若先翻譯再重寫資訊架構，會造成重工。
- `tmp/translation-plan-zhtw.md` 已定義翻譯流程與治理文件，可在英文架構穩定後直接套用。

### D-03 五主軸教學架構正式採用

決策：

Deep dive 區段將採用以下主軸：

1. Foundry Model
2. Foundry IQ
3. Foundry Agent
4. Foundry Tool
5. Fabric IQ
6. Control Plane

原因：

- 目前 repo 只明顯呈現 Foundry IQ / Fabric IQ，無法完整教學 Foundry 平台能力。
- `tmp/foundry-teaching-plan-zhtw.md` 已把五主軸視為目標資訊架構。

### D-04 必要能力與選配能力明確分流

決策：

#### 必要能力

- `azd up` 可部署主流程所需 Azure 資源
- 至少一個可用的 orchestration model
- 至少一個可用的 embedding model
- 文件檢索主流程
- 結構化資料查詢主流程
- Orchestrator Agent 建立與基本測試流程

#### 選配能力

- 額外模型部署
- agent trace
- publish to Teams / Microsoft 365 Copilot
- Content Understanding
- Browser Automation
- Web Search
- PII
- Image Generation

原則：

- 選配能力若因權限、區域、配額、preview 條件或租戶政策無法啟用，需 warning 並跳過，不得阻塞主流程。

### D-05 先承諾文件可教學，後承諾進階能力真實可執行

決策：

- 第一階段先確保每個主軸都有可獨立閱讀的技術文件，並對應到 repo 現有實作。
- 只有主流程必要能力必須做到可執行與可測試。
- 選配能力可先做到：
  - 文件說明
  - pseudo flow
  - minimal demo 設計
  - skip 條件定義

### D-06 多模型與進階工具採最佳努力策略

決策：

- 文件中會描述多模型與進階工具策略。
- 程式與 IaC 若要補強，需支援最佳努力部署或 guarded execution。

不承諾：

- 所有租戶、區域與訂閱都能成功啟用所有模型與工具。

### D-07 現有腳本風格必須保留

決策：

新增腳本或補強時遵循：

1. 以環境變數為主要設定來源
2. 單檔腳本單一責任
3. 清楚 console output
4. warning 與 skip 明確可見

### D-08 繁中站台先採單源翻譯，不先做雙語站台設計

決策：

- 先完成繁中內容資產與翻譯規範。
- 是否要做雙語站台或語系切換，延後到英文主文件定稿後再決定。

原因：

- 目前還在補主內容骨架，不適合現在就綁定語系資訊架構。

## 本階段交付承諾

T-00 到 T-02 完成後，代表已確定：

1. 內容來源治理
2. 五主軸資訊架構方向
3. 必要能力與選配能力分界
4. 英文先行、繁中跟進的執行順序
5. 多 Agent 平行處理的合理切分方式

## 尚待後續任務處理

以下事項在 T-00 不做最終實作，只做方向確認：

- 多模型 Bicep 參數與 guarded deployment 實作
- trace / publish 實作細節
- 各進階工具的最小 demo
- 繁中站台是否單語覆蓋或雙語共存