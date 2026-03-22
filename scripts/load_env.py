"""
Load environment variables from azd deployment and project .env file.

This module provides a unified way to load configuration:
1. Azure service settings from azd environment (.azure/<env>/.env)
2. Project-specific settings from project root .env (Fabric, industry, etc.)

Azure services (from azd):
    - AZURE_AI_PROJECT_ENDPOINT
    - AZURE_AI_ENDPOINT
    - AZURE_OPENAI_ENDPOINT
    - AZURE_AI_SEARCH_ENDPOINT
    - AZURE_STORAGE_BLOB_ENDPOINT
    - AZURE_CHAT_MODEL
    - AZURE_EMBEDDING_MODEL
    - etc.

Project settings (from .env):
    - FABRIC_WORKSPACE_ID
    - SOLUTION_NAME
    - INDUSTRY
    - USECASE
    - DATA_SIZE
    - DATA_FOLDER
    - FOUNDRY_AGENT_ID
    - etc.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv


def _env_file_has_core_azure_values(env_path: Path) -> bool:
    """Return True when an azd env file contains deployed Azure endpoint values."""
    try:
        content = env_path.read_text(encoding="utf-8")
    except OSError:
        return False

    core_keys = (
        "AZURE_AI_PROJECT_ENDPOINT=",
        "AZURE_AI_SEARCH_ENDPOINT=",
        "AZURE_AI_ENDPOINT=",
    )
    return any(key in content for key in core_keys)


def load_azd_env():
    """
    Load environment variables from azd deployment.

    Reads from .azure/<defaultEnvironment>/.env
    Returns True if azd env was found and loaded.
    """
    script_dir = Path(__file__).parent
    azure_dir = script_dir.parent / ".azure"

    shell_env_name = os.environ.get("AZURE_ENV_NAME", "").strip()
    default_env_name = ""
    if (azure_dir / "config.json").exists():
        with open(azure_dir / "config.json") as f:
            config = json.load(f)
            default_env_name = config.get("defaultEnvironment", "").strip()

    candidate_env_names = []
    if shell_env_name:
        candidate_env_names.append(shell_env_name)
    if default_env_name and default_env_name not in candidate_env_names:
        candidate_env_names.append(default_env_name)

    fallback_env_name = ""
    fallback_env_path = None

    for env_name in candidate_env_names:
        env_path = azure_dir / env_name / ".env"
        if env_path.exists():
            if fallback_env_path is None:
                fallback_env_name = env_name
                fallback_env_path = env_path

            if not _env_file_has_core_azure_values(env_path):
                continue

            load_dotenv(env_path)
            os.environ["AZURE_ENV_NAME"] = env_name
            return True

    if fallback_env_path is not None:
        load_dotenv(fallback_env_path)
        os.environ["AZURE_ENV_NAME"] = fallback_env_name
        return True

    return False


def load_project_env():
    """
    Load environment variables from project root .env file.

    Contains Fabric-specific and project settings.
    """
    script_dir = Path(__file__).parent
    project_env = script_dir.parent / ".env"

    if project_env.exists():
        load_dotenv(project_env, override=False)  # Don't override azd values
        return True

    return False


def load_all_env():
    """
    Load both azd and project environment variables.

    Priority:
    1. azd environment (Azure service endpoints)
    2. Project .env (Fabric, industry settings)

    Returns tuple (azd_loaded, project_loaded)
    """
    azd_loaded = load_azd_env()
    project_loaded = load_project_env()

    return azd_loaded, project_loaded


def get_required_env(var_name: str, description: str = None) -> str:
    """
    Get a required environment variable or raise an error.

    Args:
        var_name: Environment variable name
        description: Human-readable description for error message

    Returns:
        The environment variable value

    Raises:
        ValueError: If variable is not set
    """
    value = os.environ.get(var_name)
    if not value:
        desc = description or var_name
        raise ValueError(
            f"{var_name} not set. {desc}\n"
            f"Run 'azd up' to deploy Azure resources or configure in .env"
        )
    return value


def print_env_status():
    """Print status of loaded environment variables (for debugging)."""
    print("\n📋 Environment Configuration:")
    print("-" * 50)

    # Azure services (from azd)
    azure_vars = [
        ("AZURE_AI_PROJECT_ENDPOINT", "AI Foundry Project"),
        ("AZURE_AI_ENDPOINT", "AI Services"),
        ("AZURE_OPENAI_ENDPOINT", "OpenAI"),
        ("AZURE_AI_SEARCH_ENDPOINT", "AI Search"),
        ("AZURE_CHAT_MODEL", "Chat Model"),
        ("AZURE_EMBEDDING_MODEL", "Embedding Model"),
    ]

    print("\n🔵 Azure Services (from azd):")
    for var, name in azure_vars:
        value = os.environ.get(var, "")
        if value:
            # Truncate long URLs
            display = value[:50] + "..." if len(value) > 50 else value
            print(f"  [OK] {name}: {display}")
        else:
            print(f"  [FAIL] {name}: not set")

    # Project settings (from .env)
    project_vars = [
        ("FABRIC_WORKSPACE_ID", "Fabric Workspace"),
        ("SOLUTION_NAME", "Solution Name"),
        ("AZURE_ENV_NAME", "azd Environment"),
        ("INDUSTRY", "Industry"),
        ("USECASE", "Use Case"),
        ("DATA_FOLDER", "Data Folder"),
        ("FOUNDRY_AGENT_ID", "Agent ID"),
    ]

    print("\n🟢 Project Settings (from .env):")
    for var, name in project_vars:
        value = os.environ.get(var, "")
        if value:
            display = value[:50] + "..." if len(value) > 50 else value
            print(f"  [OK] {name}: {display}")
        else:
            print(f"  ○ {name}: not set")

    print("-" * 50)
