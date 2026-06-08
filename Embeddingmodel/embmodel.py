from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

response = embeddings.embed_documents(
    ["Hello my name is divyanshu", "Hello my name is madhur raaj"]
)

print(response)
