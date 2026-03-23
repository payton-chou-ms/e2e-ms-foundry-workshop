# retail_launch_incident

這是給 workshop repo 使用的零售新品異常應變情境包。

它把 manual demo 裡的零售新品危機處理故事，整理成 repo 目前可理解的 `data/<scenario>/` 結構，並把適合在 workshop 中展示的內容翻成繁體中文。

## 目錄結構

```text
retail_launch_incident/
  config/
    ontology_config.json
    schema.json
    schema_prompt.txt
    sample_questions.txt
  documents/
    customer_message_guidelines.pdf
    launch_campaign_brief.pdf
    shift_lead_response_guide.pdf
    store_incident_playbook.pdf
  tables/
    launch_incidents.csv
    store_response_actions.csv
```

## 啟用方式

將 `.env` 中的 `DATA_FOLDER` 指到這個 scenario：

```env
DATA_FOLDER=data/retail_launch_incident
```

## 這個情境包的用途

- 支援 Foundry IQ / AI Search 文件 grounding
- 提供 Fabric 載入用的 CSV tables
- 提供 single-agent 與 multi-agent demo 的 sample questions
- 讓手動 demo、repo data 與 `multi_agent/workflow.yaml` 逐步對齊

## 對應文件

- 入口整合稿：`tmp/manual-demo-connected-retail-scenario.md`
- 主講稿：`tmp/manual-demo-retail-portal-script.md`
- 零售 workflow：`multi_agent/workflow.yaml`
