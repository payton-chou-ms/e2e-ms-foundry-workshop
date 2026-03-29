import importlib.util
import os
import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"


def load_shared_module(module_relative_path: str, module_name: str):
    sys.path.insert(0, str(SCRIPTS_DIR))
    module_path = SCRIPTS_DIR / module_relative_path
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:  # pragma: no cover - defensive guard
        raise RuntimeError(f"Failed to load {module_relative_path}")
    spec.loader.exec_module(module)
    return module


class FoundryTraceTests(unittest.TestCase):
    def test_configure_foundry_tracing_prefers_standard_app_insights_env_over_azd_env(self):
        module = load_shared_module("shared/foundry_trace.py", "shared_foundry_trace_precedence")
        tracer = object()
        configure_azure_monitor = Mock()
        instrumentor = Mock()
        project_client = SimpleNamespace(
            telemetry=SimpleNamespace(get_application_insights_connection_string=Mock())
        )

        fake_modules = {
            "azure.monitor.opentelemetry": types.SimpleNamespace(
                configure_azure_monitor=configure_azure_monitor
            ),
            "azure.ai.projects.telemetry": types.SimpleNamespace(
                AIProjectInstrumentor=Mock(return_value=instrumentor)
            ),
            "opentelemetry": types.SimpleNamespace(
                trace=types.SimpleNamespace(get_tracer=Mock(return_value=tracer))
            ),
        }

        with patch.dict(
            os.environ,
            {
                "ENABLE_FOUNDRY_TRACING": "true",
                "APPLICATIONINSIGHTS_CONNECTION_STRING": (
                    "InstrumentationKey=standard-key;"
                    "IngestionEndpoint=https://standard.applicationinsights.azure.com/"
                ),
                "AZURE_APPINSIGHTS_CONNECTION_STRING": (
                    "InstrumentationKey=azd-key;"
                    "IngestionEndpoint=https://azd.applicationinsights.azure.com/"
                ),
            },
            clear=True,
        ):
            with patch.dict(sys.modules, fake_modules, clear=False):
                session = module.configure_foundry_tracing(
                    project_client=project_client,
                    scenario_name="scenario-name",
                    service_name="service-name",
                )

        self.assertTrue(session.enabled)
        self.assertEqual(
            session.connection_string,
            (
                "InstrumentationKey=standard-key;"
                "IngestionEndpoint=https://standard.applicationinsights.azure.com/"
            ),
        )
        project_client.telemetry.get_application_insights_connection_string.assert_not_called()

    def test_configure_foundry_tracing_prefers_azd_connection_string_env(self):
        module = load_shared_module("shared/foundry_trace.py", "shared_foundry_trace_env")
        tracer = object()
        configure_azure_monitor = Mock()
        instrumentor = Mock()
        project_client = SimpleNamespace(
            telemetry=SimpleNamespace(get_application_insights_connection_string=Mock())
        )

        fake_modules = {
            "azure.monitor.opentelemetry": types.SimpleNamespace(
                configure_azure_monitor=configure_azure_monitor
            ),
            "azure.ai.projects.telemetry": types.SimpleNamespace(
                AIProjectInstrumentor=Mock(return_value=instrumentor)
            ),
            "opentelemetry": types.SimpleNamespace(
                trace=types.SimpleNamespace(get_tracer=Mock(return_value=tracer))
            ),
        }

        with patch.dict(
            os.environ,
            {
                "ENABLE_FOUNDRY_TRACING": "true",
                "AZURE_APPINSIGHTS_CONNECTION_STRING": (
                    "InstrumentationKey=test-key;"
                    "IngestionEndpoint=https://example.applicationinsights.azure.com/"
                ),
            },
            clear=True,
        ):
            with patch.dict(sys.modules, fake_modules, clear=False):
                session = module.configure_foundry_tracing(
                    project_client=project_client,
                    scenario_name="scenario-name",
                    service_name="service-name",
                )

        self.assertTrue(session.enabled)
        self.assertIs(session.tracer, tracer)
        self.assertEqual(
            session.connection_string,
            (
                "InstrumentationKey=test-key;"
                "IngestionEndpoint=https://example.applicationinsights.azure.com/"
            ),
        )
        configure_azure_monitor.assert_called_once_with(
            connection_string=(
                "InstrumentationKey=test-key;"
                "IngestionEndpoint=https://example.applicationinsights.azure.com/"
            )
        )
        instrumentor.instrument.assert_called_once_with(
            enable_trace_context_propagation=False
        )
        project_client.telemetry.get_application_insights_connection_string.assert_not_called()

    def test_configure_foundry_tracing_rejects_non_connection_string_values(self):
        module = load_shared_module("shared/foundry_trace.py", "shared_foundry_trace_invalid")
        project_client = SimpleNamespace(
            telemetry=SimpleNamespace(
                get_application_insights_connection_string=Mock(
                    return_value="appi-dadq4sqofepi64"
                )
            )
        )

        with patch.dict(
            os.environ,
            {
                "ENABLE_FOUNDRY_TRACING": "true",
            },
            clear=True,
        ):
            session = module.configure_foundry_tracing(
                project_client=project_client,
                scenario_name="scenario-name",
                service_name="service-name",
            )

        self.assertFalse(session.enabled)
        self.assertIn("does not look like a connection string", session.warning)


if __name__ == "__main__":
    unittest.main()