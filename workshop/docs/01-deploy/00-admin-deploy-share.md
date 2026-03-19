# Admin deploy and share

Use this route when one person or team is responsible for deploying the solution and preparing it for others.

## Audience

- Platform admin
- Solution lead
- Workshop host
- Technical seller preparing a repeatable demo environment

## What this route covers

1. Deploy Azure resources.
2. Create or select the Fabric workspace.
3. Configure the shared environment.
4. Run the sample scenario once.
5. Share the prepared environment with operators or participants.

## Before you start

Make sure you have:

- Azure deployment rights for the subscription and resource group.
- Permission to create Azure role assignments if you are using the provided Bicep templates.
- Fabric workspace admin or equivalent authoring rights.
- Required model capacity and quota for the selected Azure region.

!!! warning "Contributor may not be sufficient"
    The infrastructure creates Azure RBAC role assignments.
    In many subscriptions, the deploying identity needs `Owner`, `User Access Administrator`, or another role that includes `Microsoft.Authorization/roleAssignments/write`.

## Recommended sequence

### 1. Deploy Azure resources

Follow [Deploy Azure resources](01-deploy-azure.md).

### 2. Create or choose the Fabric workspace

Follow [Create Fabric workspace](02-setup-fabric.md).

### 3. Configure the shared environment

Follow [Configure dev environment](03-configure.md).

At this stage, capture the values that downstream users will need, especially:

- `FABRIC_WORKSPACE_ID`
- Any environment naming convention you want participants to reuse
- Which identity or group should be granted Azure and Fabric access

### 4. Build and validate the default scenario

Follow [Build solution](04-run-scenario.md).

Run the default scenario once before sharing it. This confirms that:

- Azure resources are healthy
- Fabric items can be created
- Documents are indexed
- The orchestrator agent answers sample questions

### 5. Share with participants or operators

The current repo does not automate all collaboration steps. Before handing off the environment, decide:

- Who can only run tests
- Who can rebuild data or customize scenarios
- Who can manage Azure resources and Fabric artifacts

Minimum handoff checklist:

- Grant Azure access to the required users or groups.
- Grant Fabric workspace access to the required users.
- Share the required local configuration values.
- Tell participants whether they should only validate the sample scenario or also run customization steps.

## What to share with the next user

- The repository URL
- The expected sign-in identity or tenant
- The `FABRIC_WORKSPACE_ID`
- Whether they should start from [Participant run and validate](00-participant-run-validate.md) or from a later customization page

## When this route is complete

You are done when another user can open the repo, sign in, and run the sample validation flow without redoing the Azure deployment.

---

[← Deploy overview](index.md) | [Participant run and validate →](00-participant-run-validate.md)