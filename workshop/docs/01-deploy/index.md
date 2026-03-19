# Deploy solution

This section is the entry point for getting the sample scenario running end-to-end.

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

The solution combines Microsoft Fabric and Microsoft Foundry to create an AI solution that can answer questions using both structured data and unstructured documents:

- **Microsoft Fabric** provides the data layer with Lakehouse, Warehouse, and the Fabric IQ semantic layer for natural language to SQL translation
- **Microsoft Foundry** hosts the AI agents, including Foundry IQ for document retrieval and the Orchestrator Agent that orchestrates both capabilities
- **Azure AI Services** powers the language models (GPT-4o-mini) and embeddings
- **Azure AI Search** stores document vectors for semantic retrieval

!!! tip "Stuck? Ask Copilot"
    Use GitHub Copilot Chat (`Ctrl+I`) for help with errors.

!!! note "Canonical content"
    This MkDocs tree is the canonical workshop documentation.
    Generated PDFs and site output are secondary artifacts.

---

[← Get Started](../00-get-started/workshop-flow.md) | [Admin deploy and share →](00-admin-deploy-share.md)
