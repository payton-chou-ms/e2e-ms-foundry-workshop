# Multi-agent 與進階範例

這些不是基本 workshop 必跑步驟。它們是給你在主流程跑通之後，往 multi-agent workflow 或新版 Agent Framework 延伸用的。

### `14_create_multi_agent_workflow.py`

用途：依照 `multi_agent/workflow.yaml` 建立多角色 agents。這條是 **Fabric + Search** 完整版。

```bash
python scripts/14_create_multi_agent_workflow.py
python scripts/14_create_multi_agent_workflow.py --scenario policy_gap_analysis
```

### `14b_create_multi_agent_search_only_workflow.py`

用途：建立 **search-only** multi-agent 版本，不需要 Fabric。

```bash
python scripts/14b_create_multi_agent_search_only_workflow.py
python scripts/14b_create_multi_agent_search_only_workflow.py --scenario policy_gap_analysis
```

### `15_test_multi_agent_workflow.py`

用途：執行 **Fabric + Search** multi-agent workflow。

```bash
python scripts/15_test_multi_agent_workflow.py --scenario policy_gap_analysis
python scripts/15_test_multi_agent_workflow.py --scenario exception_triage --question "We saw an unusual spike in escalations. What policy applies and what does the data suggest?"
```

### `15b_test_multi_agent_search_only_workflow.py`

用途：執行 **search-only** multi-agent workflow。

```bash
python scripts/15b_test_multi_agent_search_only_workflow.py --scenario policy_gap_analysis
python scripts/15b_test_multi_agent_search_only_workflow.py --scenario exception_triage --question "We saw an unusual spike in escalations. What policy guidance applies?"
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