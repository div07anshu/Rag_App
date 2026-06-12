from fastapi import FastAPI
from pydantic import BaseModel
from backend.src.services.retrieval import search

app = FastAPI()


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
            formatted.append(
                {
                    "content": doc,
                    "metadata": meta,
                }
            )
        else:
            formatted.append(
                {
                    "content": result.page_content,
                    "metadata": result.metadata,
                }
            )

    return {
        "query": request.ques,
        "results": formatted,
    }
