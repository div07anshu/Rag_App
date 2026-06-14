from langchain_chroma import Chroma
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "imdb_db"


def create_db(documents, embeddings):
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(DB_PATH),
    )

    return vector_store


def load_db(embeddings):
    vector_store = Chroma(
        persist_directory=str(DB_PATH),
        embedding_function=embeddings,
    )

    return vector_store
