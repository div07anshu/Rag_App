from langchain_huggingface import HuggingFaceEmbeddings
from backend.src.db.chroma import load_db
from dotenv import load_dotenv
from backend.src.services.gemini import improve_query
from backend.src.services.gemini import query_decomposition
from backend.src.services.gemini import should_decompose
import math
import re

load_dotenv()

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
    retriever = vector_store.as_retriever(search_kwargs={"k": 15})
    unique_results = []

    if should_decompose(query):
        loq = query_decomposition(query)

        results = []

        for q in loq:
            output = retriever.invoke(q)
            results.extend(output)

        seen = set()

        for result in results:
            tconst = result.metadata["tconst"]
            if tconst not in seen:
                seen.add(tconst)
                unique_results.append(result)

    else:
        unique_results = retriever.invoke(query)

    unique_results = sorted(
        unique_results,
        key=lambda doc: (doc.metadata["rating"] * math.log10(doc.metadata["votes"])),
        reverse=True,
    )

    return unique_results[:5]


def search(query):
    improved_query = improve_query(query)
    result = []

    route, entity = route_query(improved_query)

    if route == "actor":
        result = actor_search(entity)
    elif route == "director":
        result = director_search(entity)
    else:
        result = semantic_search(entity)

    return result

