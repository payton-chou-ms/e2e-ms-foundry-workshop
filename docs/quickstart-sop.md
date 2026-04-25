# Foundry Lab

## Reference

- Download: https://github.com/payton-chou-ms/e2e-ms-foundry-workshop
- Doc: https://payton-chou-ms.github.io/e2e-ms-foundry-workshop/
- Microsoft Foundry: https://ai.azure.com/

## SOP

### 1. Deploy infra

Ref: https://payton-chou-ms.github.io/e2e-ms-foundry-workshop/01-deploy/01-deploy-azure.html

```bash
az login --tenant <TENANT_ID> --use-device-code
az account set --subscription <SUBSCRIPTION_ID>
azd auth login --tenant-id <TENANT_ID> --use-device-code
azd up
```

### 2. Test and validate

Ref: https://payton-chou-ms.github.io/e2e-ms-foundry-workshop/01-deploy/00-participant-run-validate.html

```bash
python scripts/admin_prepare_shared_demo.py
python scripts/participant_validate_docs.py
```

### 3. Live tour

Ref: https://payton-chou-ms.github.io/e2e-ms-foundry-workshop/01-deploy/04a-manual-experiments.html

Sample agent:

```text
udajw4-telco-iq
```

Sample questions:

```text
reply in zhtw

Which outage events exceeded our maximum duration policy?
What is the escalation procedure for high-impact outages?
Which open trouble tickets are linked to outages still under monitoring?
How many affected customers were involved in high-impact fiber outages?
When must customer updates be issued during a major outage?
```

### 4. Demo scripts

```bash
python scripts/09_demo_content_understanding.py
python scripts/12_demo_pii_redaction.py
```

### 5. Deploy gpt-image-1.5 and gpt-image-2

TBC

### 6. Agent Framework workflow example

```bash
python scripts/16_agent_framework_workflow_example.py
# pip install --pre "agent-framework-core==1.0.0rc3" "agent-framework-azure-ai==1.0.0rc3"
```

### 7. Retail launch incident manual demo

Ref: https://payton-chou-ms.github.io/e2e-ms-foundry-workshop/02-customize/04-retail-manual-demo.html

#### 7.1 Create `retail-store-ops-agent`

Upload data and CSV:

| File | Agent |
| --- | --- |
| `data/retail_launch_incident/documents/ops-store-incident-playbook.pdf` | `retail-store-ops-agent` |
| `data/retail_launch_incident/documents/ops-shift-lead-response-guide.pdf` | `retail-store-ops-agent` |
| `data/retail_launch_incident/tables/launch_incidents.csv` | `retail-store-ops-agent` |
| `data/retail_launch_incident/tables/store_response_actions.csv` | `retail-store-ops-agent` |

Instruction:

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

Sample question:

```text
今天上午 BlueLeaf Sparkling Oat Latte 上市後，三家門市回報與 topping sachet 標示有關的顧客投訴。請說明區經理與門市經理在前 15 分鐘與前 60 分鐘各自應做什麼。
```

#### 7.2 Create `retail-launch-comms-agent`

Upload data and CSV:

| File | Agent |
| --- | --- |
| `data/retail_launch_incident/documents/comms-launch-campaign-brief.pdf` | `retail-launch-comms-agent` |
| `data/retail_launch_incident/documents/comms-customer-message-guidelines.pdf` | `retail-launch-comms-agent` |
| `data/retail_launch_incident/tables/launch_incidents.csv` | `retail-launch-comms-agent` |
| `data/retail_launch_incident/tables/store_response_actions.csv` | `retail-launch-comms-agent` |

Instruction:

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

Sample question:

```text
BlueLeaf Sparkling Oat Latte 因品質檢查，暫時在三家門市停售。請提供一段安全的對客櫃台說法、一版短告示文案、一則社群回覆，以及門市海報的創意方向。
```

#### 7.3 Create `retail-incident-router-agent`

Instruction:

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

Sample question:

```text
今天 BlueLeaf Sparkling Oat Latte 上市後，市中心三家門市回報顧客投訴，指出部分 topping sachet 疑似把杏仁糖漿標錯成一般 oat topping。

請不要直接給最終處置方案，而是先整理成一份 handoff brief，提供給 operations specialist 與 communications specialist 使用。

這份 brief 必須清楚區分：
- 事件摘要
- 營運面需要回答的問題
- 對客溝通面需要回答的問題
- 最後要交付給區經理的成果項目
```

#### 7.4 Create `retail-incident-coordinator-agent`

Instruction:

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

Sample question:

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

#### 7.5 Create workflow

```yaml
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

Test workflow:

```text
今天 BlueLeaf Sparkling Oat Latte 上市後，市中心三家門市回報顧客投訴，指出部分 topping sachet 疑似把杏仁糖漿標錯成一般 oat topping。請產出一份可供區經理直接採用的 recovery package，內容需包含：立即門市動作、店員話術、對客安全說法、臨時店內告示方向，以及一版門市海報的視覺方向。
```