from tools import search_weaviate_docs, fetch_weaviate_docs_page
import dotenv

dotenv.load_dotenv(override=True)

query = "collection aliases in Weaviate"

r = search_weaviate_docs(query)
for i in r:
    print(i["path"])
    print(i["summary"])
    print("\n")


for i in r:
    page = fetch_weaviate_docs_page(i["path"])
    print("Page length: ", len(page), "characters")
    print(page[:100] + "...")
    print("\n")
