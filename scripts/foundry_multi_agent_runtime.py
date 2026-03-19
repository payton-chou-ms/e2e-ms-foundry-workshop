"""Shared runtime helpers for the workshop multi-agent extension."""

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

load_all_env()


class WorkshopMultiAgentRuntime:
    def __init__(self):
        self.project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        self.search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
        self.workspace_id = os.getenv("FABRIC_WORKSPACE_ID")
        self.data_folder = os.getenv("DATA_FOLDER")

        if not self.project_endpoint:
            raise ValueError("AZURE_AI_PROJECT_ENDPOINT not set")
        if not self.search_endpoint:
            raise ValueError("AZURE_AI_SEARCH_ENDPOINT not set")
        if not self.workspace_id:
            raise ValueError("FABRIC_WORKSPACE_ID not set")
        if not self.data_folder:
            raise ValueError("DATA_FOLDER not set")

        self.project_root = Path(__file__).resolve().parent.parent
        data_path = Path(self.data_folder)
        if not data_path.is_absolute():
            data_path = self.project_root / data_path
        self.data_dir = data_path.resolve()
        self.config_dir = self.data_dir / "config"
        if not self.config_dir.exists():
            self.config_dir = self.data_dir

        self.ontology_config = self._load_json("ontology_config.json")
        self.fabric_ids = self._load_json("fabric_ids.json")
        self.search_ids = self._load_json(
            "search_ids.json", required=False) or {}
        self.schema_prompt = self._load_text(
            "schema_prompt.txt", required=False) or ""

        self.tables = list(self.ontology_config.get("tables", {}).keys())
        self.solution_name = self.fabric_ids.get("solution_name") or self.ontology_config.get(
            "scenario", "demo"
        ).lower().replace(" ", "-")
        self.index_name = self.search_ids.get(
            "index_name", f"{self.solution_name}-documents"
        )
        self.lakehouse_name = self.fabric_ids.get("lakehouse_name")
        self.lakehouse_id = self.fabric_ids.get("lakehouse_id")

        if not self.lakehouse_id or not self.lakehouse_name:
            raise ValueError("Fabric lakehouse metadata is not available")

        self._sql_endpoint = None

    def _load_json(self, file_name, required=True):
        path = self.config_dir / file_name
        if not path.exists():
            if required:
                raise ValueError(f"{file_name} not found in {self.config_dir}")
            return None

        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def _load_text(self, file_name, required=True):
        path = self.config_dir / file_name
        if not path.exists():
            if required:
                raise ValueError(f"{file_name} not found in {self.config_dir}")
            return None

        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()

    @property
    def sql_endpoint(self):
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
                f"Could not resolve Fabric SQL endpoint ({response.status_code}): {response.text}"
            )

        properties = response.json().get("properties", {})
        sql_properties = properties.get("sqlEndpointProperties", {})
        sql_endpoint = sql_properties.get("connectionString")
        if not sql_endpoint:
            raise RuntimeError(
                "Fabric SQL endpoint is missing from lakehouse metadata")
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
        raise ValueError(f"Unsupported tool mode: {tool_mode}")

    def execute_sql(self, sql_query):
        import pyodbc

        normalized = " ".join(sql_query.strip().lower().split())
        if not normalized:
            return "SQL Error: SQL query is empty"
        if not (normalized.startswith("select ") or normalized.startswith("with ")):
            return "SQL Error: only read-only SELECT and CTE statements are allowed"

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
                return "SQL Error: write operations and DDL statements are not allowed"

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
            return f"SQL Error: {exc}"

        lines = ["| " + " | ".join(columns) + " |"]
        lines.append("|" + "|".join(["---"] * len(columns)) + "|")
        for row in rows[:SQL_RESULT_ROW_LIMIT]:
            values = [
                str(value) if value is not None else "NULL" for value in row]
            lines.append("| " + " | ".join(values) + " |")
        if len(rows) > SQL_RESULT_ROW_LIMIT:
            lines.append(
                f"\n... and {len(rows) - SQL_RESULT_ROW_LIMIT} more rows")
        lines.append(f"\n({len(rows)} rows returned)")
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
            return f"Search Error: {exc}"

        lines = []
        for index, result in enumerate(results, 1):
            lines.append(f"\n--- Result {index} ---")
            lines.append(
                f"Source: {result.get('source', 'Unknown')} (Page {result.get('page_number', '?')})"
            )
            lines.append(f"Title: {result.get('title', 'Unknown')}")
            lines.append(f"Content: {result.get('content', '')[:500]}...")

        if not lines:
            return "No documents found matching the query."
        return "\n".join(lines)

    def ids_output_path(self):
        return self.config_dir / "multi_agent_ids.json"
