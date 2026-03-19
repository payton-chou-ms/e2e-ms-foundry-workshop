# Customer Documentation Audit

## Purpose

This note consolidates three decisions for this repository:

1. Define a single customer-facing documentation structure.
2. Identify Azure and Fabric permission gaps for an admin-predeployed shared environment.
3. Record where PDF and website content overlap or drift.

## Current Documentation Topology

### Source files

- `workshop/docs/`: Markdown source for the workshop website.
- `workshop/mkdocs.yml`: Navigation and site configuration for the workshop website.
- `guides/deployment_guide.md`: Separate Markdown quick-start guide.
- `scripts/generate_deployment_guide.py`: Hand-authored PDF generator for `guides/deployment_guide.pdf`.
- `scripts/generate_workshop_guide.py`: Hand-authored PDF generator for `guides/workshop_guide.pdf`.

### Generated outputs

- `workshop/site/`: Local MkDocs build output.
- `site/`: GitHub Pages workflow output when `mkdocs build --site-dir ../site` is used.
- `guides/deployment_guide.pdf`: Generated from Python, not from Markdown.
- `guides/workshop_guide.pdf`: Generated from Python, not from Markdown.
- `docs/Foundry_IQ_Fabric_IQ_Workshop_Guide.pdf`: Existing PDF artifact with no current generator path in code.

## Recommended Customer Documentation Architecture

### Single source of truth

Use `workshop/docs/` as the only authored customer documentation source.

Why:

- It already contains the full information architecture.
- It is versionable, reviewable, and deployable to HTML.
- It avoids duplicating step content in Markdown and Python PDF scripts.

### Role of each folder going forward

| Path | Recommended role | Edit manually? |
| --- | --- | --- |
| `workshop/docs/` | Canonical customer and partner-facing content | Yes |
| `workshop/site/` | Local build artifact only | No |
| `site/` | CI/CD deployment artifact only | No |
| `guides/` | Distribution artifacts only: quick start PDF, workshop PDF, review notes | Prefer no for generated files |
| `docs/` | Remove or repurpose; do not keep orphaned PDFs here | No |

### Audience split

To make the material customer-ready, organize `workshop/docs/` by audience and task instead of by authoring history.

Suggested structure:

- `00-overview/`
  - Business outcome, architecture summary, prerequisites.
- `01-admin-deploy/`
  - Azure deployment, Fabric setup, tenant prerequisites, sharing model.
- `02-user-run/`
  - How a workshop participant or customer engineer uses the prepared environment.
- `03-customize/`
  - How to generate a customer scenario and rebuild the solution.
- `04-operate/`
  - Validation, troubleshooting, cleanup, next steps.

### Output policy

Recommended publication flow:

1. Author content in `workshop/docs/`.
2. Build HTML with MkDocs.
3. If PDF is needed, export from the same Markdown source.
4. Treat `guides/*.pdf` as release artifacts, not separate authored content.

### Recommended cleanup

- Keep one workshop PDF artifact name.
- Keep one deployment quick-start artifact name.
- Remove or archive duplicate PDF files under `guides/` and `docs/`.
- Standardize on one site output location for documentation builds.

## Admin Predeployment and Sharing Model

### What the current repo supports well

- One deployer provisions Azure resources with `azd up`.
- The same deployer configures a Fabric workspace by setting `FABRIC_WORKSPACE_ID`.
- The same signed-in identity runs the scripts locally to create Fabric items, load data, create the Foundry agent, and test the solution.

### What the current repo does not automate

- Sharing Azure runtime access with additional users.
- Sharing Fabric workspace access with additional users.
- Assigning Azure RBAC to a group instead of only the deploying user.
- A shared web application for end users who do not run the scripts locally.

### Azure permissions already configured in code

The infrastructure creates Azure role assignments in `infra/modules/foundry.bicep` for:

- AI Project managed identity.
- AI Search managed identity.
- Deploying user.

Current user-scoped assignments include:

- Cognitive Services User.
- Azure AI User.
- Search Index Data Contributor.
- Search Service Contributor.
- Storage Blob Data Contributor.

Important limitation:

- These assignments are granted to `deployingUserPrincipalId`, not to a reusable Entra group.
- A new user will not automatically inherit the same access after admin deployment.

### Permission gap for deployment itself

The docs currently describe Azure prerequisites as Contributor access, but the Bicep template deploys `Microsoft.Authorization/roleAssignments` resources.

Implication:

- The deploying identity typically needs permission to create role assignments, which is broader than plain Contributor.
- In practice this usually means `Owner`, `User Access Administrator`, or an equivalent custom role with `Microsoft.Authorization/roleAssignments/write`.

This is the biggest Azure permission gap between the written prerequisites and the actual deployment behavior.

### Fabric permissions assumed by scripts

The Fabric scripts use the signed-in Azure identity directly and assume that identity already has sufficient Fabric workspace rights.

Current assumptions:

- Workspace exists already.
- Workspace has Fabric capacity assigned.
- Current user can create Lakehouse, Ontology, Data Agent, and load data.

The repo docs explicitly mention workspace admin permissions, and the scripts do not provision Fabric access for other users.

### Minimum sharing scenarios to decide between

#### Scenario A: Admin deploys, only one operator runs scripts

This is the current best-supported model.

Needed:

- Admin or operator with Azure deployment rights.
- Same operator with Fabric workspace admin or equivalent authoring rights.
- No extra user sharing automation required.

#### Scenario B: Admin deploys, several engineers run scripts and tests

Additional gaps to close:

- Azure RBAC must be assigned to a group or to each additional engineer.
- Fabric workspace access must be granted to each engineer.
- Additional engineers need access to the Foundry project, Search index, and any required data endpoints.

Recommended Azure group-based sharing targets:

- Azure AI User or equivalent runtime access for the Foundry project.
- Search index reader or contributor depending on whether users only query or also build indexes.
- Storage access only if they need to upload or manage documents.

Recommended Fabric sharing targets:

- Workspace role sufficient to query and manage the Lakehouse and Data Agent.
- Clear separation between authors and read-only consumers if customer users are not expected to rebuild the environment.

#### Scenario C: Admin deploys, customer end users only consume the solution

This repo does not fully package that model today.

Missing pieces:

- A shared application endpoint or UI for users who do not run local scripts.
- Centralized app authentication and authorization.
- Operational guidance for user onboarding.

### Recommended permission model for customer-ready sharing

| Persona | Azure | Fabric | Notes |
| --- | --- | --- | --- |
| Platform admin | Owner or User Access Administrator plus deployment rights | Fabric admin or workspace admin | Needed to deploy and assign RBAC |
| Solution operator | Azure AI runtime access, Search access, Storage access only if needed | Workspace authoring access | Runs scripts and refreshes scenarios |
| Customer viewer | Prefer app-level access, not direct Azure resource access | Prefer app-level or workspace viewer access | Avoid giving raw infra permissions unless necessary |

## PDF and Website Overlap

### Same information currently maintained in multiple places

| Topic | Website source | Other source |
| --- | --- | --- |
| Azure deployment with `azd up` | `workshop/docs/01-deploy/01-deploy-azure.md` | `guides/deployment_guide.md`, `scripts/generate_deployment_guide.py`, `README.md` |
| Fabric workspace setup | `workshop/docs/01-deploy/02-setup-fabric.md` | `guides/deployment_guide.md` |
| `.env` setup and `FABRIC_WORKSPACE_ID` | `workshop/docs/01-deploy/03-configure.md` | `guides/deployment_guide.md`, `README.md` |
| Build pipeline command | `workshop/docs/01-deploy/04-run-scenario.md` | `guides/deployment_guide.md`, `README.md`, `scripts/generate_workshop_guide.py` |
| Sample questions | `workshop/docs/01-deploy/04-run-scenario.md` | `guides/deployment_guide.md`, `scripts/generate_deployment_guide.py`, `scripts/generate_workshop_guide.py` |

## Current Inconsistencies and Stale References

### Critical

1. `scripts/generate_deployment_guide.py` still points to the old repository slug in the clone command and footer.
2. The written prerequisite says Contributor access, but the infrastructure performs RBAC role assignments.

### Medium

1. `scripts/generate_workshop_guide.py` docstring still describes an output under `docs/`, while the implementation writes to `guides/workshop_guide.pdf`.
2. Local docs build output is described as `workshop/site/`, while the GitHub Pages workflow writes to root `site/`.
3. `guides/deployment_guide.md` and `scripts/generate_deployment_guide.py` are two separate sources for the same deployment handout.

### Low

1. There are multiple PDF artifacts with overlapping purpose:
   - `guides/workshop_guide.pdf`
   - `guides/Foundry_IQ_Fabric_IQ_Workshop_Guide.pdf`
   - `docs/Foundry_IQ_Fabric_IQ_Workshop_Guide.pdf`
   - `guides/deployment_guide copy.pdf`
2. The website content is modular, but the PDF scripts restate the same instructions as standalone prose, which increases maintenance cost.

## Recommended Consolidation Plan

### Phase 1: Freeze the source of truth

- Treat `workshop/docs/` as canonical.
- Stop adding new authored content to Python PDF generators.
- Mark `guides/` as generated or review-only artifacts.

### Phase 2: Align the audience model

- Add a dedicated admin deployment page.
- Add a dedicated participant or customer user page.
- State clearly whether a step is for platform admins, solution builders, or viewers.

### Phase 3: Simplify distribution artifacts

- Keep one quick-start PDF.
- Keep one full workshop PDF.
- Remove duplicates and stale PDF names.
- Either generate PDF from Markdown or clearly accept that PDFs are secondary artifacts with manual sync cost.

### Phase 4: Make sharing explicit

- Document the Azure roles needed for deployment.
- Document the Azure roles needed for collaborative operation.
- Document the Fabric roles needed for authoring versus consumption.
- If shared end-user usage is a goal, add an application delivery path instead of relying on local scripts.

## Recommended Next Action

If this repo is intended for customer delivery, the next most valuable change is to rewrite `workshop/docs/01-deploy/` into two tracks:

- `Admin deploy and share`
- `Participant run and validate`

That change will remove the main ambiguity in the current workshop flow.