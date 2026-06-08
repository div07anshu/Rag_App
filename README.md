# IMDb Movie Recommendation System

## Overview

A movie recommendation system built using IMDb datasets, Hugging Face embeddings, LangChain, and ChromaDB.

The system converts movie information into vector embeddings and performs semantic search to recommend relevant movies based on natural language queries.

---

## Features

* Semantic movie search
* IMDb-based movie database
* Director information
* Top-billed actor information
* IMDb ratings and vote counts
* ChromaDB vector storage
* Hugging Face sentence-transformer embeddings
* Ranking based on rating and popularity

---

## Dataset

This project uses IMDb public datasets:

* title.basics.tsv
* title.ratings.tsv
* title.crew.tsv
* title.principals.tsv
* name.basics.tsv

Movies with fewer than 5000 votes are excluded to improve recommendation quality.

---

## Technologies Used

* Python
* Pandas
* LangChain
* ChromaDB
* Hugging Face Embeddings
* IMDb Dataset

Embedding Model:

sentence-transformers/all-MiniLM-L6-v2

---

## Database Construction

Each movie document contains:

* Title
* Release Year
* Genres
* IMDb Rating
* Vote Count
* Director Names
* Top 3 Actors

Example:

Title : Interstellar

Year : 2014

Genres : Adventure, Drama, Sci-Fi

Rating : 8.7

Votes : 2200000

Directors : Christopher Nolan

Actors : Matthew McConaughey, Anne Hathaway, Jessica Chastain

---

## Building the Database

Run:

python src/build_db.py

This will:

1. Load IMDb datasets
2. Extract directors and actors
3. Generate embeddings
4. Store vectors inside ChromaDB

---

## Searching Movies

Run:

python src/search.py

Example queries:

* Christopher Nolan movies
* Shah Rukh Khan movies
* Aamir Khan movies
* High rated sci-fi movies
* Space exploration movies
* Sports drama movies

---

## Ranking Strategy

Retrieved movies are ranked using:

score = rating × log10(votes)

This balances movie quality and popularity.

---

## Current Limitations

* Plot summaries are not included.
* Actor/director query routing is not implemented yet.
* Semantic search may occasionally return loosely related movies.
* No web interface currently available.

---

## Roadmap

### Phase 1

* Actor query routing
* Director query routing
* Metadata-based filtering

### Phase 2

* Gemini reranking layer
* Natural language recommendation explanations

### Phase 3

* Plot summary integration
* Hybrid retrieval system

### Phase 4

* Streamlit interface
* Online deployment

##
