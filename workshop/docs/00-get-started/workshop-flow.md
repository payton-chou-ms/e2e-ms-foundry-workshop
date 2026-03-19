# Workshop Flow

## Step 1: Deploy solution

Start with one of these two routes:

| Route | Use this when | Primary page |
|-------|---------------|--------------|
| **Admin deploy and share** | You are responsible for deploying Azure resources, configuring Fabric, and preparing access for others | [Admin deploy and share](../01-deploy/00-admin-deploy-share.md) |
| **Participant run and validate** | Someone already prepared the environment and you need to run the sample scenario or validate the agent | [Participant run and validate](../01-deploy/00-participant-run-validate.md) |

Both routes converge on the same sample scenario and validation steps.

The full deployment path includes:

- Deploy **Microsoft Foundry** and Azure resources (AI Services, AI Search, Storage)
- Configure **Microsoft Fabric** connection
- Configure your development environment
- See the agent working with sample data
- Takes ~15 minutes

## Step 2: Customize for your use case

Generate custom data for **each use case**:

| Customer Industry | Use Case Example | Sample Questions |
|-------------------|------------------|------------------|
| Telecommunications | Network outages + service policies | "Which outages exceeded our SLA threshold?" |
| Manufacturing | Equipment data + maintenance docs | "Which machines are overdue for maintenance per our schedule?" |
| Retail | Product catalog + return policies | "What's our return policy for electronics over $500?" |
| Finance | Account data + lending policies | "Which loan applications meet our approval criteria?" |
| Insurance | Claims data + policy documents | "What's the status of claims filed this week vs our SLA?" |
| Energy | Grid monitoring + safety protocols | "Which substations are operating above 80% capacity?" |
| **Customer X** | **Their data + Their docs** | **Their burning questions** |

!!! tip "Pre-PoC prep"
    Run Step 2 before your PoC. Enter the industry and a brief use case description. The AI generates realistic sample data, documents, and test questions tailored to your scenario.

!!! note "Single documentation source"
    Use the pages under `workshop/docs/` as the current instructions.
    Files in `guides/` and PDF outputs are distribution artifacts and may be shorter summaries.

## Step 3: Deep dive

Prepare for technical questions in customer conversations:

- **Fabric IQ**: How ontology translates business questions to SQL
- **Foundry IQ**: How agentic retrieval plans, iterates, and reflects
- **Orchestrator Agent**: How the agent decides which source to query

---

[← Get Started](index.md) | [Deploy solution →](../01-deploy/index.md)
