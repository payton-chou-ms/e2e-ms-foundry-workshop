# 建置與驗證解決方案

!!! info "兩條路徑都會使用"
       管理員使用本頁來驗證預設部署。
       本頁一律假設：目前**還沒有預載資料與 Agent**。

如果你接手的是**管理員已經預載好的共享環境**，請改看 [參與者執行與驗證](00-participant-run-validate.md)。

## 超速使用（主線只保留 Foundry path）

以下都以 `default` 這個預設 scenario 為前提。

#### Path 1A: Foundry IQ only

```bash
python scripts/participant_validate_docs.py
```

#### Path 1B: Foundry-native IQ Agent

```bashpython scripts/09_demo_content_understanding.py

python scripts/participant_validate_foundry_iq.py
```

如果你之後要補文件 + 資料整合路徑，請改看 [附錄延伸](../05-appendix/index.md)。

## 執行完整流程

如果你只想知道該跑哪一條，直接用上面的「超速使用」即可。
如果你想理解各 mode 背後差在哪裡，再看 [腳本用途與執行順序](05-script-sequence.md)。

!!! tip "如果要換情境"
       請直接到 [產生自訂資料](../02-customize/02-generate.md) 看完整做法。
       本頁只保留預設情境的建置與驗證。

### Path 1: Foundry IQ only

適合先做文件問答，不接資料附錄。

預設 use case 使用 `data/default` 這套資料。

- 文件 source：`data/default/documents`
- sample question：`data/default/config/sample_questions.txt` 裡的 `DOCUMENT QUESTIONS`

這條 path 有兩種 prepare 模式，差別只在文件問答能力建立的位置：

- **search-only 版本**：走 search-only prepare 路徑，後面用 `participant_validate_docs.py` 驗證
- **Foundry-native 版本**：走 knowledge base + MCP prepare 路徑，後面用 `participant_validate_foundry_iq.py` 驗證

#### Path 1A: 本機 workshop runtime

用上面「超速使用」區塊的兩行指令即可。

#### Path 1B: Foundry-native IQ Agent

這條變體仍然使用 `data/default` 的文件資料，但 prepare 不是走 search-only 路徑，而是改走 Foundry knowledge base + MCP tool 這條路。

- 主要差異：會建立 Foundry knowledge base、project connection，以及 Foundry-native IQ agent

同樣直接用上面「超速使用」區塊的兩行指令即可。

### 資料路徑延後到附錄

如果你要把這套 PoC 擴充成文件 + 資料整合問答，請等 Foundry 主線全部完成後，再回頭看 [附錄延伸](../05-appendix/index.md)。

附錄會補上：

- `admin_prepare_docs_data_demo.py` / `participant_validate_docs_data.py` 這條完整路徑
- 資料工作區、Lakehouse、Ontology 的設定與手動驗證
- 資料 IQ 的 grounding 說明

## 選配 demo

`09` 到 `13` 都是選配 demo，不是主流程必要步驟。

如果你之後要測 Browser Automation，再回頭看 [Browser Automation 補充設定](05d-browser-automation-setup.md)。

## 檢查點

!!! success "方案已可執行！"
       你現在至少擁有一個可運作的方案：

       - [x] Path 1：**Foundry IQ** 可回答文件問題
       - [x] Path 1B：如果你選 Foundry-native 變體，也可在 Foundry 內用 knowledge base 回答文件問題
       - [ ] 如果你之後要補資料問答，可再進附錄完成資料路徑

---

[← 設定開發環境](03-configure.md) | [Microsoft Foundry Live Tour →](04a-manual-experiments.md)
