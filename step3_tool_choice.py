# Reference: https://ai.pydantic.dev/direct/
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
import random


class UserInfo(BaseModel):
    name: str
    city: str


# Make a synchronous request to the model
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
    if ctx.deps.city == "Edinburgh":
        rand_weather = random.choice(["cloudy", "rainy", "unusually sunny"])
        rand_temp = random.randint(5, 10)
    else:
        rand_weather = random.choice(["sunny", "cloudy", "rainy", "snowy"])
        rand_temp = random.randint(15, 20)
    return f"The weather in {ctx.deps.city} is {rand_weather} today. The expected temperature is {rand_temp} degrees Celsius."


@basic_agent.tool
def get_trending_news(ctx: RunContext[UserInfo]) -> str:
    """Get the trending news item in a given location"""
    print(">> TOOL USED: Getting trending news for user: ", ctx.deps)
    return f"""
    Today in {ctx.deps.city}, a surprisingly large {random.choice(['mouse', 'snake', 'mongoose'])}
    was found {random.choice(['chasing', 'cuddling', 'playing'])}
    with a startled {random.choice(['child', 'jogger', 'park manager'])}.
    """


user_info = UserInfo(name="JP", city="Edinburgh")
for prompt in [
    "What's the weather like today where I am?",
    "What's the trending news item where I am today??",
]:
    print(f">> RUNNING PROMPT: {prompt} for user: {user_info.name}")
    model_response = basic_agent.run_sync(user_prompt=prompt, deps=user_info)
    print(f"Agent response for: {user_info.name}")
    print(model_response.output, "\n\n")
