# Building Agentic Applications with Weaviate and Pydantic AI

A hands-on workshop exploring the fundamentals of AI agents, from simple LLM calls to intelligent systems that know when to use tools.

## Workshop Overview

**Duration:** 60 minutes
**Level:** Intermediate
**Format:** Live coding demo with follow-along exercises

By the end of this workshop, you'll understand:
- The difference between workflows and agentic systems
- When agents should (and shouldn't) use tools
- How to build production-ready agents with Weaviate integration

## Prerequisites

- Basic Python knowledge
- GitHub account (for Codespaces)
- Familiarity with APIs and async/await patterns

## Setup

### Option 1: GitHub Codespaces (Recommended)
1. Click the green "Code" button on this repo
2. Select "Codespaces" → "Create codespace on main"
3. Wait ~1-2 minutes for automatic environment setup
4. Add your API keys to `.env` file (see below)
5. Run `python setup_check.py` to verify everything works
6. You're ready to go!

### Option 2: Local Development
```bash
git clone https://github.com/weaviate-tutorials/weaviate-pydantic-ai-workshop.git
cd weaviate-pydantic-ai-workshop
uv sync
source .venv/bin/activate
cp .env.example .env
# Add your API keys to .env (see below)
python setup_check.py  # Verify setup
```

### Required API Keys

Add these to your `.env` file:

| Service | Get Key From | Required For |
|---------|-------------|--------------|
| **Weaviate Cloud** | [console.weaviate.cloud](https://console.weaviate.cloud/) (free tier) | Steps 4-6 |
| **Anthropic API** | [console.anthropic.com](https://console.anthropic.com/) | All steps |
| **Cohere API** | [dashboard.cohere.com](https://dashboard.cohere.com/) (free tier) | Steps 4-6 |

During the workshop, temporary API keys will be provided for the Anthropic API and Cohere API, and read-only credentials for the Weaviate Cloud instance with pre-populated data.

## Workshop Outline

### Part 1: Foundation (15 min)
**From LLM calls to basic agents**

- `step1_llm_call.py` - Simple LLM interaction
- `step2_basic_agent.py` - Adding a tool (weather lookup)
- Key concept: Tools extend LLM capabilities

**Demo:** Ask "What's the weather in San Francisco?" and see the agent use the tool

---

### Part 2: Intelligent Tool Selection (15 min)
**Agentic Systems: Knowing When (and When NOT) to Use Tools**

- `step3_tool_choice.py` - Agent with multiple tools
    - Demo: Three prompts showing selective tool use
    - Weather question → Uses weather tool only
    - News question → Uses news tool only
    - Geography question → Uses NO tools (LLM knowledge)

**Key insight:** Good agents use tools when needed, not
reflexively

---

### Part 3: Real-World Agentic System (10 min)
**Search the Weaviate docs**

- `step4_weaviate_demo.py`
    - Search functionality to find the most relevant Weaviate docs
    - Fetch functionality to get the full content of the document page
- `step5_weaviate_tools.py`
    - Integrate Weaviate tools into an agent
    - Agent chooses to use the tools when needed

---

### Part 4: Building the Complete System (10 min)
**Chatbot**

- `step6_final_chatbot.py` - Putting it all together
- Agent that can:
  - Answer questions from Weaviate documentation
  - Make intelligent decisions about when to escalate further (e.g. contact human support)

**Demo:** Run the complete chatbot end-to-end

---

### Wrap-up (5 min)
**Next Steps & Resources**

- Extending the agent (multiple repos, more tools, streaming responses)
- Deployment options (FastAPI + Modal/Railway/Render)
- Best practices for production agents

## Project Structure

```
weaviate-pydantic-ai-workshop/
├── .devcontainer/
│   ├── devcontainer.json       # GitHub Codespaces configuration
│   └── setup.sh                # Automatic setup script
├── step1_llm_call.ipynb        # Basic LLM interaction
├── step2_basic_agent.ipynb     # Agent with tool
├── step3_tool_choice.ipynb     # Demonstrate agent tool choice
├── step4_weaviate_tools.py     # Show how to integrate Weaviate tools into an agent
├── step5_final_chatbot.py      # Complete system
├── tools.py                    # Tools used in the workshop
├── setup_check.py              # Verify your environment setup
├── .env.example                # Template for API keys
├── pyproject.toml              # Python dependencies
└── README.md
```

## Key Concepts

### What is an Agent?
An agent is an LLM that can:
1. Reason about a problem
2. Decide which tools (if any) to use
3. Execute actions based on its reasoning
4. Iterate until the task is complete

### Workflow vs. Agent

| Workflow | Agent |
|----------|-------|
| Fixed sequence of steps | Dynamic decision-making |
| Always executes all tools | Uses tools only when needed |
| Predictable, rigid | Adaptive, flexible |
| Good for: Known processes | Good for: Varied user needs / complex tasks |

### When to Use Which?

**Use workflows when:**
- Steps are always required
- Compliance/audit requirements
- Predictable inputs and outputs
- Example: Data processing pipelines

**Use agents when:**
- User intent varies widely
- Tools should be used conditionally
- Natural language interaction
- Example: Customer support, research assistants

## Resources

- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)

## License

MIT

---

**Questions during the workshop?** Drop them in chat - we'll address them as we go or in the Q&A at the end.
```
