# 零售手動 demo

這一頁整理一個可直接搭配既有素材展示的零售 incident 情境，適合在 workshop 主流程之外，補一段 Foundry portal 手動操作示範。
它的定位是導讀與操作索引，不重複貼完整 instruction blocks 或完整 workflow YAML；需要逐字內容時，請直接回到來源檔案。

!!! info "適用時機"
    如果你要在 workshop 既有腳本之外，再補一段 portal 手動操作展示，這個情境比從零設計新案例更快。

!!! tip "如何使用本頁"
    先用本頁掌握展示順序與各元件角色；真的要建立 agent 或貼入 workflow 時，再開啟下列來源：

    - `data/retail_launch_incident/README.md`
    - `tmp/retail-launch-incident-foundry-low-code-workflow.yaml`

!!! note "這個情境目前是 image-only"
    本頁與對應來源材料都已改成只產出 image prompt，不包含 video 或 Sora 流程。

## Demo 目標

這場 demo 要回答的問題是：

當零售新品上市遇到疑似標示錯誤時，Foundry 能不能協助團隊快速整理：

1. 門市立即應變動作
2. 店員與對客溝通說法
3. 臨時店內告示方向
4. 一版可直接拿去測試的 image prompt

## 情境摘要

- Contoso Retail 推出新品 `BlueLeaf Sparkling Oat Latte`
- 上市當天，三家門市回報 topping sachet 疑似把 almond syrup 標錯成一般 oat topping
- 區經理需要快速決定是否暫停銷售、如何統一店員說法，以及如何提供門市告示與海報方向

這個案例特別適合展示三件事：

1. 用知識文件讓 specialist agents 回答更穩定
2. 用多 agent 分工拆開營運與溝通責任
3. 用 workflow 把多個 agent 的輸出整合成區經理可直接採用的 recovery package

## 展示順序

建議用下面順序進行：

1. 準備文件與表格素材
2. 建立兩個 specialist agents
3. 補上 router 與 coordinator agent
4. 在 workflow 中串接四個 agent
5. 用 workflow 的最終結果驗證 image prompt

## 完整設定來源

本頁只保留足夠上台 demo 的摘要。需要完整內容時，請直接對照以下來源：

| 需求 | 來源檔案 |
|------|----------|
| 完整情境與手動 demo 步驟 | `data/retail_launch_incident/README.md` |
| agent instruction blocks | `data/retail_launch_incident/README.md` |
| Foundry low-code workflow 草稿 | `tmp/retail-launch-incident-foundry-low-code-workflow.yaml` |
| 示範問題 | `data/retail_launch_incident/config/sample_questions.txt` |

## Step 1：準備素材

### 文件素材

來源資料夾：`data/retail_launch_incident/documents/`

建議直接使用既有腳本，把 PDF 寫入 Blob Storage、Azure AI Search 與 Foundry Knowledge：

```bash
python data/retail_launch_incident/prepare_search_and_blob_assets.py
python scripts/06b_upload_to_foundry_knowledge.py
```

會用到的文件包括：

1. `store_incident_playbook.pdf`
2. `shift_lead_response_guide.pdf`
3. `launch_campaign_brief.pdf`
4. `customer_message_guidelines.pdf`

### 表格素材

來源資料夾：`data/retail_launch_incident/tables/`

會用到的表格包括：

1. `launch_incidents.csv`
2. `store_response_actions.csv`

如果你要走手動 portal 展示，建議仍把這些表格先匯入共用的 Search 或 Foundry knowledge 層，而不是只掛在單一 specialist agent 下面。

### 示範問題

示範問題可直接從這裡取用：`data/retail_launch_incident/config/sample_questions.txt`

## Step 2：建立兩個 specialist agents

!!! note "本頁只保留 agent 角色摘要"
    如果你要在 Foundry portal 中逐字貼上 instruction，請直接從 `data/retail_launch_incident/README.md` 複製對應段落。

### `retail-store-ops-agent`

用途：回答門市第一線營運應變、前 15 分鐘與前 60 分鐘動作、升級條件與店員一致話術。

建議掛載 knowledge：

- `retail-store-ops-kb`

建議測試題：

```text
今天上午 BlueLeaf Sparkling Oat Latte 上市後，三家門市回報與 topping sachet 標示有關的顧客投訴。請說明區經理與門市經理在前 15 分鐘與前 60 分鐘各自應做什麼。
```

### `retail-launch-comms-agent`

用途：產出對客說法、短告示文案、社群回覆與門市海報方向。

建議掛載 knowledge：

- `retail-launch-comms-kb`

建議測試題：

```text
BlueLeaf Sparkling Oat Latte 因品質檢查，暫時在三家門市停售。請提供一段安全的對客櫃台說法、一版短告示文案、一則社群回覆，以及門市海報的創意方向。
```

## Step 3：補上 router 與 coordinator

!!! note "Router / Coordinator 的完整 prompt 來源"
    Router 與 Coordinator 的完整 instruction 與測試輸入，也都維持在 `data/retail_launch_incident/README.md`，這裡只保留結構與責任切分。

### `retail-incident-router-agent`

用途：不直接解題，只把使用者原始請求整理成 specialist agents 可處理的 handoff brief。

它應該明確拆出：

1. Situation summary
2. Operations questions to answer
3. Communications questions to answer
4. Required final deliverables

### `retail-incident-coordinator-agent`

用途：整合 router、store operations、launch communications 三方輸出，形成區經理可直接採用的 recovery package。

最後交付內容應至少包含：

1. Executive summary
2. Immediate store actions
3. Customer communication package
4. Risks or open questions
5. Image-generation prompt
6. Implementation notes for the poster

!!! tip "關鍵原則"
    Coordinator 要做的是 synthesize，不是自行發明政策或補不存在的事實。

## Step 4：串 workflow

!!! note "Workflow 示範原則"
    這裡刻意只描述最小節點順序。實際貼入 Foundry editor 的 YAML，請使用 `tmp/retail-launch-incident-foundry-low-code-workflow.yaml` 中目前已整理過的版本。

如果你要在 Foundry low-code workflow editor 裡示範，可以用這個最小順序：

1. Router
2. Store Operations
3. Launch Communications
4. Coordinator

這個順序的重點，不是展示複雜分支，而是讓觀眾清楚看到：

- 先把 incident request 轉成 handoff brief
- 再分別取得營運與溝通答案
- 最後整合成單一 recovery package

如果你已經用本 repo 的暫存 workflow 草稿做測試，請優先沿用目前可存檔、可執行的最小版本，不要在 demo 前再加入額外節點或複雜 expression。

## Step 5：驗證最終輸出

最後請把 coordinator 產出的 image prompt 拿去測 image model，確認它是否同時符合三個要求：

1. 語氣穩定且對客安全
2. 視覺方向符合 premium retail launch
3. 海報重點和前面 agent 給出的營運與溝通指引一致

建議不要只看 prompt 本身，也要回頭比對：

- 是否與 quality check 的措辭一致
- 是否避免過度戲劇化或醫療、法律語言
- 是否和門市現場暫停銷售的說法一致

## 建議展示話術

如果你要在現場口頭帶 demo，可以用下面節奏：

1. 先說明這不是 recall，而是 launch-day quality check incident
2. 再展示 specialist agents 各自只處理自己負責的範圍
3. 最後強調 workflow 的價值在於把跨角色輸出整理成單一管理包

## 參考來源

- 主要情境說明：`data/retail_launch_incident/README.md`
- 示範問題：`data/retail_launch_incident/config/sample_questions.txt`
- Foundry low-code workflow 草稿：`tmp/retail-launch-incident-foundry-low-code-workflow.yaml`

## 檢查點

!!! success "零售手動 demo 已就緒"
    你應該能夠完成以下展示：

    - [x] 用知識文件支撐 specialist agent 回答
    - [x] 用 router 與 coordinator 展示多 agent 分工
    - [x] 產出一致的 store actions 與 customer communication package
    - [x] 產出可直接測試的 image-generation prompt

---

[← 建置與測試](03-demo.md) | [深入解析 →](../03-understand/index.md)