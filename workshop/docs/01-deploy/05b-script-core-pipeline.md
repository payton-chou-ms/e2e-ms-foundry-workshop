# 停用：手動拆解與低階除錯

這個 repo 不再支援手動拆解與低階除錯。

這一頁只保留給舊書籤、舊投影片和歷史連結使用，不再提供逐支腳本的維護者對照，也不再把 low-level pipeline 當成 workshop 支援路徑。

## 請改走目前支援的入口

主線建置與驗證，請回到 [腳本用途與執行順序](05-script-sequence.md) 或 [建置與驗證解決方案](04-run-scenario.md)。

如果你需要文件加資料的附錄路徑，請看 [附錄中的資料腳本對照](../05-appendix/05-maintainer-data-scripts.md)。

## 目前建議的公開命令

```bash
python scripts/admin_prepare_shared_demo.py --mode foundry-only
python scripts/admin_prepare_shared_demo.py --mode foundry-iq

python scripts/participant_validate_docs.py
python scripts/participant_validate_foundry_iq.py
python scripts/participant_validate_docs_data.py

python scripts/admin_prepare_docs_data_demo.py
python scripts/author_generate_custom_data.py
python scripts/author_rebuild_custom_poc.py --industry "Insurance" --usecase "Property insurance with claims processing and policy management"
```

如果你是想理解頁面之間怎麼分工，請直接看上面的公開入口頁與附錄頁，不要再依賴這個舊的維護者對照頁。

---

[← 腳本用途、快速路徑與執行順序](05-script-sequence.md) | [附錄中的資料腳本對照 →](../05-appendix/05-maintainer-data-scripts.md)