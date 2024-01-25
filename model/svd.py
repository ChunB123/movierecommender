import pandas as pd
import numpy as np

from scipy.linalg import svd




file_path = 'data_2.csv'

df = pd.read_csv(file_path, index_col=0)
matrix = df.values

matrix[matrix == -1] = 0

U, S, Vt = svd(matrix, full_matrices=False)

num_components = 100

U_reduced = U[:, :num_components]
S_reduced = np.diag(S[:num_components])
Vt_reduced = Vt[:num_components, :]



def recommend_movies(user_id, num_recommendations=20):

    user_vector = U_reduced[df.index.get_loc(user_id), :]

    user_watched_movies = df.loc[user_id, df.loc[user_id] != -1].index

    # cos sim
    similarity_scores = np.dot(U_reduced, user_vector) / (np.linalg.norm(U_reduced, axis=1) * np.linalg.norm(user_vector))

    most_similar_users = np.argsort(similarity_scores)[::-1][1:num_recommendations + 1]

    similar_users_ratings = df.iloc[most_similar_users, :]

    average_ratings = similar_users_ratings[user_watched_movies].mean(axis=0)

    recommended_movies = average_ratings.sort_values(ascending=False).index[:num_recommendations]

    return recommended_movies


user_id = 490  
recommended_movies = recommend_movies(user_id)
print(recommended_movies)