import requests
import os
from dotenv import load_dotenv
import time
import pandas as pd

load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")

#read the movie_data
movie_df = pd.read_csv("data/movie_data.csv")
plot_df = pd.read_csv("data/plots.csv")

print(len(plot_df))
exit()

#sort the movies with high votes
movie_df = movie_df.sort_values(
    "numVotes",
    ascending=False,
)

# it contains the id whoose plots are with us
done_ids = set(plot_df["tconst"])

#this remove the movies from movie_df with id that are in done_ids
movie_df = movie_df[~movie_df["tconst"].isin(done_ids)]
plots = plot_df.to_dict("records")

for _, row in movie_df.head(1000).iterrows():
    imdb_id = row["tconst"]

    response = requests.get(
        "http://www.omdbapi.com/",
        params={
            "apikey": API_KEY,
            "i": imdb_id,
        },
        timeout=30,
    )

    data = response.json()

    if data.get("Response") == "True":
        plots.append(
            {
                "tconst": imdb_id,
                "plot": data["Plot"],
            }
        )
    else:
        print(len(plots), "Error")
        break

    if len(plots) % 100 == 0:
        plot_df = pd.DataFrame(plots)
        plot_df.to_csv(
            "data/plots.csv",
            index=False,
        )

    print(len(plots), imdb_id)
    time.sleep(0.1)


plot_df = pd.DataFrame(plots)

plot_df.to_csv(
    "data/plots.csv",
    index=False,
)
