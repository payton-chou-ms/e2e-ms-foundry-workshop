# 零售新品危機處理 Manual Demo 統一稿

這份文件的目標，是讓你在 **Microsoft Foundry portal 手動 demo** 時，可以用**同一條故事線**自然串起下面幾件事：

- `Discover / Models`
- `Deploy model-router and test`
- `Deploy image models and test`
- `Deploy sora-2 model and test`
- `Build / Agents`
- `Create two agents with Knowledge (Foundry IQ)`
- `Create multi-agent with workflow`

這份稿刻意設計成 **portal-first、可複製貼上**。

補充說明：**說明文字、講者講稿、knowledge 文件內容與 sample questions 已翻成繁體中文；agent instruction 與 workflow step prompt 則依需求保留英文風格。**

---

## 1. Demo 主故事：零售新品危機處理

### 一句話版本

Contoso Retail 正在全台門市推出新品 **BlueLeaf Sparkling Oat Latte**，但上市當天有三家門市回報：部分 topping sachet 疑似把 **almond syrup** 標錯成一般 oat topping。門市需要在不製造恐慌的前提下，快速完成：

1. 現場停售與隔離
2. 店員說法與客訴應對
3. 對消費者的門市告示與短影音數位看板
4. 由多代理協作產出區經理級別的整體處置方案

### 為什麼這條故事適合 demo

它可以自然把各能力串起來：

- **model-router**：先示範不同任務要走不同模型能力
- **兩個有 knowledge 的 agents**：一個負責門市營運與事件處理，一個負責品牌溝通與對外說法
- **multi-agent workflow**：把兩個 specialists 的結果整合成區經理級決策包
- **image model**：產生臨時店內告示海報
- **sora-2**：產生門市數位看板短片提示詞

---

## 2. Demo 你要讓觀眾記住什麼

### 觀眾 takeaway

這場 demo 最重要的訊息不是「Foundry 有很多按鈕」，而是：

1. **同一個商業事件，可以拆成模型選擇、知識 grounding、角色分工與內容生成**
2. **不是所有任務都該塞進同一個 agent**
3. **Knowledge agents 適合先把專業責任拆開**
4. **Workflow 的價值，在於 handoff 與可重複的協調**
5. **創意輸出不是孤立功能，而是可以接在營運決策後面**

---

## 3. 建議的 demo 路線

### Phase A：Discover / Models

先從平台能力切入，不要一開始就講事故。

你可以這樣鋪陳：

- `model-router` 代表「不是每個 request 都該進同一條推理路徑」
- image model 代表「後續會需要快速生成門市素材」
- `sora-2` 代表「同一個 incident 最後可能延伸到數位看板或短影片內容」

### Phase B：Build / Knowledge + Agents

接著切到 Build，說明這次不是做泛用聊天，而是做**兩個有責任邊界的 specialists**：

- `Store Operations Coach`
- `Launch Communications Coach`

兩者都吃 Foundry IQ knowledge，但各自只看自己的文件集合。

### Phase C：Multi-agent Workflow

最後說明：真正面對上市事故時，區經理不需要兩份分散的答案，而是要一份可執行方案。

所以 workflow 會做：

- Intake / Router
- 門市營運分析
- 對客溝通分析
- Coordinator 彙整
- 產出最終營運方案 + image prompt + sora prompt

### Phase D：生成創意輸出

最後把 workflow 產出的 creative prompts 丟到：

- image model：生成店內告示
- `sora-2`：生成數位看板短片

這樣整條故事就完整了：**從模型探索 → 單一專家 → 多代理協作 → 最終素材產出**。

---

## 4. 建議的資產命名

### Models

- `model-router`
- `retail-image-gen`
- `sora-2`

### Knowledge

- `retail-store-ops-kb`
- `retail-launch-comms-kb`

### Agents

- `retail-store-ops-agent`
- `retail-launch-comms-agent`
- `retail-incident-router-agent`
- `retail-incident-coordinator-agent`

### Workflow

- `retail-launch-incident-workflow`

---

## 5. Discover / Models 測試 prompt

> 備註：不同租戶的 `model-router` 體驗可能不同。  
> 如果你的 `model-router` 主要是做文字模型路由，那就把它當成「任務分類 / 入口推理」示範；  
> image 與 `sora-2` 則在後面用 workflow 產出的 prompts 直接測。

### 5.1 model-router 測試 prompt：文字推理任務

```text
今天上午 BlueLeaf Sparkling Oat Latte 上市後，市中心三家門市回報顧客投訴，指出部分 topping sachet 疑似把杏仁糖漿標錯成一般 oat topping。請列出區經理在接下來兩小時內應該優先完成的五個動作。
```

### 5.2 model-router 測試 prompt：圖片任務分類

```text
請設計一張適合精品咖啡門市使用的直式告示海報，內容說明 BlueLeaf Sparkling Oat Latte 目前因品質檢查而暫時停售，並請顧客向門市人員詢問今日替代優惠。風格要沉穩、安心、易讀，主色以青綠、奶油白與柔和銅色為主。
```

### 5.3 model-router 測試 prompt：影片任務分類

```text
請產生一支 8 秒、無聲、可循環播放的門市數位看板短片，用來說明 BlueLeaf Sparkling Oat Latte 因品質檢查而暫時停售，並邀請顧客向店員詢問今日替代優惠。風格需沉穩、精品咖啡感、文字清楚、不要使用警示或危機感過強的畫面。
```

### 5.4 image model 備用 prompt

```text
請設計一張精品咖啡門市適用的直式告示海報。

標題：BlueLeaf 上市更新
內文：BlueLeaf Sparkling Oat Latte 因品質檢查暫時停售，歡迎向門市夥伴詢問今日替代優惠。

視覺方向：
- 沉穩、精品、讓人安心
- 青綠、奶油白、柔和銅色
- 現代咖啡館風格
- 高對比、遠距離可讀
- 可用杯子輪廓或燕麥感抽象背景
- 不要醫療圖像
- 不要危險警示圖示
```

### 5.5 sora-2 備用 prompt

```text
請產生一支適用於精品咖啡門市的 8 秒無聲循環數位看板短片。

要傳達的訊息：
- BlueLeaf 上市更新
- 因品質檢查暫時停售
- 歡迎向門市夥伴詢問今日替代優惠

視覺方向：
- 沉穩、精品、現代咖啡館風格
- 青綠與奶油白搭配柔和銅色點綴
- 動態簡潔、轉場優雅、文字大且易讀
- 適合店內螢幕播放
- 無聲
- 不使用警示圖示
- 不要過度危機化的視覺語言
```

---

## 6. 要上傳到 Knowledge 的資料

建議你把下面內容各自存成 `.md` 或 PDF 再上傳到 Foundry Knowledge。  
目前 repo 中的 `data/retail_launch_incident/documents/` 已經準備好對應 PDF，檔名維持英文，但內容已翻成繁體中文。

---

## 6A. 上傳到 `retail-store-ops-kb`

### 檔案 1：`store_incident_playbook.pdf`

```md
# 門市新品事件應變手冊

本手冊適用於新品上市期間，若產品出現安全、標示或配料處理疑慮時的門市應變。

## 事件分級規則

- 若符合以下任一條件，應列為 **第一級事件**：
  - 四小時內有兩家以上門市回報同一產品問題
  - 顧客投訴中提到疑似過敏反應
  - 門市人員無法確認批號標示是否與核准版上市資料一致

- 若符合以下條件，可列為 **第二級事件**：
  - 問題僅限單一門市
  - 沒有健康相關投訴
  - 初步判斷為門市操作失誤，而非標示錯誤

## 第一級事件的立即動作

### 前 15 分鐘
- 暫停所有已回報門市的受影響產品販售
- 將產品從前台與點餐區移除
- 保留剩餘產品與 topping sachet，等待批次確認

### 前 30 分鐘
- 移除所有上市日促銷陳列物
- 通知區經理與零售營運負責人
- 記錄批號、門市編號、值班主管姓名與大約庫存數

### 前 60 分鐘
- 升級通報給品質、零售營運與客服團隊
- 確認其他未回報門市是否也應轉為 hold status
- 下發統一店員說法，避免門市自行解讀

## 店員可使用的說法

可使用：
- 我們目前正在進行品質檢查，因此暫時停售。
- 今天可以協助您退款或更換其他品項。
- 區經理與相關團隊正在確認目前批次狀況。

不得使用：
- 這是正式召回。
- 產品不安全。
- 總部送來了有問題的貨。
- 顧客被產品傷害了。

## 重新上架條件

在品質負責人或指定事件 owner 明確批准前，不得恢復販售。
```

### 檔案 2：`shift_lead_response_guide.pdf`

```md
# 值班主管應對指引

## 若顧客已購買產品

第一線人員應：
- 冷靜致歉
- 立即停止繼續出杯
- 提供退款或替代品
- 記錄門市、時間與投訴摘要
- 若顧客提到疑似過敏，立刻升級處理

## 若顧客詢問為什麼上市宣傳物被撤下

店員應說：
- 我們正在對這項新品做暫時性的品質檢查。
- 今天我們可以協助您改選替代優惠。

不得自行推測配方、供應商或法律責任。

## 若其他未回報門市詢問是否可繼續販售

預設規則：
- 先把庫存轉為 hold status，等區經理批准
- 不要因為問題出現在別家店就繼續販售
- 至少保留一份未開封樣品供後續查核

## 店長下班前檢查清單

- 產品已移除販售
- 宣傳物已撤下
- 店員已收到統一說法
- 事件已回報區經理
- 顧客補償紀錄已完成
```

---

## 6B. 上傳到 `retail-launch-comms-kb`

### 檔案 3：`launch_campaign_brief.pdf`

```md
# BlueLeaf Sparkling Oat Latte 上市溝通簡報

## 產品定位

BlueLeaf Sparkling Oat Latte 被定位為適合都會通勤族的精品系下午咖啡飲品，主打清爽、輕盈、仍保有咖啡感的體驗。

## 品牌語氣

BlueLeaf 上市期間的語氣應該是：
- 沉穩
- 精品感
- 負責任
- 有人味
- 願意幫忙

不要使用防禦性、過度醫療化或過度戲劇化的語氣。

## 上市暫停期間的核准用語

優先使用：
- 品質檢查
- 暫時停售
- 感謝您的耐心等候
- 今日替代優惠
- 我們的門市夥伴可以協助您

除非品質或法務明確批准，避免使用：
- 不安全
- 污染
- 召回
- 健康事件
- 供應商失誤

## 視覺方向

- 主色：青綠、奶油白
- 點綴色：柔和銅色
- 風格：精品咖啡零售、乾淨字體、現代但溫暖
- 告示應能在排隊區或門市入口清楚閱讀
- 用安心、服務型語言，不要用警告式語言

## 暫時替代優惠

上市暫停期間可提供：
- 其他 oat 系飲品免費升級
- 點心兌換券
- 原品項退款

## 數位看板原則

- 以無聲循環為主
- 6 到 10 秒為佳
- 文字要大且少
- 明確留下單一 CTA：請向門市夥伴詢問今日優惠
```

### 檔案 4：`customer_message_guidelines.pdf`

```md
# 顧客訊息撰寫指引

## 櫃台說法結構

順序建議：
1. 先表達理解與不便致意
2. 說明目前正在做品質檢查
3. 給顧客一個立刻可採取的下一步

## 社群回覆原則

- 保持精簡
- 保持冷靜
- 不提未確認的根因
- 只有在需要個案追蹤時才邀請私訊

## 海報文案原則

- 標題要短且一眼可見
- 內文以兩句短句為限
- 避免法律或醫療語氣

## 影片看板原則

- 純文字也可以成立
- 螢幕上的總字數要少
- 必須在無聲情況下也能看懂
- 應該像精品服務更新，不像危機警報

## 範例語氣

感謝您的耐心等候。BlueLeaf Sparkling Oat Latte 因品質檢查暫時停售，歡迎向門市夥伴詢問今日替代優惠。
```

---

## 7. 建立兩個有 Knowledge 的 agents

這裡的重點是：**只先建立兩個 specialists**。

- 一個負責門市營運
- 一個負責品牌溝通

你可以後面再補 router / coordinator 這兩個不帶 knowledge 的 agents，專門用在 workflow。

---

## 7A. Agent 1：`retail-store-ops-agent`

### 角色定位

Store Operations Coach，專門回答：

- 現場停售與隔離
- 店員話術邊界
- 區經理 escalation
- shift-by-shift action plan

### 建議 instruction

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

### 掛載 knowledge

- `retail-store-ops-kb`

### 單 agent 測試 prompt

```text
今天上午 BlueLeaf Sparkling Oat Latte 上市後，三家門市回報與 topping sachet 標示有關的顧客投訴。請說明區經理與門市經理在前 15 分鐘與前 60 分鐘各自應做什麼。
```

---

## 7B. Agent 2：`retail-launch-comms-agent`

### 角色定位

Launch Communications Coach，專門回答：

- 對客說法
- 店員對話腳本
- 店內告示語
- 社群回覆語氣
- 視覺與數位看板方向

### 建議 instruction

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

### 掛載 knowledge

- `retail-launch-comms-kb`

### 單 agent 測試 prompt

```text
BlueLeaf Sparkling Oat Latte 因品質檢查，暫時在三家門市停售。請提供一段安全的對客櫃台說法、一版短告示文案、一則社群回覆，以及數位看板的創意方向。
```

---

## 8. Workflow 需要的另外兩個 agents

如果你在 portal workflow 裡希望每個節點都是 agent，而不是單純 prompt step，建議再建立下面兩個**不帶 knowledge**的 agents。

---

## 8A. Agent 3：`retail-incident-router-agent`

### 建議 instruction

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

---

## 8B. Agent 4：`retail-incident-coordinator-agent`

### 建議 instruction

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

## 9. Multi-agent workflow 設計

### 推薦流程

```text
User request
  -> Incident Router
  -> Store Operations Specialist
  -> Launch Communications Specialist
  -> Incident Coordinator
  -> Final response
```

### 為什麼這樣設計

- Router 先把問題拆乾淨
- Store ops 負責營運與現場處置
- Launch comms 負責對客與品牌語氣
- Coordinator 最後產出一份區經理看得懂、又能直接接到 image / video generation 的整合結果

---

## 10. Workflow 節點可複製貼上的 prompt

如果你的 workflow UI 支援變數，就保留 `{{ ... }}`。  
如果你的 workflow UI 暫時不支援，就先手動把上一個 step 的輸出貼進下一步。

### 10A. Workflow 啟動用使用者問題

```text
今天 BlueLeaf Sparkling Oat Latte 上市後，市中心三家門市回報顧客投訴，指出部分 topping sachet 疑似把杏仁糖漿標錯成一般 oat topping。請產出一份可供區經理直接採用的 recovery package，內容需包含：立即門市動作、店員話術、對客安全說法、臨時店內告示方向，以及一支 8 秒無聲數位看板概念。
```

### 10B. Router 節點 prompt

- agent：`retail-incident-router-agent`

```text
User request:
{{user_request}}

Create a handoff brief for the specialist agents.

Make sure the handoff clearly separates:
- operations questions,
- communications questions,
- final deliverables needed by the district manager.
```

### 10C. Store Operations 節點 prompt

- agent：`retail-store-ops-agent`

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

### 10D. Launch Communications 節點 prompt

- agent：`retail-launch-comms-agent`

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

### 10E. Coordinator 節點 prompt

- agent：`retail-incident-coordinator-agent`

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

## 11. 如果你想把 workflow 寫成更像 YAML 的設計稿

```yaml
workflow_name: retail-launch-incident-workflow

agents:
  router: retail-incident-router-agent
  store_ops: retail-store-ops-agent
  launch_comms: retail-launch-comms-agent
  coordinator: retail-incident-coordinator-agent

steps:
  - id: route_incident
    agent: router
    input: "{{user_request}}"

  - id: store_ops_guidance
    agent: store_ops
    input: |
      User request:
      {{user_request}}

      Router brief:
      {{route_incident.output}}

  - id: launch_comms_guidance
    agent: launch_comms
    input: |
      User request:
      {{user_request}}

      Router brief:
      {{route_incident.output}}

  - id: final_package
    agent: coordinator
    input: |
      Original user request:
      {{user_request}}

      Router brief:
      {{route_incident.output}}

      Store Operations output:
      {{store_ops_guidance.output}}

      Launch Communications output:
      {{launch_comms_guidance.output}}
```

---

## 12. Workflow 跑完後，怎麼接到 image 與 sora-2

當 Coordinator 輸出完成後，它最後應該已經包含：

- `Image-generation prompt`
- `Video-generation prompt`

你接下來可以這樣做：

1. 回到 image model，把 image prompt 直接貼進 playground
2. 回到 `sora-2`，把 video prompt 直接貼進對應 playground
3. 用一句話收斂：**我們不是先想著做圖和做影片，而是先把營運與對客決策做對，再把這份決策延伸成門市素材。**

---

## 13. 單場 demo 的建議操作順序

1. 在 `Discover / Models` 介紹 `model-router`、image model、`sora-2`
2. 在 `Build / Knowledge` 建兩個 knowledge 並上傳 PDF
3. 在 `Build / Agents` 建兩個有 knowledge 的 specialists 並各自測一次
4. 再建 `retail-incident-router-agent` 與 `retail-incident-coordinator-agent`
5. 建立 `retail-launch-incident-workflow`
6. 用 workflow 啟動問題跑一次
7. 把輸出的 image / video prompts 分別丟到 image model 與 `sora-2`

---

## 14. 現場可直接用的收尾句

```text
今天的 demo 想說明的不是 Foundry 可以 chat、search、生成圖片、生成影片，而是這些能力可以被接成一條業務可落地的回應鏈：從模型選擇、grounded specialists、workflow orchestration，到最終顧客會看到的內容，全部來自同一份 incident context。
```

---

## 15. 如果你下一步要把它搬回 repo

後續可以再把這份內容拆回：

- `data/<new_scenario>/documents/`
- `data/<new_scenario>/config/sample_questions.txt`
- `multi_agent/workflow.yaml` 的新 scenario
- `workshop/docs/01-deploy/04a-manual-experiments.md` 的 demo 段落

但第一步建議先用這份 Markdown 在 portal 裡把整條故事跑通。

## 16. 衍生產物

- 主講稿：`tmp/manual-demo-retail-portal-script.md`
- Repo-ready scenario：`data/retail_launch_incident/`
