# Deploy solution

This section is the entry point for getting the sample scenario running end-to-end.

The deployment path stays focused on the minimum needed for a working PoC, but the architecture you are deploying now supports the broader five-axis technical story used in the Deep Dive section.

## Pick the route that matches your role

### Admin deploy and share

Use this route if you are preparing the environment for a team, customer, or workshop participants.

You will:

- Deploy Azure resources with `azd up`
- Create or choose the Fabric workspace
- Configure the shared environment
- Decide what access other users need
- Hand off a ready-to-use environment

[Go to Admin deploy and share](00-admin-deploy-share.md)

### Participant run and validate

Use this route if Azure resources and the Fabric workspace are already prepared for you.

You will:

- Open the repo and sign in with your assigned identity
- Configure local settings
- Run the sample scenario
- Test the orchestrator agent and validate outputs

[Go to Participant run and validate](00-participant-run-validate.md)

## Architecture

<!-- TODO: Add architecture diagram image here -->
![Architecture Diagram](../assets/architecture.png)

The solution combines Microsoft Fabric and Microsoft Foundry to create an AI solution that can answer questions using both structured data and unstructured documents.

At deployment time, it helps to think in two layers:

### Main workshop path

- a prompt agent in Foundry
- a SQL tool for structured data
- a document-search tool for unstructured knowledge
- Foundry IQ and Fabric IQ as the two grounding paths

### Five-axis architecture behind the path

| Axis | Deployment implication |
|------|------------------------|
| **Foundry Model** | Required chat + embedding deployments, with optional model extensions kept separate |
| **Foundry Agent** | A project-scoped agent definition is created and later reused at runtime |
| **Foundry Tool** | The runtime depends on a strict SQL + search function contract |
| **Foundry IQ + Fabric IQ** | Search and Fabric resources ground the agent in documents and data |
| **Control Plane** | Azure AI Services, Foundry project, Search, Storage, telemetry, and RBAC wire the whole environment together |

In other words, the user experience still feels like one conversational PoC, but the deployment prepares the full technical scaffolding that supports it.

- **Microsoft Fabric** provides the data layer with Lakehouse, Warehouse, and the Fabric IQ semantic layer for natural language to SQL translation
- **Microsoft Foundry** hosts the prompt agent, the tool contract, and Foundry IQ document retrieval
- **Azure AI Services** powers the chat and embedding model deployments used by the workshop
- **Azure AI Search** stores document vectors for semantic retrieval
- **Application Insights** can optionally receive tracing when observability is enabled

!!! tip "Stuck? Ask Copilot"
    Use GitHub Copilot Chat (`Ctrl+I`) for help with errors.

!!! note "Canonical content"
    This MkDocs tree is the canonical workshop documentation.
    Generated PDFs and site output are secondary artifacts.

---

[← Get Started](../00-get-started/workshop-flow.md) | [Admin deploy and share →](00-admin-deploy-share.md)
