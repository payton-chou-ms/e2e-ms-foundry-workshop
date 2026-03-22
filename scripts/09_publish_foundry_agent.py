"""
09 - Publish Foundry Agent (Guarded Precheck)

This helper script prepares the optional publish flow for Teams / Microsoft 365 Copilot.
It intentionally does NOT force a publish operation. Instead it:

1. Loads the current Foundry project environment
2. Resolves the target agent from args, env, or data config
3. Verifies the agent exists in the current project
4. Checks Azure CLI session and Microsoft.BotService provider state when possible
5. Prints the next UI steps for publishing

The script is non-blocking by default. If a prerequisite is missing, it prints a
warning and exits successfully so workshop setup can continue.

Usage:
    python scripts/09_publish_foundry_agent.py
    python scripts/09_publish_foundry_agent.py --agent-id <id>
    python scripts/09_publish_foundry_agent.py --agent-name <name>
    python scripts/09_publish_foundry_agent.py --teams

Optional behavior:
    --strict   Return a non-zero exit code on missing prerequisites.
    --teams    Print the extra Teams / Microsoft 365 Copilot publishing checklist.
"""

import argparse
import json
import os
import subprocess
import sys

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from load_env import load_all_env
from optional_demo_utils import print_demo_header


def warn(message: str) -> None:
    print(f"[WARN] {message}")


def ok(message: str) -> None:
    print(f"[OK] {message}")


def info(message: str) -> None:
    print(message)


def exit_skip(message: str, strict: bool) -> None:
    warn(message)
    if strict:
        sys.exit(1)
    print("[SKIP] Publish flow left for manual UI steps. Main workshop flow can continue.")
    sys.exit(0)


def run_az(command_args):
    result = subprocess.run(
        ["az", *command_args],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def parse_project_endpoint(endpoint: str):
    marker = ".services.ai.azure.com/api/projects/"
    if marker not in endpoint:
        return None, None

    left, project_name = endpoint.split(marker, 1)
    account_name = left.split("https://", 1)[-1]
    return account_name, project_name.strip("/")


def resolve_agent_inputs(agent_id_arg: str, agent_name_arg: str, data_folder: str):
    agent_id = agent_id_arg or os.getenv("FOUNDRY_AGENT_ID")
    agent_name = agent_name_arg or os.getenv("FOUNDRY_AGENT_NAME")

    if not data_folder:
        return agent_id, agent_name

    config_dir = os.path.join(os.path.abspath(data_folder), "config")
    if not os.path.exists(config_dir):
        config_dir = os.path.abspath(data_folder)

    agent_ids_path = os.path.join(config_dir, "agent_ids.json")
    if os.path.exists(agent_ids_path):
        with open(agent_ids_path) as handle:
            agent_ids = json.load(handle)
        agent_id = agent_id or agent_ids.get("agent_id")
        agent_name = agent_name or agent_ids.get("agent_name")

    return agent_id, agent_name


parser = argparse.ArgumentParser()
parser.add_argument("--agent-id", default="")
parser.add_argument("--agent-name", default="")
parser.add_argument("--teams", action="store_true",
                    help="Print the Teams / Microsoft 365 Copilot checklist")
parser.add_argument("--strict", action="store_true",
                    help="Fail with non-zero exit code when prerequisites are missing")
args = parser.parse_args()


load_all_env()

ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
DATA_FOLDER = os.getenv("DATA_FOLDER")

print_demo_header(
    title="Foundry Agent Publish Precheck",
    description="Check whether an existing Foundry agent is ready for the manual publish flow.",
    env_items=[
        {"name": "AZURE_AI_PROJECT_ENDPOINT", "value": ENDPOINT},
        {"name": "DATA_FOLDER", "value": DATA_FOLDER},
        {"name": "FOUNDRY_AGENT_ID", "value": os.getenv("FOUNDRY_AGENT_ID")},
        {"name": "FOUNDRY_AGENT_NAME",
            "value": os.getenv("FOUNDRY_AGENT_NAME")},
    ],
)

if not ENDPOINT:
    exit_skip("AZURE_AI_PROJECT_ENDPOINT not set. Run 'azd up' first.", args.strict)

agent_id, agent_name = resolve_agent_inputs(
    args.agent_id, args.agent_name, DATA_FOLDER)
if not agent_id and not agent_name:
    exit_skip(
        "No agent identifier found. Run 07_create_foundry_agent.py first or pass --agent-id / --agent-name.",
        args.strict,
    )

account_name, project_name = parse_project_endpoint(ENDPOINT)
info("This demo does not publish automatically. It only checks prerequisites and prints the next manual steps.")
ok(f"Project endpoint loaded: {ENDPOINT}")
if account_name and project_name:
    ok(f"Foundry account: {account_name}")
    ok(f"Foundry project: {project_name}")
else:
    warn("Could not fully parse account and project names from endpoint.")

print("\nChecking target agent...")
credential = DefaultAzureCredential()

try:
    project_client = AIProjectClient(endpoint=ENDPOINT, credential=credential)
except Exception as exc:
    exit_skip(f"Failed to initialize AIProjectClient: {exc}", args.strict)

try:
    with project_client:
        if agent_id:
            agent = project_client.agents.get(agent_id)
        else:
            agent = project_client.agents.get(agent_name)
except Exception as exc:
    identifier = agent_id or agent_name
    exit_skip(f"Failed to resolve agent '{identifier}': {exc}", args.strict)

ok(f"Agent found: {agent.name}")
ok(f"Agent ID: {agent.id}")

print("\nChecking Azure CLI session...")
code, stdout, stderr = run_az(["account", "show", "-o", "json"])
if code != 0:
    warn("Azure CLI is not ready or not logged in.")
    if stderr:
        print(f"       {stderr}")
else:
    try:
        account = json.loads(stdout)
        ok(f"Azure subscription: {account.get('name', '<unknown>')}")
        ok(f"Subscription ID: {account.get('id', '<unknown>')}")
        ok(f"Tenant ID: {account.get('tenantId', '<unknown>')}")
    except json.JSONDecodeError:
        warn("Could not parse Azure account information from CLI output.")

print("\nChecking Microsoft.BotService provider registration...")
code, stdout, stderr = run_az(["provider", "show", "--namespace",
                              "Microsoft.BotService", "--query", "registrationState", "-o", "tsv"])
if code != 0:
    warn("Could not verify Microsoft.BotService provider registration.")
    if stderr:
        print(f"       {stderr}")
else:
    state = stdout or "<unknown>"
    if state.lower() == "registered":
        ok("Microsoft.BotService provider is registered")
    else:
        warn(f"Microsoft.BotService provider state: {state}")
        print("       Teams / Microsoft 365 Copilot publish may fail until this provider is registered.")

print("\nPublish guidance (manual UI flow):")
print("  1. Open the Foundry portal and select the target agent version.")
print("  2. Publish the agent as an Agent Application first.")
print("  3. After publish, note the new application identity and endpoint.")
print("  4. Reassign RBAC for any downstream Azure resources used by tools.")
print("  5. If needed, continue with 'Publish to Teams and Microsoft 365 Copilot'.")

print("\nRBAC reminder:")
print("  - Publishing creates a new Agent Application identity.")
print("  - Tool access that worked in the project can fail after publish until RBAC is reassigned.")
print("  - Recheck Azure AI Search, Storage, and any other connected Azure resources.")

if args.teams:
    print("\nTeams / Microsoft 365 Copilot checklist:")
    print("  1. Confirm the agent version was tested successfully in Foundry before publishing.")
    print("  2. Confirm you can create Azure Bot Service resources in the selected subscription.")
    print("  3. Prepare metadata: name, short description, full description, publisher, website, privacy URL, terms URL.")
    print("  4. Choose Individual scope for small pilots, or Organization scope if admin approval is available.")
    print("  5. After packaging, test the app in Teams before broader rollout.")
    print("  6. Remember that streaming responses and citations are currently limited in published experiences.")

print("\nResult:")
print("  This script completed prechecks only.")
print("  Use the UI to finish publishing so the workshop can stay simple and demo-focused.")
