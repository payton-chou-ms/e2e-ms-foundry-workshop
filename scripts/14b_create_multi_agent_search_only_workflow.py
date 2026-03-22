"""在 Foundry 中建立各情境的 search-only 多代理工作流定義。"""

import argparse
import json
import random
import re
import string
from datetime import datetime, timezone
from pathlib import Path

import yaml
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential

from foundry_multi_agent_runtime import WorkshopMultiAgentRuntime


OUTPUT_FILE_NAME = "multi_agent_search_ids.json"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="multi_agent/workflow.yaml",
        help="宣告式多代理工作流 YAML 的路徑。",
    )
    parser.add_argument(
        "--scenario",
        default="all",
        help="要建立的 scenario key。輸入 'all' 代表建立 YAML 中所有 scenario。",
    )
    return parser.parse_args()


def load_workflow_config(config_path):
    with open(config_path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def sanitize_agent_name(value):
    lowered = value.lower().replace("_", "-")
    lowered = re.sub(r"[^a-z0-9-]", "-", lowered)
    lowered = re.sub(r"-+", "-", lowered).strip("-")
    return lowered[:60]


def make_short_prefix(length=3):
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def abbreviate(key):
    """Turn 'policy_gap_analysis' -> 'pga', 'planner' -> 'pln'."""
    parts = key.replace("-", "_").split("_")
    if len(parts) > 1:
        return "".join(p[0] for p in parts if p)
    return key[:3]


def get_effective_tool_mode(tool_mode):
    if tool_mode in {"sql", "both"}:
        return "search"
    return tool_mode


def build_instruction_context(runtime, scenario):
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


def create_or_replace_agent(project_client, agent_name, definition, description):
    try:
        existing = project_client.agents.get(agent_name)
    except Exception:
        existing = None

    if existing:
        project_client.agents.delete(agent_name)

    return project_client.agents.create_version(
        agent_name=agent_name,
        definition=definition,
        description=description,
    )


def main():
    args = parse_args()
    runtime = WorkshopMultiAgentRuntime(require_fabric=False)
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = runtime.project_root / config_path

    workflow_config = load_workflow_config(config_path)
    scenarios = workflow_config["scenarios"]
    agent_templates = workflow_config["agent_templates"]
    model = runtime.ontology_config.get("chat_model") or None

    selected_scenarios = scenarios.keys() if args.scenario == "all" else [
        args.scenario]
    missing = [key for key in selected_scenarios if key not in scenarios]
    if missing:
        raise ValueError(f"未知的 scenario：{', '.join(missing)}")

    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        endpoint=runtime.project_endpoint, credential=credential)

    output = {
        "workflow_name": workflow_config["workflow_name"],
        "config_path": str(config_path.relative_to(runtime.project_root)),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "runtime_mode": "search-only",
        "scenarios": {},
    }

    prefix = make_short_prefix()

    with project_client:
        for scenario_key in selected_scenarios:
            scenario = scenarios[scenario_key]
            context = build_instruction_context(runtime, scenario)
            output["scenarios"][scenario_key] = {
                "title": scenario["title"],
                "agents": {},
            }

            print("\n" + "=" * 60)
            print(
                f"正在為 scenario 建立 search-only 多代理組合：{scenario_key}")
            print("=" * 60)
            print("執行模式：search-only")

            for agent_key, template in agent_templates.items():
                requested_tool_mode = template["tool_mode"]
                tool_mode = get_effective_tool_mode(requested_tool_mode)
                agent_name = sanitize_agent_name(
                    f"{prefix}-{abbreviate(scenario_key)}-{abbreviate(template['display_name_suffix'])}-s"
                )
                instructions = template["instructions_template"].format(
                    **context)
                tools = runtime.build_tools_for_mode(tool_mode)
                definition = PromptAgentDefinition(
                    model=model or "gpt-5.4-mini",
                    instructions=instructions,
                    tools=tools,
                )

                agent = create_or_replace_agent(
                    project_client=project_client,
                    agent_name=agent_name,
                    definition=definition,
                    description=f"{scenario['title']} - {agent_key}（search-only）",
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
                        f"[OK] {agent_key}: {agent.name} ({agent.id}) [由 {requested_tool_mode} 改為 search-only fallback]"
                    )
                else:
                    print(f"[OK] {agent_key}: {agent.name} ({agent.id})")

    output_path = runtime.ids_output_path(OUTPUT_FILE_NAME)
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2)

    print("\n已把 search-only 多代理中繼資料寫入：")
    print(f"  {output_path}")


if __name__ == "__main__":
    main()
