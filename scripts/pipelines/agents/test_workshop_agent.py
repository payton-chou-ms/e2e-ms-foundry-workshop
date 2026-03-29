"""測試 AI Foundry Agent 的互動式聊天腳本。"""

import os
import sys

SCRIPTS_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, SCRIPTS_ROOT)

from foundry_tool_contract import (
    DEFAULT_SEARCH_TOP,
    MAX_SEARCH_TOP,
    SQL_RESULT_ROW_LIMIT,
    get_tool_summary_lines,
)
from foundry_trace import configure_foundry_tracing
from azure.search.documents import SearchClient
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from load_env import load_all_env
from scenario_utils import build_scenario_resource_name, resolve_data_paths, resolve_scenario
import json
import struct
import argparse

# Parse arguments first
parser = argparse.ArgumentParser()
parser.add_argument("--agent-id", default=os.getenv("FOUNDRY_AGENT_ID"))
parser.add_argument("--foundry-only", action="store_true",
                    help="只使用 Search 的模式（不使用 Fabric / SQL）")
parser.add_argument("--scenario", default="",
                    help="要使用的情境 key（優先於 DATA_FOLDER）")
parser.add_argument("--data-folder", default="",
                    help="資料資料夾路徑（預設讀取 .env）")
args = parser.parse_args()

FOUNDRY_ONLY = args.foundry_only

# Load environment from azd + project .env
load_all_env()


pyodbc = None
PYODBC_IMPORT_ERROR = None

if not FOUNDRY_ONLY:
    try:
        import pyodbc as _pyodbc
        pyodbc = _pyodbc
    except ImportError as exc:
        PYODBC_IMPORT_ERROR = exc

# ============================================================================
# Configuration
# ============================================================================

# Azure services - from azd environment
ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
SEARCH_ENDPOINT = os.getenv("AZURE_AI_SEARCH_ENDPOINT")

# Project settings - from .env
WORKSPACE_ID = os.getenv("FABRIC_WORKSPACE_ID")

if not ENDPOINT:
    print("錯誤：未設定 AZURE_AI_PROJECT_ENDPOINT")
    print("      請先執行 'azd up' 部署 Azure 資源")
    sys.exit(1)

if not FOUNDRY_ONLY and not WORKSPACE_ID:
    print("錯誤：.env 中未設定 FABRIC_WORKSPACE_ID")
    print("      若要略過 Fabric，請使用 --foundry-only；否則請補上 FABRIC_WORKSPACE_ID")
    sys.exit(1)

if not SEARCH_ENDPOINT:
    print("錯誤：.env 中未設定 AZURE_AI_SEARCH_ENDPOINT")
    sys.exit(1)

scenario = resolve_scenario(args.scenario or os.getenv("SCENARIO_KEY") or None, args.data_folder or os.getenv("DATA_FOLDER"), require_capability="search")
paths = resolve_data_paths(scenario)
data_dir = scenario["absoluteDataFolder"]
config_dir = os.fspath(paths["config_dir"])

# Get agent ID
AGENT_ID = args.agent_id

if not AGENT_ID:
    # Try to load from agent_ids.json
    agent_ids_path = os.path.join(config_dir, "agent_ids.json")
    if os.path.exists(agent_ids_path):
        with open(agent_ids_path) as f:
            agent_ids = json.load(f)
        # agents.get() expects the plain name, not the versioned id (name:version)
        AGENT_ID = agent_ids.get("agent_name") or agent_ids.get("agent_id")

if not AGENT_ID:
    print("錯誤：找不到 agent ID。")
    print("      請先執行 admin_prepare_shared_demo.py --mode foundry-only 或 admin_prepare_docs_data_demo.py，或自行提供 --agent-id")
    sys.exit(1)

# Load Fabric IDs (optional in foundry-only mode)
LAKEHOUSE_NAME = None
LAKEHOUSE_ID = None
fabric_ids_path = os.path.join(config_dir, "fabric_ids.json")
if os.path.exists(fabric_ids_path):
    with open(fabric_ids_path) as f:
        fabric_ids = json.load(f)
    LAKEHOUSE_NAME = fabric_ids.get("lakehouse_name")
    LAKEHOUSE_ID = fabric_ids.get("lakehouse_id")
elif not FOUNDRY_ONLY:
    print("錯誤：找不到 fabric_ids.json。請先執行 02_create_fabric_items.py，或使用 --foundry-only")
    sys.exit(1)

# Load Search IDs
search_ids_path = os.path.join(config_dir, "search_ids.json")
if os.path.exists(search_ids_path):
    with open(search_ids_path) as f:
        search_ids = json.load(f)
    INDEX_NAME = search_ids.get("index_name")
else:
    # Try to get solution name from fabric_ids or ontology
    solution_name = "demo"
    if os.path.exists(fabric_ids_path):
        with open(fabric_ids_path) as f:
            solution_name = json.load(f).get("solution_name", "demo")
    INDEX_NAME = f"{build_scenario_resource_name(solution_name, scenario['key'])}-documents"

# ============================================================================
# Load Sample Questions
# ============================================================================


def load_sample_questions():
    questions_path = os.path.join(config_dir, "sample_questions.txt")
    questions = []
    target_section = "DOCUMENT QUESTIONS" if FOUNDRY_ONLY else "COMBINED INSIGHT QUESTIONS"
    in_target_section = False

    if os.path.exists(questions_path):
        with open(questions_path, "r") as f:
            for line in f.read().splitlines():
                if target_section in line:
                    in_target_section = True
                    continue
                if in_target_section and line.startswith("==="):
                    break
                if in_target_section and line.strip().startswith("- "):
                    questions.append(line.strip()[2:])

    if questions:
        return questions

    if FOUNDRY_ONLY:
        return [
            "文件裡怎麼規定停機事件要通知客戶？",
            "文件裡如何定義客戶影響等級？",
        ]

    return [
        "你可以從資料中整理出哪些重點？",
        "資料結果和文件中的政策規定相比，有哪些差異？",
    ]


def print_sample_questions():
    if FOUNDRY_ONLY:
        print("文件類範例問題：")
    else:
        print("範例問題（可能會同時用到兩種工具）：")

    for question in sample_questions:
        print(f"  - {question}")


sample_questions = load_sample_questions()

print(f"\n{'='*60}")
if FOUNDRY_ONLY:
    print("AI Agent 對話（只用 Search）")
else:
    print("Orchestrator Agent 對話")
print(f"{'='*60}")
print(f"Scenario：{scenario['key']}")
print("可用工具：")
for line in get_tool_summary_lines(FOUNDRY_ONLY):
    print(f"  {line}")
print_sample_questions()
print("輸入 'quit' 離開，輸入 'help' 可再次查看範例問題\n")

# ============================================================================
# Get SQL Endpoint (skip in foundry-only mode)
# ============================================================================

SQL_ENDPOINT = None

if not FOUNDRY_ONLY:
    def get_sql_endpoint():
        """Get the SQL analytics endpoint for the Lakehouse"""
        credential = DefaultAzureCredential()
        token = credential.get_token(
            "https://api.fabric.microsoft.com/.default")

        import requests
        headers = {"Authorization": f"Bearer {token.token}"}
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{WORKSPACE_ID}/lakehouses/{LAKEHOUSE_ID}"

        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            props = data.get("properties", {})
            sql_props = props.get("sqlEndpointProperties", {})
            return sql_props.get("connectionString")
        return None

    SQL_ENDPOINT = get_sql_endpoint()
    if not SQL_ENDPOINT:
        print("警告：無法取得 SQL endpoint，SQL 查詢可能失敗。")

# ============================================================================
# SQL Execution Function
# ============================================================================

DISALLOWED_SQL_TERMS = (
    " insert ",
    " update ",
    " delete ",
    " merge ",
    " drop ",
    " alter ",
    " create ",
    " truncate ",
    " exec ",
    " execute ",
)


def validate_sql_query(sql_query):
    """Ensure the tool remains read-only and limited to queries."""
    normalized = " ".join(sql_query.strip().lower().split())
    if not normalized:
        return False, "SQL 查詢不可為空"
    if not (normalized.startswith("select ") or normalized.startswith("with ")):
        return False, "只允許唯讀的 SELECT 或 CTE 查詢"

    padded = f" {normalized} "
    for term in DISALLOWED_SQL_TERMS:
        if term in padded:
            return False, "不允許寫入操作或 DDL 語句"

    return True, ""


def format_sql_results(columns, rows):
    """Format SQL rows as a compact markdown table for the model."""
    result_lines = []
    result_lines.append("| " + " | ".join(columns) + " |")
    result_lines.append("|" + "|".join(["---"] * len(columns)) + "|")

    for row in rows[:SQL_RESULT_ROW_LIMIT]:
        values = [str(value) if value is not None else "NULL" for value in row]
        result_lines.append("| " + " | ".join(values) + " |")

    if len(rows) > SQL_RESULT_ROW_LIMIT:
        result_lines.append(
            f"\n... 另外還有 {len(rows) - SQL_RESULT_ROW_LIMIT} 列")

        result_lines.append(f"\n(共回傳 {len(rows)} 列)")
    return "\n".join(result_lines)


def execute_sql(sql_query):
    """Execute SQL query against Fabric Lakehouse and return results"""
    if not SQL_ENDPOINT:
        return "錯誤：目前沒有 SQL endpoint 可用"

    if pyodbc is None:
        detail = f": {PYODBC_IMPORT_ERROR}" if PYODBC_IMPORT_ERROR else ""
        return f"SQL 錯誤：pyodbc 無法使用{detail}"

    is_valid, validation_message = validate_sql_query(sql_query)
    if not is_valid:
        return f"SQL 錯誤：{validation_message}"

    try:
        # Get AAD token for SQL
        credential = DefaultAzureCredential()
        token = credential.get_token('https://database.windows.net//.default')

        # Build token struct with UTF-16-LE encoding (required for ODBC)
        token_bytes = token.token.encode('UTF-16-LE')
        token_struct = struct.pack(
            f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)

        # Connection string
        conn_str = f'Driver={{ODBC Driver 18 for SQL Server}};Server={SQL_ENDPOINT};Database={LAKEHOUSE_NAME};Encrypt=yes;TrustServerCertificate=no'

        # Connect with token
        SQL_COPT_SS_ACCESS_TOKEN = 1256
        conn = pyodbc.connect(conn_str, attrs_before={
                              SQL_COPT_SS_ACCESS_TOKEN: token_struct})
        cursor = conn.cursor()

        cursor.execute(sql_query)

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        conn.close()
        return format_sql_results(columns, rows)

    except Exception as e:
        return f"SQL 錯誤：{str(e)}"

# ============================================================================
# AI Search Function
# ============================================================================


def search_documents(query, top=3):
    """Search documents in Azure AI Search"""
    try:
        try:
            top_value = int(top)
        except (TypeError, ValueError):
            top_value = DEFAULT_SEARCH_TOP

        top_value = max(1, min(top_value, MAX_SEARCH_TOP))

        credential = DefaultAzureCredential()
        search_client = SearchClient(
            endpoint=SEARCH_ENDPOINT,
            index_name=INDEX_NAME,
            credential=credential
        )

        # Perform hybrid search (text + vector if available)
        results = search_client.search(
            search_text=query,
            top=top_value,
            query_type="semantic",
            semantic_configuration_name="default-semantic",
            select=["content", "title", "source", "page_number"]
        )

        # Format results
        result_lines = []
        for i, result in enumerate(results, 1):
            result_lines.append(f"\n--- 結果 {i} ---")
            result_lines.append(
                f"來源：{result.get('source', '未知')}（第 {result.get('page_number', '?')} 頁）")
            result_lines.append(f"標題：{result.get('title', '未知')}")
            result_lines.append(
                f"內容：{result.get('content', '')[:500]}...")

        if not result_lines:
            return "找不到符合這個查詢的文件。"

        return "\n".join(result_lines)

    except Exception as e:
        return f"搜尋錯誤：{str(e)}"

# ============================================================================
# Initialize Client
# ============================================================================


credential = DefaultAzureCredential()
project_client = AIProjectClient(
    endpoint=ENDPOINT,
    credential=credential
)

trace_session = configure_foundry_tracing(
    project_client=project_client,
    scenario_name="08_test_foundry_agent",
    service_name="e2e-ms-foundry-workshop.agent-chat",
)

if trace_session.enabled:
    print("追蹤：已啟用")
elif trace_session.warning:
    print(f"追蹤：{trace_session.warning}")

# Get agent details
with trace_session.span("get-agent"):
    agent = project_client.agents.get(AGENT_ID)
agent_def = agent.versions['latest']['definition']
MODEL = agent_def['model']
INSTRUCTIONS = agent_def['instructions']
TOOLS = agent_def['tools']

# Get OpenAI client
openai_client = project_client.get_openai_client()

# Create a conversation
with trace_session.span("create-conversation"):
    conversation = openai_client.conversations.create()
print("-" * 60)

# ============================================================================
# Chat Function
# ============================================================================


def chat(user_message):
    """Send a message and handle function calls"""

    # Build input with conversation context
    with trace_session.span("create-response"):
        response = openai_client.responses.create(
            model=MODEL,
            input=user_message,
            instructions=INSTRUCTIONS,
            tools=TOOLS,
            conversation={'id': conversation.id}
        )

    # Process the response
    final_text = ""

    while True:
        # Check for function calls in output
        function_calls = []
        for item in response.output:
            if hasattr(item, 'type'):
                if item.type == 'function_call':
                    function_calls.append(item)
                elif item.type == 'message':
                    # Extract text from message
                    for content in item.content:
                        if hasattr(content, 'text'):
                            final_text += content.text + "\n"

        if not function_calls:
            break

        # Handle function calls
        tool_outputs = []
        for fc in function_calls:
            args = json.loads(fc.arguments)

            if fc.name == "execute_sql":
                sql_query = args.get("sql_query", "")

                print(f"\n  [SQL 工具] 執行查詢：")
                # Print full query with indentation
                for line in sql_query.strip().split('\n'):
                    print(f"    {line}")

                with trace_session.span("tool-execute-sql"):
                    result = execute_sql(sql_query)

                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": fc.call_id,
                    "output": result
                })

            elif fc.name == "search_documents":
                query = args.get("query", "")
                top = args.get("top", DEFAULT_SEARCH_TOP)

                print(
                    f"\n  [搜尋工具] 查詢中：{query}（top={top}）...")

                with trace_session.span("tool-search-documents"):
                    result = search_documents(query, top)

                # Show the result that goes to the agent
                print(f"  [搜尋結果]：")
                # Truncate if too long, but show meaningful content
                display = result[:500] if len(result) > 500 else result
                for line in display.strip().split('\n'):
                    print(f"    {line}")
                if len(result) > 500:
                    print(f"    ...（總長度 {len(result)} 字元）")

                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": fc.call_id,
                    "output": result
                })
            else:
                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": fc.call_id,
                    "output": f"未知函式：{fc.name}"
                })

        # Submit function results and continue conversation
        with trace_session.span("create-followup-response"):
            response = openai_client.responses.create(
                model=MODEL,
                input=tool_outputs,
                instructions=INSTRUCTIONS,
                tools=TOOLS,
                conversation={'id': conversation.id}
            )

    return final_text.strip()

# ============================================================================
# Chat Loop
# ============================================================================


print("-" * 60)

while True:
    try:
        user_input = input("\n你：").strip()
    except (EOFError, KeyboardInterrupt):
        print()  # New line after ^C
        break

    if not user_input:
        continue

    if user_input.lower() in ["quit", "exit", "q"]:
        break

    if user_input.lower() == "help":
        print()
        print_sample_questions()
        continue

    print("\nAgent：", end="", flush=True)

    try:
        response = chat(user_input)
        if response:
            print(response)
        else:
            print("（沒有回應）")
    except Exception as e:
        print(f"錯誤：{e}")

# Cleanup
print("\n已結束。")
