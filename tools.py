import random
import weaviate
from dotenv import load_dotenv
import os
from typing import Dict
from weaviate.classes.query import Filter


load_dotenv(override=True)

COLLECTION_NAME = "DocCatalog"


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


def search_weaviate_docs(query: str) -> list[Dict[str, str]]:
    """
    Search Weaviate docs based on a similarity of the query to the overall document summary.

    Return a list of dictionaries with the path and summary of the documents.
    """
    with weaviate.connect_to_weaviate_cloud(
        cluster_url=os.getenv("WEAVIATE_URL"),
        auth_credentials=os.getenv("WEAVIATE_RO_KEY"),
        headers={
            "X-Cohere-Api-Key": os.getenv("COHERE_API_KEY"),
        },
    ) as client:
        col = client.collections.use("DocCatalog")
        response = col.query.near_text(query=query, limit=5, target_vector="default")
    print("Returned results:")
    for o in response.objects:
        print(o.properties["path"])
    return [
        {"path": o.properties["path"], "summary": o.properties["summary"]}
        for o in response.objects
    ]


def fetch_weaviate_docs_page(path: str) -> str:
    """
    Fetch a specific Weaviate docs page by its path.

    Return the full content of the document page, including any referenced documents within.
    """
    with weaviate.connect_to_weaviate_cloud(
        cluster_url=os.getenv("WEAVIATE_URL"),
        auth_credentials=os.getenv("WEAVIATE_RO_KEY"),
        headers={
            "X-Cohere-Api-Key": os.getenv("COHERE_API_KEY"),
        },
    ) as client:
        col = client.collections.use("DocCatalog")
        response = col.query.fetch_objects(
            limit=1,
            filters=Filter.by_property("path").equal(path),
        )
    return (
        response.objects[0].properties["content"]
        + "\n\n"
        + str(response.objects[0].properties["referenced_files"])
    )
