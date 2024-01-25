import json
import pandas as pd
import numpy as np
import os
import sys
import csv
import random
import pickle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.metrics.pairwise import cosine_similarity

import requests

def curl_req(link:str):
    response = requests.get(link)
    return response.json()

def getMostSimilarUser(userid):

    datafile = "../data/info/users_info.json"

    with open(datafile) as file:
        data = json.load(file)

    user_data = {k : v['user_info'] for k, v in data.items()}
    user_data[str(userid)] = curl_req('http://fall2023-comp585.cs.mcgill.ca:8080/user/'+str(userid))

    df = pd.DataFrame(user_data).T
    df = df.drop('user_id', axis=1)
    df = pd.get_dummies(df, columns=['occupation', 'gender'])

    similarity_matrix = cosine_similarity(df)

    np.fill_diagonal(similarity_matrix, 0)

    similarity_df = pd.DataFrame(similarity_matrix, index=df.index, columns=df.index)

    scores = similarity_df.loc[str(userid)]

    sorted_scores = scores.sort_values(ascending=False)

    return sorted_scores.head(20).index.tolist()

if __name__ == '__main__' :

    outputfile = "commonmovies.pkl"
    datafile = "../data/info/users_info.pkl"

    with open(datafile, 'rb') as file:
        data = pickle.load(file)

    movies = {}
    for v in data.values():
        for m in v["ratings"].keys():
            if m not in movies:
                movies[m] = 1
            else:
                movies[m] += 1
    
    totalm = sum(movies.values())
    probs = {movie : count / totalm for movie, count in movies.items()}

    nlists = 100
    l = 20 

    rl = []
    for i in range(nlists):
        rl.append(random.sample(list(probs.keys()), k=l))

    d = {}
    for o in range(100):
        d[o] = rl[o]

    with open(outputfile, 'wb') as file:
        pickle.dump(d, file)
    


    with open(outputfile, 'rb') as rfile:
        loaded_dict = pickle.load(rfile)
    
    print(loaded_dict)

    #print(getMostSimilarUser(1))