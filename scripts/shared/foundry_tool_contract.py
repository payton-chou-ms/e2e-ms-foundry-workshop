"""Foundry agent 與本機執行階段共用的工具契約。"""

from copy import deepcopy


DEFAULT_SEARCH_TOP = 3
MAX_SEARCH_TOP = 10
SQL_RESULT_ROW_LIMIT = 50

TOOL_EXECUTION_LOOP = [
    "先判斷使用者問題需要結構化資料、文件內容，或兩者都需要。",
    "只用工具契約裡定義的參數發出一個或多個函式呼叫。",
    "由本機執行階段執行工具，並把原始結果以 function_call_output 回傳。",
    "根據工具輸出整理最終答案，並說明資料來源不足或不可用之處。",
]

TOOL_CONTRACT_ROWS = [
    {
        "name": "execute_sql",
        "mode": "full",
        "use_for": "適合查詢計數、總和、趨勢、排名、關聯查詢與 Fabric 資料表記錄。",
        "avoid_for": "不適合回答政策、流程、說明性內容，也不能做任何寫入操作。",
        "input_schema": "sql_query: string",
        "result_shape": "含列數說明的 Markdown 表格。",
    },
    {
        "name": "search_documents",
        "mode": "all",
        "use_for": "適合查詢政策、流程、常見問答、指引與其他非結構化文件內容。",
        "avoid_for": "不適合做計算或大範圍表格掃描。",
        "input_schema": "query: string",
        "result_shape": "附來源、標題與頁碼資訊的引文片段。",
    },
]

SEARCH_DOCUMENTS_PARAMETERS = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "用自然語言在已索引文件中尋找相關段落。",
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
            "在 Azure AI Search 中搜尋已索引的業務文件。"
            "適合查詢政策、流程、指引、常見問答與其他非結構化文字。"
            "回傳結果會附來源與頁碼資訊。"
        ),
        parameters=deepcopy(SEARCH_DOCUMENTS_PARAMETERS),
        strict=True,
    )



def build_execute_sql_tool(table_names):
    from azure.ai.projects.models import FunctionTool

    table_list = ", ".join(table_names) if table_names else "情境資料表"
    parameters = {
        "type": "object",
        "properties": {
            "sql_query": {
                "type": "string",
                "description": (
                    "要在 Fabric Lakehouse SQL 端點執行的唯讀 T-SQL 查詢。"
                    f"請直接使用資料表名稱：{table_list}。不要加 schema 前綴。"
                ),
            }
        },
        "required": ["sql_query"],
        "additionalProperties": False,
    }

    return FunctionTool(
        name="execute_sql",
        description=(
            "在 Fabric Lakehouse 上執行唯讀 T-SQL 查詢，取得結構化資料。"
            f"適合查詢數值、計數、彙總、關聯與特定記錄。可用資料表：{table_list}。"
        ),
        parameters=parameters,
        strict=True,
    )



def get_tool_summary_lines(foundry_only=False):
    if foundry_only:
        return ["1. search_documents - 在 Azure AI Search 中搜尋非結構化文件"]

    return [
        "1. execute_sql - 查詢 Fabric Lakehouse 的結構化資料",
        "2. search_documents - 在 Azure AI Search 中搜尋非結構化文件",
    ]



def get_response_loop_lines():
    return list(TOOL_EXECUTION_LOOP)



def get_tool_contract_rows(foundry_only=False):
    if foundry_only:
        return [row for row in TOOL_CONTRACT_ROWS if row["mode"] == "all"]

    return list(TOOL_CONTRACT_ROWS)



def build_tool_instruction_block(foundry_only, table_names, schema_text, join_hints):
    if foundry_only:
        return f"""你目前只能使用一個唯讀工具：

    ## 工具：search_documents
    用途：從已索引文件中找出政策、流程、常見問答與指引內容。
    適合：
    - 政策或流程相關問題
    - 說明某個工作流程怎麼運作
    - 查找原始文件中的文字內容
    不適合：
    - 計數、總和或其他計算
    - 列出結構化資料表中的記錄
    參數：
    - query（字串，必填）：自然語言文件搜尋問題
    回傳：
    - 一個或多個引文片段，附來源、標題與頁碼資訊

    ## 回應流程
    1. 先理解使用者問題。
    2. 當答案依賴文件內容時，使用 search_documents。
    3. 檢查取回的段落，引用相關來源。
    4. 如果問題需要結構化資料，請明確說明這個 search-only agent 無法查資料表。
    """

    table_list = ", ".join(table_names) if table_names else "情境資料表"
    join_hint_text = "; ".join(join_hints) if join_hints else "請參考 schema prompt 裡的外鍵關聯"
    schema_section = schema_text.strip() or "目前沒有 schema prompt。請小心使用列出的資料表，並優先採用簡單的唯讀查詢。"

    return f"""你目前可以使用兩個唯讀工具：

## 工具 1：execute_sql
用途：查詢 Fabric Lakehouse 中的結構化業務資料。
適合：
- 計數、總和、平均、趨勢、排名與關聯查詢
- 查找結構化資料表中的特定記錄
- 需要數值證據的問題
不適合：
- 政策、流程或其他存放在文件中的敘述內容
- 任何 INSERT、UPDATE、DELETE、DDL 或其他寫入操作
參數：
- sql_query（字串，必填）：使用下列資料表的唯讀 T-SQL 查詢：{table_list}
SQL 規則：
- 使用與 Fabric Lakehouse 相容的 T-SQL 語法
- 不要使用 dbo 之類的 schema 前綴
- 用 TOP，不要用 LIMIT
- 聚合欄位和一般欄位混用時要搭配 GROUP BY
- 優先參考這些 join 路徑：{join_hint_text}
- 查詢必須保持唯讀

可用 schema 內容：
{schema_section}

## 工具 2：search_documents
用途：從已索引文件中找出政策、流程、常見問答與指引內容。
適合：
- 政策或流程相關問題
- 說明某個工作流程怎麼運作
- 查找原始文件中的文字內容
不適合：
- 應由結構化資料回答的計數、總和或計算
- 需要大範圍掃描業務記錄的問題
參數：
- query（字串，必填）：自然語言文件搜尋問題
回傳：
- 一個或多個引文片段，附來源、標題與頁碼資訊

## 工具選擇規則
- 數值、計數、彙總、排名或記錄查詢 -> execute_sql
- 政策、流程、常見問答或說明 -> search_documents
- 跨來源問題可能需要兩個工具依序搭配使用

## 回應流程
1. 先理解使用者問題，判斷要用 execute_sql、search_documents，還是兩者都用。
2. 呼叫工具時，只能使用契約中定義的參數。
3. 檢查工具輸出。
4. 如有需要，再呼叫第二個工具，把政策脈絡與資料證據合併。
5. 整理成簡潔答案，並說明來源或限制。
"""
