# Reference: https://ai.pydantic.dev/agents/
from pydantic_ai import Agent, RunContext
from tools import search_weaviate_docs, fetch_weaviate_docs_page
from typing import Literal
from random import randint
import dotenv

dotenv.load_dotenv(override=True)

chatbot_agent = Agent(
    model="anthropic:claude-3-5-haiku-latest",
)


@chatbot_agent.system_prompt
def set_system_prompt() -> str:
    return """
    You are a helpful Weaviate support assistant.

    Your job is to help users with their Weaviate questions by:
    1. Searching and reading the Weaviate documentation
    2. Providing clear, accurate answers with citations
    3. Filing GitHub issues when you encounter:
       - Bugs or unexpected behavior in production
       - Feature requests
       - Questions you cannot answer from the documentation

    When filing issues:
    - Provide a clear title and description
    - Include relevant context from the conversation
    - Tag appropriately (bug, feature-request, question)

    Be helpful, but know your limits. When in doubt, escalate to human support via GitHub issue.

    If the questions is not related to Weaviate, politely (but firmly) tell the user that you are a Weaviate support assistant and you can only help with Weaviate questions.
    """


@chatbot_agent.tool
def tool_search_weaviate_docs(ctx: RunContext[None], query: str) -> str:
    """
    Search Weaviate docs based on semantic similarity to the query.

    Returns a list of relevant document paths and summaries.
    Use this first to find potentially relevant documentation.
    """
    print(f">> TOOL USED: Searching Weaviate docs. Query: '{query}'")
    response = search_weaviate_docs(query)
    return response


@chatbot_agent.tool
def tool_fetch_weaviate_docs_page(ctx: RunContext[None], path: str) -> str:
    """
    Fetch the full content of a specific Weaviate documentation page.

    Returns the complete document content including referenced files.
    Use this after searching to get detailed information.
    """
    print(f">> TOOL USED: Fetching Weaviate docs page. Path: '{path}'")
    response = fetch_weaviate_docs_page(path)
    return response


@chatbot_agent.tool
def contact_human_support(
    ctx: RunContext[None],
    title: str,
    description: str,
    issue_type: str,
    department: Literal["support", "sales", "other"],
) -> str:
    """
    Contact human support for problems that need human attention.

    Args:
        title: Clear, concise issue title
        description: Detailed description with context and reproduction steps if applicable
        issue_type: One of: 'bug', 'feature-request', 'question'

    Use this when:
    - User reports a bug or unexpected behavior
    - Documentation doesn't answer the question
    - User needs feature that doesn't exist
    - For non-technical issues

    Then, tell the user that you have escalated the issue to human support. Give them the issue number.
    """
    print(f">> TOOL USED: Contacting human support")
    print(f"   To department: {department}")
    print(f"   Title: {title}")
    print(f"   Type: {issue_type}")
    print(f"   Description: {description[:100]}...")

    # In a real implementation, this could send a message, use a ticketing system, etc.
    # For the workshop, we'll simulate it
    issue_number = randint(10000, 99999)
    return f"Successfully filed GitHub issue #{issue_number}: '{title}' (type: {issue_type})"


print("=" * 80)
print("WEAVIATE SUPPORT CHATBOT")
print("=" * 80)
print("Ask questions about Weaviate! (Type 'quit' or 'exit' to stop)")
print("=" * 80)
print()

while True:
    user_input = input("\nYou: ").strip()

    if user_input.lower() in ["quit", "exit", "q"]:
        print("\nGoodbye! 👋")
        break

    if not user_input:
        continue

    print(f"\n{'=' * 80}")
    print("Agent is thinking...")
    print(f"{'=' * 80}\n")

    model_response = chatbot_agent.run_sync(user_prompt=user_input)

    print(f"\nAgent: {model_response.output}\n")
