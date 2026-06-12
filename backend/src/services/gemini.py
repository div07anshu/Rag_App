from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from pydantic import BaseModel
from typing import List, Optional, cast
from backend.src.db.chroma import load_db
from dotenv import load_dotenv

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")


class decomposed_query(BaseModel):
    sub_queries: List[str]


def improve_query(query):
    prompt = f"""
   You are improving movie search queries for a retrieval system.
   Rewrite the user's query to make it more descriptive and retrieval-friendly.

   Rules:
  - Preserve the original intent.
  - Preserve important keywords and named entities.
  - Expand vague concepts using related movie terminology.
  - Do not remove core concepts from the query.
  - Return only the improved query.

   User Query :
   {query}
   """
    response = model.invoke(prompt)
    return response.content


def query_decomposition(query):
    prompt = f"""
    You are helping a movie recommendation system.
    Your task is to break the user's movie search query into 2 to 4 distinct sub-queries that capture different aspects of the same intent.

    Rules:
    - Preserve the original intent.
    - Generate retrieval-friendly search queries.
    - Focus on different semantic aspects of the request.
    - Preserve important constraints such as language, actors, directors, genres, moods, and movie titles across the generated sub-queries whenever relevant.
    - Do NOT return rephrased versions of the same query.
    - Keep actor names, director names, movie titles, and genres unchanged if they are mentioned.
    - Return ONLY the list of sub-queries.

    User Query : 
    {query}

    Examples:

    Query: "feel good Hindi movies about friendship"

    Sub-queries:
    - feel good Hindi movies
    - Hindi movies about friendship
    - uplifting Hindi movies with friendship themes
    """

    structured_model = model.with_structured_output(decomposed_query)
    response = cast(decomposed_query, structured_model.invoke(prompt))
    return response.sub_queries


def should_decompose(query):
    keywords = ["with", "like", "about", "similar", "and"]

    return len(query.split()) >= 5 or any( k in query for k in keywords)
