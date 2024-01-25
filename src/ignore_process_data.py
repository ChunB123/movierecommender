import os
import os.path as osp
import random
import warnings
import zipfile
from pathlib import Path

import pandas as pd
# import tensorflow as tf
# import tqdm
warnings.filterwarnings("ignore")  

def load_ml_1m():

    # read and merge data into same table
    cur_path = Path(".").absolute()
    ratings = pd.read_csv(
        cur_path / "ml-1m" / "ratings.dat",
        sep="::",
        usecols=[0, 1, 2, 3],
        names=["user", "item", "rating", "time"],
    )
    users = pd.read_csv(
        cur_path / "ml-1m" / "users.dat",
        sep="::",
        usecols=[0, 1, 2, 3],
        names=["user", "sex", "age", "occupation"],
    )
    items = pd.read_csv(
        cur_path / "ml-1m" / "movies.dat",
        sep="::",
        usecols=[0, 2],
        names=["item", "genre"],
        encoding="iso-8859-1",
    )
    items[["genre1", "genre2", "genre3"]] = (
        items["genre"].str.split(r"|", expand=True).fillna("missing").iloc[:, :3]
    )
    items.drop("genre", axis=1, inplace=True)
    data = ratings.merge(users, on="user").merge(items, on="item")
    data.rename(columns={"rating": "label"}, inplace=True)
    # random shuffle data
    data = data.sample(frac=1, random_state=42).reset_index(drop=True)
    return data

def main():
    data = load_ml_1m()  
    print(data.iloc[random.choices(range(len(data)), k=10)])

    FILENAME = "movielens"
    data.to_csv(f'/home/tyang30/data/{FILENAME}.csv')

if __name__ == "__main__":
    main()
    

