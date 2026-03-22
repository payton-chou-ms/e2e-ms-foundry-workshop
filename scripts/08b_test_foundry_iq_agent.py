"""
08b - Test Foundry IQ agent
Interactive chat for the Foundry-native MCP knowledge-base agent.

Usage:
    python 08b_test_foundry_iq_agent.py
"""

from pathlib import Path
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from load_env import load_all_env
import argparse
import json
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--agent-name", default="")
parser.add_argument("--agent-id", default="")
args = parser.parse_args()

load_all_env()

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
DATA_FOLDER = os.getenv("DATA_FOLDER")

if not PROJECT_ENDPOINT:
    print("ERROR: AZURE_AI_PROJECT_ENDPOINT not set")
    print("       Run 'azd up' to deploy Azure resources")
    sys.exit(1)

if not DATA_FOLDER:
    print("ERROR: DATA_FOLDER not set in .env")
    print("       Run 01_generate_sample_data.py first")
    sys.exit(1)

data_dir = Path(DATA_FOLDER)
config_dir = data_dir / "config"
if not config_dir.exists():
    config_dir = data_dir

agent_ids_path = config_dir / "foundry_iq_agent_ids.json"
questions_path = config_dir / "sample_questions.txt"

agent_name = args.agent_name
agent_id = args.agent_id
if agent_ids_path.exists():
    with open(agent_ids_path) as f:
        agent_ids = json.load(f)
    agent_name = agent_name or agent_ids.get("agent_name", "")
    agent_id = agent_id or agent_ids.get("agent_id", "")

if not agent_name and not agent_id:
    print("ERROR: No Foundry IQ agent reference found")
    print("       Run 07b_create_foundry_iq_agent.py first")
    sys.exit(1)

sample_questions = []
if questions_path.exists():
    with open(questions_path) as f:
        lines = f.read().splitlines()
    in_document_section = False
    for line in lines:
        if "DOCUMENT QUESTIONS" in line:
            in_document_section = True
            continue
        if in_document_section and line.startswith("==="):
            break
        if in_document_section and line.strip().startswith("- "):
            sample_questions.append(line.strip()[2:])

if not sample_questions:
    sample_questions = [
        "What are the policies for notifying customers of outages?",
        "How is customer impact classified in our documentation?",
    ]

project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai_client = project_client.get_openai_client()

with project_client:
    agent = project_client.agents.get(agent_name or agent_id)

conversation = openai_client.conversations.create()

print(f"\n{'='*60}")
print("Foundry IQ Agent Chat")
print(f"{'='*60}")
print(f"Agent Name: {agent.name}")
print("Type 'quit' to exit, 'help' for sample questions")


def print_citations(response):
    try:
        for item in getattr(response, "output", []) or []:
            if getattr(item, "type", "") != "message":
                continue
            for content in getattr(item, "content", []) or []:
                if getattr(content, "type", "") != "output_text":
                    continue
                annotations = getattr(content, "annotations", []) or []
                for annotation in annotations:
                    annotation_type = getattr(annotation, "type", "citation")
                    details = []
                    for field_name in ["filename", "title", "source", "url"]:
                        field_value = getattr(annotation, field_name, None)
                        if field_value:
                            details.append(str(field_value))

                    if details:
                        print(
                            f"\n  [Citation:{annotation_type}] {' | '.join(details)}")
                    else:
                        print(f"\n  [Citation:{annotation_type}]")
        return
    except Exception:
        return


while True:
    try:
        user_input = input("\nYou: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        break

    if not user_input:
        continue
    if user_input.lower() in ["quit", "exit", "q"]:
        break
    if user_input.lower() == "help":
        print("\nSample document questions:")
        for question in sample_questions:
            print(f"  - {question}")
        continue

    response = openai_client.responses.create(
        conversation=conversation.id,
        input=user_input,
        extra_body={"agent_reference": {
            "name": agent.name, "type": "agent_reference"}},
    )

    print(f"\nAgent: {getattr(response, 'output_text', '')}")
    print_citations(response)
