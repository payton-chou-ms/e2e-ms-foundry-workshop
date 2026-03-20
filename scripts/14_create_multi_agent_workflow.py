"""Create scenario-specific multi-agent workflow definitions in Foundry."""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential

from foundry_multi_agent_runtime import WorkshopMultiAgentRuntime


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="multi_agent/workflow.yaml",
        help="Path to the declarative multi-agent workflow YAML.",
    )
    parser.add_argument(
        "--scenario",
        default="all",
        help="Scenario key to create. Use 'all' to create every scenario in the YAML.",
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


def build_instruction_context(runtime, scenario):
    return {
        "solution_name": runtime.solution_name,
        "domain_name": runtime.ontology_config.get("name", "Business Data"),
        "domain_description": runtime.ontology_config.get("description", ""),
        "table_list": ", ".join(runtime.tables) or "No tables discovered",
        "schema_prompt": runtime.schema_prompt.strip() or "Schema prompt unavailable.",
        "scenario_title": scenario["title"],
        "scenario_description": scenario["description"],
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
    runtime = WorkshopMultiAgentRuntime()
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
        raise ValueError(f"Unknown scenarios: {', '.join(missing)}")

    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        endpoint=runtime.project_endpoint, credential=credential)

    output = {
        "workflow_name": workflow_config["workflow_name"],
        "config_path": str(config_path.relative_to(runtime.project_root)),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "scenarios": {},
    }

    with project_client:
        for scenario_key in selected_scenarios:
            scenario = scenarios[scenario_key]
            context = build_instruction_context(runtime, scenario)
            output["scenarios"][scenario_key] = {
                "title": scenario["title"],
                "agents": {},
            }

            print("\n" + "=" * 60)
            print(f"Creating multi-agent set for scenario: {scenario_key}")
            print("=" * 60)

            for agent_key, template in agent_templates.items():
                agent_name = sanitize_agent_name(
                    f"{runtime.solution_name}-{scenario_key}-{template['display_name_suffix']}"
                )
                instructions = template["instructions_template"].format(
                    **context)
                tools = runtime.build_tools_for_mode(template["tool_mode"])
                definition = PromptAgentDefinition(
                    model=model or "gpt-5.4-mini",
                    instructions=instructions,
                    tools=tools,
                )

                agent = create_or_replace_agent(
                    project_client=project_client,
                    agent_name=agent_name,
                    definition=definition,
                    description=f"{scenario['title']} - {agent_key}",
                )

                output["scenarios"][scenario_key]["agents"][agent_key] = {
                    "id": agent.id,
                    "name": agent.name,
                    "version": agent.version,
                    "tool_mode": template["tool_mode"],
                }
                print(f"[OK] {agent_key}: {agent.name} ({agent.id})")

    output_path = runtime.ids_output_path()
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2)

    print("\nSaved multi-agent metadata to:")
    print(f"  {output_path}")


if __name__ == "__main__":
    main()
