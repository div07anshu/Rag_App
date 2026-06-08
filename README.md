# Movie Recommendation System

A semantic movie recommendation system built using LangChain, ChromaDB, HuggingFace Embeddings, and the MovieLens dataset.

The system converts movie information into vector embeddings and performs semantic similarity search to recommend relevant movies based on natural language queries.


## Features

- Semantic movie search
- ChromaDB vector database
- HuggingFace sentence-transformer embeddings
- MovieLens dataset integration
- Genome tag enrichment
- Average rating and rating count integration
- Natural language movie queries


## Dataset

This project uses the MovieLens dataset and combines information from:

- movies.csv
- ratings.csv
- genome-tags.csv
- genome-scores.csv

The final movie documents contain:

- Movie Title
- Genres
- Average Rating
- Rating Count
- Top Relevant Tags

Example:

Title : The Martian (2015)

Genres : Adventure, Drama, Sci-Fi

Average Rating : 4.04

Rating Count : 890

Top Tags : astronauts, mars, space travel, nasa, space program


## Project Architecture


MovieLens Dataset
        │
        ▼
Data Processing (Pandas)
        │
        ▼
Document Creation
        │
        ▼
HuggingFace Embeddings
        │
        ▼
Chroma Vector Database
        │
        ▼
Retriever
        │
        ▼
Semantic Search



## Project Structure

.
├── data/
│   ├── movies.csv
│   ├── finalrating.csv
│   ├── genome-tags.csv
│   └── genome-scores.csv
│
├── src/
│   ├── build_db.py
│   ├── database.py
│   └── search.py
│
├── vector_data/
│   └── movie_db/
│
├── README.md
├── pyproject.toml
├── requirements.txt
└── .env


---

## Installation

Clone the repository:

git clone <repository-url>
cd movie-recommender

Install dependencies:

uv sync


## Build the Database

python src/build_db.py


This will:

1. Load movie metadata.
2. Merge ratings information.
3. Merge genome tags.
4. Create enriched movie documents.
5. Generate embeddings.
6. Store vectors in ChromaDB.


## Search Movies

python src/search.py

Example query:

result = retriever.invoke(
    "space survival movie like the martian"
)


## Example Queries

- fantasy adventure movie
- movie like interstellar
- emotional animated movie
- science fiction space exploration movie
- movie about astronauts stranded in space
- highly rated fantasy adventure movie


## Technologies Used

- Python
- Pandas
- LangChain
- ChromaDB
- HuggingFace Embeddings
- MovieLens Dataset


## Future Improvements

- Metadata-based filtering
- Rating-based reranking
- Gemini integration
- Streamlit web interface
- Conversational movie recommender
- Full RAG pipeline