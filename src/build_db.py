import pandas as pd
from langchain_core.documents import Document
from db import create_db
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

basic_df = pd.read_csv(
    "data/title.basics.tsv",
    sep="\t",
    low_memory=False,
)

rating_df = pd.read_csv(
    "data/title.ratings.tsv",
    sep="\t",
    low_memory=False,
)

# it filter out only movies

basic_df = basic_df[basic_df["titleType"] == "movie"]

movie_df = basic_df.merge(
    rating_df,
    on="tconst",
    how="inner",
)

# keep the movie with atleast votes 1000

movie_df = movie_df[movie_df["numVotes"] >= 10000]

# now only keep the important and usefull columns

movie_df = movie_df[
    ["tconst", "primaryTitle", "startYear", "genres", "averageRating", "numVotes"]
]

crew_df = pd.read_csv(
    "data/title.crew.tsv",
    sep="\t",
    low_memory=False,
    usecols=["tconst", "directors"],
)

name_df = pd.read_csv(
    "data/name.basics.tsv",
    sep="\t",
    low_memory=False,
    usecols=["nconst", "primaryName"],
)

movie_df = movie_df.merge(crew_df, on="tconst", how="inner")

pairs = zip(name_df["nconst"], name_df["primaryName"])
director_look = dict(pairs)


def get_director_name(director_ids):

    if pd.isna(director_ids) or director_ids == r"\N":
        return "Unknown"

    names = []

    for director_id in director_ids.split(","):
        name = director_look.get(director_id)
        if name:
            names.append(name)

    return ", ".join(names)


movie_df["director_names"] = movie_df["directors"].apply(get_director_name)

documents = []

for _, row in movie_df.iterrows():

    genres = row["genres"]

    if genres == r"\N":
        genres = "Unknown"
    else:
        genres = row["genres"].replace(",", ", ")

    doc = Document(
        page_content=f"""
    Title : {row["primaryTitle"]}
    Year : {row["startYear"]}
    Genres : {genres}
    Rating :{row["averageRating"]}
    Votes : {row["numVotes"]}
    Directors : {row["director_names"]}
    """,
        metadata={
            "year": row["startYear"],
            "rating": row["averageRating"],
            "votes": row["numVotes"],
            "tconst": row["tconst"],
        },
    )

    documents.append(doc)

print(len(documents))
create_db(documents, embeddings)
