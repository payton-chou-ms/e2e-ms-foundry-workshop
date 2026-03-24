# AI 合約關鍵字審閱 demo

這個資料夾保留 workshop 用的正式素材、腳本與展示輸出。

如果你要用和零售案例相同的 manual 形式來講解這個情境，請直接閱讀：

- `workshop/docs/02-customize/05-contract-keyword-review-manual-demo.md`

那一頁已整理成 workshop manual 版面，包含：

1. 情境摘要與展示順序
2. 真實輸入、正式中間產物與最終輸出的位置
3. 最小必要腳本與建議指令
4. reviewer 應該實際讀取的 JSON / Markdown 素材

## 本資料夾用途

### `input/`

正式輸入檔：

1. `06-合約範本.docx`
2. `07-待審閱合約.docx`
3. `04-規則檔.xlsx`

### `intermediate/`

正式中間產物：

1. `04-規則清單.json`
2. `04-規則清單.md`
3. `06-合約範本-可比較內容.md`
4. `06-合約範本-可比較段落.json`
5. `07-待審閱合約-可比較內容.md`
6. `07-待審閱合約-可比較段落.json`
7. `ref-08-差異比較.html`

### `output/`

正式展示輸出：

1. `09-審閱結果.html`

### `config/`

reviewer 相關設定：

1. `reviewer_prompt.txt`
2. `sample_questions.txt`
3. `diff_prompt.txt`

## 最小必要腳本

1. `generate_content_artifacts.py`

這支腳本固定使用真實 Azure Content Understanding 重建正式中間產物；如果 CU 或環境未就緒，會直接失敗，不再走本機 fallback。

重建與展示方式，請以 workshop manual 那一頁為主，避免這裡與教學頁的說明分叉。
