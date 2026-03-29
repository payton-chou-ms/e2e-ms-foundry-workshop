"""Optional tracing utilities for Foundry workshop scripts.

Tracing is intentionally best-effort. Missing packages, unavailable
Application Insights wiring, or preview feature changes should never block the
main workshop flow.
"""

from contextlib import nullcontext
from dataclasses import dataclass
import os


_TRACE_INITIALIZED = False


def _looks_like_connection_string(value):
    if not value:
        return False

    parts = [part.strip() for part in value.split(";") if part.strip()]
    if not parts:
        return False

    return all("=" in part for part in parts)


def _resolve_connection_string(project_client):
    connection_string = (
        os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
        or os.getenv("AZURE_APPINSIGHTS_CONNECTION_STRING")
    )

    if connection_string:
        return connection_string, None

    try:
        connection_string = project_client.telemetry.get_application_insights_connection_string()
    except Exception as exc:
        return None, (
            "Tracing requested but the project telemetry connection string "
            f"could not be resolved: {exc}"
        )

    if not connection_string:
        return None, (
            "Tracing requested but no Application Insights connection string "
            "is available for this project."
        )

    if not _looks_like_connection_string(connection_string):
        return None, (
            "Tracing requested but the resolved telemetry value does not look "
            "like a connection string."
        )

    return connection_string, None



def _env_flag(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class TraceSession:
    enabled: bool
    tracer: object | None = None
    connection_string: str | None = None
    warning: str | None = None

    def span(self, name):
        if self.enabled and self.tracer:
            return self.tracer.start_as_current_span(name)

        return nullcontext()



def configure_foundry_tracing(project_client, scenario_name, service_name):
    """Enable SDK tracing when explicitly requested via environment variables."""

    global _TRACE_INITIALIZED

    if not _env_flag("ENABLE_FOUNDRY_TRACING"):
        return TraceSession(enabled=False)

    os.environ.setdefault("AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING", "true")
    os.environ.setdefault("OTEL_SERVICE_NAME", service_name)

    if _env_flag("ENABLE_FOUNDRY_CONTENT_TRACING"):
        os.environ.setdefault("AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED", "true")
        os.environ.setdefault("OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT", "true")

    connection_string, warning = _resolve_connection_string(project_client)
    if warning:
        return TraceSession(
            enabled=False,
            warning=warning,
        )

    try:
        from azure.monitor.opentelemetry import configure_azure_monitor
        from azure.ai.projects.telemetry import AIProjectInstrumentor
        from opentelemetry import trace

        configure_azure_monitor(connection_string=connection_string)

        if not _TRACE_INITIALIZED:
            AIProjectInstrumentor().instrument(
                enable_trace_context_propagation=_env_flag("ENABLE_TRACE_CONTEXT_PROPAGATION")
            )
            _TRACE_INITIALIZED = True

        tracer = trace.get_tracer(scenario_name)
        return TraceSession(enabled=True, tracer=tracer, connection_string=connection_string)
    except Exception as exc:
        return TraceSession(
            enabled=False,
            warning=f"Tracing requested but instrumentation failed: {exc}",
        )
