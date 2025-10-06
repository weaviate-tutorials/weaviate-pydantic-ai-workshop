# Reference: https://ai.pydantic.dev/direct/
from pydantic_ai import ModelRequest
from pydantic_ai.direct import model_request_sync
import dotenv

dotenv.load_dotenv(override=True)

prompt = "What's the weather like in October in Edinburgh?"
# prompt = "How's the weather today in Edinburgh?"

model_response = model_request_sync(
    "anthropic:claude-3-5-haiku-latest", [ModelRequest.user_text_prompt(prompt)]
)

print(model_response.parts[0].content, "\n\n")
