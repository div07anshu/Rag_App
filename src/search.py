from langchain_huggingface import HuggingFaceEmbeddings
from db import load_db
import math
import re

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = load_db(embeddings)

data = vector_store.get(
    include=["documents", "metadatas"],
)

actor_set = set()
director_set = set()

for meta in data["metadatas"]:
    director_set.add(meta["director"].lower())

    for actor in meta["actor"].split(","):
        actor_set.add(actor.strip().lower())


query = input("enter your query : ").lower()


def route_query(query):
    query = query.lower()

    for actor in actor_set:
        pattern = r"\b" + re.escape(actor) + r"\b"
        if re.search(pattern, query):
            return "actor", actor

    for director in director_set:
        pattern = r"\b" + re.escape(director) + r"\b"
        if re.search(pattern, query):
            return "director", director

    return "semantic", query


def actor_search(query):
    query = query.lower()
    results = []

    for doc, meta in zip(data["documents"], data["metadatas"]):
        if query in meta["actor"].lower():
            results.append((doc, meta))

    results = sorted(
        results,
        key=lambda x: (x[1]["rating"] * math.log10(x[1]["votes"])),
        reverse=True,
    )

    return results[:5]


def director_search(query):
    query = query.lower()
    results = []

    for doc, meta in zip(data["documents"], data["metadatas"]):
        if query in meta["director"].lower():
            results.append((doc, meta))

    results = sorted(
        results,
        key=lambda x: (x[1]["rating"] * math.log10(x[1]["votes"])),
        reverse=True,
    )

    return results[:5]


def semantic_search(query):
    query = query.lower()
    retriever = vector_store.as_retriever(search_kwargs={"k": 20})

    result = retriever.invoke(query)
    print("Retrieved:", len(result))

    result = sorted(
        result,
        key=lambda x: (x.metadata["rating"] * math.log10(x.metadata["votes"])),
        reverse=True,
    )

    return result[:5]


ans = []
route, entity = route_query(query)
print(route)

if route == "actor":
    ans = actor_search(entity)
elif route == "director":
    ans = director_search(entity)
else:
    ans = semantic_search(entity)


for movie in ans:

    if isinstance(movie, tuple):
        print(movie[0])
    else:
        print(movie.page_content)

    print("-" * 50)
