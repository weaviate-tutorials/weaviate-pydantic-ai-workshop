from pydantic_ai import Agent, RunContext
from tools import search_weaviate_docs, fetch_weaviate_docs_page
import dotenv
from typing import Dict

dotenv.load_dotenv(override=True)


basic_agent = Agent(
    model="anthropic:claude-3-5-haiku-latest",
)


@basic_agent.system_prompt
def set_system_prompt() -> str:
    return f"""
    You are a helpful assistant.
    Answer questions as best you can, using any tools as needed.
    """


# STUDENT TODO
# Run the script first to see what happens when you don't implement the tools.
# Then, implement the tools and run the script again to see the difference.


# STUDENT TODO: Implement a tool to search Weaviate docs.
#
# Simply call the search_weaviate_docs function.
# It searches Weaviate docs based on a similarity of the query to the overall document summary.
#
# search_weaviate_docs takes a query (str) and returns a list of dictionaries
# with the path and summary of the documents.
#
# In the tool, print a message saying ">> TOOL USED: Searching Weaviate docs for user. Query: " and the query.
# Then call the search_weaviate_docs function and return the result.
# BEGIN_SOLUTION
@basic_agent.tool
def tool_search_weaviate_docs(
    ctx: RunContext[None], query: str
) -> list[Dict[str, str]]:
    """
    Search Weaviate docs based on a similarity of the query to the overall document summary.

    Return a list of dictionaries with the path and summary of the documents.
    """
    print(">> TOOL USED: Searching Weaviate docs for user. Query: ", query)
    response = search_weaviate_docs(query)
    return response


# END_SOLUTION


# STUDENT TODO: Implement a tool to fetch a specific Weaviate docs page by its path.
#
# Simply call the fetch_weaviate_docs_page function.
# It fetches a specific Weaviate docs page by its path.
#
# fetch_weaviate_docs_page takes a path (str) and returns a string
# with the full content of the document page, including any referenced documents within.
#
# In the tool, print a message saying ">> TOOL USED: Fetching Weaviate docs page for user. Path: " and the path.
# Then call the fetch_weaviate_docs_page function and return the result.
# BEGIN_SOLUTION
@basic_agent.tool
def tool_fetch_weaviate_docs_page(ctx: RunContext[None], path: str) -> str:
    """
    Fetch a specific Weaviate docs page by its path.

    Return the full content of the document page, including any referenced documents within.
    """
    print(">> TOOL USED: Fetching Weaviate docs page for user. Path: ", path)
    response = fetch_weaviate_docs_page(path)
    return response


# END_SOLUTION


for prompt in [
    "What aliases are available in Weaviate? How do I use it?",
]:
    print(f">> RUNNING PROMPT: {prompt}")
    model_response = basic_agent.run_sync(user_prompt=prompt)
    print(f"Agent response:")
    print(model_response.output, "\n\n")
