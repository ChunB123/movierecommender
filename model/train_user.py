import math
import json
import pickle
import numpy as np
import pandas as pd

numNeighbors = 30
top_n = 20
matrix_ratings = []
average_ratings = []
users = []
movies = []

model_version = 0
training_data_version = 0
user_sims_version = 0

def _removeLabels(df):
    df.columns.name = None
    df.index.names = ['']
    return df

def getRatings():
    global matrix_ratings
    global average_ratings

    for row in matrix_ratings:
        sum = 0
        cnt = 0

        for rating in row:
            if not rating == -1:
                sum += rating
                cnt += 1
        average_ratings.append(sum / cnt)
    
    average_ratings = np.array(average_ratings, dtype = float)

def simimilarity(posU1, posU2):
    numerator = 0
    denominator = 0
    firstDenom = 0
    secondDenom = 0

    for i in range(len(movies)):
        if not matrix_ratings[posU1][i] == -1 and not matrix_ratings[posU2][i] == -1:
            numerator += (matrix_ratings[posU1][i] - average_ratings[posU1]) * (matrix_ratings[posU2][i] - average_ratings[posU2])
            firstDenom += pow(matrix_ratings[posU1][i] - average_ratings[posU1], 2)
            secondDenom += pow(matrix_ratings[posU2][i] - average_ratings[posU2], 2)
        
    denominator = math.sqrt(firstDenom) * math.sqrt(secondDenom)
    
    if numerator == 0:
        return 0
    
    return numerator/denominator

def prediction(pos, sims, average):
    numerator = 0
    denominator = 0
    

    for i in range(len(sims)):    
        numerator += sims[i][0] * (matrix_ratings[sims[i][1]][pos] - average_ratings[sims[i][1]])
        denominator += sims[i][0]

    if numerator == 0:
        return average

    return average + numerator/denominator

def getNeighbours(sims):
    sims = sorted(sims, key=lambda x: x[0], reverse=True)
    
    sims = sims[0: numNeighbors]
    return sims

def calculateRatings():
    recommendedMovies = []
    print(len(users))
    for i in range(len(users)):
        print(i)
        tempRow = []
        for j in range(len(movies)):
            if matrix_ratings[i][j] == -1:
                sims = []
                for k in range(len(users)):
                    if not k == i and not matrix_ratings[k][j] == -1:
                        tempSim = simimilarity(i, k)
                        if tempSim > 0:
                            tup = (tempSim, k)
                            sims.append(tup)
                sims = getNeighbours(sims)
                tempRow.append((prediction(j, sims, average_ratings[i]), movies[j]))
        tempRow = sorted(tempRow, key=lambda x: x[0], reverse=True)[:20]
        tempRow = [x[1] for x in tempRow]
        print(tempRow)
        recommendedMovies.append(tempRow)

    return recommendedMovies

def train_user(df):
    global matrix_ratings
    global users
    global movies

    # inout_info = "../data/info/info.json"
    inout_info = "../data/info/info.pkl"
    info = {}
    # with open(inout_info, 'r') as file:
    #     info = json.load(file)
    with open(inout_info, 'rb') as file:
        info = pickle.load(file)
    
    model_version = str(int(info["model_version"]) + 1)
    training_data_version = str(int(info["training_data_version"]) + 1)

    # outfile_model = "../data/model_versions/user_model_" + model_version + ".csv"
    # outfile_training_data = "../data/training_data_versions/data_" + training_data_version + ".csv"
    # outfile_users = "../data/recommendation_versions/users_" + model_version + ".csv"
    # outfile_movies = "../data/recommendation_versions/movies_" + model_version + ".csv"
    # outfile_user_movies = "../data/recommendation_versions/recommendation_user_" + model_version + ".csv"
    outfile_model = "../data/model_versions/user_model_" + model_version + ".pkl"
    outfile_training_data = "../data/training_data_versions/data_" + training_data_version + ".pkl"
    outfile_user_movies = "../data/recommendation_versions/recommendation_user_" + model_version + ".pkl"

    data_df = df.pivot(index='userID', columns='movieID', values='rating')
    model_df = data_df.fillna(0)
    model_array = np.corrcoef(model_df, rowvar=True)
    model_df = pd.DataFrame(model_array, index=model_df.index, columns=model_df.index)
    # model_df.to_csv(outfile_model)
    model_df.to_pickle(outfile_model)
    
    data_df = data_df.fillna(-1)
    data_df = _removeLabels(data_df)
    # data_df.to_csv(outfile_training_data)
    data_df.to_pickle(outfile_training_data)
    
    matrix_ratings = data_df.to_numpy()

    users = list(data_df.index.values)
    movies = list(data_df.columns.values)
    # users_df = pd.DataFrame({'userid':users})
    # movies_df = pd.DataFrame({'movieid':movies})
    # users_df.to_csv(outfile_users)
    # movies_df.to_csv(outfile_movies)

    getRatings()
    recommendedMovies = calculateRatings()
    user_movie_recommendation = dict(zip(users, recommendedMovies))

    with open(outfile_user_movies, 'wb') as file:
        pickle.dump(user_movie_recommendation, file)

    info["model_version"] = int(model_version)
    info["training_data_version"] = int(training_data_version)

    with open(inout_info, 'wb') as file:
        pickle.dump(info, file)
    
if __name__ == '__main__':
    data_path = "../data/logs/logs_advanced.pkl"
    df = pd.read_pickle(data_path)
    train_user(df)