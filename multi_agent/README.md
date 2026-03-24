# Multi-agent 與零售新品事件工作流

這個資料夾提供一條宣告式 multi-agent 路徑，讓 workshop 可以從原本的單一 agent 問答，延伸成更貼近實際營運事件處理的工作流。

這條延伸路徑目前採用 **零售新品異常應變** 情境，重點不是多建幾個 agent，而是把同一個 incident 拆成更清楚的角色與 handoff。

## 這裡新增了什麼

- `workflow.yaml`：零售專用的宣告式 workflow 設計
- `scripts/15_test_multi_agent_workflow.py`：刷新 scenario agents，然後執行 Fabric + Search workflow
- `scripts/15b_test_multi_agent_search_only_workflow.py`：刷新 search-only agents，然後執行同一條 workflow
- `scripts/16_agent_framework_workflow_example.py`：最小化的 code-first workflow 範例

## 目前的角色設計

1. `router`
2. `store_ops_specialist`
3. `launch_comms_specialist`
4. `coordinator`

### 各角色負責什麼

- `router`：先整理 incident，明確指出後續 specialists 需要回答什麼
- `store_ops_specialist`：結合文件搜尋與唯讀 SQL，整理門市應變與 reopen blocker
- `launch_comms_specialist`：只用文件搜尋，整理對客說法、告示與創意方向
- `coordinator`：整合前三者結果，產出區經理等級 recovery package

## 為什麼這和主 workshop 一致

- Foundry prompt agent 的建立方式仍然與主流程一致
- 本機 tool execution model 仍然沿用現有 `search_documents` 與 `execute_sql`
- 變的只有 orchestration 形狀，不是底層資料或搜尋基礎

## 使用方式

### Fabric + Search 版本

用預設 sample question 直接跑：

```bash
python scripts/15_test_multi_agent_workflow.py
```

指定 scenario 與問題：

```bash
python scripts/15_test_multi_agent_workflow.py   --scenario launch_incident_response   --question "請整合門市立即動作、店員話術、對客安全說法，以及暫時店內海報與數位看板方向。"
```

### Search-only 版本

```bash
python scripts/15b_test_multi_agent_search_only_workflow.py
python scripts/15b_test_multi_agent_search_only_workflow.py   --scenario launch_incident_response   --question "如果沒有 Fabric 資料，只靠文件知識，門市應該如何對 BlueLeaf 上市事件做第一時間應對？"
```

## 可見輸出階段

workflow 會輸出四段可觀察結果：

1. router brief
2. store operations output
3. customer communications output
4. final coordinated answer

這很適合 demo，因為你不只看到最終答案，也能清楚看到 handoff 是如何被拆開的。
