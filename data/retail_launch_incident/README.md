## Demo 要帶學員看到什麼

這場 demo 要回答一個簡單問題：

當零售新品上市遇到疑似標示錯誤時，Foundry 能不能協助團隊快速整理營運應變、對客說法，以及門市素材方向。

情境如下：

- Contoso Retail 推出新品 `BlueLeaf Sparkling Oat Latte`
- 上市當天，有三家門市回報 topping sachet 疑似把 almond syrup 標錯成一般 oat topping
- 區經理需要快速決定停售、店員說法、顧客告示與數位看板方向

這個情境適合示範三件事：

1. 用知識文件讓 agent 回答更穩定
2. 用 specialist agents 拆開營運與溝通責任
3. 用 workflow 把多個 agent 的結果整合成完整處置方案

---

## 素材清單

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

### 可拿來做資料查詢或結構化分析的表格

資料夾：[data/retail_launch_incident/tables](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/data/retail_launch_incident/tables)

這些 CSV 也不需要手動上傳。上面的 script 會自動把它們轉成可檢索的 Search 文件。

1. `launch_incidents.csv`
2. `store_response_actions.csv`

### 可直接拿來問的示範問題

檔案：[data/retail_launch_incident/config/sample_questions.txt](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/data/retail_launch_incident/config/sample_questions.txt)

---

## 建議展示順序

整場 demo 建議照這個順序：

1. 在 `Discover / Models` 先測試模型理解情境的能力
2. 先執行 script，讓 PDF 與 CSV 自動進入 Blob Storage / Azure AI Search / Foundry Knowledge
3. 在 `Build / Agents` 建兩個 specialist agents
4. 再補一個 router agent 和一個 coordinator agent
5. 在 workflow 裡把前面幾個 agent 串起來
6. 最後把 workflow 產出的 image prompt 和 video prompt 拿去測 image model 與 `sora-2`

如果只做最短版 demo：

1. 先在 `Discover / Models` 貼入事件描述
2. 先執行資料準備 script，再確認 knowledge 已建立完成
3. 建立兩個 specialist agents
4. 用一個 workflow 把結果整合起來

---

## 開場講法

```text
今天這場 demo，我們先不談太多系統設計，而是直接帶大家走一遍操作流程。

我們會從一個零售新品事件出發，先讓模型理解情境，再放入知識文件，接著建立兩個專責 agent，最後用 workflow 把結果整合成可以直接操作與重做的處置方案。
```

---

## Step 1：Discover / Models

### 對學員解說

```text
第一步，我們先在 Discover / Models 測試模型能不能抓住事件重點。這一步很單純，就是先貼入 incident 描述，看看模型會不會整理出區經理該做的優先動作。
```

### 請貼上的文字

```text
今天上午 BlueLeaf Sparkling Oat Latte 上市後，市中心三家門市回報顧客投訴，指出部分 topping sachet 疑似把杏仁糖漿標錯成一般 oat topping。請列出區經理在接下來兩小時內應該優先完成的五個動作。
```

### 這一步要讓學員理解什麼

1. 模型能先整理事件重點
2. 模型能把任務轉成具體行動
3. 接下來就可以把問題交給更專門的 knowledge agents

---

## Step 2：Build / Knowledge

### 對學員解說

```text
第二步，我們不在 Foundry 介面裡手動上傳檔案，而是直接跑一支 scenario script。這支 script 會把 PDF 原檔放到 Blob Storage，接著把 PDF 內容與 CSV 資料都寫進 Azure AI Search，最後再由 workshop script 建立 Foundry IQ knowledge base。這樣學員之後重做時只要跑指令，不用逐頁點選上傳。
```

### 這時候請執行

```bash
python data/retail_launch_incident/prepare_search_and_blob_assets.py
python scripts/06b_upload_to_foundry_knowledge.py
```

### 這一步完成後會得到

```text
1. Blob Storage 裡的 PDF 原檔
2. Azure AI Search 裡的文件索引與表格索引
3. 可供 Foundry IQ agent 使用的 knowledge base 與 project connection
```

```text
這一段是 script-first 的 Foundry IQ 路徑，目的是讓學員快速重做資料準備與 knowledge 建立。

如果你後面要繼續做 portal 裡的 specialist agents / workflow 示範，README 後面的段落仍然是在說明 portal 示範時的人工作業方式。
```

---

## Step 3：Build / Agents

這一步開始，是切回 portal 裡的手動 specialist agent / workflow 示範路徑。

### 對學員解說

```text
第三步，我們開始建立兩個 specialist。第一個只回答營運處置，第二個只回答對客溝通。這樣示範的重點會很清楚，也比較容易讓學員理解 agent 分工。
```

### Step 3A：建立 `retail-store-ops-agent`

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

### Step 3B：建立 `retail-launch-comms-agent`

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
5. Creative direction for image or video generation
```

掛載的 Knowledge：

```text
retail-launch-comms-kb
```

測試時請貼上的文字：

```text
BlueLeaf Sparkling Oat Latte 因品質檢查，暫時在三家門市停售。請提供一段安全的對客櫃台說法、一版短告示文案、一則社群回覆，以及數位看板的創意方向。
```

---

## Step 4：補上 router 和 coordinator

### 對學員解說

```text
前面兩個 agent 各自回答自己的領域。接下來，我們補上兩個角色，讓整個流程可以串起來。一個負責把問題整理成 handoff brief，另一個負責把結果整合成最後交付內容。
```

### Router agent 要貼入的 instruction

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

### Coordinator agent 要貼入的 instruction

```text
You are the Incident Coordinator for Contoso Retail.

Your job is to combine the outputs from the Incident Router, Store Operations Coach, and Launch Communications Coach into one district-manager-ready recovery package.

Operating rules:
- Synthesize, do not invent.
- Keep operational actions and communication guidance aligned.
- Highlight anything that remains unconfirmed.
- End with two production-ready creative prompts:
  - one image-generation prompt for an in-store poster
  - one video-generation prompt for a silent digital signage loop

Always use this structure:
1. Executive summary
2. Immediate store actions
3. Customer communication package
4. Risks or open questions
5. Image-generation prompt
6. Video-generation prompt
```

---

## Step 5：建立 workflow

### 對學員解說

```text
現在我們把前面的 agent 串成一條 workflow。這一步的重點是，讓學員看到每個角色都很清楚，而且最後能組成一份完整答案。
```

### 這時候建立的流程順序

```text
retail-incident-router-agent
retail-store-ops-agent
retail-launch-comms-agent
retail-incident-coordinator-agent
```

### 啟動 workflow 時貼入

```text
今天 BlueLeaf Sparkling Oat Latte 上市後，市中心三家門市回報顧客投訴，指出部分 topping sachet 疑似把杏仁糖漿標錯成一般 oat topping。請產出一份可供區經理直接採用的 recovery package，內容需包含：立即門市動作、店員話術、對客安全說法、臨時店內告示方向，以及一支 8 秒無聲數位看板概念。
```

### Router step 請貼上的文字

```text
User request:
{{user_request}}

Create a handoff brief for the specialist agents.

Make sure the handoff clearly separates:
- operations questions,
- communications questions,
- final deliverables needed by the district manager.
```

### Store Operations step 請貼上的文字

```text
User request:
{{user_request}}

Router brief:
{{router_output}}

Use your knowledge base to produce the operations guidance needed for this launch-day incident.

Focus on:
- incident classification,
- first 15 minutes,
- first 60 minutes,
- staff talking points,
- escalation and reopen conditions.
```

### Launch Communications step 請貼上的文字

```text
User request:
{{user_request}}

Router brief:
{{router_output}}

Use your knowledge base to produce the communication package needed for this launch-day incident.

Focus on:
- customer-facing summary,
- counter script,
- poster copy,
- one social reply,
- creative direction for image or video generation.
```

### Coordinator step 請貼上的文字

```text
Original user request:
{{user_request}}

Router brief:
{{router_output}}

Store Operations output:
{{store_ops_output}}

Launch Communications output:
{{launch_comms_output}}

Combine everything into one district-manager-ready recovery package.

The final answer must include:
1. Executive summary
2. Immediate store actions
3. Customer communication package
4. Risks or open questions
5. Image-generation prompt
6. Video-generation prompt
```

---

## Step 6：把結果接回 image model 和 `sora-2`

### 對學員解說

```text
workflow 跑完之後，我們不只看文字結果，還會把最後產生的 image prompt 和 video prompt 直接拿去做素材。這一步是讓大家看到，內容生成其實是建立在前面已經整理好的決策基礎上。
```

### 接下來怎麼做

1. 從最終輸出找到 `Image-generation prompt`
2. 把它貼到 image model playground
3. 從最終輸出找到 `Video-generation prompt`
4. 把它貼到 `sora-2` playground

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

### 如果現場要直接示範，可先用這組 video prompt

```text
Create an 8-second silent looping digital signage video for a premium coffee retail store.

Message to communicate:
- BlueLeaf Product Update
- BlueLeaf Sparkling Oat Latte is temporarily unavailable during a quality check
- Please ask our store team about today's alternative offer

Visual direction:
- calm, premium, modern cafe atmosphere
- teal green and cream white as main colors, with soft copper accents
- elegant transitions and minimal motion
- large readable text designed for in-store screens
- reassuring service-oriented tone
- suitable for silent playback

Avoid:
- warning symbols
- medical or emergency imagery
- dramatic crisis visuals
- crowded layouts or too much text
```

---

## 收尾講法

```text
今天這場 demo 想讓大家學到的，不是很多獨立功能，而是一條完整流程：先理解事件、再放入知識、再交給專責 agent，最後由 workflow 組成可以落地的結果，並直接延伸成門市素材。
```

---

## 相關檔案

1. 情境素材夾：[data/retail_launch_incident](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/data/retail_launch_incident)
2. workflow 設定：[multi_agent/workflow.yaml](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/multi_agent/workflow.yaml)