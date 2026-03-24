# 零售 demo

這個資料夾存放零售 incident demo 的來源素材。
如果你要看完整操作步驟、agent 指令、workflow YAML、展示問題與 image prompt，請以 [workshop/docs/02-customize/04-retail-manual-demo.md](../../workshop/docs/02-customize/04-retail-manual-demo.md) 為主要參考。

## 主要參考

請優先閱讀：[workshop/docs/02-customize/04-retail-manual-demo.md](../../workshop/docs/02-customize/04-retail-manual-demo.md)

這份 workshop 頁面已經整合：

1. 情境摘要與展示順序
2. 自動與手動兩種素材準備方式
3. 四個 agents 的 instruction 與測試問題
4. workflow 範例
5. image prompt 驗證方式

## 情境摘要

- 品牌：Contoso Retail
- 產品：`BlueLeaf Sparkling Oat Latte`
- 事件：三家門市回報 topping sachet 疑似把 almond syrup 標錯成一般 oat topping
- 目標：整理門市應變、對客溝通、臨時告示與 image prompt

## 素材位置

### 文件

- [documents/ops-store-incident-playbook.pdf](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/data/retail_launch_incident/documents/ops-store-incident-playbook.pdf)
- [documents/ops-shift-lead-response-guide.pdf](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/data/retail_launch_incident/documents/ops-shift-lead-response-guide.pdf)
- [documents/comms-launch-campaign-brief.pdf](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/data/retail_launch_incident/documents/comms-launch-campaign-brief.pdf)
- [documents/comms-customer-message-guidelines.pdf](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/data/retail_launch_incident/documents/comms-customer-message-guidelines.pdf)

### 表格

- [tables/launch_incidents.csv](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/data/retail_launch_incident/tables/launch_incidents.csv)
- [tables/store_response_actions.csv](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/data/retail_launch_incident/tables/store_response_actions.csv)

### 腳本與相關檔案

- [prepare_search_and_blob_assets.py](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/data/retail_launch_incident/prepare_search_and_blob_assets.py)
- [06b_upload_to_foundry_knowledge.py](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/scripts/06b_upload_to_foundry_knowledge.py)
- [retail-launch-incident-foundry-low-code-workflow.yaml](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/tmp/retail-launch-incident-foundry-low-code-workflow.yaml)

## 維護原則

1. 這份 README 只保留素材入口與簡短情境說明。
2. 操作流程、agent 設定與展示內容，統一維護在 [workshop/docs/02-customize/04-retail-manual-demo.md](../../workshop/docs/02-customize/04-retail-manual-demo.md)。
3. 如果兩份文件需要同步，請以 workshop 頁為準，不要在這裡維護第二份完整教學。