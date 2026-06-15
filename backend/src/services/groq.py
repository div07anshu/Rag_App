import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant", temperature=0)


def generate_explanation(query, movie):
    meta = movie["meta"]
    prompt = f"""
   User Query:
   {query}

   Movie Details:
   Title: {meta["title"]}
   Genres: {", ".join(meta["genres"])}
   Director: {meta["director"]}
   Actors: {meta["actor"]}
   Plot: {meta["plot"]}

   Explain in 1-2 sentences why this movie was recommended for the user's query.

   Rules:
   - Focus on the relationship between the user's preferences and the movie.
   - Mention themes, tone, genres, storytelling style, or performances only if relevant.
   - Avoid repeating the plot.
   - Write naturally, as if an intelligent movie assistant is speaking.
   - Keep the explanation under 40 words.
    """


    response = model.invoke(prompt)
    return response.content
