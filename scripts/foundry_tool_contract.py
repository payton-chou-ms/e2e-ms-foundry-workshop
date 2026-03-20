"""Canonical tool contract for the Foundry agent and local runtime.

This module keeps the tool schema, responsibility boundaries, and execution
loop in one place so agent creation and local testing do not drift.
"""

from copy import deepcopy


DEFAULT_SEARCH_TOP = 3
MAX_SEARCH_TOP = 10
SQL_RESULT_ROW_LIMIT = 50

TOOL_EXECUTION_LOOP = [
    "Inspect the user question and decide whether structured data, documents, or both are required.",
    "Emit one or more function calls with only the parameters defined in the tool schema.",
    "Have the local runtime execute each function call and send the raw output back as function_call_output.",
    "Synthesize the final answer from the tool outputs and explain when a source is unavailable.",
]

TOOL_CONTRACT_ROWS = [
    {
        "name": "execute_sql",
        "mode": "full",
        "use_for": "Counts, totals, trends, rankings, joins, and record lookup in Fabric tables.",
        "avoid_for": "Policies, procedures, narrative explanations, or any write operation.",
        "input_schema": "sql_query: string",
        "result_shape": "Markdown table with row count.",
    },
    {
        "name": "search_documents",
        "mode": "all",
        "use_for": "Policies, procedures, FAQs, guidance, and other unstructured document content.",
        "avoid_for": "Calculations or broad table scans.",
        "input_schema": "query: string",
        "result_shape": "Cited passages with source, title, and page metadata.",
    },
]

SEARCH_DOCUMENTS_PARAMETERS = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "Natural-language search query for finding relevant passages in indexed documents.",
        },
    },
    "required": ["query"],
    "additionalProperties": False,
}


def build_search_documents_tool():
    from azure.ai.projects.models import FunctionTool

    return FunctionTool(
        name="search_documents",
        description=(
            "Search indexed business documents in Azure AI Search. "
            "Use for policies, procedures, guidance, FAQs, and other unstructured text. "
            "Returns cited passages with source and page metadata."
        ),
        parameters=deepcopy(SEARCH_DOCUMENTS_PARAMETERS),
        strict=True,
    )


def build_execute_sql_tool(table_names):
    from azure.ai.projects.models import FunctionTool

    table_list = ", ".join(table_names) if table_names else "scenario tables"
    parameters = {
        "type": "object",
        "properties": {
            "sql_query": {
                "type": "string",
                "description": (
                    "Read-only T-SQL query to execute against the Fabric Lakehouse SQL endpoint. "
                    f"Use table names directly: {table_list}. Do not use schema prefixes."
                ),
            }
        },
        "required": ["sql_query"],
        "additionalProperties": False,
    }

    return FunctionTool(
        name="execute_sql",
        description=(
            "Execute a read-only T-SQL query against the Fabric Lakehouse for structured data. "
            f"Use for numbers, counts, aggregations, joins, and specific records across: {table_list}."
        ),
        parameters=parameters,
        strict=True,
    )


def get_tool_summary_lines(foundry_only=False):
    if foundry_only:
        return [
            "1. search_documents - Search unstructured data in Azure AI Search",
        ]

    return [
        "1. execute_sql - Query structured data in the Fabric Lakehouse",
        "2. search_documents - Search unstructured data in Azure AI Search",
    ]


def get_response_loop_lines():
    return list(TOOL_EXECUTION_LOOP)


def get_tool_contract_rows(foundry_only=False):
    if foundry_only:
        return [row for row in TOOL_CONTRACT_ROWS if row["mode"] == "all"]

    return list(TOOL_CONTRACT_ROWS)


def build_tool_instruction_block(foundry_only, table_names, schema_text, join_hints):
    if foundry_only:
        return f"""You have access to ONE read-only tool:

## Tool: search_documents
Purpose: Retrieve policy, process, FAQ, and guidance content from indexed documents.
Use it for:
- Policy or procedure questions
- Explanations of how a workflow works
- Looking up wording from source documents
Do not use it for:
- Counts, totals, or calculations
- Listing records from structured tables
Parameters:
- query (string, required): natural-language document search query
Returns:
- One or more cited passages with source, title, and page metadata

## Response Loop
1. Analyze the user's question.
2. Use search_documents when the answer depends on document content.
3. Review the retrieved passages and cite the relevant sources.
4. If the question requires structured data, explain that this search-only agent cannot query tables.
"""

    table_list = ", ".join(table_names) if table_names else "scenario tables"
    join_hint_text = "; ".join(
        join_hints) if join_hints else "check the schema prompt for foreign-key relationships"
    schema_section = schema_text.strip(
    ) or "Schema prompt unavailable. Use the listed tables carefully and prefer simple, read-only queries."

    return f"""You have access to TWO read-only tools:

## Tool 1: execute_sql
Purpose: Query structured business data in the Fabric Lakehouse.
Use it for:
- Counts, totals, averages, trends, rankings, and joins
- Looking up specific records in structured tables
- Questions that require numeric evidence from data
Do not use it for:
- Policies, procedures, or other narrative content stored in documents
- Any INSERT, UPDATE, DELETE, DDL, or other write operations
Parameters:
- sql_query (string, required): read-only T-SQL query using these tables: {table_list}
SQL rules:
- Use T-SQL syntax compatible with Fabric Lakehouse
- Do not use schema prefixes such as dbo.
- Use TOP instead of LIMIT
- Use GROUP BY when mixing aggregates with non-aggregated columns
- Prefer these join paths: {join_hint_text}
- Keep queries read-only

Available schema context:
{schema_section}

## Tool 2: search_documents
Purpose: Retrieve policy, process, FAQ, and guidance content from indexed documents.
Use it for:
- Policy or procedure questions
- Explanations of how a workflow works
- Looking up wording from source documents
Do not use it for:
- Counts, totals, or calculations that belong in structured data
- Questions that need a full table scan of business records
Parameters:
- query (string, required): natural-language document search query
Returns:
- One or more cited passages with source, title, and page metadata

## Tool Selection Rules
- Numbers, counts, aggregations, rankings, or record lookups -> execute_sql
- Policies, procedures, FAQs, or explanations -> search_documents
- Cross-source questions may require both tools in sequence

## Response Loop
1. Inspect the user question and choose execute_sql, search_documents, or both.
2. Call the selected tool with only the schema-defined parameters.
3. Review the tool outputs.
4. If needed, call the second tool to combine policy context with data evidence.
5. Synthesize a concise final answer and mention sources or limitations.
"""
