# Reference: https://ai.pydantic.dev/agents/
from pydantic_ai import Agent
from tools import weaviate_docs_mcp_server


basic_agent = Agent(
    model="anthropic:claude-3-5-haiku-latest", toolsets=[weaviate_docs_mcp_server]
)


@basic_agent.system_prompt
def set_system_prompt() -> str:
    return f"""
    You are a helpful assistant.
    Answer questions as best you can, using any tools as needed.
    You MUST cite your sources, such as an answer from a tool that you used.
    If the source is very long, you can truncate it, or provide a relevant info like the file path.
    """


for prompt in [
    "How do I configure backups in Weaviate? ",
]:
    print(f">> RUNNING PROMPT: {prompt}")
    model_response = basic_agent.run_sync(user_prompt=prompt)
    print(f"Agent response:")
    print(model_response.output, "\n\n")
