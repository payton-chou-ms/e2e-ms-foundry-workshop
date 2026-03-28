# 維護者：資料腳本對照

這一頁集中整理附錄資料路徑專用的維護者腳本。

主線頁面不再展開這些腳本，因為它們只在資料附錄或除錯資料路徑時才需要。

## 資料路徑核心順序

```text
02 建立資料工作區項目
03 載入資料到工作區
05 舊版資料 agent 相容層
```

## 維護者腳本對照

### `02_create_fabric_items.py`（維護者入口）

- 用途：建立 Lakehouse、Ontology、DataBindings 和 relationships
- 什麼時候跑：你要使用完整資料問答路徑時

```bash
python scripts/02_create_fabric_items.py
python scripts/02_create_fabric_items.py --clean
```

### `03_load_fabric_data.py`（維護者入口）

- 用途：把 CSV 載入資料工作區
- 什麼時候跑：`02` 完成之後

```bash
python scripts/03_load_fabric_data.py
```

### `05_create_fabric_agent.py`（Deprecated shim）

- 用途：較早期的資料 agent 路徑；目前只保留作為轉呼叫 `legacy/create_fabric_data_agent.py` 的相容層
- 什麼時候跑：你在維護舊筆記或比對舊資料路徑時

```bash
python scripts/05_create_fabric_agent.py
```

如果你只是要跑通主線，請回到 [腳本用途與執行順序](../01-deploy/05-script-sequence.md) 或 [進階：維護者腳本對照](../01-deploy/05b-script-core-pipeline.md)。

---

[← Fabric IQ：資料](04-fabric-iq.md) | [清理 →](../04-cleanup/index.md)