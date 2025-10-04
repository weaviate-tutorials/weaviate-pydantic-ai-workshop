from tools import ask_weaviate_docs

query = "How does a collection alias work in Weaviate?"
query = "Show me how to create a collection alias in Weaviate with Python"

print(ask_weaviate_docs(query))
