# 延伸示範與快貼範例

這些都不是主流程必要步驟。只有在你要示範額外能力時才需要。

如果某支 script 印出 `SKIP:`，通常代表這個選配能力在目前環境還沒配置好。這不影響主 workshop 路徑，可以先略過。

## 可直接執行的 script

### `09_demo_content_understanding.py`

示範什麼：把本機 PDF 丟給 Azure Content Understanding，看看它怎麼轉成可讀的文件內容。

??? example "執行指令"
	```bash
	python scripts/09_demo_content_understanding.py
	```

### `10_demo_browser_automation.py`

示範什麼：讓 Foundry agent 開一個受信任的 Microsoft Learn 頁面，讀取頁面內容後回報結果。

??? example "執行指令"
	```bash
	python scripts/10_demo_browser_automation.py
	```

如果你要真的測這支 script，先看 [Browser Automation 補充設定](05d-browser-automation-setup.md)。

### `11_demo_web_search.py`

示範什麼：讓 Foundry agent 用 Web Search tool 查公開網站資訊，並附上引用來源。

??? example "執行指令"
	```bash
	python scripts/11_demo_web_search.py
	```

### `12_demo_pii_redaction.py`

示範什麼：把一小段含個資的文字送進 Azure Language，看看它怎麼偵測並遮罩 PII。

??? example "執行指令"
	```bash
	python scripts/12_demo_pii_redaction.py
	```

### `13_demo_image_generation.py`

示範什麼：呼叫 image generation API，產生一張示範圖片並存到本機。

??? example "執行指令"
	```bash
	python scripts/13_demo_image_generation.py
	```

### `16_agent_framework_workflow_example.py`

示範什麼：用新版 Microsoft Agent Framework 跑一條最小 workflow。這支 script 會建立兩個簡單 agent 並串成 `mini-policy-workflow`，適合現場快速展示 Agent Framework 的基本寫法。

??? example "執行指令"
	```bash
	python scripts/16_agent_framework_workflow_example.py
	```

??? example "安裝 preview 套件"
	```bash
	pip install --pre "agent-framework-core==1.0.0rc3" "agent-framework-azure-ai==1.0.0rc3"
	```

`1.0.0rc3` 這個版本請用 `from azure.identity.aio import DefaultAzureCredential`，而且在 `AzureAIClient(...)` 內傳 `credential=credential`；不要寫成 `async_credential=...`。

??? example "進階執行指令"
	```bash
	python scripts/16_agent_framework_workflow_example.py --question "Summarize the policy risk and next step."
	```

### `16b_agent_framework_magentic_example.py`

示範什麼：用 `MagenticBuilder` 跑 code-first 的 multi-agent orchestration。這支 script 會建立一個 manager agent 加兩個 specialist agents，適合現場展示「先規劃、再分派、最後整合」的 open-ended agent 流程。

??? example "執行指令"
	```bash
	python scripts/16b_agent_framework_magentic_example.py
	```

??? example "安裝 preview 套件"
	```bash
	pip install --pre \
	  "agent-framework-core==1.0.0rc5" \
	  "agent-framework-azure-ai==1.0.0rc5" \
	  "agent-framework-orchestrations==1.0.0b260319"
	```

這支 script 需要 `agent-framework-orchestrations`，而目前可用版本線會把 `Agent Framework` 核心套件帶到 `rc5`，所以不要沿用前面 `16` 的 `rc3` 安裝指令。

??? example "進階執行指令"
	```bash
	python scripts/16b_agent_framework_magentic_example.py --question "請為高優先客服佇列事故整理一份簡短應變包。"
	```

如果你要把 Agent Framework workflow 繼續延伸成更完整的 multi-agent 流程，再回頭看 [Multi-agent 與進階範例](05e-script-advanced.md)。

## 複製貼上範例

這一段集中放 prompt、workflow 定義和 code-first 範例。為了讓頁面好掃描，所有可直接複製的內容都改成折疊區塊。

### Visual prompt 快貼範例

如果你只是想快速測模型表現，而不是先花時間寫 prompt，下面放 6 個可直接貼用的範例。風格刻意對齊 workshop 常見場景：企業海報、產品宣傳、服務狀態更新、短影片 opening。

### Flux model prompt 快貼範例

Flux 比較適合先拿來測整體構圖、材質、光線與視覺氛圍。下面兩個 prompt 都偏向「畫面乾淨、可做海報主視覺」的方向。

??? example "Flux Prompt A"
	```text
	A premium in-store poster for a retail beverage launch, featuring a chilled sparkling oat latte in a clear glass can beside a minimal display stand, soft natural morning light, elegant neutral color palette, clean product photography, subtle reflections on the can, shallow depth of field, modern premium retail aesthetic, high detail, no watermark, no text overlay
	```

??? example "Flux Prompt B"
	```text
	A clean operations dashboard hero image for a telecom outage response center, large wall display with service health indicators, city network map glowing in amber and teal, two engineers reviewing the screen, cinematic but realistic lighting, polished enterprise control room, ultra-detailed, realistic reflections, editorial technology photography, no brand logos, no text
	```

### GPT Image prompt 快貼範例

GPT Image 比較適合描述更完整的版面需求、文字位置、設計元素與畫面用途。這兩個範例故意寫得比 Flux 更像「設計 brief」。

??? example "GPT Image Prompt A"
	```text
	Create a polished square social media campaign image for a premium coffee launch. Show a sparkling oat latte as the hero product on a light stone surface, with a soft spring window-light mood. Reserve clean negative space in the upper-left area for marketing copy. The style should feel premium, calm, modern, and safe for a retail brand. Use natural beige, silver, and muted green tones. Avoid clutter, avoid exaggerated splash effects, and avoid any visible brand text in the image itself.
	```

??? example "GPT Image Prompt B"
	```text
	Create a customer-facing service update poster for a temporary quality check in a retail store. The image should show a clean premium counter area, a discreet tabletop sign, and a reassuring, professional atmosphere. Composition should support adding a short notice headline and two short bullet lines afterward. Keep the tone calm and responsible, not dramatic. Use soft neutral lighting, premium materials, and subtle visual emphasis on trust and order. No legal imagery, no hazard tape, no alarm signals.
	```

### Sora prompt 快貼範例

Sora 這兩個範例是短影片方向。雖然目前這個 repo 沒有對應的 Sora demo script，但同一頁先放 prompt reference，方便你做現場延伸或後續自己測。

??? example "Sora Prompt A"
	```text
	A 10-second cinematic product launch video for a premium sparkling oat latte. Start with a close-up of chilled condensation on the can, then a smooth camera pull-back to reveal a bright retail counter with soft morning sunlight. End on a clean hero shot with the drink centered and subtle sparkling highlights. The mood is premium, fresh, modern, and calm. Realistic motion, realistic lighting, no visible text, no logo, no exaggerated liquid explosions.
	```

??? example "Sora Prompt B"
	```text
	A 12-second enterprise operations video showing a support response team during a service incident. Begin with a large digital wall of service metrics and a city network map, then move to a medium shot of two operators coordinating calmly, then finish on a composed wide shot of the control room returning to stable status. Tone should be credible, professional, and reassuring. Realistic office motion, subtle screen glow, no sci-fi holograms, no panic, no visible brand marks.
	```

## Microsoft Agent Service workflow 快貼範例

如果你想在 workshop 後半段順手展示一下「多個 agent 串起來會長怎樣」，下面放兩個最小可貼用的 workflow。兩個都刻意不依賴額外工具，先讓你把 workflow 跑通；之後再往裡面加 Search、Web Search 或 Browser Automation 都可以。

這兩個範例的 workflow 結構是參考官方的 declarative workflow / agent workflow 範例整理而成：

- [Declarative Workflows - Advanced patterns](https://learn.microsoft.com/agent-framework/workflows/declarative)
- [Agents in Workflows](https://learn.microsoft.com/agent-framework/workflows/agents-in-workflows)

### Workflow A: Content Pipeline

適合情境：把一段很亂的產品或活動需求，整理成可直接寄出的短公告。

建議建立三個 agent，模型都先沿用同一個 chat model 即可：

### `announcement-researcher-agent`

用途：先把原始需求拆成重點，不直接寫成最後公告。

??? example "Researcher instruction"
    ```text
    You are the Researcher Agent.

    Your job is to read a rough internal request and extract the key facts that a communications writer will need.

    Always produce:
    1. Audience
    2. Core message
    3. Constraints
    4. Missing information or assumptions

    Do not write the final announcement.
    Keep the output concise and structured.
    ```

### `announcement-writer-agent`

用途：根據前一步重點，產出第一版公告草稿。

??? example "Writer instruction"
    ```text
    You are the Writer Agent.

    Your job is to turn the research summary into a short external-facing announcement.

    Always produce:
    1. Title
    2. One-paragraph announcement
    3. Three bullet highlights

    Keep the tone clear, calm, and professional.
    Do not add facts that were not confirmed earlier.
    ```

### `announcement-editor-agent`

用途：把草稿修成可直接貼出的版本。

??? example "Editor instruction"
	```text
	You are the Editor Agent.

	Your job is to review the draft announcement and make it publication-ready.

	Always produce:
	1. Final announcement
	2. Edits made
	3. Any remaining risk or ambiguity

	Improve clarity and tone, but do not invent new facts.
	```

??? example "最小 workflow YAML"
	```yaml
	name: content-pipeline
	description: Sequential agent pipeline for announcement drafting

	kind: Workflow
	trigger:
	  kind: OnConversationStart
	  id: content_workflow
	  actions:
	    -
	      kind: InvokeAzureAgent
	      id: invoke_researcher
	      displayName: Research phase
	      conversationId: =System.ConversationId
	      agent:
	        name: announcement-researcher-agent

	    -
	      kind: InvokeAzureAgent
	      id: invoke_writer
	      displayName: Writing phase
	      conversationId: =System.ConversationId
	      agent:
	        name: announcement-writer-agent

	    -
	      kind: InvokeAzureAgent
	      id: invoke_editor
	      displayName: Editing phase
	      conversationId: =System.ConversationId
	      agent:
	        name: announcement-editor-agent
	      output:
	        autoSend: true
	```

測試時可直接貼：

??? example "測試輸入"
	```text
	We need a short public announcement for a one-day delay of our spring rewards launch.

	Audience: existing loyalty members.
	Tone: calm and helpful.
	Must mention that existing points are safe and no user action is required.
	Avoid legal language and avoid blaming any internal team.
	```

### Workflow B: Translation Review Pipeline

適合情境：把一段英文說明先翻譯成法文、再翻成西班牙文，最後再回英文做語意檢查。這個流程直接對應官方 `Agents in Workflows` 教學的 sequential pattern，只是把 agent 名稱改成比較好貼用的版本。

建議建立三個 agent：

### `french-translator-agent`

用途：把輸入翻成法文。

??? example "French translator instruction"
    ```text
    You are the French Translator Agent.

    Translate the user's text into natural French.
    Keep names, product names, URLs, and numbers unchanged unless translation is clearly required.
    Output only the translated text.
    ```

### `spanish-translator-agent`

用途：把法文內容再翻成西班牙文。

??? example "Spanish translator instruction"
    ```text
    You are the Spanish Translator Agent.

    Translate the input text into natural Spanish.
    Keep names, product names, URLs, and numbers unchanged unless translation is clearly required.
    Output only the translated text.
    ```

### `english-review-agent`

用途：把最後內容轉回英文，方便檢查意思有沒有跑掉。

??? example "English review instruction"
	```text
	You are the English Review Agent.

	Translate the input back into English and provide a short fidelity check.

	Always produce:
	1. Back-translated English
	2. Meaning drift check
	3. Terms that should stay unchanged
	```

??? example "最小 workflow YAML"
	```yaml
	name: translation-review-pipeline
	description: Sequential translation and review workflow

	kind: Workflow
	trigger:
	  kind: OnConversationStart
	  id: translation_workflow
	  actions:
	    -
	      kind: InvokeAzureAgent
	      id: invoke_french
	      displayName: Translate to French
	      conversationId: =System.ConversationId
	      agent:
	        name: french-translator-agent

	    -
	      kind: InvokeAzureAgent
	      id: invoke_spanish
	      displayName: Translate to Spanish
	      conversationId: =System.ConversationId
	      agent:
	        name: spanish-translator-agent

	    -
	      kind: InvokeAzureAgent
	      id: invoke_english_review
	      displayName: Back-translate and review
	      conversationId: =System.ConversationId
	      agent:
	        name: english-review-agent
	      output:
	        autoSend: true
	```

測試時可直接貼：

??? example "測試輸入"
	```text
	Our support portal will be under scheduled maintenance on Saturday from 02:00 to 04:00 UTC.
	Customers can still submit urgent cases by phone.
	Do not translate the product name Contoso Care.
	```

## Agent Framework multi-agent 範例（Magentic pattern）

如果你要展示的是 code-first 的 multi-agent，而不是前面的 declarative workflow，可以用 Microsoft Agent Framework 的 Magentic orchestration。這個 pattern 的重點不是固定流程順序，而是由一個 manager 先規劃，再動態決定下一步要叫哪個 specialist agent。

這一段是參考官方的 Magentic orchestration 範例整理成 workshop 版：

- [Microsoft Agent Framework Workflows Orchestrations - Magentic](https://learn.microsoft.com/agent-framework/workflows/orchestrations/magentic)
- [AI agent orchestration patterns - Magentic orchestration](https://learn.microsoft.com/azure/architecture/ai-ml/guide/ai-agent-design-patterns#magentic-orchestration)

!!! note "什麼時候用 Magentic"
    這個 pattern 比 sequential 更適合 open-ended 任務：先規劃、再分派、過程中可能重排步驟或回頭補資料。
    如果你的流程本來就是固定順序，前面的 `content-pipeline` 那種 sequential 反而更簡單。

### 範例情境

適合情境：客服主管看到某個排隊佇列突然爆量，想快速得到一份「先處理什麼、對客怎麼說、哪些風險要升級」的最小應變方案。

這個例子刻意保持簡單，只放一個 manager 和兩個 specialists：

### `triage-manager-agent`

用途：規劃要先查什麼、先問哪個 specialist、什麼時候該結案。

??? example "Manager instruction"
    ```text
    You are the triage manager for a support queue incident.

    Your job is to break the task into the smallest useful subtasks, decide which specialist should act next, and track whether the user's request has been fully answered.

    Priorities:
    - First understand the operational issue.
    - Then request a customer-safe communication draft.
    - Stop once the user has a complete and practical response package.

    Do not do all specialist work yourself if another agent is better suited.
    ```

### `queue-ops-agent`

用途：整理營運面判斷，例如 queue 爆量時先看什麼、先做什麼。

??? example "Queue operations instruction"
    ```text
    You are the queue operations specialist.

    Focus on:
    - likely operational causes,
    - immediate triage actions,
    - what to verify in the next 15 minutes,
    - what conditions should trigger escalation.

    Keep the answer concise and action-oriented.
    ```

### `customer-comms-agent`

用途：把營運處置轉成對客與對內都能直接用的說法。

??? example "Customer communications instruction"
	```text
	You are the customer communications specialist.

	Convert the incident context into:
	- a short customer-facing explanation,
	- a support-agent talking point,
	- a short status-page update.

	Keep the tone calm, factual, and reassuring.
	Do not promise timelines unless they are explicitly provided.
	```

### 對應 script

這個 code-first 範例現在已經落成 repo 內的 [scripts/16b_agent_framework_magentic_example.py](/Users/payton/work/01_lab/e2e-ms-foundry-workshop/scripts/16b_agent_framework_magentic_example.py)。它沿用官方 `MagenticBuilder`，但把角色和預設問題改成比較適合 workshop 展示的 queue triage 場景，並且改成 `AzureAIClient` + `DefaultAzureCredential` 的新版寫法。

如果你要看最小結構，重點就是三個角色：

- `triage-manager-agent`
- `queue-ops-agent`
- `customer-comms-agent`

以及一個 `MagenticBuilder(participants=[...], manager_agent=...)`。

測試時可直接貼：

??? example "測試輸入"
	```text
	Our premium support queue is suddenly 4x above normal volume after a portal release.
	We need a concise response package for the operations lead and frontline support team.
	Include immediate triage actions, the next 15-minute checks, escalation triggers, and a safe customer-facing message.
	```

---

[← 腳本用途與執行順序](05-script-sequence.md) | [Browser Automation 補充設定 →](05d-browser-automation-setup.md)