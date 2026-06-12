from langchain_chroma import Chroma


def create_db(documents, embeddings):
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./database/imdb_db",
    )

    return vector_store


def load_db(embeddings):
    vector_store = Chroma(
        persist_directory="./database/imdb_db",
        embedding_function=embeddings,
    )

    return vector_store
