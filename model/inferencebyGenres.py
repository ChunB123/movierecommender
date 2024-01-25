import os
import pandas as pd
import numpy as np
import json 


def inference(usrid):

    usrid = int(usrid)
    curdir = os.getcwd()

    similarity_df = pd.read_csv(f'{curdir}/../data/user_movie_sim.csv', index_col=0)

    if usrid not in similarity_df.index:
        movie_popularity_scores = similarity_df.sum(axis=0)

        sorted_movies_by_popularity = movie_popularity_scores.sort_values(ascending=False).index

        top_popular_movies = list(sorted_movies_by_popularity[:20])

        return top_popular_movies

    with open(f'{curdir}/../data/users_genres.json', 'r') as user_prefs_file:
        user_preferences = json.load(user_prefs_file)

    user_similarity_scores = similarity_df.loc[usrid]

    sorted_movie_indices = user_similarity_scores.sort_values(ascending=False).index

    recommended_movies = []

    for movie_title in sorted_movie_indices:
            recommended_movies.append(movie_title)
            if len(recommended_movies) == 20:
                break

    return recommended_movies


def main():
    user_to_predict = '4070'
    print(f'Recommed 20 movies for user {user_to_predict}:\n\t',
          inference(user_to_predict))

if __name__ == "__main__":
    main()