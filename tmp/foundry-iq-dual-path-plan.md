# Foundry IQ Dual-Path Implementation Plan

## Goal

Keep the current local-tools agent flow intact, while adding a second Foundry-native knowledge flow that works naturally inside Microsoft Foundry and is easier for learners to understand in the portal.

## Design Summary

The repo should support two distinct agent paths.

### Path A: Local Tools Orchestrator

This is the current path and should remain supported.

- Uses local function tools
- Uses Azure AI Search for document retrieval
- Uses Fabric SQL for structured data
- Uses local runtime orchestration in `08_test_foundry_agent.py`
- Best for mixed document + data questions

Files kept as-is in this path:

- `scripts/06_upload_to_search.py`
- `scripts/07_create_foundry_agent.py`
- `scripts/08_test_foundry_agent.py`

### Path B: Foundry-Native Knowledge Agent

This is the new path to add.

- Uses Azure AI Search knowledge source and knowledge base
- Uses a Foundry MCP tool connection to `knowledge_base_retrieve`
- Creates a Foundry-native agent for document-based IQ
- Supports direct use from the Foundry portal
- Best for learner-facing Foundry IQ walkthroughs and manual portal experiments

Files to add for this path:

- `scripts/06b_upload_to_foundry_knowledge.py`
- `scripts/07b_create_foundry_iq_agent.py`
- `scripts/08b_test_foundry_iq_agent.py`

## Current Implementation Direction

The repo now uses preview Azure AI Search knowledge-base APIs for the Foundry IQ path.

- `azure-search-documents==11.7.0b2` provides `KnowledgeBase` and `create_or_update_knowledge_base`
- `06b` now provisions a Search knowledge source, a knowledge base, and a Foundry project connection
- `07b` now creates the agent with `MCPTool(..., allowed_tools=["knowledge_base_retrieve"])`

## Why Two Paths Instead of One

The current `07_create_foundry_agent.py` is a local-tools design, not a fully Foundry-managed knowledge-agent design.

- The current path stores tool schemas in the agent definition
- Tool execution happens in local Python code, not inside Foundry-hosted tool runtime
- Azure AI Search is queried by local code, not by attaching a Foundry-native knowledge asset

Trying to force both models into one script would make the code harder to reason about and make learner documentation more confusing.

The cleaner design is:

- keep the current path for orchestration and mixed-tool demos
- add a separate Foundry-native path for portal-first knowledge demos

## Recommended File and Metadata Layout

Each scenario should continue to store generated metadata under `data/<scenario>/config/`.

### Existing Metadata Kept

- `ontology_config.json`
- `schema_prompt.txt`
- `search_ids.json`
- `agent_ids.json`

### New Metadata to Add

- `knowledge_ids.json`
- `foundry_iq_agent_ids.json`

### Recommended Contract: `knowledge_ids.json`

```json
{
  "knowledge_type": "azure_search_knowledge_base",
  "search_index_name": "telecom-documents",
  "knowledge_source_name": "telecom-foundry-iq-source",
  "knowledge_base_name": "telecom-foundry-iq-kb",
  "project_connection_id": "<project-connection-id>",
  "mcp_endpoint": "https://<search>.search.windows.net/knowledgebases/<kb>/mcp?api-version=2025-11-01-preview",
  "source_folder": "data/.../documents",
  "status": "ready"
}
```

### Recommended Contract: `foundry_iq_agent_ids.json`

```json
{
  "agent_name": "telecom-foundry-iq-agent",
  "agent_id": "<agent-id>",
  "knowledge_base_name": "telecom-foundry-iq-kb",
  "project_connection_id": "<project-connection-id>"
}
```

## Script Responsibilities

### `06_upload_to_search.py`

Keep current responsibility:

- create/update Azure AI Search index
- upload PDF chunks
- save `search_ids.json`

### `06b_upload_to_foundry_knowledge.py`

New responsibility:

- ensure the Search index exists and contains the current workshop documents
- create or update a Search knowledge source
- create or update a Search knowledge base
- create or update a Foundry project connection for the knowledge-base MCP endpoint
- save `knowledge_ids.json`

This script should not create agents.

### `07_create_foundry_agent.py`

Keep current responsibility:

- create local-tools orchestrator agent
- register function-tool schemas
- use current instructions pattern
- save `agent_ids.json`

### `07b_create_foundry_iq_agent.py`

New responsibility:

- read `ontology_config.json`
- read `knowledge_ids.json`
- create a Foundry-native document IQ agent
- attach Foundry `MCPTool`
- save `foundry_iq_agent_ids.json`

Its instructions should focus on document-based answering and citations, not local function tools.

### `08_test_foundry_agent.py`

Keep current responsibility:

- load current agent tools
- intercept `function_call`
- execute local SQL and Search functions
- send `function_call_output` back to the model

### `08b_test_foundry_iq_agent.py`

New responsibility:

- invoke the Foundry-native IQ agent directly
- display answer and citations
- avoid local function execution loop

## Naming Rules

To avoid confusion, the two agent paths should not reuse the same agent name.

### Current Path Naming

- `{SOLUTION_NAME}-agent`

### New Foundry-Native Naming

- `{SOLUTION_NAME}-foundry-iq-agent`

This makes it obvious in the portal which agent belongs to which path.

## Build Orchestration Strategy

`00_build_solution.py` should remain usable for current workshop flows.

Recommended direction:

- keep current default behavior unchanged
- add an explicit Foundry-native IQ path later, instead of replacing current steps
- avoid making first-time learners choose among too many flags up front

Possible future options:

- add explicit flags such as `--foundry-native-iq`
- add a separate helper script for the Foundry-native path
- document both routes clearly before exposing both in the default learner flow

## Learner Documentation Strategy

Documentation should optimize for clarity first, not completeness first.

### Principle 1: Teach Choice Before Internals

Learners should first see:

1. I want document Q&A only
2. I want document + data Q&A
3. I want to test directly in the Foundry portal

Do not start with implementation details like `FunctionTool`, `AI Search index`, or `knowledge asset`.

### Principle 2: One Page, One Job

- Build page: commands and expected outcome only
- Manual experiment page: portal steps only
- Script reference pages: script purpose and when to use them
- Deep dive pages: explain architectural differences and tradeoffs

### Principle 3: Use Clear Path Names

Suggested learner-facing names:

- `Path A: Foundry IQ + Fabric IQ`
- `Path B: Foundry IQ in the Foundry portal`

Avoid exposing internal wording like `local-tool orchestrator` on first-contact learner pages.

### Principle 4: Use Comparison Tables

One simple table can explain the difference better than several paragraphs.

Suggested columns:

- What it answers
- Where you test it
- Whether it uses Fabric
- Whether it appears as Foundry knowledge in the portal
- Which scripts to run

## Implementation Order

The safest order is:

1. Define metadata contracts
2. Add `06b_upload_to_foundry_knowledge.py`
3. Add `07b_create_foundry_iq_agent.py`
4. Add `08b_test_foundry_iq_agent.py`
5. Update orchestration entry points
6. Update learner docs
7. Validate both paths end to end

## Work Items

- [x] Define dual agent architecture
- [ ] Design knowledge metadata contract
- [ ] Add Foundry-native ingestion path
- [ ] Add Foundry-native agent path
- [ ] Add Foundry-native test path
- [ ] Update build orchestration
- [ ] Revise learner documentation
- [ ] Validate end-to-end flows

## Out of Scope for the First Increment

- Replacing the current `07_create_foundry_agent.py`
- Merging both runtime models into one script
- Rewriting all learner docs before the new path works end to end

## Next Step

The next implementation step should be to formalize `knowledge_ids.json` and then scaffold `06b_upload_to_foundry_knowledge.py`.