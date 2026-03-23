# 零售新品危機處理 Portal Demo 講稿

這份講稿是給 demo 主講者現場使用的版本。

說明文字、講者口白與一般示範 prompt 已翻成繁體中文；**agent instruction 與 workflow step prompt 依你的需求保留英文**，方便直接複製貼上到 Foundry。

---

## Demo 目標

今天要讓觀眾看到的不是一堆分散功能，而是一條完整商業處理鏈：

1. 先看 Foundry 有哪些模型能力
2. 再把 incident 拆給兩個有知識邊界的 specialists
3. 最後用 workflow 彙整成區經理級別的處置方案
4. 再把結果延伸成可實際使用的門市素材

---

## 建議時長

- 開場：1 分鐘
- Discover / Models：3 分鐘
- Knowledge + Agents：4 分鐘
- Workflow：4 分鐘
- Image + sora-2：2 分鐘
- Q&A 緩衝：1 分鐘

總計約 15 分鐘。

---

## 開場白

```text
今天我想展示的不是一組彼此分離的功能，而是一條可以串起來的商業處理情境。

請想像 Contoso Retail 剛推出新品 BlueLeaf Sparkling Oat Latte，結果上市當天上午，就有三家門市回報：部分 topping sachet 疑似把杏仁糖漿標錯成一般 oat topping。此時營運端必須在極短時間內完成四件事：先停售與隔離、指導店員怎麼說、用安全的方式對客溝通，最後還要快速產出臨時門市素材。

今天的問題是：Foundry 能不能把模型選擇、知識 grounding、workflow 協作與最終內容生成，串成同一條回應迴圈？
```

---

## Phase 1：Discover / Models

### 你要做什麼

進入 `Discover / Models`，快速指出今天會用到三種能力：

- `model-router`
- image generation model
- `sora-2`

### 你要說什麼

```text
我從 Discover 開始，是因為我想先把今天的 demo 定義成一張能力地圖。

重點不是所有任務都塞進同一個 model，而是不同任務需要不同的模型行為。像 incident routing、視覺素材生成、短影片數位看板，其實是相關但不同的工作。
```

### model-router 測試 prompt

```text
今天上午 BlueLeaf Sparkling Oat Latte 上市後，市中心三家門市回報顧客投訴，指出部分 topping sachet 疑似把杏仁糖漿標錯成一般 oat topping。請列出區經理在接下來兩小時內應該優先完成的五個動作。
```

### 你可以補一句

```text
這一步先幫我們建立事件框架，但它還是偏泛用。下一步我們要把問題接到真正有領域邊界的 knowledge agent。
```

### image model 測試 prompt

```text
請設計一張適合精品咖啡門市使用的直式告示海報，內容說明 BlueLeaf Sparkling Oat Latte 目前因品質檢查而暫時停售，並請顧客向門市人員詢問今日替代優惠。風格要沉穩、安心、易讀，主色以青綠、奶油白與柔和銅色為主。
```

### sora-2 測試 prompt

```text
請產生一支 8 秒、無聲、可循環播放的門市數位看板短片，用來說明 BlueLeaf Sparkling Oat Latte 因品質檢查而暫時停售，並邀請顧客向店員詢問今日替代優惠。風格需沉穩、精品咖啡感、文字清楚、不要使用警示或危機感過強的畫面。
```

### 轉場講法

```text
看完模型能力之後，我們接下來不再停留在 generic prompt，而是把這件事拆給有明確責任邊界的 agent。
```

---

## Phase 2：Build / Knowledge

### 你要做什麼

在 `Build / Knowledge` 建兩個 knowledge base：

- `retail-store-ops-kb`
- `retail-launch-comms-kb`

上傳對應 PDF：

- Store ops knowledge:
  - `store_incident_playbook.pdf`
  - `shift_lead_response_guide.pdf`
- Comms knowledge:
  - `launch_campaign_brief.pdf`
  - `customer_message_guidelines.pdf`

### 你要說什麼

```text
我刻意把 knowledge 拆開，因為門市營運規則和對客溝通規則，本來就不該被塞進同一個超大 prompt。

與其做一個什麼都會、但越來越難維護的 agent，不如先把責任邊界切清楚，再用 workflow 把它們協調起來。
```

### 補充重點

```text
這通常是很多人第一個會踩到的設計問題：先做一個很強的 agent，然後一直往上疊 instruction。今天我想示範的是另一種比較乾淨的做法：先拆責任，再做協作。
```

---

## Phase 3：Build / Agents

## Agent A：Store Operations Coach

### 名稱

`retail-store-ops-agent`

### 掛載 knowledge

`retail-store-ops-kb`

### instruction

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

### 測試 prompt

```text
今天上午 BlueLeaf Sparkling Oat Latte 上市後，三家門市回報與 topping sachet 標示有關的顧客投訴。請說明區經理與門市經理在前 15 分鐘與前 60 分鐘各自應做什麼。
```

### 你要說什麼

```text
這個 agent 的工作不是創意發想，而是維持營運紀律與事件處理的一致性。
```

---

## Agent B：Launch Communications Coach

### 名稱

`retail-launch-comms-agent`

### 掛載 knowledge

`retail-launch-comms-kb`

### instruction

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

### 測試 prompt

```text
BlueLeaf Sparkling Oat Latte 因品質檢查，暫時在三家門市停售。請提供一段安全的對客櫃台說法、一版短告示文案、一則社群回覆，以及數位看板的創意方向。
```

### 你要說什麼

```text
這個 agent 的 grounding 重點是品牌語氣與對客溝通，而不是門市應變程序。這個責任分離本身，就是今天 demo 的核心。
```

---

## Phase 4：Build router 與 coordinator

### Router agent 名稱

`retail-incident-router-agent`

### Router instruction

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

### Coordinator agent 名稱

`retail-incident-coordinator-agent`

### Coordinator instruction

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

### 你要說什麼

```text
接下來我補上兩個 orchestration 角色：一個負責把 incident 拆成清楚的 handoff brief，另一個負責把所有 specialist 的結果整合成區經理可直接採用的 recovery package。
```

---

## Phase 5：Workflow

### Workflow 名稱

`retail-launch-incident-workflow`

### 流程結構

```text
User request
  -> Incident Router
  -> Store Operations Specialist
  -> Launch Communications Specialist
  -> Incident Coordinator
```

### 啟動用 user request

```text
今天 BlueLeaf Sparkling Oat Latte 上市後，市中心三家門市回報顧客投訴，指出部分 topping sachet 疑似把杏仁糖漿標錯成一般 oat topping。請產出一份可供區經理直接採用的 recovery package，內容需包含：立即門市動作、店員話術、對客安全說法、臨時店內告示方向，以及一支 8 秒無聲數位看板概念。
```

### Router step prompt

```text
User request:
{{user_request}}

Create a handoff brief for the specialist agents.

Make sure the handoff clearly separates:
- operations questions,
- communications questions,
- final deliverables needed by the district manager.
```

### Store operations step prompt

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

### Launch communications step prompt

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

### Coordinator step prompt

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

### 你要說什麼

```text
workflow 的價值不是 agent 比較多，而是每個 agent 的工作變得更乾淨，handoff 也更可觀察。
```

---

## Phase 6：把 workflow 輸出接回 image 與 sora-2

### 你要做什麼

從 coordinator 的最終輸出中找出：

- `Image-generation prompt`
- `Video-generation prompt`

再分別貼到：

- image model
- `sora-2`

### 你要說什麼

```text
現在我把 workflow 的最終結果接回 creative generation。

這一段很重要，因為它代表圖片與影片不是獨立炫技功能，而是從同一份 grounded 決策包自然延伸出來的最後一哩。
```

---

## 收尾句

```text
今天看到的不是 chat、search、image、video 各自獨立的能力，而是一條完整的商業應變迴圈：先選對模型、再用 grounded specialists 分工、再用 workflow 做協調，最後產出顧客真正會看到的內容。
```

---

## 如果時間不夠的縮短版

如果現場只剩 6 到 8 分鐘，建議保留下面順序：

1. 快速介紹三種 models
2. 展示兩個 knowledge agents
3. 直接跑 workflow
4. 用 workflow 產出的 prompt 去測 image model
5. 用口頭方式帶過 `sora-2`

---

## 相關檔案

- 主整合稿：`tmp/manual-demo-connected-retail-scenario.md`
- Repo scenario pack：`data/retail_launch_incident/`
