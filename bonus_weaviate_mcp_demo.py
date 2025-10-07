# Reference: https://ai.pydantic.dev/agents/
# Using a simple, personal demo MCP server for Weaviate docs (https://github.com/databyjp/weaviate-docs-mcp)
from pydantic_ai import Agent
from pathlib import Path
from pydantic_ai.mcp import MCPServerStdio
import os

weaviate_docs_mcp_directory = Path.home() / "code" / "weaviate-docs-mcp"
weaviate_docs_mcp_server = MCPServerStdio(
    command="uv",
    args=["--directory", str(weaviate_docs_mcp_directory), "run", "weaviate-docs-mcp"],
    env=os.environ.copy(),
)

basic_agent = Agent(
    model="anthropic:claude-3-5-haiku-latest",
    toolsets=[weaviate_docs_mcp_server]
)


@basic_agent.system_prompt
def set_system_prompt() -> str:
    return f"""
    You are a helpful Weaviate assistant.
    Answer questions as best you can, using any tools as needed, as many times as needed.

    IMPORTANT: Do not rely on your internal knowledge for any Weaviate related knowledge.
    This is especially true for any code examples.

    For any code examples, even basic, please use the tools to search for, and get relevant code examples.

    This is true for something as basic as connecting to a Weaviate server.

    The syntax may have changed, so look up the latest syntax using the provided tools.
    """


for prompt in [
    # "How do I configure backups in Weaviate? ",
    """What vector compression methods are available in Weaviate?
    Concretely, how do I configure it?
    Show me a code example using an actual compression method.
    Preferably, show me an end-to-end example from connection, collection creation, data ingestion and query.
    """,
]:
    print(f">> RUNNING PROMPT: {prompt}")
    model_response = basic_agent.run_sync(user_prompt=prompt)
    print(f"Agent response:")
    print(model_response.output, "\n\n")
