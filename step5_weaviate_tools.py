from pydantic_ai import Agent, RunContext
from tools import search_weaviate_docs, fetch_weaviate_docs_page
import dotenv

dotenv.load_dotenv(override=True)


basic_agent = Agent(
    model="anthropic:claude-3-5-haiku-latest",
)


@basic_agent.system_prompt
def set_system_prompt() -> str:
    return f"""
    You are a helpful assistant.
    Answer questions as best you can, using any tools as needed.
    You MUST cite your sources, such as an answer from a tool that you used.
    If the source is very long, you can truncate it, or provide a relevant info like the file path.
    """


@basic_agent.tool
def tool_search_weaviate_docs(ctx: RunContext[None], query: str) -> str:
    """
    Search Weaviate docs based on a similarity of the query to the overall document summary.

    Return a list of dictionaries with the path and summary of the documents.
    """
    print(">> TOOL USED: Searching Weaviate docs for user. Query: ", query)
    response = search_weaviate_docs(query)
    return response


@basic_agent.tool
def tool_fetch_weaviate_docs_page(ctx: RunContext[None], path: str) -> str:
    """
    Fetch a specific Weaviate docs page by its path.

    Return the full content of the document page, including any referenced documents within.
    """
    print(">> TOOL USED: Fetching Weaviate docs page for user. Path: ", path)
    response = fetch_weaviate_docs_page(path)
    return response


for prompt in [
    "How does a collection alias work in Weaviate? How do I use it?",
]:
    print(f">> RUNNING PROMPT: {prompt}")
    model_response = basic_agent.run_sync(user_prompt=prompt)
    print(f"Agent response:")
    print(model_response.output, "\n\n")
