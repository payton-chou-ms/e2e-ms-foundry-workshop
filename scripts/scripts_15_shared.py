"""Shared helpers for the declarative multi-agent workflow runners."""

from datetime import datetime, timezone
import json
from pathlib import Path
import re

import yaml
from azure.ai.projects.models import PromptAgentDefinition

from foundry_trace import TraceSession

_NO_TRACE = TraceSession(enabled=False)


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_ids(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def resolve_config_path(runtime, config_path):
    path = Path(config_path)
    if not path.is_absolute():
        path = runtime.project_root / path
    return path


def build_instruction_context(runtime, scenario):
    return {
        "solution_name": runtime.solution_name,
        "domain_name": runtime.ontology_config.get("name", "Business Data"),
        "domain_description": runtime.ontology_config.get("description", ""),
        "table_list": ", ".join(runtime.tables) or "No tables discovered",
        "schema_prompt": runtime.schema_prompt.strip() or "Schema prompt unavailable.",
        "scenario_title": scenario["title"],
        "scenario_description": scenario["description"],
        "structured_data_status": "Fabric SQL access is available for this scenario.",
        "data_specialist_operating_mode": (
            "Use read-only SQL against the Fabric Lakehouse to produce "
            "quantitative evidence."
        ),
        "runtime_mode": runtime.runtime_mode,
    }


def build_search_only_instruction_context(runtime, scenario):
    return {
        "solution_name": runtime.solution_name,
        "domain_name": runtime.ontology_config.get("name", "業務資料"),
        "domain_description": runtime.ontology_config.get("description", ""),
        "table_list": ", ".join(runtime.tables) or "目前沒有可用資料表",
        "schema_prompt": "search-only 模式下沒有結構化資料 schema 可用。",
        "scenario_title": scenario["title"],
        "scenario_description": scenario["description"],
        "structured_data_status": (
            "這個 scenario 沒有設定 Fabric。請只使用文件搜尋，並在無法做結構化資料驗證時清楚說明。"
        ),
        "data_specialist_operating_mode": (
            "只使用文件搜尋，不要查 SQL。請從已索引文件中整理營運事實、門檻、範例與注意事項。"
        ),
        "runtime_mode": "search-only",
    }


def sanitize_agent_name(value):
    lowered = value.lower().replace("_", "-")
    lowered = re.sub(r"[^a-z0-9-]", "-", lowered)
    lowered = re.sub(r"-+", "-", lowered).strip("-")
    return lowered[:60]


def abbreviate(key):
    parts = key.replace("-", "_").split("_")
    if len(parts) > 1:
        return "".join(part[0] for part in parts if part)
    return key[:3]


def short_slug(value, max_length=12):
    return sanitize_agent_name(value)[:max_length].strip("-")


def build_agent_name(workflow_name, runtime_mode, scenario_key, agent_key,
                     display_name_suffix):
    mode_token = "fs" if runtime_mode == "fabric+search" else "so"
    workflow_token = short_slug(workflow_name)
    scenario_token = abbreviate(scenario_key)
    agent_token = abbreviate(display_name_suffix or agent_key)
    return sanitize_agent_name(
        f"{workflow_token}-{mode_token}-{scenario_token}-{agent_token}"
    )


def delete_agent(project_client, agent_record, trace_session=None):
    ts = trace_session or _NO_TRACE
    for field_name in ("name", "id"):
        identifier = agent_record.get(field_name, "")
        if not identifier:
            continue
        try:
            with ts.span(f"delete-agent-by-{field_name}"):
                project_client.agents.delete(identifier)
            return True
        except Exception:
            continue
    return False


def get_agent(project_client, agent_record, trace_session=None):
    ts = trace_session or _NO_TRACE
    agent_name = agent_record.get("name", "")
    agent_id = agent_record.get("id", "")

    if agent_name:
        try:
            with ts.span("get-agent-by-name"):
                return project_client.agents.get(agent_name)
        except Exception:
            pass

    if agent_id:
        with ts.span("get-agent-by-id"):
            return project_client.agents.get(agent_id)

    raise ValueError("Agent metadata does not contain a usable name or id")


def create_or_replace_agent(project_client, agent_name, definition, description,
                            trace_session=None):
    ts = trace_session or _NO_TRACE
    try:
        with ts.span("get-agent-by-name"):
            existing = project_client.agents.get(agent_name)
    except Exception:
        existing = None

    if existing:
        delete_agent(project_client, {"name": agent_name},
                     trace_session=trace_session)

    with ts.span("create-agent"):
        return project_client.agents.create_version(
            agent_name=agent_name,
            definition=definition,
            description=description,
        )


def _config_display_path(runtime, config_path):
    try:
        return str(config_path.relative_to(runtime.project_root))
    except ValueError:
        return str(config_path)


def search_only_tool_mode(tool_mode):
    if tool_mode in {"sql", "both"}:
        return "search"
    return tool_mode


def ensure_workflow_agents(project_client, runtime, workflow_config,
                           config_path, scenario_keys, trace_session=None):
    ts = trace_session or _NO_TRACE
    output_path = runtime.ids_output_path()
    output = {
        "workflow_name": workflow_config["workflow_name"],
        "config_path": _config_display_path(runtime, config_path),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "runtime_mode": runtime.runtime_mode,
        "scenarios": {},
    }
    if output_path.exists():
        existing_output = load_ids(output_path)
        if isinstance(existing_output, dict):
            output["scenarios"] = existing_output.get("scenarios", {})

    agent_templates = workflow_config["agent_templates"]
    scenarios = workflow_config["scenarios"]
    model = runtime.ontology_config.get("chat_model") or "gpt-5.4-mini"

    for scenario_key in scenario_keys:
        scenario = scenarios[scenario_key]
        context = build_instruction_context(runtime, scenario)
        previous_agents = (
            output.get("scenarios", {})
            .get(scenario_key, {})
            .get("agents", {})
        )

        if previous_agents:
            print(f"\nRefreshing existing agent set for scenario: {scenario_key}")
            for agent_key, agent_record in previous_agents.items():
                if delete_agent(project_client, agent_record, trace_session=trace_session):
                    print(
                        f"[OK] Removed previous {agent_key}: "
                        f"{agent_record.get('name') or agent_record.get('id')}"
                    )

        output["scenarios"][scenario_key] = {
            "title": scenario["title"],
            "agents": {},
        }

        print("\n" + "=" * 60)
        print(f"Preparing multi-agent set for scenario: {scenario_key}")
        print("=" * 60)
        print(f"Runtime mode: {runtime.runtime_mode}")

        for agent_key, template in agent_templates.items():
            agent_name = build_agent_name(
                workflow_name=workflow_config["workflow_name"],
                runtime_mode=runtime.runtime_mode,
                scenario_key=scenario_key,
                agent_key=agent_key,
                display_name_suffix=template["display_name_suffix"],
            )
            instructions = template["instructions_template"].format(**context)
            tools = runtime.build_tools_for_mode(template["tool_mode"])
            definition = PromptAgentDefinition(
                model=model,
                instructions=instructions,
                tools=tools,
            )
            agent = create_or_replace_agent(
                project_client=project_client,
                agent_name=agent_name,
                definition=definition,
                description=f"{scenario['title']} - {agent_key}",
                trace_session=trace_session,
            )

            output["scenarios"][scenario_key]["agents"][agent_key] = {
                "id": agent.id,
                "name": agent.name,
                "version": agent.version,
                "tool_mode": template["tool_mode"],
            }
            print(f"[OK] {agent_key}: {agent.name} ({agent.id})")

    with ts.span("write-agent-metadata"):
        with open(output_path, "w", encoding="utf-8") as handle:
            json.dump(output, handle, indent=2)

    print("\nSaved multi-agent metadata to:")
    print(f"  {output_path}")
    return output_path, output


def ensure_search_only_workflow_agents(project_client, runtime, workflow_config,
                                       config_path, scenario_keys,
                                       trace_session=None,
                                       output_file_name="multi_agent_search_ids.json"):
    ts = trace_session or _NO_TRACE
    output_path = runtime.ids_output_path(output_file_name)
    output = {
        "workflow_name": workflow_config["workflow_name"],
        "config_path": _config_display_path(runtime, config_path),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "runtime_mode": "search-only",
        "scenarios": {},
    }
    if output_path.exists():
        existing_output = load_ids(output_path)
        if isinstance(existing_output, dict):
            output["scenarios"] = existing_output.get("scenarios", {})

    agent_templates = workflow_config["agent_templates"]
    scenarios = workflow_config["scenarios"]
    model = runtime.ontology_config.get("chat_model") or "gpt-5.4-mini"

    for scenario_key in scenario_keys:
        scenario = scenarios[scenario_key]
        context = build_search_only_instruction_context(runtime, scenario)
        previous_agents = (
            output.get("scenarios", {})
            .get(scenario_key, {})
            .get("agents", {})
        )

        if previous_agents:
            print(f"\nRefreshing existing search-only agent set for scenario: {scenario_key}")
            for agent_key, agent_record in previous_agents.items():
                if delete_agent(project_client, agent_record, trace_session=trace_session):
                    print(
                        f"[OK] Removed previous {agent_key}: "
                        f"{agent_record.get('name') or agent_record.get('id')}"
                    )

        output["scenarios"][scenario_key] = {
            "title": scenario["title"],
            "agents": {},
        }

        print("\n" + "=" * 60)
        print(f"Preparing search-only multi-agent set for scenario: {scenario_key}")
        print("=" * 60)
        print("Runtime mode: search-only")

        for agent_key, template in agent_templates.items():
            requested_tool_mode = template["tool_mode"]
            tool_mode = search_only_tool_mode(requested_tool_mode)
            agent_name = build_agent_name(
                workflow_name=workflow_config["workflow_name"],
                runtime_mode="search-only",
                scenario_key=scenario_key,
                agent_key=agent_key,
                display_name_suffix=template["display_name_suffix"],
            )
            instructions = template["instructions_template"].format(**context)
            tools = runtime.build_tools_for_mode(tool_mode)
            definition = PromptAgentDefinition(
                model=model,
                instructions=instructions,
                tools=tools,
            )
            agent = create_or_replace_agent(
                project_client=project_client,
                agent_name=agent_name,
                definition=definition,
                description=f"{scenario['title']} - {agent_key}（search-only）",
                trace_session=trace_session,
            )

            output["scenarios"][scenario_key]["agents"][agent_key] = {
                "id": agent.id,
                "name": agent.name,
                "version": agent.version,
                "tool_mode": tool_mode,
                "requested_tool_mode": requested_tool_mode,
            }
            if tool_mode != requested_tool_mode:
                print(
                    f"[OK] {agent_key}: {agent.name} ({agent.id}) "
                    f"[fallback {requested_tool_mode} -> search]"
                )
            else:
                print(f"[OK] {agent_key}: {agent.name} ({agent.id})")

    with ts.span("write-search-agent-metadata"):
        with open(output_path, "w", encoding="utf-8") as handle:
            json.dump(output, handle, indent=2)

    print("\nSaved search-only multi-agent metadata to:")
    print(f"  {output_path}")
    return output_path, output


def run_prompt_agent_step(openai_client, definition, conversation_id, message,
                          runtime, trace_session=None):
    ts = trace_session or _NO_TRACE
    model = definition["model"]
    instructions = definition["instructions"]
    tools = definition.get("tools", [])

    with ts.span("create-response"):
        response = openai_client.responses.create(
            model=model,
            input=message,
            instructions=instructions,
            tools=tools,
            conversation={"id": conversation_id},
        )

    final_text = ""

    while True:
        function_calls = []
        for item in response.output:
            if getattr(item, "type", None) == "function_call":
                function_calls.append(item)
            elif getattr(item, "type", None) == "message":
                for content in getattr(item, "content", []):
                    if hasattr(content, "text"):
                        final_text += content.text + "\n"

        if not function_calls:
            break

        tool_outputs = []
        for function_call in function_calls:
            arguments = json.loads(function_call.arguments)
            if function_call.name == "search_documents":
                with ts.span("tool-search-documents"):
                    result = runtime.search_documents(
                        query=arguments.get("query", ""),
                        top=arguments.get("top"),
                    )
            elif function_call.name == "execute_sql":
                with ts.span("tool-execute-sql"):
                    result = runtime.execute_sql(arguments.get("sql_query", ""))
            else:
                result = f"Unknown function: {function_call.name}"

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": function_call.call_id,
                    "output": result,
                }
            )

        with ts.span("create-followup-response"):
            response = openai_client.responses.create(
                model=model,
                input=tool_outputs,
                instructions=instructions,
                tools=tools,
                conversation={"id": conversation_id},
            )

    return final_text.strip()
