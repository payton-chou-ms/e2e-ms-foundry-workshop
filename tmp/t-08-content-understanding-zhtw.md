# T-08 Content Understanding 評估結果

## 狀態

- 已完成

## 決策

- 採「腳本示範 + 文件輸入素材」兩者都做。
- 不把 Content Understanding 併入主流程 agent tool loop。
- 先提供一個可獨立執行的最小 demo，供 T-15 `Foundry Tool` 頁面後續引用。

## 最小 demo 定義

- 檔案：`scripts/09_demo_content_understanding.py`
- 輸入：repo 既有 PDF（預設優先使用 `outage_management_policies.pdf`）
- Analyzer：`prebuilt-documentSearch`
- 呼叫方式：使用 Python SDK `begin_analyze_binary`，直接上傳本機檔案 bytes
- 輸出：
  - operation id
  - document mime type / 頁數 / table 數量 / figure 數量
  - markdown 摘要片段

## 為什麼這樣做

- 與 workshop 現有文件型資料最貼近，無需額外建立發票或外部 sample URL。
- `prebuilt-documentSearch` 比 `prebuilt-invoice` 更符合這個 repo 的 policy / process 類情境。
- 使用 binary upload 可避免為 demo 額外準備公開 Blob URL。
- 讓延伸工具能力維持獨立示範，不污染主流程的 `search_documents` / `execute_sql` 敘事。

## 先決條件

- 已有 Foundry resource endpoint
- 資源位於 Content Understanding 支援區域
- 資源已完成 default model deployment 設定
- 執行者具備 `Cognitive Services User` 或可正常使用 API key
- 已安裝 `azure-ai-contentunderstanding`

## 目前採用的環境變數策略

- endpoint 解析順序：
  - `CONTENTUNDERSTANDING_ENDPOINT`
  - `CONTENT_UNDERSTANDING_ENDPOINT`
  - `AZURE_AI_ENDPOINT`
- key 解析順序：
  - `CONTENTUNDERSTANDING_KEY`
  - `CONTENT_UNDERSTANDING_KEY`
  - `AZURE_AI_KEY`
- 若未提供 key，改用 `DefaultAzureCredential`

## Skip 條件

以下情況一律顯示明確 `SKIP:` 文案，不阻塞主流程：

1. 未安裝 `azure-ai-contentunderstanding`
2. 找不到 endpoint
3. 找不到可分析的 PDF 檔案
4. 驗證失敗，通常代表未登入 Azure 或缺少 `Cognitive Services User`
5. 未設定 Content Understanding 的 default model deployments
6. 資源區域不支援，或 processing location 不支援
7. 配額 / capacity / service availability 問題

## 驗證方式

最小驗證指令：

```bash
python scripts/09_demo_content_understanding.py
```

成功條件：

- 能看到 `SUCCESS` 開頭訊息
- 能看到 pages / tables / figures 等 metadata
- 能看到 markdown 摘要

可接受的 skip 條件：

- 顯示 `SKIP:` 與明確原因
- 預設模式結束碼為 0，不影響整體 workshop 流程

除錯模式：

```bash
python scripts/09_demo_content_understanding.py --strict
```

## 對後續文件的影響

T-15 `Foundry Tool` 頁面可直接引用以下敘事：

- 主流程 tool 維持 `search_documents` + `execute_sql`
- `Content Understanding` 屬延伸展示工具
- 最小 demo 使用獨立腳本，不與 orchestrator agent 綁死
- 若資源、區域、權限或 defaults 不齊，教學上直接 skip 並說明 prerequisites

## 主要依據

- Microsoft Learn: Content Understanding quickstart
- Microsoft Learn: region support
- Microsoft Learn: service limits
- Azure SDK for Python `azure-ai-contentunderstanding` sample `sample_analyze_binary.py`