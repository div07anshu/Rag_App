from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from src.services.retrieval import search
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    ques: str


@app.get("/")
def root():
    return {"message": "welcome to cinesage"}


@app.post("/search")
async def movie_search(request: Query):
    results = search(request.ques)

    formatted = []

    for result in results:
        if isinstance(result, tuple):
            doc, meta = result
        else:
            doc = result.page_content
            meta = result.metadata

        imdb_id = meta["tconst"]

        omdb_db = requests.get(
            "http://www.omdbapi.com/",
            params={
                "apikey": API_KEY,
                "i": imdb_id,
            },
            timeout=30,
        )

        omdb_db = omdb_db.json()

        formatted.append(
            {
                "title": meta["title"],
                "plot": meta["plot"],
                "genres": meta["genres"],
                "year": meta["year"],
                "rating": meta["rating"],
                "votes": meta["votes"],
                "director": meta["director"],
                "actor": meta["actor"],
                "imdb_id": meta["tconst"],
                "poster": omdb_db.get("Poster"),
                "runtime": omdb_db.get("Runtime"),
            }
        )

    print(formatted)
    return {
        "query": request.ques,
        "results": formatted,
    }
