"""Run the declarative multi-agent workshop workflow for one scenario."""

import argparse
import json
from pathlib import Path

import yaml
from azure.ai.projects import AIProjectClient
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
        required=True,
        help="Scenario key to run.",
    )
    parser.add_argument(
        "--question",
        help="Override the scenario's default sample question.",
    )
    return parser.parse_args()


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_ids(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def run_prompt_agent_step(openai_client, definition, conversation_id, message, runtime):
    model = definition["model"]
    instructions = definition["instructions"]
    tools = definition.get("tools", [])

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
                result = runtime.search_documents(
                    query=arguments.get("query", ""),
                    top=arguments.get("top"),
                )
            elif function_call.name == "execute_sql":
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

        response = openai_client.responses.create(
            model=model,
            input=tool_outputs,
            instructions=instructions,
            tools=tools,
            conversation={"id": conversation_id},
        )

    return final_text.strip()


def main():
    args = parse_args()
    runtime = WorkshopMultiAgentRuntime()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = runtime.project_root / config_path

    workflow_config = load_yaml(config_path)
    if args.scenario not in workflow_config["scenarios"]:
        raise ValueError(f"Unknown scenario: {args.scenario}")

    ids_path = runtime.ids_output_path()
    if not ids_path.exists():
        raise ValueError(
            f"{ids_path} not found. Run scripts/14_create_multi_agent_workflow.py first."
        )

    ids_config = load_ids(ids_path)
    if args.scenario not in ids_config.get("scenarios", {}):
        raise ValueError(
            f"Scenario '{args.scenario}' has no created agent metadata. Run the create script for this scenario first."
        )

    scenario = workflow_config["scenarios"][args.scenario]
    scenario_ids = ids_config["scenarios"][args.scenario]["agents"]
    question = args.question or scenario["sample_question"]

    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        endpoint=runtime.project_endpoint, credential=credential)
    openai_client = project_client.get_openai_client()

    context = {
        "scenario_title": scenario["title"],
        "scenario_description": scenario["description"],
        "document_focus": scenario["document_focus"],
        "data_focus": scenario["data_focus"],
        "question": question,
    }

    outputs = {}

    with project_client:
        for step in workflow_config["workflow_steps"]:
            step_id = step["id"]
            agent_key = step["agent"]
            prompt = step["prompt_template"].format(**context, **outputs)

            agent_record = scenario_ids[agent_key]
            agent = project_client.agents.get(agent_record["id"])
            definition = agent.versions["latest"]["definition"]
            conversation = openai_client.conversations.create()

            print("\n" + "=" * 60)
            print(f"Step: {step_id} ({agent_key})")
            print("=" * 60)
            result = run_prompt_agent_step(
                openai_client=openai_client,
                definition=definition,
                conversation_id=conversation.id,
                message=prompt,
                runtime=runtime,
            )
            outputs[step_id] = result
            print(result or "(no content returned)")

    print("\n" + "=" * 60)
    print("Final multi-agent answer")
    print("=" * 60)
    print(outputs.get("final_answer", "(final answer missing)"))


if __name__ == "__main__":
    main()
