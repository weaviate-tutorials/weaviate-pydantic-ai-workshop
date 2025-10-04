import random
import weaviate
from weaviate.agents.query import QueryAgent
from weaviate.agents.classes import QueryAgentCollectionConfig
from dotenv import load_dotenv
import os

load_dotenv(override=True)

COLLECTION_NAME = "ManualPages"


def get_weather_for_city(city: str) -> str:
    """Get weather for any city"""
    if city == "Edinburgh":
        rand_weather = random.choice(["cloudy", "rainy", "unusually sunny"])
        rand_temp = random.randint(5, 10)
    else:
        rand_weather = random.choice(["sunny", "cloudy", "rainy", "snowy"])
        rand_temp = random.randint(15, 20)

    return f"The weather in {city} is {rand_weather} today. The expected temperature is {rand_temp} degrees Celsius."


def get_trending_news_for_city(city: str) -> str:
    """Get trending news for a given city"""
    return f"""
    Today in {city}, a surprisingly large {random.choice(["mouse", "snake", "mongoose"])}
    was found {random.choice(["chasing", "cuddling", "playing"])}
    with a startled {random.choice(["child", "jogger", "park manager"])}.
    """


def ask_weaviate_docs(query: str) -> str:
    """Ask a question to the Weaviate docs"""
    with weaviate.connect_to_weaviate_cloud(
        cluster_url=os.getenv("WEAVIATE_URL"),
        auth_credentials=os.getenv("WEAVIATE_RO_KEY"),
        headers={
            "X-Cohere-Api-Key": os.getenv("COHERE_API_KEY"),
        }
    ) as client:
        qa = QueryAgent(client=client, collections=[QueryAgentCollectionConfig(name="DocChunks", target_vector="chunk"), QueryAgentCollectionConfig(name="DocCatalog")])
        response = qa.ask(query=query)
    return response.final_answer

