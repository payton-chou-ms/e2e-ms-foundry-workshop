"""Shared helpers for the declarative multi-agent workflow runners."""

import json


def get_agent(project_client, agent_record):
    agent_name = agent_record.get("name", "")
    agent_id = agent_record.get("id", "")

    if agent_name:
        try:
            return project_client.agents.get(agent_name)
        except Exception:
            pass

    if agent_id:
        return project_client.agents.get(agent_id)

    raise ValueError("Agent metadata does not contain a usable name or id")


def run_prompt_agent_step(openai_client, definition, conversation_id, message, runtime):
    model = definition["model"]
    instructions = definition["instructions"]
    tools = definition.get("tools", [])

    response = openai_client.responses.create(
        model=model,
        input=message,
        instructions=instructions,
        tools=tools,
        conversation={"id": conversation_id},
    )

    final_text = ""

    while True:
        function_calls = []
        for item in response.output:
            if getattr(item, "type", None) == "function_call":
                function_calls.append(item)
            elif getattr(item, "type", None) == "message":
                for content in getattr(item, "content", []):
                    if hasattr(content, "text"):
                        final_text += content.text + "\n"

        if not function_calls:
            break

        tool_outputs = []
        for function_call in function_calls:
            arguments = json.loads(function_call.arguments)
            if function_call.name == "search_documents":
                result = runtime.search_documents(
                    query=arguments.get("query", ""),
                    top=arguments.get("top"),
                )
            elif function_call.name == "execute_sql":
                result = runtime.execute_sql(arguments.get("sql_query", ""))
            else:
                result = f"Unknown function: {function_call.name}"

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": function_call.call_id,
                    "output": result,
                }
            )

        response = openai_client.responses.create(
            model=model,
            input=tool_outputs,
            instructions=instructions,
            tools=tools,
            conversation={"id": conversation_id},
        )

    return final_text.strip()
