"""Create/update and run the declarative search-only multi-agent workflow."""

import argparse


DEFAULT_SCENARIO = "launch_incident_response"


def single_scenario(value):
    if value == "all":
        raise argparse.ArgumentTypeError(
            "Use one scenario at a time for the search-only workflow."
        )
    return value


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Single-entry search-only multi-agent demo: refresh the scenario "
            "agents and run the workflow."
        )
    )
    parser.add_argument(
        "--config",
        default="multi_agent/workflow.yaml",
        help="Path to the declarative multi-agent workflow YAML.",
    )
    parser.add_argument(
        "--scenario",
        type=single_scenario,
        default=DEFAULT_SCENARIO,
        help=(
            "Scenario key to run. Defaults to launch_incident_response for a "
            "one-command demo."
        ),
    )
    parser.add_argument(
        "--question",
        help="Override the scenario's default sample question.",
    )
    return parser.parse_args(argv)


def main():
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential

    from foundry_multi_agent_runtime import WorkshopMultiAgentRuntime
    from foundry_trace import configure_foundry_tracing
    from scripts_15_shared import (
        ensure_search_only_workflow_agents,
        get_agent,
        load_yaml,
        resolve_config_path,
        run_prompt_agent_step,
    )

    args = parse_args()
    runtime = WorkshopMultiAgentRuntime(require_fabric=False)
    config_path = resolve_config_path(runtime, args.config)

    workflow_config = load_yaml(config_path)
    if args.scenario not in workflow_config["scenarios"]:
        raise ValueError(f"Unknown scenario: {args.scenario}")

    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        endpoint=runtime.project_endpoint, credential=credential)
    openai_client = project_client.get_openai_client()

    trace_session = configure_foundry_tracing(
        project_client=project_client,
        scenario_name="15b_test_multi_agent_search_only_workflow",
        service_name="e2e-ms-foundry-workshop.multi-agent-search-test",
    )

    if trace_session.enabled:
        print("追蹤：已啟用")
    elif trace_session.warning:
        print(f"追蹤：{trace_session.warning}")

    with project_client:
        _, ids_config = ensure_search_only_workflow_agents(
            project_client=project_client,
            runtime=runtime,
            workflow_config=workflow_config,
            config_path=config_path,
            scenario_keys=[args.scenario],
            trace_session=trace_session,
        )

        if args.scenario not in ids_config.get("scenarios", {}):
            raise ValueError(
                f"Scenario '{args.scenario}' has no search-only agent metadata after refresh."
            )

        scenario = workflow_config["scenarios"][args.scenario]
        scenario_ids = ids_config["scenarios"][args.scenario]["agents"]
        question = args.question or scenario["sample_question"]

        context = {
            "scenario_title": scenario["title"],
            "scenario_description": scenario["description"],
            "document_focus": scenario["document_focus"],
            "data_focus": scenario["data_focus"],
            "question": question,
            "runtime_mode": "search-only",
        }

        print("Runtime mode: search-only")

        outputs = {}

        for step in workflow_config["workflow_steps"]:
            step_id = step["id"]
            agent_key = step["agent"]
            prompt = step["prompt_template"].format(**context, **outputs)

            agent_record = scenario_ids[agent_key]
            with trace_session.span("get-agent"):
                agent = get_agent(project_client, agent_record, trace_session=trace_session)
            definition = agent.versions["latest"]["definition"]
            with trace_session.span("create-conversation"):
                conversation = openai_client.conversations.create()

            print("\n" + "=" * 60)
            print(f"Step: {step_id} ({agent_key})")
            print("=" * 60)
            with trace_session.span(f"workflow-step-{step_id}"):
                result = run_prompt_agent_step(
                    openai_client=openai_client,
                    definition=definition,
                    conversation_id=conversation.id,
                    message=prompt,
                    runtime=runtime,
                    trace_session=trace_session,
                )
            outputs[step_id] = result
            print(result or "(no content returned)")

    print("\n" + "=" * 60)
    print("Final multi-agent answer")
    print("=" * 60)
    print(outputs.get("final_answer", "(final answer missing)"))


if __name__ == "__main__":
    main()
