# Participant run and validate

Use this route when an admin or solution lead already prepared the Azure and Fabric environment for you.

## Audience

- Workshop participant
- Solution builder
- Customer engineer
- Technical seller validating the sample scenario

## What this route covers

1. Sign in with the assigned identity.
2. Open the repo and configure your local environment.
3. Validate the sample scenario.
4. Test the agent.

## What you should already have from the admin

- Access to the Azure subscription or prepared resources you need to use.
- Access to the Fabric workspace.
- The correct `FABRIC_WORKSPACE_ID`.
- Confirmation of whether the admin already ran the sample build.

## Recommended sequence

### 1. Verify sign-in and workspace access

Confirm you can authenticate to the right Azure tenant and open the target Fabric workspace.

If you cannot access the workspace or Azure resources, stop here and ask the admin to grant access before continuing.

### 2. Configure your local environment

Follow [Configure dev environment](03-configure.md).

At minimum, your `.env` should contain the shared `FABRIC_WORKSPACE_ID` and the expected `DATA_FOLDER`.

### 3. Run the sample scenario

Follow [Build solution](04-run-scenario.md).

Choose the right starting point:

- If the admin deployed infrastructure but did not run the build, run the documented sample build flow.
- If the admin already completed the sample build, you can usually move directly to the test step.

### 4. Validate the agent behavior

Run the sample questions and confirm you can test:

- Structured data questions
- Document questions
- Combined questions that use both data sources

## What this route does not cover

- Provisioning Azure resources from scratch
- Creating the Fabric workspace from scratch
- Granting Azure RBAC to other users
- Sharing the environment with additional participants

Use [Admin deploy and share](00-admin-deploy-share.md) for those tasks.

## Next step after validation

Once the sample scenario works, continue to [Customize for your use case](../02-customize/index.md).

---

[← Admin deploy and share](00-admin-deploy-share.md) | [Configure dev environment →](03-configure.md)