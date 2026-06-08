from langchain_huggingface import HuggingFaceEmbeddings
from db import load_db
import math

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = load_db(embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 20})
result = retriever.invoke("Nitesh Tiwari")

result = sorted(
    result,
    key=lambda doc: (doc.metadata["rating"] * math.log10(doc.metadata["votes"])),
    reverse=True,
)

top_movies = result[:5]


for doc in top_movies:
    print(doc.page_content)
    print("-" * 50)
