"""16 - Minimal Microsoft Agent Framework workflow example.

This is a small, standalone example that mirrors the workshop's
multi-agent idea using the newer Microsoft Agent Framework API.

Install preview packages first:
    pip install --pre "agent-framework-core==1.0.0rc3" "agent-framework-azure-ai==1.0.0rc3"

Run:
    python scripts/16_agent_framework_workflow_example.py
    python scripts/16_agent_framework_workflow_example.py --question "Summarize the policy risk and next step."
"""

import argparse
import asyncio
import os

from agent_framework import WorkflowBuilder
from agent_framework.azure import AzureAIClient
from azure.identity.aio import DefaultAzureCredential

from load_env import load_all_env


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--question",
        default="我們看到異常升高的 escalations，先幫我整理適用政策與下一步。",
        help="Question sent into the workflow agent.",
    )
    return parser.parse_args()


def get_required_env(*names):
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    raise ValueError(
        f"Missing required environment variable. Tried: {', '.join(names)}")


async def main():
    args = parse_args()
    load_all_env()

    project_endpoint = get_required_env(
        "AZURE_AI_PROJECT_ENDPOINT",
        "FOUNDRY_PROJECT_ENDPOINT",
    )
    model_deployment_name = get_required_env(
        "AZURE_AI_MODEL_DEPLOYMENT_NAME",
        "FOUNDRY_MODEL_DEPLOYMENT_NAME",
        "AZURE_CHAT_MODEL",
    )

    async with (
        DefaultAzureCredential() as credential,
        AzureAIClient(
            async_credential=credential,
            project_endpoint=project_endpoint,
            model_deployment_name=model_deployment_name,
        ).as_agent(
            name="policy-researcher",
            instructions="找出和問題最相關的政策重點，列出 3 點。",
        ) as researcher,
        AzureAIClient(
            async_credential=credential,
            project_endpoint=project_endpoint,
            model_deployment_name=model_deployment_name,
        ).as_agent(
            name="answer-synthesizer",
            instructions="把前一步重點整理成使用者可直接採取的下一步。",
        ) as synthesizer,
    ):
        workflow = (
            WorkflowBuilder(start_executor=researcher)
            .add_edge(researcher, synthesizer)
            .build()
        )

        workflow_agent = workflow.as_agent(name="mini-policy-workflow")
        stream = workflow_agent.run(args.question, stream=True)

        async for update in stream:
            if update.text:
                print(update.text, end="", flush=True)
        print()

        await stream.get_final_response()


if __name__ == "__main__":
    asyncio.run(main())
