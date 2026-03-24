## 零售 demo

這場 demo 要回答一個簡單問題：

當零售新品上市遇到疑似標示錯誤時，Foundry 能不能協助團隊快速整理營運應變、對客說法，以及門市素材方向。

情境如下：

- Contoso Retail 推出新品 `BlueLeaf Sparkling Oat Latte`
- 上市當天，有三家門市回報 topping sachet 疑似把 almond syrup 標錯成一般 oat topping
- 區經理需要快速決定停售、店員說法、顧客告示與門市視覺素材方向

這個情境適合示範三件事：

1. 用知識文件讓 agent 回答更穩定
2. 用 specialist agents 拆開營運與溝通責任
3. 用 workflow 把多個 agent 的結果整合成完整處置方案

---

## 展示順序

1. 先執行 script，讓 PDF 與 CSV 自動進入 Blob Storage / Azure AI Search / Foundry Knowledge
2. 在 `Build / Agents` 建兩個 specialist agents
3. 再補一個 router agent 和一個 coordinator agent
4. 在 workflow 裡把前面幾個 agent 串起來
5. 最後把 workflow 產出的 image prompt 拿去測 image model

---

## Step 1：素材清單

### 要準備成 Knowledge 與檢索資料的文件

資料夾：[data/retail_launch_incident/documents](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/data/retail_launch_incident/documents)

這些 PDF 不需要再手動上傳。請直接執行：

```bash
python data/retail_launch_incident/prepare_search_and_blob_assets.py
python scripts/06b_upload_to_foundry_knowledge.py
```

這個流程會自動完成三件事：

1. 把 PDF 原檔上傳到 Blob Storage
2. 把 PDF 內容切 chunk 後寫進 Azure AI Search
3. 用 Search index 建立 Foundry IQ knowledge base

會被處理的 PDF：

1. `store_incident_playbook.pdf`
2. `shift_lead_response_guide.pdf`
3. `launch_campaign_brief.pdf`
4. `customer_message_guidelines.pdf`

### 手動上傳對照表

如果你要改走 portal 裡的手動 knowledge / agent 示範路徑，可先照下面分配：

| 檔案 | 手動上傳到哪個 agent / knowledge |
|------|------------------------------|
| `store_incident_playbook.pdf` | `retail-store-ops-agent` / `retail-store-ops-kb` |
| `shift_lead_response_guide.pdf` | `retail-store-ops-agent` / `retail-store-ops-kb` |
| `launch_campaign_brief.pdf` | `retail-launch-comms-agent` / `retail-launch-comms-kb` |
| `customer_message_guidelines.pdf` | `retail-launch-comms-agent` / `retail-launch-comms-kb` |

對應原則很簡單：

1. 營運應變類文件給 `retail-store-ops-agent`
2. 對客溝通類文件給 `retail-launch-comms-agent`

### 可拿來做資料查詢或結構化分析的表格

資料夾：[data/retail_launch_incident/tables](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/data/retail_launch_incident/tables)

這些 CSV 也不需要手動上傳。上面的 script 會自動把它們轉成可檢索的 Search 文件。

1. `launch_incidents.csv`
2. `store_response_actions.csv`

手動路徑下，這兩份 CSV 不建議只掛給單一 specialist agent。

比較正確的理解是：

1. 它們屬於共用的 Search / Foundry knowledge 資料層
2. 不屬於 `retail-store-ops-agent` 或 `retail-launch-comms-agent` 其中一個人的專屬 knowledge
3. 如果走目前 repo 的建議流程，仍然應該用 script 先寫進 Azure AI Search，再供後續 Foundry IQ 或 workflow 使用

### 可直接拿來問的示範問題

檔案：[data/retail_launch_incident/config/sample_questions.txt](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/data/retail_launch_incident/config/sample_questions.txt)

---


## Step 2：建立 Specialist Agents

### 2A：建立 `retail-store-ops-agent`

請貼上的 instruction：

```text
You are the Store Operations Coach for Contoso Retail.

Your job is to help district managers and store managers handle launch-day product incidents using only the approved operating guidance in your connected knowledge base.

Operating rules:
- Use the connected knowledge as the source of truth.
- Prioritize immediate operational actions, escalation, and frontline staff consistency.
- If the knowledge does not confirm a fact, say that it is not confirmed.
- Do not invent medical, legal, or supplier details.
- Do not turn a temporary quality check into a confirmed recall unless the knowledge explicitly says so.

When you answer, always use this structure:
1. Incident classification
2. First 15 minutes
3. First 60 minutes
4. Staff talking points
5. Escalation or reopen conditions
```

掛載的 Knowledge：

```text
retail-store-ops-kb
```

測試時請貼上的文字：

```text
今天上午 BlueLeaf Sparkling Oat Latte 上市後，三家門市回報與 topping sachet 標示有關的顧客投訴。請說明區經理與門市經理在前 15 分鐘與前 60 分鐘各自應做什麼。
```

### 2B：建立 `retail-launch-comms-agent`

請貼上的 instruction：

```text
You are the Launch Communications Coach for Contoso Retail.

Your job is to turn launch-day incident guidance into customer-safe, brand-consistent communication using only the approved guidance in your connected knowledge base.

Operating rules:
- Use the connected knowledge as the source of truth.
- Keep the tone calm, premium, responsible, and human.
- Avoid dramatic, legal, or medical language unless explicitly supported by the knowledge.
- Prefer "quality check" and "temporarily unavailable" over stronger language.
- Include actionable next steps for customers and store staff.

When you answer, always use this structure:
1. Customer-facing summary
2. Counter script
3. Poster copy
4. Social reply
5. Creative direction for image generation
```

掛載的 Knowledge：

```text
retail-launch-comms-kb
```

測試時請貼上的文字：

```text
BlueLeaf Sparkling Oat Latte 因品質檢查，暫時在三家門市停售。請提供一段安全的對客櫃台說法、一版短告示文案、一則社群回覆，以及門市海報的創意方向。
```

---

## Step 3：補上 Router 和 Coordinator

- 前面兩個 agent 各自回答自己的領域。接下來，我們補上兩個角色，讓整個流程可以串起來。一個負責把問題整理成 handoff brief，另一個負責把結果整合成最後交付內容。

### 3A：建立 `retail-incident-router-agent`

Create agent: `retail-incident-router-agent`

```text
You are the Incident Router for a retail launch-day issue.

Your job is not to solve the incident directly. Your job is to create a clean handoff brief for specialist agents.

You must identify:
- what happened,
- what operations evidence is needed,
- what customer communication evidence is needed,
- what final deliverables should be produced.

Do not invent policies. Do not write customer-facing copy. Do not answer as if you are the final decision-maker.

Always use this structure:
1. Situation summary
2. Operations questions to answer
3. Communications questions to answer
4. Required final deliverables
```

測試時請貼上的文字：

```text
今天 BlueLeaf Sparkling Oat Latte 上市後，市中心三家門市回報顧客投訴，指出部分 topping sachet 疑似把杏仁糖漿標錯成一般 oat topping。

請不要直接給最終處置方案，而是先整理成一份 handoff brief，提供給 operations specialist 與 communications specialist 使用。

這份 brief 必須清楚區分：
- 事件摘要
- 營運面需要回答的問題
- 對客溝通面需要回答的問題
- 最後要交付給區經理的成果項目
```

### 3B：建立 `retail-incident-coordinator-agent`

Create agent: `retail-incident-coordinator-agent`

```text
You are the Incident Coordinator for Contoso Retail.

Your job is to combine the outputs from the Incident Router, Store Operations Coach, and Launch Communications Coach into one district-manager-ready recovery package.

Operating rules:
- Synthesize, do not invent.
- Keep operational actions and communication guidance aligned.
- Highlight anything that remains unconfirmed.
- End with one production-ready creative prompt:
  - one image-generation prompt for an in-store poster

Always use this structure:
1. Executive summary
2. Immediate store actions
3. Customer communication package
4. Risks or open questions
5. Image-generation prompt
6. Implementation notes for the poster
```

測試時請貼上的文字：

```text
Original user request:
今天 BlueLeaf Sparkling Oat Latte 上市後，市中心三家門市回報顧客投訴，指出部分 topping sachet 疑似把杏仁糖漿標錯成一般 oat topping。請產出一份可供區經理直接採用的 recovery package，內容需包含：立即門市動作、店員話術、對客安全說法、臨時店內告示方向，以及一版門市海報的視覺方向。

Router brief:
1. Situation summary
- Launch-day incident involving possible topping sachet labeling mismatch across three city-center stores.
- Customer complaints have already been reported at the counter.
- District manager needs immediate operations guidance and customer communication guidance.
2. Operations questions to answer
- Should stores temporarily pause sales of the affected drink?
- What should store managers do in the first 15 and 60 minutes?
- What evidence should be collected before escalation?
3. Communications questions to answer
- How should frontline staff explain the temporary pause safely?
- What short poster copy and social reply should be used?
- What visual direction should be used for in-store signage?
4. Required final deliverables
- Immediate store actions
- Staff talking points
- Customer-facing summary
- Poster copy
- Social reply
- Image prompt
- Poster implementation notes

Store Operations output:
1. Incident classification
- Treat as a quality-check incident requiring temporary sales pause at affected stores until SKU / sachet labeling is confirmed.
2. First 15 minutes
- Pause sales of the affected drink at reported stores.
- Isolate remaining sachets tied to the affected launch stock.
- Notify district manager and capture store-level incident facts.
3. First 60 minutes
- Confirm whether the issue is isolated or broader.
- Align shift leads on one staff script.
- Reopen only when approved guidance confirms the product can return to sale.
4. Staff talking points
- The item is temporarily unavailable while a quality check is completed.
- Please offer an alternative beverage and apologize for the inconvenience.
5. Escalation or reopen conditions
- Escalate if additional stores report the same issue.
- Reopen only after approved confirmation from operations leadership.

Launch Communications output:
1. Customer-facing summary
- BlueLeaf Sparkling Oat Latte is temporarily unavailable while we complete a quality check.
2. Counter script
- We're temporarily pausing this item while we verify product quality. I'd be happy to help you choose today's closest alternative.
3. Poster copy
- BlueLeaf Product Update
- BlueLeaf Sparkling Oat Latte is temporarily unavailable during a quality check.
- Please ask our store team about today's alternative offer.
4. Social reply
- Thanks for checking with us. This item is temporarily unavailable at select stores while we complete a quality check. Our store teams can recommend an alternative in the meantime.
5. Creative direction for image generation
- Calm, premium, reassuring cafe look with teal, cream, and soft copper accents.

Combine everything into one district-manager-ready recovery package.
```



---

## Step 4：建立 workflow

現在我們把前面的 agent 串成一條 workflow。這一步的重點是，讓學員看到每個角色都很清楚，而且最後能組成一份完整答案。

### 這時候建立的流程順序

```text
name: retail-launch-incident-workflow
description: Sequential Foundry workflow for the retail launch incident recovery scenario

kind: Workflow
trigger:
  kind: OnConversationStart
  id: retail_launch_incident
  actions:
    - kind: InvokeAzureAgent
      id: invoke_router
      displayName: Route incident
      conversationId: =System.ConversationId
      agent:
        name: retail-incident-router-agent

    - kind: InvokeAzureAgent
      id: invoke_store_ops
      displayName: Build store operations response
      conversationId: =System.ConversationId
      agent:
        name: retail-store-ops-agent

    - kind: InvokeAzureAgent
      id: invoke_launch_comms
      displayName: Build customer communications response
      conversationId: =System.ConversationId
      agent:
        name: retail-launch-comms-agent

    - kind: InvokeAzureAgent
      id: invoke_coordinator
      displayName: Synthesize district manager package
      conversationId: =System.ConversationId
      agent:
        name: retail-incident-coordinator-agent
      output:
        autoSend: true
```

### 啟動 workflow 時貼入

```text
今天 BlueLeaf Sparkling Oat Latte 上市後，市中心三家門市回報顧客投訴，指出部分 topping sachet 疑似把杏仁糖漿標錯成一般 oat topping。請產出一份可供區經理直接採用的 recovery package，內容需包含：立即門市動作、店員話術、對客安全說法、臨時店內告示方向，以及一版門市海報的視覺方向。
```

---

## Step 5：把結果接回 image model

workflow 跑完之後，我們不只看文字結果，還會把最後產生的 image prompt 直接拿去做素材。這一步是讓大家看到，內容生成其實是建立在前面已經整理好的決策基礎上。


### 接下來怎麼做

1. 從最終輸出找到 `Image-generation prompt`
2. 把它貼到 image model playground

### 如果現場要直接示範，可先用這組 image prompt

```text
Create a premium in-store vertical poster for a specialty coffee retail brand.

Title:
BlueLeaf Product Update

Body copy:
BlueLeaf Sparkling Oat Latte is temporarily unavailable while we complete a quality check.
Please ask our store team about today's alternative offer.

Visual direction:
- calm, premium, reassuring, modern cafe style
- color palette: teal green, cream white, soft copper accents
- high readability from a distance
- elegant typography with clean layout
- subtle oat or cup-inspired abstract background
- suitable for a retail entrance or queue area poster

Avoid:
- medical imagery
- hazard icons
- warning-tape style visuals
- panic, crisis, or recall language
```

---

今天這場 demo 想讓大家學到的，不是很多獨立功能，而是一條完整流程：先理解事件、再放入知識、再交給專責 agent，最後由 workflow 組成可以落地的結果，並直接延伸成門市素材。

---

## 相關檔案

1. 情境素材夾：[data/retail_launch_incident](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/data/retail_launch_incident)
2. workflow 設定：[multi_agent/workflow.yaml](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/multi_agent/workflow.yaml)