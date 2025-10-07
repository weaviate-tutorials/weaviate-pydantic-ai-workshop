# Step 5: Production-Ready Support Chatbot
# Reference: https://ai.pydantic.dev/agents/
#
# This brings together everything from Steps 1-4:
# - LLM interaction (Step 1)
# - Tool usage (Step 2)
# - Intelligent tool selection (Step 3)
# - Real Weaviate integration (Step 4)
# Plus: Smart escalation to human support when needed!

from pydantic_ai import Agent, RunContext
from tools import search_weaviate_docs, fetch_weaviate_docs_page
from typing import Literal
from random import randint
import dotenv

dotenv.load_dotenv(override=True)

# Create our support agent - same pattern as Steps 2-3, but now with 3 tools
chatbot_agent = Agent(
    model="anthropic:claude-3-5-haiku-latest",
)


@chatbot_agent.system_prompt
def set_system_prompt() -> str:
    """
    Define the agent's role and behavior.

    Key addition: Instructions on WHEN to escalate to humans.
    This makes the agent self-aware of its limitations!
    """
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


# Tool 1: Search for relevant documentation
# Same as Step 4, but now part of a larger system
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


# Tool 2: Fetch full document content
# The agent often chains these: search → fetch → answer
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


# Tool 3: Escalate to human support
# NEW! This is the production pattern: agents should know when they need help
# Notice the detailed docstring - this guides the agent's decision-making
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

    # Production note: Replace this with actual ticketing system integration
    # Could be: Zendesk, Jira, GitHub Issues, Linear, etc.
    issue_number = randint(10000, 99999)
    return f"Successfully filed GitHub issue #{issue_number}: '{title}' (type: {issue_type})"


# ============================================================================
# Interactive Chat Loop
# ============================================================================
# This is a simple REPL (Read-Eval-Print Loop) for the chatbot
# In production, this would be replaced by a web interface, Slack bot, etc.

print("=" * 80)
print("WEAVIATE SUPPORT CHATBOT")
print("=" * 80)
print("Ask questions about Weaviate! (Type 'quit' or 'exit' to stop)")
print("=" * 80)
print()

# Demo tip: Try these questions to showcase different behaviors:
# 1. "How do collection aliases work?" → Uses search + fetch tools
# 2. "I'm getting a 404 error" → May escalate to human support
# 3. "What's the weather?" → Should refuse (out of scope)

while True:
    user_input = input("\nYou: ").strip()

    # Exit conditions
    if user_input.lower() in ["quit", "exit", "q"]:
        print("\nGoodbye! 👋")
        break

    # Skip empty inputs
    if not user_input:
        continue

    print(f"\n{'=' * 80}")
    print("Agent is thinking...")
    print(f"{'=' * 80}\n")

    # Run the agent - it will decide which tools (if any) to use!
    # Watch the ">> TOOL USED" messages to see its decision-making
    model_response = chatbot_agent.run_sync(user_prompt=user_input)

    print(f"\nAgent: {model_response.output}\n")
