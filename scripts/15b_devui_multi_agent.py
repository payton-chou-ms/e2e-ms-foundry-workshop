"""15b DevUI - Launch the P2P multi-agent workflow via Agent Framework DevUI.

Wraps the declarative multi-agent search-only workflow as Agent Framework
agents in a sequential WorkflowBuilder and serves it via DevUI web UI.

Prerequisites:
    pip install --pre agent-framework-devui \
        "agent-framework-core>=1.0.0" \
        "agent-framework-openai>=1.0.0"

Run:
    python scripts/15b_devui_multi_agent.py
    python scripts/15b_devui_multi_agent.py \
        --config data/p2p/multi_agent/p2p_workflow.yaml \
        --scenario p2p_invoice_verification
    python scripts/15b_devui_multi_agent.py --port 9090
"""

import argparse
import os
import sys

# Ensure scripts/ is on the import path for local helpers.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_framework import Agent, Executor, WorkflowBuilder, WorkflowContext, handler
from agent_framework._workflows._agent_executor import AgentExecutorResponse
from agent_framework.devui import serve
from agent_framework.openai import OpenAIChatClient
from azure.identity.aio import DefaultAzureCredential

from foundry_multi_agent_runtime import WorkshopMultiAgentRuntime
from scripts_15_shared import (
    build_search_only_instruction_context,
    load_yaml,
    resolve_config_path,
    search_only_tool_mode,
)


DEFAULT_CONFIG = "data/p2p/multi_agent/p2p_workflow.yaml"
DEFAULT_SCENARIO = "p2p_invoice_verification"


# ── Helper executors for DevUI-friendly workflow topology ───────────

class _TextGateway(Executor):
    """Accepts a plain str so DevUI shows a simple text box."""

    @handler
    async def handle(self, message: str, ctx: WorkflowContext[str]) -> None:
        await ctx.send_message(message)


class _SpecialistCollector(Executor):
    """Collects outputs from N parallel specialists, then forwards one
    combined message to the coordinator."""

    def __init__(self, expected: int, labels: list[str], **kwargs):
        super().__init__(**kwargs)
        self._expected = expected
        self._labels = labels
        self._buffer: list[str] = []

    @handler
    async def handle(self, msg: AgentExecutorResponse, ctx: WorkflowContext[str]) -> None:
        text = msg.agent_response.text or "(no content)"
        self._buffer.append(text)
        if len(self._buffer) >= self._expected:
            sections = []
            for i, result in enumerate(self._buffer):
                label = self._labels[i] if i < len(self._labels) else f"Specialist {i + 1}"
                sections.append(f"=== {label} ===\n{result}")
            combined = "\n\n".join(sections)
            self._buffer.clear()
            await ctx.send_message(combined)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Launch the multi-agent search-only workflow in DevUI."
    )
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG,
        help="Path to the declarative multi-agent workflow YAML.",
    )
    parser.add_argument(
        "--scenario",
        default=DEFAULT_SCENARIO,
        help="Scenario key to present in DevUI.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9090,
        help="Port for the DevUI web server (default: 9090).",
    )
    parser.add_argument(
        "--no-open",
        dest="auto_open",
        action="store_false",
        default=True,
        help="Do not automatically open the browser.",
    )
    parser.add_argument(
        "--question",
        help="Override the scenario's default sample question.",
    )
    return parser.parse_args(argv)


def _get_required_env(*names):
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    raise ValueError(f"Missing required env var. Tried: {', '.join(names)}")


def main():
    args = parse_args()

    # ── runtime & config ────────────────────────────────────────────
    runtime = WorkshopMultiAgentRuntime(require_fabric=False)
    config_path = resolve_config_path(runtime, args.config)
    workflow_config = load_yaml(config_path)

    if args.scenario not in workflow_config["scenarios"]:
        raise ValueError(
            f"Unknown scenario: {args.scenario}. "
            f"Available: {', '.join(workflow_config['scenarios'])}"
        )

    scenario = workflow_config["scenarios"][args.scenario]
    context = build_search_only_instruction_context(runtime, scenario)

    # ── Azure env ───────────────────────────────────────────────────
    azure_endpoint = _get_required_env(
        "AZURE_AI_ENDPOINT", "AZURE_OPENAI_ENDPOINT",
    )
    model = _get_required_env(
        "AZURE_CHAT_MODEL",
        "AZURE_AI_MODEL_DEPLOYMENT_NAME",
        "FOUNDRY_MODEL_DEPLOYMENT_NAME",
    )

    # ── tools ───────────────────────────────────────────────────────
    def search_documents(query: str) -> str:
        """在 Azure AI Search 中搜尋已索引的業務文件，回傳相關段落與來源。"""
        return runtime.search_documents(query=query)

    tool_map = {
        "search": [search_documents],
        "none": [],
    }

    # ── build Agent Framework agents from YAML templates ────────────
    credential = DefaultAzureCredential()
    agent_templates = workflow_config["agent_templates"]
    agents: dict[str, Agent] = {}

    for agent_key, template in agent_templates.items():
        tool_mode = search_only_tool_mode(template["tool_mode"])
        instructions = template["instructions_template"].format(**context)

        client = OpenAIChatClient(
            model=model,
            azure_endpoint=azure_endpoint,
            credential=credential,
        )

        agents[agent_key] = Agent(
            name=f"p2p-{template['display_name_suffix']}",
            description=f"{scenario['title']} — {agent_key}",
            instructions=instructions,
            client=client,
            tools=tool_map.get(tool_mode, []) or None,
        )

    # ── Build fan-out / fan-in DAG from workflow_steps ──────────────
    #
    # The YAML defines these steps:
    #   route_request        (router)
    #   contract_review      (contract_review_specialist)
    #   invoice_verification (invoice_verification_specialist)
    #   payment_guard        (payment_guard_specialist)
    #   final_answer         (coordinator)
    #
    # Topology:
    #   gate → router ─┬→ contract_review  ─┐
    #                   ├→ invoice_verify   ─┤→ collector → coordinator
    #                   └→ payment_guard   ─┘
    #
    steps = workflow_config["workflow_steps"]
    specialist_steps = [s for s in steps if s["id"] != steps[0]["id"] and s["id"] != steps[-1]["id"]]
    specialist_labels = [s["id"] for s in specialist_steps]

    text_gateway = _TextGateway(id="text-input")
    collector = _SpecialistCollector(
        expected=len(specialist_steps),
        labels=specialist_labels,
        id="collector",
    )

    router_agent = agents[steps[0]["agent"]]
    coordinator_agent = agents[steps[-1]["agent"]]

    builder = WorkflowBuilder(start_executor=text_gateway)
    builder.add_edge(text_gateway, router_agent)

    for spec_step in specialist_steps:
        spec_agent = agents[spec_step["agent"]]
        builder.add_edge(router_agent, spec_agent)
        builder.add_edge(spec_agent, collector)

    builder.add_edge(collector, coordinator_agent)

    workflow = builder.build()
    workflow.name = f"{workflow_config['workflow_name']}-search-only"

    # ── launch DevUI ────────────────────────────────────────────────
    question = args.question or scenario.get("sample_question", "")

    print(f"Scenario : {args.scenario} — {scenario['title']}")
    print(f"Agents   : {' → '.join(s['agent'] for s in steps)}")
    print(f"DevUI    : http://localhost:{args.port}")
    if question:
        print(f"\nSample question (paste into DevUI):\n  {question}")
    print()

    serve(
        entities=[workflow],
        port=args.port,
        auto_open=args.auto_open,
    )


if __name__ == "__main__":
    main()
