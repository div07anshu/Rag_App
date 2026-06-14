import pandas as pd
from langchain_core.documents import Document
from src.db.chroma import create_db
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
CSV_PATH = BASE_DIR / "data"

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

basic_df = pd.read_csv(
    str(CSV_PATH / "title.basics.tsv"),
    sep="\t",
    low_memory=False,
)

rating_df = pd.read_csv(
    str(CSV_PATH / "title.ratings.tsv"),
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

# keep the movie with atleast votes 5000

movie_df = movie_df[movie_df["numVotes"] >= 5000]

# now only keep the important and usefull columns

movie_df = movie_df[
    ["tconst", "primaryTitle", "startYear", "genres", "averageRating", "numVotes"]
]

crew_df = pd.read_csv(
    str(CSV_PATH / "title.crew.tsv"),
    sep="\t",
    low_memory=False,
    usecols=["tconst", "directors"],
)

name_df = pd.read_csv(
    str(CSV_PATH / "name.basics.tsv"),
    sep="\t",
    low_memory=False,
    usecols=["nconst", "primaryName"],
)

movie_df = movie_df.merge(
    crew_df,
    on="tconst",
    how="inner",
)

# this creates a dict of pair of nconst with there primary name
pairs = zip(name_df["nconst"], name_df["primaryName"])
director_look = dict(pairs)


# helper function for getting director name from nconst
def get_director_name(director_ids):

    if pd.isna(director_ids) or director_ids == r"\N":
        return "Unknown"

    names = []

    for director_id in director_ids.split(","):
        name = director_look.get(director_id)
        if name:
            names.append(name)

    return ", ".join(names)


# it will create a new coloumn named director_names and each row get_director_name func will be called
movie_df["director_names"] = movie_df["directors"].apply(get_director_name)

# load the principle file and select the required columns
principal_df = pd.read_csv(
    str(CSV_PATH / "title.principals.tsv"),
    sep="\t",
    low_memory=False,
    usecols=["tconst", "ordering", "nconst", "category"],
)


# filter out the rows which contain either actor or actress
principal_df = principal_df[
    principal_df["category"].isin(
        ["actor", "actress"],
    )
]

# movies_id contain all the tconst from movie_df
movies_id = set(movie_df["tconst"])

# we onlt keep the movies in principal_df whoose tconst are there in movie_df
principal_df = principal_df[principal_df["tconst"].isin(movies_id)]


# merge name_df with principal_df on basis of nconst
actor_df = principal_df.merge(
    name_df,
    on="nconst",
    how="left",
)

# it will sort the actor_df first on basis of tconst and then ordering
actor_df = actor_df.sort_values(
    ["tconst", "ordering"],
)

# for each each tconst keep only 3 top actor , t1 ----- a1 , t1 ------ a2 , t1----- a3
actor_df = actor_df.groupby("tconst").head(3)

# group the actor , for eg.  tconst ------ a1,a2,a3
actor_data = (
    actor_df.groupby("tconst")["primaryName"]
    .apply(lambda x: ", ".join(x))
    .reset_index(name="actor")
)

# merge the movie_df with actor data
movie_df = movie_df.merge(
    actor_data,
    on="tconst",
    how="left",
)

# handles the case when no actor is there
movie_df["actor"] = movie_df["actor"].fillna("Actor Not Available")

# saved the movie_df to use it in omdb.py
movie_df.to_csv(
    str(CSV_PATH / "movie_data.csv"),
    index=False,
)

# contain plot for the movies
plot_df = pd.read_csv(str(CSV_PATH / "plots.csv"))

# merge the plots and movies using tconst
movie_df = movie_df.merge(
    plot_df,
    on="tconst",
    how="left",
)

# for the movies which doesnt have plot fill it with pna
movie_df["plot"] = movie_df["plot"].fillna("Plot Not Available")

# now create the document
documents = []

for _, row in movie_df.iterrows():

    genres = row["genres"]

    if genres == r"\N":
        genres = ["Unknown"]
    else:
        genres = row["genres"].split(",")

    doc = Document(
        page_content=f"""
    Title : {row["primaryTitle"]}
    Year : {row["startYear"]}
    Genres : {", ".join(genres)}
    Rating :{row["averageRating"]}
    Votes : {row["numVotes"]}
    Directors : {row["director_names"]}
    Actors : {row["actor"]}
    Plot : {row["plot"]}
    """,
        metadata={
            "title": row["primaryTitle"],
            "plot": row["plot"],
            "year": row["startYear"],
            "genres": genres,
            "rating": row["averageRating"],
            "votes": row["numVotes"],
            "director": row["director_names"],
            "actor": row["actor"],
            "tconst": row["tconst"],
        },
    )

    documents.append(doc)

create_db(documents, embeddings)
