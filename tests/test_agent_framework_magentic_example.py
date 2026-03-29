import argparse
import importlib.util
import os
import sys
import types
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
SCRIPT_PATH = SCRIPTS_DIR / "16b_agent_framework_magentic_example.py"


def load_script_module(module_name: str):
    sys.path.insert(0, str(SCRIPTS_DIR))
    spec = importlib.util.spec_from_file_location(module_name, SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:  # pragma: no cover - defensive guard
        raise RuntimeError("Failed to load script module")
    spec.loader.exec_module(module)
    return module


class FakeDefaultAzureCredential:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeAzureAIClient:
    calls = []
    closed = 0

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        FakeAzureAIClient.calls.append(kwargs)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        FakeAzureAIClient.closed += 1
        return False


class FakeAgent:
    calls = []

    def __init__(self, client, instructions, *, name, description=None, **kwargs):
        self.client = client
        self.instructions = instructions
        self.name = name
        self.description = description
        self.kwargs = kwargs
        FakeAgent.calls.append(self)


class FakeMagenticProgressLedger:
    def to_dict(self):
        return {"status": "planning"}


class FakeMessage:
    def __init__(self, text):
        self.text = text


class FakeEvent:
    def __init__(self, event_type, data, executor_id=None):
        self.type = event_type
        self.data = data
        self.executor_id = executor_id


class FakeAgentResponseUpdate:
    def __init__(self, text, message_id):
        self.text = text
        self.message_id = message_id

    def __str__(self):
        return self.text


class FakeWorkflow:
    def run(self, task, stream=False):
        if not task:
            raise AssertionError("expected task")
        if not stream:
            raise AssertionError("expected stream=True")

        async def _generator():
            yield FakeEvent(
                "magentic_orchestrator",
                types.SimpleNamespace(event_type=types.SimpleNamespace(name="PLAN_CREATED"), content=FakeMessage("plan")),
            )
            yield FakeEvent("output", FakeAgentResponseUpdate("ops draft", "m1"), executor_id="queue-ops-agent")
            yield FakeEvent(
                "magentic_orchestrator",
                types.SimpleNamespace(event_type=types.SimpleNamespace(name="LEDGER_UPDATED"), content=FakeMagenticProgressLedger()),
            )
            yield FakeEvent(
                "output",
                [types.SimpleNamespace(text="final answer")],
                executor_id="triage-manager-agent",
            )

        return _generator()


class FakeMagenticBuilder:
    call = None

    def __init__(self, **kwargs):
        FakeMagenticBuilder.call = kwargs

    def build(self):
        return FakeWorkflow()


class AgentFrameworkMagenticExampleTests(unittest.IsolatedAsyncioTestCase):
    def test_module_defaults_and_instructions_are_traditional_chinese(self):
        fake_agent_framework = types.ModuleType("agent_framework")
        fake_agent_framework.Agent = FakeAgent
        fake_agent_framework.AgentResponseUpdate = FakeAgentResponseUpdate
        fake_agent_framework.Message = FakeMessage
        fake_agent_framework.WorkflowEvent = FakeEvent

        fake_agent_framework_azure = types.ModuleType("agent_framework.azure")
        fake_agent_framework_azure.AzureAIClient = FakeAzureAIClient

        fake_agent_framework_orchestrations = types.ModuleType("agent_framework.orchestrations")
        fake_agent_framework_orchestrations.MagenticBuilder = FakeMagenticBuilder
        fake_agent_framework_orchestrations.MagenticProgressLedger = FakeMagenticProgressLedger

        fake_azure = types.ModuleType("azure")
        fake_azure_identity = types.ModuleType("azure.identity")
        fake_azure_identity_aio = types.ModuleType("azure.identity.aio")
        fake_azure_identity_aio.DefaultAzureCredential = FakeDefaultAzureCredential

        fake_load_env = types.ModuleType("load_env")
        fake_load_env.load_all_env = lambda: None

        with patch.dict(
            sys.modules,
            {
                "agent_framework": fake_agent_framework,
                "agent_framework.azure": fake_agent_framework_azure,
                "agent_framework.orchestrations": fake_agent_framework_orchestrations,
                "azure": fake_azure,
                "azure.identity": fake_azure_identity,
                "azure.identity.aio": fake_azure_identity_aio,
                "load_env": fake_load_env,
            },
        ):
            module = load_script_module("agent_framework_magentic_example_defaults")

        self.assertIn("客服", module.DEFAULT_QUESTION)
        self.assertIn("你的工作", module.TRIAGE_MANAGER_INSTRUCTIONS)
        self.assertIn("營運", module.QUEUE_OPS_INSTRUCTIONS)
        self.assertIn("對客", module.CUSTOMER_COMMS_INSTRUCTIONS)

    async def test_main_builds_magentic_workflow_with_azure_ai_clients(self):
        FakeAzureAIClient.calls.clear()
        FakeAzureAIClient.closed = 0
        FakeAgent.calls.clear()
        FakeMagenticBuilder.call = None

        fake_agent_framework = types.ModuleType("agent_framework")
        fake_agent_framework.Agent = FakeAgent
        fake_agent_framework.AgentResponseUpdate = FakeAgentResponseUpdate
        fake_agent_framework.Message = FakeMessage
        fake_agent_framework.WorkflowEvent = FakeEvent

        fake_agent_framework_azure = types.ModuleType("agent_framework.azure")
        fake_agent_framework_azure.AzureAIClient = FakeAzureAIClient

        fake_agent_framework_orchestrations = types.ModuleType("agent_framework.orchestrations")
        fake_agent_framework_orchestrations.MagenticBuilder = FakeMagenticBuilder
        fake_agent_framework_orchestrations.MagenticProgressLedger = FakeMagenticProgressLedger

        fake_azure = types.ModuleType("azure")
        fake_azure_identity = types.ModuleType("azure.identity")
        fake_azure_identity_aio = types.ModuleType("azure.identity.aio")
        fake_azure_identity_aio.DefaultAzureCredential = FakeDefaultAzureCredential

        fake_load_env = types.ModuleType("load_env")
        fake_load_env.load_all_env = lambda: None

        with patch.dict(
            sys.modules,
            {
                "agent_framework": fake_agent_framework,
                "agent_framework.azure": fake_agent_framework_azure,
                "agent_framework.orchestrations": fake_agent_framework_orchestrations,
                "azure": fake_azure,
                "azure.identity": fake_azure_identity,
                "azure.identity.aio": fake_azure_identity_aio,
                "load_env": fake_load_env,
            },
        ):
            module = load_script_module("agent_framework_magentic_example")

        with patch.dict(
            os.environ,
            {
                "AZURE_AI_PROJECT_ENDPOINT": "https://example.services.ai.azure.com/api/projects/demo",
                "AZURE_AI_MODEL_DEPLOYMENT_NAME": "gpt-4.1-mini",
            },
            clear=False,
        ), patch.object(
            module,
            "parse_args",
            return_value=argparse.Namespace(
                question="Create a short response package for a premium support queue incident."
            ),
        ), patch("sys.stdout", new=StringIO()) as stdout:
            await module.main()

        self.assertEqual(len(FakeAzureAIClient.calls), 3)
        self.assertEqual(FakeAzureAIClient.closed, 3)
        self.assertEqual(len(FakeAgent.calls), 3)
        for call in FakeAzureAIClient.calls:
            self.assertIn("credential", call)
            self.assertNotIn("async_credential", call)
            self.assertEqual(
                call["project_endpoint"],
                "https://example.services.ai.azure.com/api/projects/demo",
            )
            self.assertEqual(call["model_deployment_name"], "gpt-4.1-mini")

        self.assertEqual(
            [agent.name for agent in FakeAgent.calls],
            ["triage-manager-agent", "queue-ops-agent", "customer-comms-agent"],
        )
        self.assertEqual(
            [agent.name for agent in FakeMagenticBuilder.call["participants"]],
            ["queue-ops-agent", "customer-comms-agent"],
        )
        self.assertEqual(FakeMagenticBuilder.call["manager_agent"].name, "triage-manager-agent")
        self.assertTrue(FakeMagenticBuilder.call["intermediate_outputs"])
        self.assertIn("final answer", stdout.getvalue())
        self.assertIn("=== 最終答案 ===", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()