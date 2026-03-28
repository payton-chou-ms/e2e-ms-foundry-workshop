# Multi-agent 與進階範例

這些不是基本 workshop 必跑步驟。它們是給你在主流程跑通之後，往 multi-agent workflow 或新版 Agent Framework 延伸用的。

### `15_test_multi_agent_workflow.py`

用途：**單一入口** 的資料查詢 + Search multi-agent demo。預設會先依照 `multi_agent/workflow.yaml` 建立或更新零售 incident scenario 的 agents，然後立刻執行整條 workflow。

```bash
python scripts/15_test_multi_agent_workflow.py
python scripts/15_test_multi_agent_workflow.py --scenario launch_incident_response
python scripts/15_test_multi_agent_workflow.py --scenario launch_incident_response --question "請整合門市立即動作、店員話術、對客安全說法，以及暫時店內海報與數位看板方向。"
```

### `15b_test_multi_agent_search_only_workflow.py`

用途：**單一入口** 的 search-only multi-agent demo。不需要資料查詢附錄，預設會先建立或更新指定 scenario 的 search-only agents，然後立刻執行整條 workflow。

```bash
python scripts/15b_test_multi_agent_search_only_workflow.py
python scripts/15b_test_multi_agent_search_only_workflow.py --scenario launch_incident_response
python scripts/15b_test_multi_agent_search_only_workflow.py --scenario launch_incident_response --question "如果沒有資料查詢能力，只靠文件知識，門市應該如何對 BlueLeaf 上市事件做第一時間應對？"
```

### `16_agent_framework_workflow_example.py`

這支是幫你理解新版 Microsoft Agent Framework 寫法的最小範例，不是目前 workshop 主流程的正式實作。

建議先固定目前常見的 preview 版本：

```bash
pip install --pre "agent-framework-core==1.0.0rc3" "agent-framework-azure-ai==1.0.0rc3"
```

如果你之後要把 workflow 包成 HTTP 服務，再另外補裝 hosting adapter：

```bash
pip install --pre "azure-ai-agentserver-core==1.0.0b16" "azure-ai-agentserver-agentframework==1.0.0b16"
```

執行方式：

```bash
python scripts/16_agent_framework_workflow_example.py
python scripts/16_agent_framework_workflow_example.py --question "Summarize the policy risk and next step."
```

---

[← Browser Automation 補充設定](05d-browser-automation-setup.md) | [為你的使用案例自訂 →](../02-customize/index.md)
