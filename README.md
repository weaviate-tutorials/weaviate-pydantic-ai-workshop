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
3. Wait ~30 seconds for environment setup
4. You're ready to go!

### Option 2: Local Development
```bash
git clone <repo-url>
cd weaviate-agent-workshop
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
```

### Tools / API Keys Used in the Workshop
- Anthropic API key
- Weaviate instance (free sandbox available at console.weaviate.cloud)

## Workshop Outline

### Part 1: Foundation (15 min)
**From LLM calls to basic agents**

- `step1_llm_call.py` - Simple LLM interaction
- `step2_basic_agent.py` - Adding a tool (weather lookup)
- Key concept: Tools extend LLM capabilities

**Demo:** Ask "What's the weather in San Francisco?" and see the agent use the tool

---

### Part 2: The Critical Distinction (15 min)
**Workflows vs. Agentic Systems**

- `step3_workflow.py` - Deterministic: Always executes all steps
- `step4_agentic.py` - Intelligent: Decides which tools to use

**Side-by-side comparison:**

**Question 1:** "How do I create a collection in Weaviate?"
- Workflow: Searches docs → Files GitHub issue (unnecessary!)
- Agent: Searches docs → Returns answer (stops appropriately)

**Question 2:** "My hybrid search returns empty results in production"
- Workflow: Searches docs → Files generic issue
- Agent: Searches docs → Recognizes need for human help → Files detailed issue

**Key insight:** Good agents know when NOT to use their tools

---

### Part 3: Real-World Agentic System (10 min)
**Weaviate Query Agent**

- `step5_weaviate_agent.py` - Pre-built agentic tool for querying Weaviate
- Demo: Answer questions using the documentation database
- Show agent translating natural language questions into Weaviate queries

---

### Part 4: Building the Complete System (10 min)
**Production-Ready Chatbot**

- `step6_final_chatbot.py` - Putting it all together
- Agent that can:
  - Answer questions from Weaviate documentation
  - File GitHub issues when human support is needed
  - Make intelligent decisions about when to escalate

**Demo:** Run the complete chatbot end-to-end

---

### Wrap-up (5 min)
**Next Steps & Resources**

- Extending the agent (multiple repos, more tools, streaming responses)
- Deployment options (FastAPI + Modal/Railway/Render)
- Best practices for production agents

## Project Structure

```
weaviate-agent-workshop/
├── .devcontainer/
│   └── devcontainer.json       # Codespaces configuration
├── step1_llm_call.py           # Basic LLM interaction
├── step2_basic_agent.py        # Agent with tool
├── step3_tool_choice.py        # Demonstrate agent tool choice
├── step4_weaviate_agent.py     # Weaviate query agent
├── step5_weaviate_chatbot.py   # Weaviate chatbot (answer questions from Weaviate docs)
├── step6_final_chatbot.py      # Complete system
├── tools/
│   ├── weather.py              # Weather lookup tool
│   ├── github_issues.py        # GitHub issue creation
│   └── weaviate_search.py      # Weaviate documentation search
├── requirements.txt
├── .env.example
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
| Good for: Known processes | Good for: Varied user needs |

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

## Advanced Exercises

Once you've completed the workshop, try these extensions:

1. **Multi-repo routing**: Make the agent choose between `weaviate/weaviate`, `weaviate/weaviate-python-client`, or `weaviate/verba` based on the question
2. **Streaming responses**: Add real-time streaming for better UX
3. **Memory**: Add conversation history so the agent remembers context
4. **Additional tools**: Add tools for checking system status, searching GitHub issues, or querying Stack Overflow
5. **Deployment**: Wrap in FastAPI and deploy to your favorite platform

## Production Considerations

This workshop uses simplified examples for teaching. In production, consider:

- **Error handling**: Retry logic, fallbacks, graceful degradation
- **Observability**: Logging, tracing, metrics (try LangSmith or Weights & Biases)
- **Rate limiting**: Protect your APIs and manage costs
- **Security**: Input validation, sandboxing, API key rotation
- **Testing**: Unit tests for tools, integration tests for agent behavior
- **Cost management**: Monitor token usage, cache results where possible

## Resources

- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Workshop Recording](link-after-event)
- [Discord Community](your-discord-link)

## Troubleshooting

**Codespace won't start:**
- Try refreshing the page
- Delete and recreate the codespace
- Use local setup as fallback

**API key errors:**
- Check `.env` file has all required keys
- Verify keys are valid (not expired)
- Ensure no extra spaces or quotes

**Agent not using tools:**
- Check tool descriptions are clear
- Verify API keys for external services
- Try more explicit prompts

**GitHub API rate limiting:**
- Use personal access token (not just GitHub auth)
- Consider mocking the issue creation for demo

## Contributing

Found a bug or have a suggestion? Open an issue or PR!

## License

MIT

---

**Questions during the workshop?** Drop them in chat - we'll address them as we go or in the Q&A at the end.
```
