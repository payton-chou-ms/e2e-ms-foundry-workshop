# Workshop Site 完整錯誤清單（2026-03-20）

## 後續處理狀態（2026-03-20，第二次驗證）

以下狀態反映目前 workspace 的最新來源與重建結果，用來補充這份稽核報告最初建立時的快照結論。

- E-01 已修正：`01-deploy/index.md` 中的首頁架構圖 placeholder 已移除，頁面現在直接使用正式圖檔。
- E-02 已修正：`03-understand/index.md` 中的 `[X]` placeholder 已改為實際可對外敘述的文字。
- E-03 至 E-07 已修正：在後續文件修正後已重新執行 `mkdocs build --clean`，`workshop/site/` 不再停留在當時 audit 所比對的過時輸出。
- E-08 已修正：`workshop/docs/assets/` 目前只剩單一 canonical 圖檔 `architecture.png`，不再有 `architecture1.png` 的命名歧義。
- E-09 仍保留為結構討論事項：這是資訊架構一致性議題，不是 blocking error。

如需重新做一次只反映目前狀態的 site audit，應以這份補充狀態為準，而不是把下方條目全部視為未修正。

## 稽核範圍

本次稽核覆蓋下列階段：

1. 來源文件與 MkDocs 導覽盤點
2. 來源文件的相對連結、圖片與 placeholder 掃描
3. `mkdocs build --clean --strict` 驗證
4. 現有 `workshop/site/` 與 fresh build 輸出的差異比對

稽核目標是先產出完整錯誤清單，暫不修改來源文件。

## 稽核結論摘要

### 已確認的高優先問題

1. 來源文件仍有 placeholder，且會直接進入站台
2. 目前 `workshop/site/` 不是最新建置結果，至少有 8 個輸出檔已過時
3. `01-deploy` 與 `03-understand` 有內容品質問題，不是單純 link 問題

### 已確認沒有出錯的項目

1. `workshop/mkdocs.yml` 中 23 個 nav leaf 都能對應到實際來源檔
2. `workshop/docs/` 來源文件的相對 markdown links 與圖片路徑目前沒有壞鏈結
3. `mkdocs build --clean --strict` 可以成功完成

### 尚待人工判斷的項目

1. 架構圖內容是否與目前實作完全一致
2. 頁面敘事是否有「雖然可建站，但內容已過時」的更多案例
3. 目前 `Deep dive` 的導覽順序是否符合產品敘事預期

## 詳細錯誤清單

## E-01 來源文件保留 TODO 註解

- 嚴重度：高
- 類型：來源內容品質
- 檔案：[workshop/docs/01-deploy/index.md](/workspaces/nc-iq-workshop/workshop/docs/01-deploy/index.md)
- 位置：來源檔內架構圖上方

問題：

- 文件仍保留 `<!-- TODO: Add architecture diagram image here -->`
- 這表示來源頁尚未完成整理，且 placeholder 已進入建置結果

影響：

- 使用者在建置後的 HTML 中仍會看到 `TODO:` 文字
- 降低文件可信度，也容易讓 reviewer 以為此頁尚未完成

驗證結果：

- 在來源檔與 fresh build 的 `01-deploy/index.html` 中都可重現

## E-02 Deep Dive 總覽頁保留未替換的 `[X]` placeholder

- 嚴重度：高
- 類型：來源內容品質
- 檔案：[workshop/docs/03-understand/index.md](/workspaces/nc-iq-workshop/workshop/docs/03-understand/index.md)
- 位置：常見客戶問題的「設定有多難？」回答段落

問題：

- 仍保留「這個 PoC 花了 `[X]` 分鐘」的占位字

影響：

- 這是對外說明的文字，placeholder 直接削弱內容可信度
- 代表 Deep Dive 總覽頁並未完成最後內容收斂

驗證結果：

- 在來源檔與 fresh build 的 `03-understand/index.html` 中都可重現

## E-03 目前 `workshop/site/` 已落後於來源內容

- 嚴重度：高
- 類型：建置輸出過時
- 範圍：[workshop/site](/workspaces/nc-iq-workshop/workshop/site)

問題：

- 以 `mkdocs build --clean --strict --site-dir /tmp/nc-iq-site-audit-build` 重建後，比對現有 `workshop/site/`，共有 8 個共同檔案內容不一致

受影響檔案：

1. [workshop/site/01-deploy/01-deploy-azure/index.html](/workspaces/nc-iq-workshop/workshop/site/01-deploy/01-deploy-azure/index.html)
2. [workshop/site/01-deploy/02-setup-fabric/index.html](/workspaces/nc-iq-workshop/workshop/site/01-deploy/02-setup-fabric/index.html)
3. [workshop/site/01-deploy/03-configure/index.html](/workspaces/nc-iq-workshop/workshop/site/01-deploy/03-configure/index.html)
4. [workshop/site/01-deploy/04-run-scenario/index.html](/workspaces/nc-iq-workshop/workshop/site/01-deploy/04-run-scenario/index.html)
5. [workshop/site/03-understand/03-foundry-tool/index.html](/workspaces/nc-iq-workshop/workshop/site/03-understand/03-foundry-tool/index.html)
6. [workshop/site/search/search_index.json](/workspaces/nc-iq-workshop/workshop/site/search/search_index.json)
7. [workshop/site/sitemap.xml](/workspaces/nc-iq-workshop/workshop/site/sitemap.xml)
8. `workshop/site/sitemap.xml.gz`

影響：

- 目前 `workshop/site/` 反映的不是最新來源內容
- 若用這份站台做人工驗證，會混入已修過但尚未重建的舊內容

## E-04 `01-deploy/04-run-scenario` 的站台內容過時

- 嚴重度：高
- 類型：建置輸出過時
- 檔案：[workshop/site/01-deploy/04-run-scenario/index.html](/workspaces/nc-iq-workshop/workshop/site/01-deploy/04-run-scenario/index.html)

問題：

- 現有建置輸出缺少最新文件內容，至少包含：
  - `--foundry-only` 現在會先設定 Content Understanding defaults 的說明
  - `--foundry-only` 的步驟表
  - 選配 demo 驗證狀態段落

影響：

- 使用者若讀現有站台，會得到過時流程說明
- 與目前腳本實際行為不一致

驗證方式：

- 比對現有建置輸出與 fresh build 的 HTML diff

## E-05 `03-understand/03-foundry-tool` 的站台內容過時

- 嚴重度：中
- 類型：建置輸出過時
- 檔案：[workshop/site/03-understand/03-foundry-tool/index.html](/workspaces/nc-iq-workshop/workshop/site/03-understand/03-foundry-tool/index.html)

問題：

- 現有建置輸出缺少最新補充內容，至少包含：
  - optional demo 腳本目前狀態
  - 新版 `azure-ai-projects` SDK 類型對齊說明
  - PII / image generation 的更新後限制說明

影響：

- Deep dive 站台內容落後於實際 repo 能力與限制說明

## E-06 搜尋索引已過時

- 嚴重度：中
- 類型：建置輸出過時
- 檔案：[workshop/site/search/search_index.json](/workspaces/nc-iq-workshop/workshop/site/search/search_index.json)

問題：

- 既然部分 HTML 已與 fresh build 不一致，搜尋索引也一定不是最新內容

影響：

- 使用者透過站內搜尋可能搜到過時文字，或搜不到剛新增的段落

## E-07 sitemap 已過時

- 嚴重度：低
- 類型：建置輸出過時
- 檔案：
  - [workshop/site/sitemap.xml](/workspaces/nc-iq-workshop/workshop/site/sitemap.xml)
  - `workshop/site/sitemap.xml.gz`

問題：

- sitemap 與 fresh build 不一致

影響：

- 對本機閱讀影響有限
- 對發佈與搜尋引擎索引一致性有影響

## E-08 架構圖資產存在雙版本，容易造成內容誤用

- 嚴重度：中
- 類型：內容治理 / 資產治理
- 檔案：
  - [workshop/docs/assets/architecture.png](/workspaces/nc-iq-workshop/workshop/docs/assets/architecture.png)
  - [workshop/docs/assets/architecture1.png](/workspaces/nc-iq-workshop/workshop/docs/assets/architecture1.png)

問題：

- `workshop/docs/01-deploy/index.md` 目前只引用 `architecture.png`
- 但 assets 目錄中同時存在 `architecture1.png`
- 兩份圖檔容易造成維護者誤判哪一張才是目前正式架構圖

影響：

- 容易導致頁面引用錯圖或 reviewer 用錯版本做內容判讀
- 這類問題屬於內容正確性風險，不一定會被自動化 link check 抓出

## E-09 Deep Dive 導覽順序與頁面敘事未完全收斂

- 嚴重度：中
- 類型：內容結構一致性
- 檔案：
  - [workshop/mkdocs.yml](/workspaces/nc-iq-workshop/workshop/mkdocs.yml)
  - [workshop/docs/03-understand/index.md](/workspaces/nc-iq-workshop/workshop/docs/03-understand/index.md)

問題：

- `mkdocs.yml` 的 Deep dive nav 順序目前為：
  1. Foundry Model
  2. Foundry Agent
  3. Foundry Tool
  4. Foundry IQ
  5. Fabric IQ
  6. Control Plane
  7. Multi-Agent Extension
- 但總覽頁中同時使用「六主軸」與「Intelligence Layer」這種合併概念
- 這種寫法不一定是錯，但很容易讓讀者以為 nav 應該是另一種分組順序

影響：

- 不是建站錯誤，但屬於內容架構一致性問題
- 會讓人工驗證時感覺「導覽順序或內容不太對」

## 已確認沒有問題的項目

## P-01 `mkdocs.yml` nav 對應來源檔完整

- 結果：通過
- 說明：23 個 nav leaf 全部對應到實際存在的來源 markdown 檔

## P-02 來源 markdown 的本地相對連結未發現壞鏈結

- 結果：通過
- 說明：掃描 `workshop/docs/**/*.md` 中的本地 markdown link 與圖片 link，未發現不存在的目標

## P-03 strict build 可成功完成

- 結果：通過
- 指令：`mkdocs build --clean --strict`
- 說明：沒有出現會阻斷建站的設定或路徑錯誤

## 不列為錯誤的觀察

## O-01 404.html 的絕對路徑引用

- 在 built HTML 掃描時，`404.html` 中出現多個以 `/nc-iq-workshop/...` 開頭的絕對連結
- 這些在本機檔案系統解析會被判成不存在，但對 GitHub Pages 的 `site_url` / base path 來說屬於正常行為
- 因此本次不列為真正錯誤

## 修正建議順序

1. 先修來源 placeholder
2. 決定正式架構圖，只保留一個 canonical 資產命名
3. 收斂 Deep dive 總覽的主軸敘事與 nav 順序說法
4. 完整重建 `workshop/site/`
5. 重新驗證 search index 與 sitemap
