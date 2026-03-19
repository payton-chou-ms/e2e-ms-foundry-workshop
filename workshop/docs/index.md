# Overview

A good PoC helps customers envision the impact of a solution on their business. It shifts the conversation from just an "interesting idea" to real "exploration". The challenge is that creating a PoC that feels relevant can take weeks of custom work. It requires infrastructure, data pipelines, integrations, and tailored scenarios that reflect their specific challenges.

This workshop helps you learn how to use solution accelerators to solve that by deploying industry-tailored scenarios quickly so you can demonstrate real value from the first conversation.

## What stays simple vs what gets deeper

The workshop runtime is intentionally simple:

- one prompt agent
- two core tools
- two grounding paths: Foundry IQ for documents and Fabric IQ for business data

But the underlying technical story now spans five axes:

| Axis | Why it matters |
|------|----------------|
| **Foundry Model** | Explains required vs optional model deployments |
| **Foundry Agent** | Explains how orchestration is created, fetched, traced, and published |
| **Foundry Tool** | Explains the strict function contract and safety boundaries |
| **Foundry IQ + Fabric IQ** | Explains how answers are grounded in documents and data |
| **Control Plane** | Explains the Azure resource topology, connections, and RBAC |

The workshop flow still emphasizes the simple runtime path first. The five-axis structure is there so you can answer technical questions once the PoC lands.

## Choose your path

This workshop supports two operating models:

| Path | Intended user | Outcome |
|------|---------------|---------|
| **Admin deploy and share** | Platform admin or solution lead | Deploy Azure resources, configure Fabric, and prepare a reusable environment for others |
| **Participant run and validate** | Solution builder, seller, or customer engineer | Use a prepared environment to validate the sample scenario and run the agent |

If one person owns the whole setup, follow the admin path first and then continue with participant validation.

## Workshop flow

| Step | Description | Time |
|------|-------------|------|
| **1. Deploy solution** | Choose either the admin path or the participant path, then configure the default scenario | ~15 min |
| **2. Customize for your use case** | Customize for a given industry and use case  | ~20 min |
| **3. Deep dive** | Technical deep dive for Q&A | ~15 min |
| **4. Cleanup** | Delete Azure resources | ~5 min |

## How to talk about the architecture

Use this progression during customer conversations:

1. Start with the business outcome: one agent answering across documents and data.
2. Explain the runtime path: one prompt agent plus two core tools.
3. Move into the five axes only when the audience wants technical depth.

That keeps the front of the workshop approachable while preserving a credible architecture story.

!!! tip "Before a PoC"
    1. Complete **Step 1** once to deploy and see it working
    2. Run **Step 2** to customize for your use case
    3. Review **Step 3** to prepare for technical questions

!!! note "Documentation source of truth"
    The canonical workshop content lives in `workshop/docs/`.
    The generated site output and any PDF artifacts should be treated as release outputs, not as separate authored content.

---

[Get Started →](00-get-started/index.md)
