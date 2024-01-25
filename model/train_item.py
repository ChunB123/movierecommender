import pandas as pd
import numpy as np
import math
import os

numNeighbors = 30
top_n = 20
matrix_ratings = []
adjusted_ratings = []
average_ratings = []
users = []
movies = []

def _removeLabels(df):
    df.columns.name = None
    df.index.names = ['']
    return df

def getRatings():
    global average_ratings
    global adjusted_ratings

    for row in matrix_ratings:
        sum = 0
        cnt = 0

        for rating in row:
            if not rating == -1:
                sum += rating
                cnt += 1
        average_ratings.append(sum / cnt)
    
    for i in range(len(matrix_ratings)):
        new_row = []
        for j in range(len(matrix_ratings[i])):
            if matrix_ratings[i][j] == -1:
                new_row.append(None)
            else:
                new_row.append(matrix_ratings[i][j] - average_ratings[i])
        adjusted_ratings.append(new_row)
    adjusted_ratings = np.array(adjusted_ratings)

def simimilarity(posI1, posI2):
    numerator = 0
    denominator = 0
    firstDenom = 0
    secondDenom = 0
    
    for i in range(len(users)):
        if not matrix_ratings[i][posI1] == -1 and not matrix_ratings[i][posI2] == -1:
            numerator += adjusted_ratings[i][posI1] * adjusted_ratings[i][posI2]
            firstDenom += pow(adjusted_ratings[i][posI1], 2)
            secondDenom += pow(adjusted_ratings[i][posI2], 2)

    denominator = math.sqrt(firstDenom) * math.sqrt(secondDenom)
    
    if numerator == 0:
        return 0
    
    return numerator/denominator

def prediction(pos, sims):
    numerator = 0
    denominator = 0

    for i in range(len(sims)):
        numerator += sims[i][0] * matrix_ratings[pos][sims[i][1]]
        denominator += sims[i][0]
    
    return numerator/denominator

def getNeighbours(sims):
    sims = sorted(sims, key=lambda x: x[0], reverse=True)
    
    sims = sims[0: numNeighbors]
    return sims

def calculateRatings():
    recommendedMovies = []
    for i in range(len(users)):
        print(i)
        tempRow = []
        for j in range(len(movies)):
            if matrix_ratings[i][j] == -1:
                sims = []
                for k in range(len(movies)):
                    if not k == j and not matrix_ratings[i][k] == -1:
                        tempSim = simimilarity(j, k)
                        if tempSim > 0:
                            obj = (tempSim, k)
                            sims.append(obj)
                sims = getNeighbours(sims)
                if not len(sims) == 0:
                    tempRow.append((prediction(i, sims), movies[j]))
        tempRow = sorted(tempRow, key=lambda x: x[0], reverse=True)[:20]
        # tempRow = [(lambda x: x if x[0] <= 100 else (100, x[1]))(x) for x in tempRow]
        recommendedMovies.append(tempRow)

    return recommendedMovies

def train_item(df):
    global matrix_ratings
    global users
    global movies

    HOME  = os.path.expanduser("~")
    HOME  = '..'

    outfile_matrix = f"{HOME}/data/matrix.csv"
    outfile_utility = f"{HOME}/data/user_watchtime_utility_new.csv"
    outfile_common_movies = f"{HOME}/data/common_movies.csv"
    outfile_users = f"{HOME}/data/users.csv"
    outfile_movies = f"{HOME}/data/movies.csv"
    outfile_user_movies = f"{HOME}/data/user_movie_i.csv"

    df["watchtime_percentage"] = df["watchtime_percentage"] * 100
    merged_df = df.pivot(index='userid', columns='movieid', values='watchtime_percentage')
    utility_df = df.pivot(index='movieid', columns='userid', values='watchtime_percentage')
    merged_df = merged_df.fillna(-1)
    merged_df = _removeLabels(merged_df)
    utility_df = _removeLabels(utility_df)

    merged_df.to_csv(outfile_matrix)
    matrix_ratings = merged_df.to_numpy()
    print(matrix_ratings)

    users = list(merged_df.index.values)
    movies = list(merged_df.columns.values)
    users_df = pd.DataFrame({'userid':users})
    movies_df = pd.DataFrame({'movieid':movies})
    users_df.to_csv(outfile_users)
    movies_df.to_csv(outfile_movies)
    
    utility_df["mean"] = utility_df.mean(axis=1,skipna=True)
    utility_df.to_csv(outfile_utility)

    utility_df = pd.read_csv(outfile_utility,index_col=0)
    utility_df.index = utility_df.index.astype(str)
    common_movies = utility_df.sort_values(by="mean",ascending=False).head(top_n).index.to_list()
    dict = {'movies': [common_movies]}
    df = pd.DataFrame(dict)
    df.to_csv(outfile_common_movies)

    getRatings()
    recommendedMovies = calculateRatings()
    user_movies = {'userid': users, 'movies': recommendedMovies}
    user_movies_df = pd.DataFrame(user_movies)
    
    user_movies_df.to_csv(outfile_user_movies)

    i = 0
    for row in recommendedMovies:
        print(users[i])
        i += 1
        print(row)
        print(len(row))
    
if __name__ == '__main__':
    data_path = "../data/user_watchtime.csv"
    df = pd.read_csv(data_path,  names = ['userid', 'movieid', 'watchtime','movie_duration','watchtime_percentage'])
    train_item(df)