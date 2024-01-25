import json 
from sklearn.metrics.pairwise import cosine_similarity
import os
import pandas as pd
import numpy as np

        
def generatesim():
    curdir = os.getcwd()

    with open(f'{curdir}/../data/users_genres.json', 'r') as user_prefs_file:
        user_preferences = json.load(user_prefs_file)


    unique_genres = set(genre for genres in user_preferences.values() for genre in genres.keys())

    user_preferences_matrix = np.zeros((len(user_preferences), len(unique_genres)))


    with open(f'{curdir}/../data/movies_genres.json', 'r') as moviegenres_file:
        movie_genres = json.load(moviegenres_file)

    movie_genres_matrix = np.zeros((len(movie_genres), len(unique_genres)))

    user_index_map = {user_id: index for index, user_id in enumerate(user_preferences.keys())}
    movie_index_map = {movie_title: index for index, movie_title in enumerate(movie_genres.keys())}

    for user_id, preferences in user_preferences.items():
        for genre, preference in preferences.items():
            user_preferences_matrix[user_index_map[user_id]][list(unique_genres).index(genre)] = preference

    for movie_title, genres in movie_genres.items():
        for genre in genres:
            movie_genres_matrix[movie_index_map[movie_title]][list(unique_genres).index(genre)] = 1

    similarity_matrix = cosine_similarity(user_preferences_matrix, movie_genres_matrix)

    similarity_df = pd.DataFrame(similarity_matrix, index=user_preferences.keys(), columns=movie_genres.keys())

    similarity_df.to_csv(f'{curdir}/../data/user_movie_sim.csv')
    

def main():
    generatesim()

if __name__ == "__main__":
    main()




    