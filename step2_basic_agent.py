# Reference: https://ai.pydantic.dev/agents/
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from tools import get_weather_for_city


class UserInfo(BaseModel):
    name: str
    city: str


basic_agent = Agent(
    model="anthropic:claude-3-5-haiku-latest",
    deps_type=UserInfo,
)


@basic_agent.system_prompt
def add_user_info(ctx: RunContext[UserInfo]) -> str:
    return f"""
    You are a helpful assistant.
    Answer questions as best you can, using any tools as needed.
    The user's name is {ctx.deps.name} and they are in {ctx.deps.city}.
    """


@basic_agent.tool
def get_weather(ctx: RunContext[UserInfo]) -> str:
    """Check the weather in a given location"""
    print(">> TOOL USED: Getting weather for user: ", ctx.deps)
    return get_weather_for_city(ctx.deps.city)


prompt = "What's the weather like today where I am?"

for user_info in [
    UserInfo(name="JP", city="Edinburgh"),
    UserInfo(name="Daniel", city="Paris"),
]:
    print(f">> RUNNING PROMPT: {prompt} for user: {user_info.name}")
    model_response = basic_agent.run_sync(user_prompt=prompt, deps=user_info)
    print(f"Agent response for: {user_info.name}")
    print(model_response.output, "\n\n")
