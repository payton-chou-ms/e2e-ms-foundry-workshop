"""Workshop 多代理程式延伸共用的執行階段輔助函式。"""

import json
import os
import struct
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient

from foundry_tool_contract import (
    DEFAULT_SEARCH_TOP,
    MAX_SEARCH_TOP,
    SQL_RESULT_ROW_LIMIT,
    build_execute_sql_tool,
    build_search_documents_tool,
)
from load_env import load_all_env
from scenario_utils import build_scenario_resource_name, resolve_data_paths, resolve_scenario

load_all_env()


class WorkshopMultiAgentRuntime:
    def __init__(self, require_fabric=True):
        self.project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        self.search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
        self.workspace_id = os.getenv("FABRIC_WORKSPACE_ID")
        self.data_folder = os.getenv("DATA_FOLDER")
        self.fabric_enabled = bool(
            self.workspace_id and self.workspace_id != "your-workspace-id-here"
        )

        if not self.project_endpoint:
            raise ValueError("未設定 AZURE_AI_PROJECT_ENDPOINT")
        if not self.search_endpoint:
            raise ValueError("未設定 AZURE_AI_SEARCH_ENDPOINT")

        self.project_root = Path(__file__).resolve().parent.parent
        self.scenario = resolve_scenario(os.getenv("SCENARIO_KEY") or None, self.data_folder)
        self.scenario_key = self.scenario["key"]
        self.data_folder = self.scenario["dataFolder"]
        paths = resolve_data_paths(self.scenario)
        self.data_dir = paths["data_dir"]
        self.config_dir = paths["config_dir"]

        self.ontology_config = self._load_json("ontology_config.json")
        self.fabric_ids = self._load_json(
            "fabric_ids.json", required=False) or {}
        self.search_ids = self._load_json(
            "search_ids.json", required=False) or {}
        self.schema_prompt = self._load_text(
            "schema_prompt.txt", required=False) or ""

        self.tables = list(self.ontology_config.get("tables", {}).keys())
        self.solution_name = (
            self.fabric_ids.get("solution_name")
            or os.getenv("SOLUTION_NAME")
            or os.getenv("SOLUTION_PREFIX")
            or build_scenario_resource_name(
                self.ontology_config.get("scenario", "demo").lower().replace(" ", "-"),
                self.scenario_key,
            )
        )
        self.index_name = self.search_ids.get(
            "index_name", f"{self.solution_name}-documents"
        )
        self.lakehouse_name = self.fabric_ids.get("lakehouse_name")
        self.lakehouse_id = self.fabric_ids.get("lakehouse_id")
        self.fabric_enabled = self.fabric_enabled and bool(
            self.lakehouse_id and self.lakehouse_name
        )
        self.runtime_mode = "fabric+search" if self.fabric_enabled else "search-only"

        if require_fabric and not self.fabric_enabled:
            if not self.workspace_id or self.workspace_id == "your-workspace-id-here":
                raise ValueError(
                    "未設定 FABRIC_WORKSPACE_ID。建立多代理工作流前，請先在 .env 填入真正的 Fabric workspace ID。"
                )
            raise ValueError(
                "目前沒有 Fabric Lakehouse 中繼資料。請先為這個情境執行 scripts/02_create_fabric_items.py 和 scripts/03_load_fabric_data.py。"
            )

        self._sql_endpoint = None

    def _load_json(self, file_name, required=True):
        path = self.config_dir / file_name
        if not path.exists():
            if required:
                if file_name == "fabric_ids.json":
                    raise ValueError(
                        f"在 {self.config_dir} 找不到 {file_name}。請先為目前情境執行 scripts/02_create_fabric_items.py 和 scripts/03_load_fabric_data.py。"
                    )
                raise ValueError(f"在 {self.config_dir} 找不到 {file_name}")
            return None

        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def _load_text(self, file_name, required=True):
        path = self.config_dir / file_name
        if not path.exists():
            if required:
                raise ValueError(f"在 {self.config_dir} 找不到 {file_name}")
            return None

        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()

    @property
    def sql_endpoint(self):
        if not self.fabric_enabled:
            raise RuntimeError(
                "search-only 模式下沒有 Fabric SQL endpoint 可用")
        if self._sql_endpoint is None:
            self._sql_endpoint = self._get_sql_endpoint()
        return self._sql_endpoint

    def _get_sql_endpoint(self):
        import requests

        credential = DefaultAzureCredential()
        token = credential.get_token(
            "https://api.fabric.microsoft.com/.default")
        headers = {"Authorization": f"Bearer {token.token}"}
        url = (
            f"https://api.fabric.microsoft.com/v1/workspaces/{self.workspace_id}"
            f"/lakehouses/{self.lakehouse_id}"
        )
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            raise RuntimeError(
                f"無法取得 Fabric SQL endpoint（{response.status_code}）：{response.text}"
            )

        properties = response.json().get("properties", {})
        sql_properties = properties.get("sqlEndpointProperties", {})
        sql_endpoint = sql_properties.get("connectionString")
        if not sql_endpoint:
            raise RuntimeError(
                "Lakehouse 中繼資料裡缺少 Fabric SQL endpoint")
        return sql_endpoint

    def build_tools_for_mode(self, tool_mode):
        if tool_mode == "none":
            return []
        if tool_mode == "search":
            return [build_search_documents_tool()]
        if tool_mode == "sql":
            return [build_execute_sql_tool(self.tables)]
        if tool_mode == "both":
            return [build_execute_sql_tool(self.tables), build_search_documents_tool()]
        raise ValueError(f"不支援的工具模式：{tool_mode}")

    def execute_sql(self, sql_query):
        import pyodbc

        normalized = " ".join(sql_query.strip().lower().split())
        if not normalized:
            return "SQL 錯誤：查詢內容是空的"
        if not (normalized.startswith("select ") or normalized.startswith("with ")):
            return "SQL 錯誤：只允許唯讀的 SELECT 或 CTE 查詢"

        disallowed_terms = (
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
        padded = f" {normalized} "
        for term in disallowed_terms:
            if term in padded:
                return "SQL 錯誤：不允許寫入操作或 DDL 語句"

        try:
            credential = DefaultAzureCredential()
            token = credential.get_token(
                "https://database.windows.net//.default")
            token_bytes = token.token.encode("UTF-16-LE")
            token_struct = struct.pack(
                f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)

            connection_string = (
                f"Driver={{ODBC Driver 18 for SQL Server}};"
                f"Server={self.sql_endpoint};"
                f"Database={self.lakehouse_name};"
                "Encrypt=yes;TrustServerCertificate=no"
            )

            sql_access_token = 1256
            connection = pyodbc.connect(
                connection_string,
                attrs_before={sql_access_token: token_struct},
            )
            cursor = connection.cursor()
            cursor.execute(sql_query)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            connection.close()
        except Exception as exc:
            return f"SQL 錯誤：{exc}"

        lines = ["| " + " | ".join(columns) + " |"]
        lines.append("|" + "|".join(["---"] * len(columns)) + "|")
        for row in rows[:SQL_RESULT_ROW_LIMIT]:
            values = [
                str(value) if value is not None else "NULL" for value in row]
            lines.append("| " + " | ".join(values) + " |")
        if len(rows) > SQL_RESULT_ROW_LIMIT:
            lines.append(f"\n... 另外還有 {len(rows) - SQL_RESULT_ROW_LIMIT} 列")
        lines.append(f"\n(共回傳 {len(rows)} 列)")
        return "\n".join(lines)

    def search_documents(self, query, top=DEFAULT_SEARCH_TOP):
        try:
            top_value = int(top)
        except (TypeError, ValueError):
            top_value = DEFAULT_SEARCH_TOP

        top_value = max(1, min(top_value, MAX_SEARCH_TOP))

        try:
            credential = DefaultAzureCredential()
            search_client = SearchClient(
                endpoint=self.search_endpoint,
                index_name=self.index_name,
                credential=credential,
            )
            results = search_client.search(
                search_text=query,
                top=top_value,
                query_type="semantic",
                semantic_configuration_name="default-semantic",
                select=["content", "title", "source", "page_number"],
            )
        except Exception as exc:
            return f"搜尋錯誤：{exc}"

        lines = []
        for index, result in enumerate(results, 1):
            lines.append(f"\n--- 結果 {index} ---")
            lines.append(
                f"來源：{result.get('source', '未知')}（第 {result.get('page_number', '?')} 頁）"
            )
            lines.append(f"標題：{result.get('title', '未知')}")
            lines.append(f"內容：{result.get('content', '')[:500]}...")

        if not lines:
            return "找不到符合這個查詢的文件。"
        return "\n".join(lines)

    def ids_output_path(self, file_name="multi_agent_ids.json"):
        return self.config_dir / file_name
