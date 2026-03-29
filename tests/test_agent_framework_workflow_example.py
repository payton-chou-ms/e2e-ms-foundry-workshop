import argparse
import importlib.util
import os
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
SCRIPT_PATH = SCRIPTS_DIR / "16_agent_framework_workflow_example.py"


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


class FakeAgentContext:
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeAzureAIClient:
    calls = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        FakeAzureAIClient.calls.append(kwargs)

    def as_agent(self, name: str, instructions: str):
        return FakeAgentContext(name=name, instructions=instructions)


class FakeStream:
    def __init__(self):
        self._updates = [types.SimpleNamespace(text="workflow ok")]

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self._updates:
            raise StopAsyncIteration
        return self._updates.pop(0)

    async def get_final_response(self):
        return types.SimpleNamespace(text="workflow ok")


class FakeWorkflowAgent:
    def run(self, question: str, stream: bool = False):
        if not question:
            raise AssertionError("expected question")
        if not stream:
            raise AssertionError("expected streaming mode")
        return FakeStream()


class FakeWorkflow:
    def as_agent(self, name: str):
        if name != "mini-policy-workflow":
            raise AssertionError("unexpected workflow name")
        return FakeWorkflowAgent()


class FakeWorkflowBuilder:
    def __init__(self, start_executor):
        self.start_executor = start_executor
        self.edges = []

    def add_edge(self, source, target):
        self.edges.append((source, target))
        return self

    def build(self):
        if len(self.edges) != 1:
            raise AssertionError("expected a single workflow edge")
        return FakeWorkflow()


class AgentFrameworkWorkflowExampleTests(unittest.IsolatedAsyncioTestCase):
    async def test_main_passes_credential_to_azure_ai_client(self):
        FakeAzureAIClient.calls.clear()

        fake_agent_framework = types.ModuleType("agent_framework")
        fake_agent_framework.WorkflowBuilder = FakeWorkflowBuilder
        fake_agent_framework_azure = types.ModuleType("agent_framework.azure")
        fake_agent_framework_azure.AzureAIClient = FakeAzureAIClient
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
                "azure": fake_azure,
                "azure.identity": fake_azure_identity,
                "azure.identity.aio": fake_azure_identity_aio,
                "load_env": fake_load_env,
            },
        ):
            module = load_script_module("agent_framework_workflow_example")

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
            return_value=argparse.Namespace(question="Summarize the policy risk and next step."),
        ):
            await module.main()

        self.assertEqual(len(FakeAzureAIClient.calls), 2)
        for call in FakeAzureAIClient.calls:
            self.assertIn("credential", call)
            self.assertNotIn("async_credential", call)
            self.assertEqual(
                call["project_endpoint"],
                "https://example.services.ai.azure.com/api/projects/demo",
            )
            self.assertEqual(call["model_deployment_name"], "gpt-4.1-mini")


if __name__ == "__main__":
    unittest.main()