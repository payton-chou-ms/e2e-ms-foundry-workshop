# Deploy Infrastructure

!!! info "Primary audience"
    This page is mainly for the **Admin deploy and share** route.
    If someone already prepared the environment for you, start with [Participant run and validate](00-participant-run-validate.md) instead.

## Clone the Repository

```bash
git clone https://github.com/nchandhi/nc-iq-workshop.git
cd nc-iq-workshop
```

## Login to Azure

```bash
azd auth login
```

This opens a browser for authentication.

!!! warning "Deployment permissions"
    This repository deploys Azure role assignments as part of the infrastructure.
    If `azd up` fails during RBAC creation, confirm that your identity can create role assignments in the target scope.

## Deploy Resources

```bash
azd up
```

Follow the prompts to select your environment name, subscription, and location etc.

!!! warning "Wait for Completion"
    Deployment takes 7-8 minutes. Don't proceed until you see the success message.

## Verify Deployment

Verify in [Azure Portal](https://portal.azure.com/) that your resource group contains all resources:

- Microsoft Foundry
- Azure AI Search
- Storage Account
- Application Insights

## Environment Variables

After deployment, Azure endpoints are automatically saved to `.azure/<env>/.env` and loaded by the scripts.

!!! note "No Manual Configuration"
    You don't need to manually set Azure connection strings. The scripts read them from the azd environment automatically.

---

[← Admin deploy and share](00-admin-deploy-share.md) | [Create Fabric workspace →](02-setup-fabric.md)
